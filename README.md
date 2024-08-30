# Camp (Kirill Astrakhantsev) Project

# solved tasks 

# Task 1
## Investigate

* Learn git basics, see links in self education plan
* What is flake8, ruff, mypy
* [Pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
* [Best practices of PRs](https://www.atlassian.com/blog/git/written-unwritten-guide-pull-requests)
* [What is github action](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)

## Cat Downloader

On some of the previous camps, intern tried to implement a cat downloader script for one of our projects.
But he didn't finish it. Please finish the script according to code styling.

1) In your personal repository, fix code style issues in `camp/cat_downloader` module
2) open PR
3) After PR completed, ensure that repo history does not contain “intermediate” fixes, i.e. it should contain just
   * Initial commit
   * Fix commit
   * Merge commit

**Save solutions in a folder `camp/`, for each task a separate file with the
according name**

# Task 2
## Github api client

Name: `github_task`

Write a program which will request data from github repository of your choice
and print the following data:

* Display unique users who committed into repository;
* Display how many commits were made last month;
* Display the most active repo's committee of all time.

It’s dangerous to go alone. Use this:

* [GitHub commits API](https://developer.github.com/v3/repos/commits/#commits) -
Check docs and take their API method;
* [request library](https://3.python-requests.org/user/quickstart/) - use this
to make requests.

# Task 3 

Add tests for all tasks that you already did (including task with github
repo - use mocking). Write tests in the task files. Configure pytest to make it
work with `*_task.py` and `test_*.py` files. Try to cover different cases and
use pytest features.

**BTW**, now for each new task we would require tests for it.

# Task 4

## Matrix class

Library for matrix computations. It must provide the following matrix operations (using magic methods):

* summing or subtractions
* multiplication of two matrices
* multiplication of matrix and a number
* matrix transposing
* In place operations
* dimensions check

```python .noeval
x = Matrix([[0, 1], [1, 2]])
x.size
```

```output
(2, 2)
```

```python
y = x + z
x += x
y = 4 * x
y = -x
y = x ** 2
y = x.transpose()
```


# Task 5

## Preparation

Read the docs from the topics in this lecture and be ready for the task.

## Description

Write a program that will be available to open different file formats
(CSV, JSON, YAML). This program should provide `load_data` and `save_data`
methods for all available formats.

* `save_data` - should get a list of dicts as a parameter and save data in a
corresponding file format
* `load_data` - should load data from a file and store it in a class in a list
of dicts format.

Each file type should have a different implementation.

You need to write a program that will convert read data of `table` typed files
(JSON, YAML, CSV) to any other format from one of `JSON / YAML / CSV and save
it in a newly converted file.

### *input.csv*

```csv
name;birthday;salary;
john;1988-12-12;100;
kevin;1972-12-12;200;
```

### *python code*

```python
data = Data.load_data("my_file.csv")
print(data)
```

### *output:*

```pycon
0:
    name: john
    birthday: 1988-12-12
    salary: 100

1:
    name: kevin
    birthday: 1972-12-12
    salary: 200
```

### *python code*

```python
new_file = data.save_data(path="1.json") # Save data to json format
```

Try to implement approach when adding new file format will not require any
change of existing code

Usage examples:

```bash
# simplest case - convert data from json to csv
python converter.py input.json -o out.csv

# user may specify input format manually
python converter.py input.json --input-format csv -o out.yaml

# user may specify output format manually
python converter.py input.json -o out --output-format csv

# no output specified - simply print content using https://github.com/astanin/python-tabulate
python converter.py input.json

  age  birthday    city         name
-----  ----------  -----------  ------
   32  1986-10-10  NY           John
   18  2000-01-11  LA           Sam
   47  1971-10-20  Krasnoyarsk  Igor
   18  1999-10-11  Los Angeles  John
```

Try another lib for CLI arguments handling: <https://click.palletsprojects.com/en/latest/>


# Tasks 6

## Backoff decorator

You need to implement a decorator which will allow you to retry function calls
if it raises exceptions. This decorator must be parametrized. It can accept the
following arguments:

* `exceptions` (tuple): exceptions to do retiring on. This is a mandatory
parameter.
* `max_retry_count` (int): count of maximum attempts of retrying, by default
is `3`.`None` value means that a function can be retried infinitely.
* `delay` (int): delay in milliseconds between retry attempts, by default
is `0`.

Example:

```python
@backoff(
    exceptions=(IndexError, KeyError, AnyConnectionError),
    max_retry_count=3,
    delay=1000,
)
def parse_internet_page(url):
    # some code which can fail because of error in page format
```

You can use ONLY pure Python, not any Python STD other libs. Each function
should have a corresponding test.

## Pokemon fetcher

There are public REST APIs with pagination, limit and offset. Implement an
iterator, which will fetch data from such API, iterate over results and return
1 at a time.

When results from a page are exhausted, fetch a new page from API. Do not fetch
all results ahead of time.

Let's use <https://pokeapi.co/> with limit of 10, and return each result as a
dictionary.

```python .noeval
pokemons_fetcher = api_fetcher("https://pokeapi.co/api/v2/")
for pokemon in pokemons_fetcher:
    print(pokemon["name"])
```

# Task 7

* Install [Docker](https://docs.docker.com/engine/install/ubuntu/);
* Go through [Post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/);
* Wrap CSV/JSON converter app into docker;
* Provide README that allows run it using docker;


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
