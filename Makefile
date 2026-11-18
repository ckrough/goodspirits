.PHONY: setup test lint format check verify

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
