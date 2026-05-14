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
SCRIPT:=move_if_no_gps_data.py

# ────────────────────────────────────────

# Run application (use ARGS="..." to pass arguments)
run: venv
	python3 $(SCRIPT) $(ARGS)


# Initialize a Python Repository using uv: https://docs.astral.sh/uv/
init:
	uv init
	mv main.py $(SCRIPT)
	uv venv


clean-logs:
	cat /dev/null > .nemo_action.log.json


venv:
	[ -f .venv/bin/activate ] && source .venv/bin/activate
