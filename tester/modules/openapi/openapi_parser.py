import copy
import os
from typing import Tuple
from prance import ResolvingParser


def get_array_validation(path, key, spec):
    """
    Get array validation info from a (application/json) request body given a key/property
    """
    path_items = spec["paths"]
    key_validations = []
    endpoint_objects = path_items[path]
    for _, endpoint_object in endpoint_objects.items():
        schema = endpoint_object["requestBody"]["content"]["application/json"]["schema"]
        if "properties" in schema:
            properties = schema["properties"]
            get_arr_validation(key, properties, key_validations)

    return key_validations


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
    parser = ResolvingParser("./apis/discovery/openapi_specs/import_api.yaml")
    spec = parser.specification
    paths = spec["paths"]
    path_list = []

    for k1, v in paths.items():
        if isinstance(v, dict):
            for k2, _ in v.items():
                method = k2
        api_path = k1
        path_list.append((api_path, method))
    return path_list


def main():
    # print(os.getcwd())
    parser = ResolvingParser("./apis/discovery/openapi_specs/import_api.yaml")
    # key = "num"
    spec = parser.specification
    get_paths(spec)
    # print(get_array_validation("/users/v1/{username}/email", key, spec))


if __name__ == "__main__":
    main()
