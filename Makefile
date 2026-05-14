# No need for @
.SILENT: ;
# Single shell for a target (required to properly use all of our local variables)
.ONESHELL: ;
# Send all vars to shell
.EXPORT_ALL_VARIABLES: ;
# Running Make without target will run the help target
.DEFAULT: help

.PHONY: help init run venv clean-logs

# ────────────────────────────────────────

SRC_DIR=$(shell basename $(PWD))

help: ## Show Help
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: venv
	. .venv/bin/activate && python3 src/$(SRC_DIR)/__main__.py 

# Initialize a Python Repository using uv: https://docs.astral.sh/uv/
init:
	uv init --package
	touch src/$(SRC_DIR)/__main__.py
	uv venv

clean-logs:
	cat /dev/null > .nemo_action.log.json


# venv:
# 	@[ -f .venv/bin/activate ] && source .venv/bin/activate
