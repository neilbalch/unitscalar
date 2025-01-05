# https://packaging.python.org/en/latest/tutorials/packaging-projects
build:
	pip install build twine flake8 pytest custom_literals forbiddenfruit
	python3 -m build

# https://stackoverflow.com/a/13245961/3339274
version = $(shell cat pyproject.toml | grep "version" | grep -oP '(?<=\").*(?=\")')
install: build
	pip install --force-reinstall dist/unitscalar-$(version)-py3-none-any.whl

# Use with pypi testpypi, i.e. upload-pypi or upload-testpypi
# https://github.com/clementvidon/Makefile_tutor?tab=readme-ov-file#extra-rules
upload-%: build
	python3 -m twine upload --repository $* dist/*

.PHONY: clean
clean:
	rm -rf dist
