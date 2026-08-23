PYTHON ?= python3
ACTIONLINT ?= actionlint
YAMLLINT ?= yamllint

.PHONY: validate validate-core validate-repository-home brand-bundle test lint

validate: validate-core validate-repository-home brand-bundle test

validate-core:
	$(PYTHON) scripts/validate_repository.py

validate-repository-home:
	$(PYTHON) scripts/validate-repository-home.py --root .

brand-bundle:
	$(PYTHON) scripts/brand_bundle.py verify

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

lint:
	$(ACTIONLINT) .github/workflows/*.yml
	$(YAMLLINT) --strict .
