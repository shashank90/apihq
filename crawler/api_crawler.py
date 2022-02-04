import glob
import os, fnmatch
import pathlib
from attr import validate
from prance import cli
import click
from click.testing import CliRunner

OPENAPI_EXTENSIONS = ["**/*.yaml", "**/*.json"]


def find_openapi_specs(src_path: str):
    """
    Find openapi files(yaml & json)
    """
    # find all files with possible openapi extensions
    for extension in OPENAPI_EXTENSIONS:
        files = find(extension, src_path)
        for file in files:
            full_path = os.path.abspath(file)
            validate_spec(full_path)


def find(pattern, src_path):
    result = []
    file_pattern = os.path.join(src_path, pattern)
    # print(file_pattern)
    result = glob.glob(file_pattern, recursive=True)
    return result


def validate_spec(spec_path):
    runner = CliRunner()
    try:
        result = runner.invoke(cli.validate, [spec_path])
        if result.exit_code == 0:
            print(spec_path + " VALID OPENAPI DOCUMENT")
        elif result.exit_code == 1:
            print("INVALID OPENAPI DOCUMENT!!")
    except Exception as e:
        print(e)


def upload(src_path: str):
    """
    Find and upload openapi files
    """
    results = find_openapi_specs(src_path)


if __name__ == "__main__":
    find_openapi_specs("/home/shashank/Desktop/appsechq")
