BUNDLED_LOC = bundled/index.html
PYTHON = uv run

.PHONY: bundle
bundle:
	$(PYTHON) dev_scripts/bundle.py
	cp $(BUNDLED_LOC) js_embedding_vis/index.html

# digits target generates both JSONL and images in one command
docs/digits/digits.jsonl docs/digits/images:
	$(PYTHON) dev_scripts/get_data.py digits

docs/iris/iris.jsonl:
	$(PYTHON) dev_scripts/get_data.py iris

docs/stress/stress.jsonl:
	$(PYTHON) dev_scripts/get_data.py stress

docs/iris-inline-data:
	mkdir -p docs/iris-inline-data

docs/iris-inline-cfg/index.html:
	$(PYTHON) -m js_embedding_vis --cfg-path docs/_configs/iris-inline-data.json --out-path docs/iris-inline-cfg/index.html

.PHONY: demo-data
demo-data: docs/digits/digits.jsonl docs/iris/iris.jsonl docs/stress/stress.jsonl docs/iris-inline-data docs/iris-inline-cfg/index.html

.PHONY: demo
demo: bundle demo-data
	cp $(BUNDLED_LOC) docs/iris/index.html
	cp $(BUNDLED_LOC) docs/digits/index.html
	cp $(BUNDLED_LOC) docs/stress/index.html
	cp $(BUNDLED_LOC) docs/iris-inline-data/index.html
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
	rm -rf docs/iris-inline-cfg
