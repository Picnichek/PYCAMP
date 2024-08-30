# Camp (Kirill Astrakhantsev) Project

## Installation

You have to have the following tools installed prior initializing the project:

- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

### Create virtualenv

```bash
pyenv install 3.12 --skip-existing
pyenv shell $(pyenv latest 3.12) && python -m venv .venv --prompt camp-python-kirill-astrakhantsev
source .venv/bin/activate
```

### Install requirements (linters, pytest)

Install requirements

```bash
pip install -r requirements.txt
```

### Install linter for your commits messages

```bash
gitlint install-hook
```

## How to check code style

Check all:

```bash
bash style.sh
```

Fix imports:

```bash
isort .
```

## Run tests

```bash
pytest
```
