import copy
import os
from tarfile import SUPPORTED_TYPES
from typing import Tuple
from prance import ResolvingParser

SUPPORTED_TYPES = ["txt", "pdf", "yaml", "json"]


def get_from_spec(path, spec, key=None, type=None):
    """
    Get validation info from a (application/json) request body given a key/property
    """
    path_items = spec["paths"]
    output = []
    endpoint_objects = path_items[path]
    for _, endpoint_object in endpoint_objects.items():
        content = endpoint_object["requestBody"]["content"]
        for _, v1 in content.items():
            schema = v1["schema"]
            if "properties" in schema:
                properties = schema["properties"]
                if type == "array":
                    get_arr_validation(key, properties, output)
                if type == "file":
                    get_file_type(properties, output)
    return output


def get_file_type(spec, types):
    """
    Given a spec, extract file type/extension from description.
    Search for `format: binary` and extract that field's description
    """
    for _, v in spec.items():
        if "type" in v:
            if "description" in v:
                types.extend(_get_file_type(v["description"]))
        if "type" in v and v["type"] == "object" and "properties" in v:
            types.extend(get_file_type(v["properties"]))
        if "type" in v and v["type"] == "array" and "items" in v:
            if "type" in v["items"] and "description" in v["items"]:
                types.extend(_get_file_type(v["items"]["description"]))


def _get_file_type(description):
    """
    Get file type from description
    """
    types = []
    for type in SUPPORTED_TYPES:
        if type in description:
            types.append(type)
    return types


def get_arr_validation(key, spec, key_validations):
    """
    Given a key, find array validations recursively
    """
    # Array of type object(s) is untested!!
    for k, v in spec.items():
        if key == k:
            prop_details = spec[key]
            if "type" in prop_details:
                validations = []
                if "array" == prop_details["type"]:
                    item = prop_details["items"]
                    validations.append(copy.deepcopy(item))
                    key_validations.append(
                        {
                            "property": key,
                            "validations": validations,
                            "type": "array",
                            "minItems": prop_details.get("minItems"),
                            "maxItems": prop_details.get("maxItems"),
                        }
                    )
        else:
            if "object" == v["type"]:
                get_arr_validation(key, v["properties"], key_validations)


def get_paths(spec_path) -> Tuple[str, str]:
    """
    Retrieve API path and http method
    """
    parser = ResolvingParser(spec_path)
    spec = parser.specification
    host = None
    api_endpoint_url = None
    # Logic to get hostname
    if "servers" in spec:
        # Picking the first server url. Warning: This may not be proper
        host = spec["servers"][0]["url"]
    paths = spec["paths"]
    path_list = []

    for k1, v in paths.items():
        if isinstance(v, dict):
            for k2, _ in v.items():
                method = k2
        api_path = k1
        if host:
            api_endpoint_url = os.path.join(host, api_path)
        path_list.append((api_path, method, api_endpoint_url))
    return path_list


def main():
    # print(os.getcwd())
    parser = ResolvingParser("./apis/discovery/openapi_specs/import_api.yaml")
    # key = "num"
    spec = parser.specification
    # get_paths(spec)
    print(get_from_spec("/apis/v1/specs", spec, type="file"))


if __name__ == "__main__":
    main()
