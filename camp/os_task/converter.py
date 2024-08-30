from __future__ import annotations

import csv
import json
import typing
from pathlib import Path

import click
import yaml
from tabulate import tabulate

FileData: typing.TypeAlias = list[
    dict[
        str,
        typing.Any,
    ]
]


class DataLoader(typing.Protocol):
    """Interface for loading and saving data in vaious formats."""

    def load_data(self, file_path: Path) -> FileData:
        pass

    def save_data(self, data: FileData, file_path: Path) -> None:
        pass


class CSVDataLoader(DataLoader):
    """Class for loading and saving data in CSV format."""

    def load_data(
        self,
        file_path: Path,
    ) -> FileData:
        """Load data from CSV file.

        Returns:
            FileData: List of dictionaries with data from the file.

        """
        with file_path.open(newline="", encoding="utf-8") as csvfile:
            sample = csvfile.read(1024)
            delimiter = self._detect_delimiter(sample)
            csvfile.seek(0)
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            data = [
                {
                    key: self._convert_value(value)
                    for key, value in row.items()
                } for row in reader
            ]
            return data

    def _detect_delimiter(self, sample: str) -> str:
        sniffer = csv.Sniffer()
        return sniffer.sniff(sample).delimiter

    def _convert_value(self, value: str) -> int | float | str:
        """Convert value to the appropriate type."""
        lower_value = value.lower()
        if lower_value == "true":
            return True
        if lower_value == "false":
            return False
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value

    def save_data(
        self,
        data: FileData,
        file_path: Path,
    ) -> None:
        """Save data to CSV file.

        Raises:
            ValueError: If there is no data to save.

        """
        self._check_for_nested_data(data)
        with file_path.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=data[0].keys(),
                delimiter=";",
            )
            writer.writeheader()
            writer.writerows(data)

    def _check_for_nested_data(
        self,
        data: FileData,
    ) -> None:
        """Check for nested data.

        Raises:
            ValueError: If the data contains nested structures.

        """
        if any(
            isinstance(value, (dict, list))
            for row in data for value in row.values()
        ):
            raise ValueError(
                "Nested data structures are not supported for CSV format",
            )


class JSONDataLoader(DataLoader):
    """Class for loading and saving data in JSON format."""

    def load_data(
        self,
        file_path: Path,
    ) -> FileData:
        """Load data from JSON file.

        Returns:
            FileData: List of dictionaries with data from the file.

        """
        with file_path.open("r", encoding="utf-8") as jsonfile:
            return json.load(jsonfile)

    def save_data(
        self,
        data: FileData,
        file_path: Path,
    ) -> None:
        """Save data to JSON file.

        Raises:
            ValueError: If there is no data to save.

        """
        if not data:
            raise ValueError("No data to save")
        with file_path.open("w", encoding="utf-8") as jsonfile:
            json.dump(data, jsonfile, indent=4)


class YAMLDataLoader(DataLoader):
    """Class for loading and saving data in YAML format."""

    def load_data(
        self,
        file_path: Path,
    ) -> FileData:
        """Load data from YAML file.

        Returns:
            FileData: List of dictionaries with data from the file.

        """
        with file_path.open("r", encoding="utf-8") as yamlfile:
            return yaml.safe_load(yamlfile)

    def save_data(
        self,
        data: FileData,
        file_path: Path,
    ) -> None:
        """Save data to YAML file.

        Raises:
            ValueError: If there is no data to save.

        """
        if not data:
            raise ValueError("No data to save")
        with file_path.open("w", encoding="utf-8") as yamlfile:
            yaml.safe_dump(data, yamlfile)


class Data:
    """Class for loading and saving data in various formats."""
    loaders: dict[str, type[DataLoader]] = {
        "json": JSONDataLoader,
        "csv": CSVDataLoader,
        "yaml": YAMLDataLoader,
        "yml": YAMLDataLoader,
    }

    @classmethod
    def _get_loader(
        cls: type[Data],
        file_path: Path,
        file_format: str | None = None,
    ) -> DataLoader:
        if not file_format:
            file_format = file_path.suffix[1:]
        loader = cls.loaders.get(file_format)
        if not loader:
            raise ValueError(
                f"Unsupported file format: {file_format}",
            )
        return loader()

    @classmethod
    def load_data(
        cls: type[Data],
        file_path: Path,
        file_format: str | None = None,
    ) -> FileData:
        """Load data from a file in the specified format.

        Args:
            file_format: File format. If no format, set them by file extension.

        Raises:
            ValueError: If the file format is not supported.

        Returns:
            FileData: A list of dictionaries with data from the file.

        """
        if file_path.stat().st_size == 0:
            raise ValueError(
                "File is empty.",
            )

        loader = cls._get_loader(file_path, file_format)

        return loader.load_data(file_path)

    @classmethod
    def save_data(
        cls: type[Data],
        data: FileData,
        file_path: Path,
        file_format: str | None = None,
    ) -> None:
        """Save data to a file with specified format.

        Args:
            file_format: File format. If no format, set them by file extension.

        Raises:
            ValueError: If the file format is not supported.

        """
        if not data:
            raise ValueError("No data to save")
        loader = cls._get_loader(file_path, file_format)
        return loader.save_data(data, file_path)


@click.command()
@click.argument(
    "input_file",
    type=click.Path(exists=True),
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    default=None,
    help="Output file path",
)
@click.option(
    "--input-format",
    type=click.Choice(
        ["csv", "json", "yaml"],
        case_sensitive=False,
    ),
    default=None,
    help="Specify input file format (csv, json, yaml)",
)
@click.option(
    "--output-format",
    type=click.Choice(
        ["csv", "json", "yaml"],
        case_sensitive=False,
    ),
    default=None,
    help="Specify output file format (csv, json, yaml)",
)
def main(
    input_file: str,
    output: str | None,
    input_format: str,
    output_format: str,
) -> None:
    """Convert data between CSV, JSON, and YAML formats."""
    data = Data.load_data(
        Path(input_file),
        input_format,
    )
    if output:
        Data.save_data(
            data,
            Path(output),
            output_format,
        )
    else:
        print(tabulate(data, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
