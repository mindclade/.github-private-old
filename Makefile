PYTHON ?= python3
ACTIONLINT ?= actionlint
YAMLLINT ?= yamllint

.PHONY: validate validate-repository-home lint

validate: validate-repository-home
	$(PYTHON) scripts/validate_repository.py

validate-repository-home:
	$(PYTHON) scripts/validate-repository-home.py --root .

lint:
	$(ACTIONLINT) .github/workflows/*.yml
	$(YAMLLINT) --strict .
