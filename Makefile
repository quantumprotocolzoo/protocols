PYTHON        = python3
PIP           = pip3
CQC_DIR		  = cqc

_clear_pyc:
	@find . -name '*.pyc' -delete

lint:
	@${PYTHON} -m flake8 ${CQC_DIR}

python-deps:
	@cat requirements.txt | xargs -n 1 -L 1 $(PIP) install

verify: clean python-deps lint _verified

_remove_build:
	@rm -f -r build

_remove_dist:
	@rm -f -r dist

_remove_egg_info:
	@rm -f -r cqc.egg-info

_clear_build: _remove_build _remove_dist _remove_egg_info

_build:
	@${PYTHON} setup.py sdist bdist_wheel

clean: _clear_pyc _clear_build

build: _clear_build _build

.PHONY: clean lint python-deps verify build
