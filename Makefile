.PHONY: setup test lint format check verify eval eval-record

EVALS := plugins/adoption-profile-writing/evals
# Writer model: the skill pins its model in its frontmatter, and that pin takes over once the skill fires,
# so the eval writes with the pinned model only. Another writer would draft the with-skill arm on the pin
# and the without-skill arm on itself, and the delta would compare two models.
SKILL_MODEL := $(shell sed -n 's/^model: *//p' plugins/adoption-profile-writing/skills/adoption-profile-writing/SKILL.md)
MODELS ?= $(SKILL_MODEL)
JUDGE_MODEL ?= claude-opus-5-5

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
# One sweep: each model's result lands in $(EVALS)/results/<sweep>/<model>/. The sweep is stamped with the
# commit it starts at and marked complete when every model finishes; eval-record refuses a sweep without both.
eval:
	@for model in $(MODELS); do [ "$$model" = "$(SKILL_MODEL)" ] || { echo "refusing: the skill pins $(SKILL_MODEL), so a sweep on $$model would compare two writers"; exit 1; }; done; \
	sweep=$$(date -u +%Y-%m-%dT%H-%M-%SZ); dir=$(EVALS)/results/$$sweep; \
	python3 $(EVALS)/record_eval.py --stamp $$dir || exit 1; \
	for model in $(MODELS); do \
		echo "== $$model"; \
		claude plugin eval plugins/adoption-profile-writing --model $$model --judge-model $(JUDGE_MODEL) --threshold 0 --no-publish --scaffold --trust-plugin --allow-tools Write --output-dir $$dir/$$model || exit 1; \
	done; \
	touch $$dir/complete

# Summarize each model's run in the newest sweep into evals/history/ for committing; refuses on an uncommitted plugin.
eval-record:
	python3 $(EVALS)/record_eval.py
