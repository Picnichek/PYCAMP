set -xe
isort camp --check-only
flake8 camp --show-source
mypy camp
