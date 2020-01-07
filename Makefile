test:
	pytest -vv --show-capture=all

ci:
	pytest --show-capture=all --cov=cliauth --no-cov-on-fail --cov-report term-missing
	$(MAKE) lint typing

format:
#	pip install -e .[dev]
	black cliauth setup.py

lint:
#	pip install -e .[dev]
	flake8 cliauth --ignore W503,E203,E501

typing:
#	pip install -e .[dev]
	mypy --strict --strict-equality --ignore-missing-imports cliauth
mypy: typing

build:
#	pip install wheel
	python setup.py bdist_wheel

upload:
#	pip install twine
	twine check dist/cliauth-$(shell cat VERSION)*
	twine upload dist/cliauth-$(shell cat VERSION)*

.PHONY: test ci format lint typing mypy build upload
