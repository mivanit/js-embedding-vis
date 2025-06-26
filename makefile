
.PHONY: bundle
bundle:
	uv run bundle.py

docs/digits/digits.jsonl:
	uv run get_data.py digits

docs/iris/iris.jsonl:
	uv run get_data.py iris

.PHONY: demo
demo: bundle docs/digits/digits.jsonl docs/iris/iris.jsonl
	cp bundled/index.html docs/iris/index.html
	cp bundled/index.html docs/digits/index.html