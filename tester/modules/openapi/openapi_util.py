from posixpath import dirname
from types import ModuleType
from typing import List, Dict
import importlib
import os
import json

from utils.constants import (
    API_DIR,
    MODEL_DIR,
    OPENAPI_CONFIG_FILE,
    PACKAGE_NAME,
    SDK_DIR,
    TEMP_FOLDER_SUFFIX,
)


def set_package_name(sdk_dir):
    """
    Extract openapi generated package name by subtracting current working dir from sdk_dir.
    """
    cwd = os.getcwd()
    gen_folder_path = os.path.relpath(sdk_dir, cwd)
    pkg_name = gen_folder_path.replace("/", ".")
    pkg = {PACKAGE_NAME: pkg_name}
    return pkg


def get_folder_path(pkg_name: str):
    """
    Get folder path from package name
    """
    return pkg_name.replace(".", "/")


def get_temp_folder_name(pkg_name: str):
    """
    Return temporary folder name
    """
    pkg_path = get_folder_path(pkg_name)
    temp = pkg_name.split(".")
    temp_folder_name = temp[len(temp) - 1] + TEMP_FOLDER_SUFFIX
    return temp_folder_name


def get_actual_dest_folder_name(pkg_name: str):
    """
    Get actual destination folder name for generated package
    """
    temp = pkg_name.split(".")
    return temp[len(temp) - 1]


def get_temp_dest_package_path(pkg_name: str):
    parent_folder = get_desired_gen_package_parent(pkg_name)
    temp_dest_folder = get_temp_folder_name(pkg_name)
    return os.path.join(parent_folder, temp_dest_folder)


def get_desired_gen_package_parent(pkg_name: str):
    """
    Return destination folder where generated packaged should reside
    """
    pkg_path = get_folder_path(pkg_name)
    full_path = os.path.join(os.getcwd(), pkg_path)
    parent_folder = dirname(full_path)
    return parent_folder


def get_desired_gen_package_path(pkg_name: str):
    """
    Return destination folder where generated packaged should reside
    """
    pkg_path = get_folder_path(pkg_name)
    full_path = os.path.join(os.getcwd(), pkg_path)
    return full_path


def get_actual_gen_package_path(pkg_name: str):
    """
    Get actual generated package folder path. For ex: <cwd>/p1/p2/p3/p1/p2/p3
    """
    pkg_path = get_folder_path(pkg_name)
    full_gen_pkg_path = os.path.join(os.getcwd(), pkg_path, pkg_path)
    return full_gen_pkg_path


def write_openapi_config(sdk_dir, pkg: Dict) -> str:
    openapi_config_file_path = os.path.join(sdk_dir, OPENAPI_CONFIG_FILE)
    with open(openapi_config_file_path, "w") as fp:
        json.dump(pkg, fp)
    return openapi_config_file_path


def get_generated_pkg_name(openapi_config_file_path: str) -> str:
    """
    Read package name from openapi invoker config file
    """
    pkg: Dict = None
    with open(openapi_config_file_path) as f_in:
        pkg = json.load(f_in)
    return pkg.get(PACKAGE_NAME)


def init_configuration(pkg_name: str) -> str:
    module_path = concat_pkg_name(pkg_name, "configuration")
    config_module = importlib.import_module(module_path)
    config_class = getattr(config_module, "Configuration")
    configuration = config_class(
        host="http://localhost:5000",
        access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDA1OTc4MzQsImlhdCI6MTY0MDU5Nzc3NCwic3ViIjoibmFtZTEifQ.KwYudK6g7CVKHE9BgVJwR7A-e1oS--EQ3HyWdiTc02k",
        disabled_client_side_validations="multipleOf,maximum,exclusiveMaximum,minimum,exclusiveMinimum,maxLength,minLength,pattern,maxItems,minItems",
    )
    # Enable Debug logging
    configuration.debug = True
    # Proxy requests through ZAP
    configuration.proxy = "http://localhost:8080"
    # Disable ssl cert verification for communicating with ZAP
    configuration.verify_ssl = False
    return configuration


def concat_pkg_name(pkg_name: str, module_name: str):
    return pkg_name + "." + module_name


def get_api_client_module(pkg_name: str) -> ModuleType:
    module_path = concat_pkg_name(pkg_name, "api_client")
    return importlib.import_module(module_path)


def get_exceptions_module(pkg_name: str) -> ModuleType:
    module_path = concat_pkg_name(pkg_name, "exceptions")
    return importlib.import_module(module_path)


def get_api_package(pkg_name: str) -> str:
    api_package_path = concat_pkg_name(pkg_name, "api")
    return api_package_path


def get_model_package(pkg_name: str) -> str:
    model_package_path = concat_pkg_name(pkg_name, "model")
    return model_package_path


def get_api_module_path(module_name: str, pkg_name: str) -> str:
    return concat_pkg_name(get_api_package(pkg_name), module_name)


def get_api_module(module_name: str, pkg_name: str) -> ModuleType:
    module_path = get_api_module_path(module_name, pkg_name)
    return importlib.import_module(module_path)


def get_model_module_path(module_name: str, pkg_name: str) -> str:
    return concat_pkg_name(get_model_package(pkg_name), module_name)


def get_api_dir(txn_dir) -> str:
    return os.path.join(txn_dir, SDK_DIR, API_DIR)


def get_gen_classes(txn_dir) -> str:
    return os.path.join(txn_dir, SDK_DIR, MODEL_DIR)
