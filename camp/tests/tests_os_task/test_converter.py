import typing
from pathlib import Path

import pytest
from pytest_lazy_fixtures import lf as lazy_fixture

from camp.os_task import converter
from camp.os_task.converter import FileData

PathType: typing.TypeAlias = Path | str


@pytest.mark.parametrize(
    argnames="path",
    argvalues=[
        pytest.param(
            lazy_fixture("tmp_json_path"),
        ),
        pytest.param(
            lazy_fixture("tmp_csv_path"),
        ),
        pytest.param(
            lazy_fixture("tmp_yaml_path"),
        ),
    ],
)
def test_load_data(
    path: PathType,
    expected_data: FileData,
) -> None:
    """Test load data from file to python."""
    data = converter.Data.load_data(Path(str(path)))
    assert data == expected_data


def test_load_empty_data(
    tmp_empty_data_csv: Path,
) -> None:
    """Test load data from empty file."""
    with pytest.raises(
        ValueError,
        match="File is empty.",
    ):
        converter.Data.load_data(Path(str(tmp_empty_data_csv)))


def test_save_empty_data(
    tmp_path: Path,
    empty_data: FileData,
) -> None:
    """Test save empty data."""
    output_path = tmp_path / "output_file.csv"
    with pytest.raises(
        ValueError,
        match="No data to save",
    ):
        converter.Data.save_data(
            empty_data,
            output_path,
        )


@pytest.mark.parametrize(
    argnames="output_format",
    argvalues=["csv", "json", "yaml"],
)
def test_save_data(
    tmp_path: Path,
    output_format: str,
    expected_data: FileData,
) -> None:
    """Test save python data to file."""
    output_path = tmp_path / f"output_file.{output_format}"
    converter.Data.save_data(
        expected_data,
        Path(output_path),
        output_format,
    )

    assert output_path.is_file()
    assert output_path.suffix[1:] == output_format
    assert converter.Data.load_data(Path(output_path)) == expected_data


def test_save_nested_date_to_csv(
    tmp_path: Path,
    nested_data: FileData,
) -> None:
    """Test save nested python data to csv file."""
    output_path = tmp_path / "output_file.csv"
    with pytest.raises(
        ValueError,
        match="Nested data structures are not supported for CSV format",
    ):
        converter.Data.save_data(
            nested_data,
            output_path,
        )


def test_load_incorrect_type(
    tmp_csv_no_extension_path: PathType,
) -> None:
    """Test load data with unsupported format."""
    file_format = ".png"
    with pytest.raises(
        ValueError,
        match=f"Unsupported file format: {file_format}",
    ):
        converter.Data.load_data(
            Path(tmp_csv_no_extension_path),
            file_format=file_format,
        )


def test_save_incorrect_type(
    expected_data: FileData,
    tmp_csv_no_extension_path: PathType,
) -> None:
    """Test save data with unsupported format."""
    file_format = ".png"
    with pytest.raises(
        ValueError,
        match=f"Unsupported file format: {file_format}",
    ):
        converter.Data.save_data(
            expected_data,
            file_path=Path(tmp_csv_no_extension_path),
            file_format=file_format,
        )
