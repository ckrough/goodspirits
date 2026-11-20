.PHONY: setup test lint format check verify eval eval-record

JUDGE_MODEL ?= claude-sonnet-5-5

setup:
	@echo "No dependencies to install: the repo has no lockfile."

test:
	python3 -m unittest discover -s tests

lint:
	uvx ruff@0.17.5 check plugins tests

format:
	uvx ruff@0.17.5 format plugins tests

check: test lint

verify: check
	claude plugin validate .
	claude plugin validate plugins/adoption-profile-writing

# Paid model calls; runs outside the Claude sandbox (`! make eval`), never in check, verify, or CI.
eval:
	claude plugin eval plugins/adoption-profile-writing --judge-model $(JUDGE_MODEL) --threshold 0 --no-publish --scaffold --trust-plugin --allow-tools Write

# Summarize the newest run into evals/history/ for committing; refuses on an uncommitted plugin.
eval-record:
	python3 plugins/adoption-profile-writing/evals/record_eval.py
