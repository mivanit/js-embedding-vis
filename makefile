
.PHONY: bundle
bundle:
	uv run bundle.py

.PHONY: demo
demo: bundle
	cp bundled/index.html docs/index.html
	uv run get_data.py