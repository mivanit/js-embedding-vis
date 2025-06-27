
.PHONY: bundle
bundle:
	uv run bundle.py

docs/digits/digits.jsonl:
	uv run get_data.py digits

docs/iris/iris.jsonl:
	uv run get_data.py iris

docs/stress/stress.jsonl:
	uv run get_data.py stress

docs/iris-inline-data:
	mkdir -p docs/iris-inline-data


docs/iris-inline-cfg/index.html:
	uv run inline_cfg.py --cfg-path docs/_configs/iris-inline-data.json --out-path docs/iris-inline-cfg/index.html

.PHONY: demo-data
demo-data: docs/digits/digits.jsonl docs/iris/iris.jsonl docs/stress/stress.jsonl docs/iris-inline-data docs/iris-inline-cfg/index.html

.PHONY: demo
demo: bundle demo-data
	cp bundled/index.html docs/iris/index.html
	cp bundled/index.html docs/digits/index.html
	cp bundled/index.html docs/stress/index.html
	cp bundled/index.html docs/iris-inline-data/index.html
	cp docs/_configs/iris.json docs/iris/config.json
	cp docs/_configs/digits.json docs/digits/config.json
	cp docs/_configs/stress.json docs/stress/config.json
	cp docs/_configs/iris-inline-data.json docs/iris-inline-data/config.json

.PHONY: clean
clean:
	rm -rf bundled
	rm -rf docs/digits
	rm -rf docs/iris
	rm -rf docs/stress
	rm -rf docs/iris-inline-data
