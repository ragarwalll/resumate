

# Define the lint:scan target
lint\:scan:
	poetry run pylint .

format\:scan:
	poetry run black . --check

run-tests:
	poetry run test

run-test-single:
	poetry run pytest __tests__/test_health.py

run-test-with-cov:
	poetry run pytest --cov=server __tests__/

.PHONY: lint\:scan format\:scan