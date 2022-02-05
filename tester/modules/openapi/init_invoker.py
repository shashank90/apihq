import os

import shutil
from typing import Dict, List
from utils.constants import SDK_DIR

from tester.modules.openapi.invoker import _invoke_apis
from tester.modules.openapi.openapi_util import (
    get_actual_gen_package_path,
    get_desired_gen_package_path,
    get_generated_pkg_name,
    get_temp_dest_package_path,
    set_package_name,
    write_openapi_config,
)
from log.factory import Logger
from utils.os_cmd_runner import run_cmd

logger = Logger(__name__)


def generate_sdk(sdk_dir: str, spec_path: str, openapi_config_file_path: str):
    """
    Generate python sdk from openapi spec(using openapi generator)
    """
    logger.info("openapi sdk generation begins...")
    output = run_cmd(
        [
            "/home/shashank/bin/openapitools/openapi-generator-cli",
            "generate",
            "-i",
            spec_path,
            "-g",
            "python",
            "-o",
            sdk_dir,
            "-c",
            openapi_config_file_path,
        ],
        timeout=50,
    )
    # logger.info(output)
    logger.info("openapi sdk generation complete")


def invoke_apis(data_dir: str, api_path: str, spec_path: str, auth_headers: List[Dict]):
    """
    Perform API conformance test by generating and invoking requests given an api
    """
    sdk_dir = os.path.join(data_dir, SDK_DIR)

    # Write package name to file. Openapi generator places generated files under this package.
    pkg = set_package_name(sdk_dir)
    openapi_config_file_path = write_openapi_config(data_dir, pkg)

    generate_sdk(sdk_dir, spec_path, openapi_config_file_path)

    gen_pkg_name = get_generated_pkg_name(openapi_config_file_path)

    move_generated_files(gen_pkg_name)

    return _invoke_apis(api_path, spec_path, data_dir, gen_pkg_name, auth_headers)


def move_generated_files(gen_pkg_name: str):
    """
    When generating openapi files, invoker package is used to set imports properly(relative to project root)
    This creates additional folder nesting also, which is redundant as invoker is already appropriately nested
    Hence moving generated files relative to invoker file
    """
    temp_dest_pkg_path = get_temp_dest_package_path(gen_pkg_name)
    actual_src_pkg_path = get_actual_gen_package_path(gen_pkg_name)
    desired_dest_pkg_path = get_desired_gen_package_path(gen_pkg_name)

    # Flatten out python_sdk folder by removing the nesting
    os.rename(actual_src_pkg_path, temp_dest_pkg_path)

    # Remove original nested folder recursively
    shutil.rmtree(desired_dest_pkg_path)

    # Rename temp folder to actual dest folder
    os.rename(temp_dest_pkg_path, desired_dest_pkg_path)


if __name__ == "__main__":
    data_dir = os.getcwd()
    api_path = "/apis/v1/{customerName}/specs"
    spec_path = "import_api.yaml"
    invoke_apis(data_dir, api_path, spec_path)
