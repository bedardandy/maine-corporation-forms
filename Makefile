# Maine Corporation Forms — developer entry points.
# Most targets are PDF-free and offline; `fetch` and `fill` need the blank PDF.
.PHONY: help test validate coverage status sync-schema rebuild-fields route plan fill fetch check-upstream mcp serve

help:
	@echo "make test                       run the deterministic test suite (the CI gate)"
	@echo "make validate FORM=CORP_MBCA-6  validate one form folder (omit FORM for --all)"
	@echo "make coverage                   validate every form; print the review worklist"
	@echo "make status                     regenerate docs/STATUS.md from the form data"
	@echo "make sync-schema FORM=..        extend schema.json to cover all mapping keys"
	@echo "make rebuild-fields FORM=..     refetch the blank + regenerate fields.csv inventory"
	@echo "make route Q='convert an LLC'   route an intent to candidate forms"
	@echo "make plan FORM=.. CASE=..       coverage of a case against a form (no PDF)"
	@echo "make fill FORM=.. CASE=.. OUT=..  fill the blank PDF from a case (needs the PDF)"
	@echo "make fetch FORMS=A,B            download blank PDFs from the official portal"
	@echo "                                (verified; omit FORMS to fetch all)"
	@echo "make check-upstream            re-probe official URLs; flag forms Maine has revised"
	@echo "make mcp                        run the MCP server (find_forms / get_form / fill_form)"
	@echo "make serve                      run the stdlib HTTP API + browser review UI on :8080"

test:
	python3 -m pytest tests/ -v

validate:
	python3 tools/validate_form.py $(if $(FORM),$(FORM) -v,--all)

coverage:
	python3 tools/validate_form.py --all -v

status:
	python3 tools/gen_status.py

sync-schema:
	python3 tools/sync_schema.py $(FORM)

rebuild-fields:
	python3 tools/fetch_pdfs.py --forms $(FORM)
	python3 tools/rebuild_fields_csv.py $(FORM)

route:
	python3 -m engine.route "$(Q)"

plan:
	python3 -m engine.plan $(FORM) $(CASE)

fill:
	python3 -m engine.fill $(FORM) $(CASE) $(or $(OUT),out.pdf)

fetch:
	python3 tools/fetch_pdfs.py $(if $(FORMS),--forms $(FORMS),)

check-upstream:
	python3 tools/check_upstream.py $(if $(FORMS),--forms $(FORMS),)

mcp:
	python3 tools/agent_server.py

serve:
	python3 tools/api_server.py
