PYTHON ?= python3
ACTIONLINT ?= actionlint
YAMLLINT ?= yamllint

.PHONY: validate validate-core validate-repository-home lint

validate: validate-core validate-repository-home

validate-core:
	$(PYTHON) scripts/validate_repository.py

validate-repository-home:
	$(PYTHON) scripts/validate-repository-home.py --root .

lint:
	$(ACTIONLINT) .github/workflows/*.yml
	$(YAMLLINT) --strict .
