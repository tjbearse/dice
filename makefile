

.PHONY: test

test: typeCheck
	python3 -m unittest

.PHONY: typeCheck
typeCheck:
	python3 -m mypy --ignore-missing-imports *.py
