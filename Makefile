.PHONY: setup test lint format check verify eval eval-record

EVALS := plugins/adoption-profile-writing/evals
# Writer models, each run over every case, to show where quality falls off.
MODELS ?= claude-haiku-5-5 claude-sonnet-5-5 claude-opus-5-5
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
# One sweep: each model's result lands in $(EVALS)/results/<sweep>/<model>/.
eval:
	@sweep=$$(date -u +%Y-%m-%dT%H-%M-%SZ); for model in $(MODELS); do \
		echo "== $$model"; \
		claude plugin eval plugins/adoption-profile-writing --model $$model --judge-model $(JUDGE_MODEL) --threshold 0 --no-publish --scaffold --trust-plugin --allow-tools Write --output-dir $(EVALS)/results/$$sweep/$$model || exit 1; \
	done

# Summarize each model's run in the newest sweep into evals/history/ for committing; refuses on an uncommitted plugin.
eval-record:
	python3 $(EVALS)/record_eval.py
