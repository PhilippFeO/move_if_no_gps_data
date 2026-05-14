.PHONY: init run venv

SRC_DIR=$(shell basename $(PWD))

run: venv
	@. .venv/bin/activate && python3 src/$(SRC_DIR)/__main__.py 

# Initialize a Python Repository using uv: https://docs.astral.sh/uv/
init:
	@uv init --package
	@touch src/$(SRC_DIR)/__main__.py
	@uv venv

# venv:
# 	@[ -f .venv/bin/activate ] && source .venv/bin/activate
