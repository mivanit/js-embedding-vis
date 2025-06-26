
.PHONY: bundle
bundle:
	uv run bundle.py

.PHONY: demo
demo: bundle
	cp bundled/index.html docs/iris/index.html
	cp bundled/index.html docs/digits/index.html
	uv run get_data.py iris
	uv run get_data.py digits