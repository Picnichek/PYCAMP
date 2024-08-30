# File convertor

This programme converts Csv, Json, Yaml files between extensions.


## options

"-o", "--output" - Output file path
"--input-format" - Specify input file format (csv, json, yaml)
"--output-format" - Specify output file format (csv, json, yaml)

## Example to convert data

```bash
python camp/os_task/converter.py JSON.json -o JSON_to_yaml.yaml --output-format yaml --input-format json

python JSON.json -o JSON_to_CSV.csv --output-format csv --input-format json

python camp/os_task/converter.py YAML.yaml -o YAML_to_JSON.json --output-format json --input-format yaml

python camp/os_task/converter.py YAML.yaml -o YAML_to_CSV.csv --output-format csv --input-format yaml

python camp/os_task/converter.py CSV.csv -o CSV_to_JSON.json --output-format json --input-format csv

python camp/os_task/converter.py CSV.csv -o CSV_to_YAML.yaml --output-format yaml --input-format csv
```

or

```bash

python camp/os_task/converter.py JSON.json -o JSON_to_yaml.yaml

python camp/os_task/converter.py JSON.json -o JSON_to_CSV.csv

python camp/os_task/converter.py YAML.yaml -o YAML_to_JSON.json

python camp/os_task/converter.py YAML.yaml -o YAML_to_CSV.csv

python camp/os_task/converter.py CSV.csv -o CSV_to_JSON.json

python camp/os_task/converter.py CSV.csv -o CSV_to_YAML.yaml
```

## Example no output

```bash
python camp.os_task.convertor input_file.csv(or json, yaml)
```

## File convertor on Docker

## Description: CLI app converting data from a file to another one

Go to os_task directory

```bash
cd camp/os_task
```

Create image by Dockerfile

```bash
docker buildx build . -t pycamp-1154:latest
```

## Example

Convert data from file to another one
get json, yaml or csv file into "os_task" folder
and run next examples of command:

```bash
docker run -v .:/app/ --rm pycamp-1154 examle.json --output json_to_csv.csv

```

To run the container without convert

```bash
docker run -v .:/app/ --rm pycamp-1154 example.csv
```
