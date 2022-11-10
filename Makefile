SHELL := /bin/bash
venv-clean:
	rm -rf .venv

venv-setup: venv-clean
	python3 -m venv .venv; \
	source .venv/bin/activate; \
	pip install --editable .

venv-activate:
	source .venv/bin/activate