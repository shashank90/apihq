import os

import shutil
from typing import Dict, List
from backend.utils.constants import SDK_DIR, API_RUN_FAILED, SDK_GENERATOR_CMD

from backend.db.helper import update_run_details
from backend.db.model.api_run import RunStatusEnum
from backend.tester.modules.openapi.invoker import _invoke_apis
from backend.tester.modules.openapi.openapi_util import (
    get_actual_gen_package_path,
    get_desired_gen_package_path,
    get_generated_pkg_name,
    get_temp_dest_package_path,
    set_package_name,
    write_openapi_config,
)
from backend.log.factory import Logger
from backend.utils.os_cmd_runner import run_cmd

logger = Logger(__name__)


def generate_sdk(
    run_id: str, sdk_dir: str, spec_path: str, openapi_config_file_path: str
):
    """
    Generate python sdk from openapi spec(using openapi generator)
    """
    logger.info(f"Openapi sdk generation begins for run_id {run_id}...")
    output = run_cmd(
        [
            SDK_GENERATOR_CMD,
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
    logger.info(f"Openapi sdk generation complete for run_id {run_id}")


def invoke_apis(
    run_id: str,
    data_dir: str,
    run_dir: str,
    api_path: str,
    spec_path: str,
    auth_headers: List[Dict],
):
    """
    Run Api tests by generating payloads from openapi spec and sending them
    """
    sdk_dir = os.path.join(data_dir, SDK_DIR)

    try:
        # Write package name to file. Openapi generator places generated files under this package.
        pkg = set_package_name(sdk_dir)
        openapi_config_file_path = write_openapi_config(data_dir, pkg)

        generate_sdk(run_id, sdk_dir, spec_path, openapi_config_file_path)

        gen_pkg_name = get_generated_pkg_name(openapi_config_file_path)

        move_generated_files(gen_pkg_name)

        return _invoke_apis(
            run_id, api_path, spec_path, data_dir, run_dir, gen_pkg_name, auth_headers
        )

    except Exception:
        update_run_details(run_id, RunStatusEnum.ERROR, API_RUN_FAILED)
        logger.exception(f"Openapi sdk generation failed for run_id: {run_id}")

    return None


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
