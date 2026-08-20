PYTHON ?= python3
ACTIONLINT ?= actionlint
YAMLLINT ?= yamllint

.PHONY: validate lint

validate:
	$(PYTHON) scripts/validate_repository.py

lint:
	$(ACTIONLINT) .github/workflows/*.yml
	$(YAMLLINT) --strict .
