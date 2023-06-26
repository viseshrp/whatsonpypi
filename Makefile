DATE = $(shell date +'%Y%m%d')

build:
	python -m build --wheel
	rm -rf build

install:
	pip uninstall whatsonpypi -y
	pip install dist/*.whl

install-dev:
	pip uninstall whatsonpypi -y
	pip install -e .
	pip install -U -r requirements/dev.txt

test:
	pytest -rvx --setup-show

test-cov:
	pytest -rvx --setup-show --cov=whatsonpypi \
  --cov-report html:coverage-html \
  --cov-report xml:coverage.xml \
  --cov-report term \
  --cov-config=.coveragerc

smoketest:
	whatsonpypi --help
	whatsonpypi --version

clean:
	find . -name \*.pyc -delete
	rm -rf dist \
  build \
  *.egg-info \
  .coverage \
  coverage-html \
  coverage.xml \
  .pytest_cache
