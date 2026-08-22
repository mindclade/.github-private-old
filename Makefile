PYTHON ?= python3
ACTIONLINT ?= actionlint
YAMLLINT ?= yamllint

.PHONY: validate validate-core validate-repository-home validate-repository-policy lint

validate: validate-core validate-repository-home

validate-core: validate-repository-policy
	$(PYTHON) scripts/validate_repository.py

validate-repository-policy:
	$(PYTHON) scripts/validate-repository-policy.py --root .

validate-repository-home:
	$(PYTHON) scripts/validate-repository-home.py --root .

lint:
	$(ACTIONLINT) .github/workflows/*.yml
	$(YAMLLINT) --strict .
