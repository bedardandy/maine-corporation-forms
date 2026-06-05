#!/usr/bin/env python3
"""Minimal HTTP API over the Maine SoS corporation-forms library.

Endpoints (all JSON unless noted):
  GET  /healthz              -> {"ok": true, "forms": N}
  GET  /forms                -> the form index
  POST /route  {situation}   -> {mode, results:[{form_id,title,hints}]}
  POST /plan   {form, case}  -> coverage plan (see engine.plan)
  POST /fill   {form, case}  -> filled PDF bytes (application/pdf)

Pure standard library (http.server) so it runs with no extra dependencies.
``/plan`` and ``/fill`` are deterministic functions of the posted case object.

    python3 tools/api_server.py --port 8080
"""
from __future__ import annotations

import argparse
import io
import json
import pathlib
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from engine import fill as fill_engine  # noqa: E402
from engine import plan as plan_engine  # noqa: E402
import route_form  # noqa: E402

_FORMS_ROOT = str(ROOT / "forms")


def _forms_index():
    idx = json.loads((ROOT / "catalog" / "forms_index.json").read_text())
    return idx.get("forms", idx) if isinstance(idx, dict) else idx


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload, ctype="application/json"):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send_static("index.html", "text/html")
        elif self.path == "/healthz":
            self._send(200, {"ok": True, "forms": len(_forms_index())})
        elif self.path == "/forms":
            self._send(200, _forms_index())
        elif self.path == "/enhancements":
            from engine import pipeline
            self._send(200, {"steps": pipeline.list_steps()})
        else:
            self._send(404, {"error": "not found"})

    def _send_static(self, name, ctype):
        path = ROOT / "web" / name
        if not path.exists():
            return self._send(404, {"error": "not found"})
        self._send(200, path.read_bytes(), ctype=ctype)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(n) or "{}")
        except json.JSONDecodeError:
            return self._send(400, {"error": "invalid JSON"})
        if self.path == "/route":
            results, mode = route_form.route(req.get("situation", ""),
                                             req.get("top_k", 5))
            self._send(200, {"mode": mode, "results": results})
        elif self.path == "/plan":
            plan = plan_engine.build_plan(req.get("form", ""),
                                          req.get("case", {}), _FORMS_ROOT)
            self._send(200 if plan.get("ok") else 400, plan)
        elif self.path == "/fill":
            self._fill(req)
        elif self.path == "/enhance":
            self._enhance(req)
        else:
            self._send(404, {"error": "not found"})

    def _enhance(self, req):
        form_id = req.get("form", "")
        steps = req.get("steps", [])
        case = req.get("case") or None
        options = req.get("options") or None
        if case is not None and not isinstance(case, dict):
            return self._send(400, {"error": "case must be a JSON object"})
        if options is not None and not isinstance(options, dict):
            return self._send(400, {"error": "options must be a JSON object"})
        if not (ROOT / "forms" / form_id / "mapping.json").exists():
            return self._send(404, {"error": f"unknown form {form_id!r}"})
        from engine import pipeline
        try:
            rep = pipeline.run_pipeline(form_id, steps, case,
                                        forms_root=_FORMS_ROOT, options=options)
        except Exception as e:  # pragma: no cover - defensive
            return self._send(500, {"error": f"{type(e).__name__}: {e}"})
        pdf = rep.pop("bytes", None)
        if req.get("report_only") or pdf is None:
            return self._send(200, rep)
        # return the PDF, with the run report in headers for the UI
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition",
                         f'attachment; filename="{form_id}_enhanced.pdf"')
        self.send_header("X-Enhance-Ran", ",".join(rep.get("ran", [])))
        self.send_header("X-Enhance-Skipped", "; ".join(rep.get("skipped", [])))
        self.send_header("Content-Length", str(len(pdf)))
        self.end_headers()
        self.wfile.write(pdf)

    def _fill(self, req):
        form_id = req.get("form", "")
        case = req.get("case", {})
        if not isinstance(case, dict):
            return self._send(400, {"error": "case must be a JSON object"})
        form_dir = ROOT / "forms" / form_id
        if not (form_dir / "mapping.json").exists():
            return self._send(404, {"error": f"unknown form {form_id!r}"})
        try:
            buf = io.BytesIO()
            fill_engine.fill_to_stream(form_id, case, buf, _FORMS_ROOT)
            self._send(200, buf.getvalue(), ctype="application/pdf")
        except Exception as e:  # pragma: no cover - defensive
            self._send(500, {"error": f"{type(e).__name__}: {e}"})

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"serving on http://{a.host}:{a.port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
