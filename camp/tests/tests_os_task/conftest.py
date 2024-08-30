from pathlib import Path

import pytest

from camp.os_task.converter import FileData


@pytest.fixture
def expected_data() -> FileData:
    """Return expected data for tests."""
    return [
        {"birthday": "1988-12-12", "name": "john", "salary": 100},
        {"birthday": "1972-12-12", "name": "kevin", "salary": 200},
    ]


@pytest.fixture
def empty_data() -> FileData:
    """Return empty data for tests."""
    return []


@pytest.fixture
def nested_data() -> FileData:
    """Return expected data for tests."""
    return [
        {
            "name": "John",
            "age": 30,
            "children": [
                {
                    "name": "Jane",
                    "age": 10,
                },
                {
                    "name": "Doe",
                    "age": 8,
                },
            ],

        },
    ]


@pytest.fixture
def tmp_empty_data_csv(tmpdir: Path) -> Path:
    """Empty csv file."""
    path = tmpdir / "empty.csv"
    csv_content = ""
    path.write_text(csv_content, encoding="utf-8")
    return path


@pytest.fixture
def tmp_csv_path(tmpdir: Path) -> Path:
    """CSV file for test."""
    path = tmpdir / "test.csv"
    csv_content = (
        "name;birthday;salary\n"
        "john;1988-12-12;100\n"
        "kevin;1972-12-12;200\n"
    )
    path.write_text(csv_content, encoding="utf-8")
    return path


@pytest.fixture
def tmp_yaml_path(tmpdir: Path) -> Path:
    """YAML file for test."""
    path = tmpdir / "test.yaml"
    yaml_content = (
        "- birthday: '1988-12-12'\n"
        "  name: john\n"
        "  salary: 100\n"
        "- birthday: '1972-12-12'\n"
        "  name: kevin\n"
        "  salary: 200\n"
    )
    path.write_text(yaml_content, encoding="utf-8")
    return path


@pytest.fixture
def tmp_json_path(tmpdir: Path) -> Path:
    """JSON file for test."""
    path = tmpdir / "test.json"
    json_content = (
        '[{"birthday": "1988-12-12", "name": "john", "salary": 100},'
        '{"birthday": "1972-12-12", "name": "kevin", "salary": 200}]'
    )
    path.write_text(json_content, encoding="utf-8")
    return path


@pytest.fixture
def tmp_csv_no_extension_path(tmpdir: Path) -> Path:
    """CSV file for test."""
    path = tmpdir / "test"
    csv_content = (
        "name;birthday;salary\n"
        "john;1988-12-12;100\n"
        "kevin;1972-12-12;200\n"
    )
    path.write_text(csv_content, encoding="utf-8")
    return path
