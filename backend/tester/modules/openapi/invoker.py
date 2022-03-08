from multiprocessing.spawn import prepare
import re
from typing import Dict, List, Tuple, Type
from urllib.parse import urljoin

import urllib3
from backend.tester.modules.openapi.file_payload_handler import (
    get_generated_file_handles,
)
from backend.utils.constants import (
    MESSAGE,
    FILE_ATTRIBUTE_TYPE,
    REQUEST_ID,
    DATA_DIR,
)

from backend.tester.modules.openapi import fuzzer
from backend.log.factory import Logger
from prance import ResolvingParser
import json
import copy
import io
import uuid
import os
from backend.tester.modules.openapi import openapi_parser
from backend.tester.modules.openapi.validator import response_validation

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
from backend.tester.modules.openapi.metadata_wrapper import (
    wrap_attribute_payload_metadata,
    wrap_attribute_payloads_metadata,
)
from backend.tester.modules.openapi.openapi_util import (
    get_api_client_module,
    get_api_dir,
    get_api_module,
    get_exceptions_module,
    get_gen_classes,
    get_model_module_path,
    init_configuration,
)


VALID_message = "All valid"
INLINE = "inline"
PARENT_ATTRIBUTE = "parent_attribute"
# Http Connection Read Timeout in seconds
READ_TIMEOUT = 20
SKIP_FILES = ["__init__.py", "__pycache__"]
STR = "str"
INT = "int"
INLINE_OBJ = "InlineObject"
# Indication that underlying object(collection of attributes) is a combination of primitives and/or inline objects
PARAM_OBJ = "ParamObject"
TEST_SPEC_PATH = "../openapi_specs/openapi3.yml"
MODEL_PACKAGE = "tester.modules.openapi.python_sdk.model"
# Assuming pdf is most popular file upload type? This assumption may be wrong
DEFAULT_VALID_FILE_TYPE = "yaml"

logger = Logger(__name__)

# Payload Generation logic:
# 1. For each attribute(json key) generate payloads
# 2. Prepare distinct openapi request objects with atmost one negative payload(atttibute value). A negative payload is one that doesn't adhere to input constraints
# 3. Send such requests iteratively

# Important wrapper objects:
# 1. Metadata object(dict)(payload metadata) that wraps generated payload along with message and constraint information
# 2. Metadata object(dict)(payloads metadata) that wraps positive(valid) and negative payloads

# Unsupported formats:
# 1. Int
# 2. Direct arrays(not as value of an object attribute). But that's probably not even a use-case

# Unit Test Cases:
# 1. Object with primitive attributes
# 2. Object with array of primitives
# 3. Object with mix of primitives and array(of primitives)
# 4. Nested objects:
#   4.1 Outer object: primitives & Inner object: primitives
#   4.2 Outer object: primitive & Inner object: array(of primitives)
#   4.3 Outer object: primitive & Inner object: array(of objects)


def get_json_payloads(
    input_params: List[str], openapi_types: Dict, validations: Dict, **kwargs
) -> List[Dict]:
    """
    Form and return different application/json payloads(path and body params) based on openapi validation constraints
    For each type of object(str, inline etc) prepare negative payloads and merge them with each other(str with str, str with inline and so on)
    """

    parent_attr = kwargs.get("parent_attribute")
    spec = kwargs.get("spec")
    path = kwargs.get("path")
    configuration = kwargs.get("configuration")
    data_dir = kwargs.get("data_dir")
    pkg_name = kwargs.get("pkg_name")

    # Prepare individual lists of fuzzed values for each attribute and add those lists to below list
    outer_param_payloads = []
    for param in input_params:

        pytype = get_python_type(
            param,
            openapi_types,
            data_dir,
            parent_attribute=kwargs.get("parent_attribute"),
        )

        # If param is primitive str
        if pytype == "str" or pytype == "int":
            validation_obj: Dict = process_validation_obj(validations)
            # Get all payloads(valid & negative) for 'param' string attribute
            attr_payloads = get_attribute_payloads_primitive(
                param, validation_obj[param], pytype
            )
            # print(attr_payloads)
            outer_param_payloads.append(attr_payloads)

        # if param is an array
        elif pytype == "array":
            # This array implementation assumes that array is a value and is part of an object,
            # which means that it has a key(parent attribute). Since, all application/json values must have string keys
            array_item_payloads = []
            python_type = get_class_type(param, openapi_types)
            if is_generated_class(python_type, data_dir):
                # Assuming array is of a single kind of object
                if param in openapi_types and len(openapi_types[param]) > 0:
                    # Change here to accomodate more than one kind of object inside the array
                    klass = openapi_types[param][0][0]
                    module_name = get_mod_name(klass)
                    new_openapi_type = {module_name: (klass,)}
                    attr_payloads = get_json_payloads(
                        [module_name],
                        new_openapi_type,
                        validations,
                        parent_attribute=parent_attr,
                        spec=spec,
                        path=path,
                        configuration=configuration,
                        data_dir=data_dir,
                        pkg_name=pkg_name,
                    )
                    # Transform single attribute payload values into array payloads
                    arr_payloads = fuzzer.get_array_payloads(attr_payloads)
                    array_item_payloads.append(arr_payloads)

            # For given parent attribute extract validation info directly from passed spec
            # since generator isn't generating for array of primitives at the moment (bug in generator?)
            else:
                item_validations = openapi_parser.get_from_spec(
                    path, spec, key=parent_attr, type="array"
                )
                property_validation_pairs = form_validation_openapi_type_details(
                    item_validations
                )

                for property_validation_pair in property_validation_pairs:
                    prop = property_validation_pair[0]
                    validation = property_validation_pair[1]
                    if param in openapi_types and len(openapi_types[param]) > 0:
                        # Change here to accomodate more than one kind of object inside the array
                        klass = openapi_types[param][0][0]
                        new_openapi_type = {param: (klass,)}
                        attr_payloads = get_json_payloads(
                            [prop],
                            new_openapi_type,
                            validation,
                            parent_attibute=parent_attr,
                            spec=spec,
                            path=path,
                            configuration=configuration,
                            data_dir=data_dir,
                            pkg_name=pkg_name,
                        )
                        # Transform single attribute payload values into array payloads
                        arr_payloads = fuzzer.get_array_payloads(
                            attr_payloads, validation
                        )
                        array_item_payloads.append(arr_payloads)

            combined_payloads = merge_sibling_mixed_attributes(
                array_item_payloads, data_dir
            )
            outer_param_payloads.append(combined_payloads)

        # If param is file
        elif pytype == "file":
            valid_file_types = openapi_parser.get_from_spec(path, spec, type="file")

            # If file type isn't specified in file description section, then pick a default.
            # TODO: Think of other data sources?
            if len(valid_file_types) == 0:
                valid_file_types = [DEFAULT_VALID_FILE_TYPE]

            file_attr_payloads = get_attribute_payloads_file(
                param, data_dir, valid_file_types=valid_file_types
            )
            outer_param_payloads.append(file_attr_payloads)

        # If param is an object
        elif pytype == "generated class":
            # Useful for merging nested objects

            obj = instantiate_class(param, pkg_name)

            # Validation constraints of members within given object
            obj_validations = process_validation_obj(obj.validations)

            # Get openapi types from object
            openapi_types = obj.openapi_types

            # Enumerate inline object attributes
            attr_payloads = get_attribute_payloads_obj(
                obj_validations, openapi_types, data_dir
            )

            # Merge enumerated primitive attribute payloads
            obj_attr_payloads = merge_sibling_primitive_attributes_obj(
                attr_payloads, obj, kwargs.get(PARENT_ATTRIBUTE)
            )

            attribute_module_name_triplets = get_nested_objects(openapi_types)
            # Iterate nested objects, get their attribute payloads and merge them with the parent object
            for attribute_module_name_triplet in attribute_module_name_triplets:
                parent_attr = attribute_module_name_triplet[0]
                module_name = attribute_module_name_triplet[1]
                object_type = attribute_module_name_triplet[2]

                # Nested object can either be an array or another object
                child_obj_attr_payloads = None
                if object_type == "array":
                    openapi_type_arr = {parent_attr: (module_name,)}
                    child_obj_attr_payloads = get_json_payloads(
                        [parent_attr],
                        openapi_type_arr,
                        None,
                        parent_attribute=parent_attr,
                        spec=spec,
                        path=path,
                        configuration=configuration,
                        data_dir=data_dir,
                        pkg_name=pkg_name,
                    )

                # Find attributes of nested objects recursively.
                # Validation dict will be extracted after object instantiation
                elif object_type == "generated class":
                    child_obj_attr_payloads = get_json_payloads(
                        [module_name],
                        openapi_types,
                        None,
                        parent_attribute=parent_attr,
                        spec=spec,
                        path=path,
                        configuration=configuration,
                        data_dir=data_dir,
                        pkg_name=pkg_name,
                    )

                # Merge sibling attributes (primitive with objects or arrays)
                obj_attr_payloads = merge_sibling_mixed_attributes_obj(
                    obj_attr_payloads,
                    child_obj_attr_payloads,
                    obj,
                    parent_attr,
                    data_dir=data_dir,
                )

            outer_param_payloads.append(obj_attr_payloads)

    # print(param_payloads)

    # Merge path and request body params to create a list of unique requests
    combined_payloads = merge_sibling_mixed_attributes(outer_param_payloads, data_dir)

    # pretty_print(combined_payloads)
    # print(combined_payloads)

    return combined_payloads


def get_mod_name(klass: Type[object]) -> str:
    """
    Get module name from class name
    """
    return convert_case(klass.__name__)


# This is a util function
def convert_case(camelcase_str):
    """
    Convert CamelCase to snake_case
    """
    res = [camelcase_str[0].lower()]
    for c in camelcase_str[1:]:
        if c in ("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            res.append("_")
            res.append(c.lower())
        else:
            res.append(c)

    return "".join(res)


def get_class_type(param: str, openapi_types: Dict) -> str:
    """
    Get class type. For ex: extract 'str' from class<str>
    """
    if param in openapi_types:
        # Get Tuple first value
        if len(openapi_types[param]) > 0:
            if (
                type(openapi_types[param][0]) is list
                and len(openapi_types[param][0]) > 0
            ):
                return openapi_types[param][0][0]
    return None


def form_validation_openapi_type_details(derived_validations: Dict) -> List:
    """
    Construct validation object(dict) & openapi_type from info derived directly from openapi spec
    """
    prop_validation_pairs = []
    for item in derived_validations:
        property = item["property"]
        min_items = item.get("minItems")
        max_items = item.get("maxItems")
        validation = {(property,): {}}
        openapi_type = {}
        item_validations = item["validations"]
        for item_validation in item_validations:
            if "pattern" in item_validation:
                validation[(property,)]["regex"] = {
                    "pattern": item_validation["pattern"]
                }
            if "maxLength" in item_validation:
                validation[(property,)]["max_length"] = item_validation["maxLength"]
            if "minimum" in item_validation:
                validation[(property,)]["minimum"] = item_validation["minimum"]
            if "maximum" in item_validation:
                validation[(property,)]["maximum"] = item_validation["maximum"]
            if min_items:
                validation[(property,)]["min_items"] = min_items
            if max_items:
                validation[(property,)]["max_items"] = max_items

            openapi_type[property] = (str,)
        prop_validation_pairs.append((property, validation, openapi_type))
    return prop_validation_pairs


def get_python_type(
    klass: Type[object], openapi_types, data_dir, parent_attribute=None
):
    """
    Extract openapi type for given field's class
    """
    for k, v in openapi_types.items():
        # Rely on passed attributes or parent attributes in case of nested objects
        if k == klass or k == parent_attribute:
            if v[0] == list or type(v[0]) == list:
                return "array"
            elif v[0] == str:
                return "str"
            elif v[0] == int:
                return "int"
            elif v[0] == bool:
                return "bool"
            elif v[0] == io.IOBase:
                return "file"
            elif is_generated_class(v[0], data_dir):
                return "generated class"

        if k == "requestBody":
            if v[0] == list:
                return "array"

    return None


def pretty_print(param: Dict):
    js = json.dumps(param, sort_keys=True, indent=4)
    print(js)


def instantiate_class(param: str, pkg_name: str):
    """
    Return instance given a class name
    """
    klass = extract_class(param)
    inline_obj = getattr(get_model_module_path(pkg_name, param), klass)
    return inline_obj


def get_nested_objects(openapi_types: Dict) -> str:
    """
    Check if param has a nested openapi generated object and return triplet of (attribute, class name, class type)
    """
    nested_objects = []
    for k, v in openapi_types.items():
        # v happens to be a tuple hence the 0 index
        # TODO: Do something about array type nested object
        if type(v[0]) == list:
            nested_objects.append((k, v[0], "array"))
        elif is_generated_class(v[0]):
            nested_objects.append(
                (k, get_qualified_module_name(v[0]), "generated class")
            )
    return nested_objects


def get_qualified_module_name(klass: Type[object]):
    """
    Get the module name only from fully qualified module path
    """
    fully_qualified_module_name = klass.__module__
    temp = fully_qualified_module_name.split(".")
    module_name = temp[len(temp) - 1]
    # print(module_name)
    return module_name


def is_primitive(param: str) -> bool:
    """
    Check if given param is a primitive like int or str
    """
    return param.__class__.__module__ == "builtins"


def is_generated_class(klass: Type[object], data_dir) -> bool:
    """
    Check if given class name is openapi generated one
    """
    gen_classes_path = [
        extract_class(module) for module in get_generated_modules(data_dir)
    ]
    class_name = klass.__name__
    if class_name in gen_classes_path:
        return True
    return False


def get_generated_modules(data_dir) -> List:
    """
    Get generated models/classes
    """
    gen_classes_path = get_gen_classes(data_dir)
    return [get_module_name(item) for item in os.listdir(gen_classes_path)]


def merge_sibling_mixed_attributes(param_payloads, data_dir) -> List:
    """
    Merge all attributes at same level into an array with atmost one attribute with negative payload
    """

    param_payloads_len = len(param_payloads)
    valid_payload = None
    negative_payloads = []

    if param_payloads_len == 1:
        # Nothing to merge
        return param_payloads[0]

    for i in range(0, param_payloads_len):

        # Add an entry of all valid attribute values
        if i == 0:
            attributes: List = []
            for m in range(i, param_payloads_len):
                attributes.append(
                    get_attribute_values(
                        param_payloads[m]["valid"],
                        data_dir=data_dir,
                        additional_info=param_payloads[m]["valid"].get(
                            "additional_info"
                        ),
                    )
                )
            attr_payload_metadata = wrap_attribute_payload_metadata(
                value=attributes, message=VALID_message
            )
            valid_payload = attr_payload_metadata

        attr_negative_payload = param_payloads[i].get("attribute")

        # Iterate negative payloads for attribute at index `i`
        for payload in param_payloads[i]["negative"]:
            attr_request_object = []
            # Iterate all attributes(and pick their valid values) before the one at index `i`
            for j in range(0, i):
                attr_request_object.append(
                    get_attribute_values(
                        param_payloads[j]["valid"],
                        data_dir=data_dir,
                        additional_info=param_payloads[j]["valid"].get(
                            "additional_info"
                        ),
                    )
                )

            # Pick the negative payload value for attribute at index `i`
            attr_request_object.append(
                get_attribute_values(
                    payload,
                    data_dir=data_dir,
                    additional_info=payload.get("additional_info"),
                )
            )

            # Iterate all attributes(and pick their valid values) after the one at index `i`
            for k in range(i + 1, param_payloads_len):
                attr_request_object.append(
                    get_attribute_values(
                        param_payloads[k]["valid"],
                        data_dir=data_dir,
                        additional_info=param_payloads[k]["valid"].get(
                            "additional_info"
                        ),
                    )
                )

            attr_payload_metadata = wrap_attribute_payload_metadata(
                value=attr_request_object,
                attribute=attr_negative_payload,
                metadata=payload,
            )

            negative_payloads.append(attr_payload_metadata)

    # Wrap positive and negative payloads into a dict useful for merging
    attr_payloads = wrap_attribute_payloads_metadata(
        None, PARAM_OBJ, valid_payload, negative_payloads
    )

    return attr_payloads


def merge_sibling_primitive_attributes_obj(
    attr_payloads: List,
    inline_obj: object,
    parent_attribute: str = None,
    configuration=None,
) -> List:
    """
    Merge all primitive attributes of an object with atmost one negative attribute payload for each request
    """
    attr_payload_len = len(attr_payloads)
    valid_payload = None
    negative_payloads = []

    for i in range(0, attr_payload_len):

        # Inline object attribute with negative payloads
        attr_negative_payload = attr_payloads[i]["attribute"]

        # Add an entry of all valid attribute values
        if i == 0:
            inline_attributes: Dict = {}
            for m in range(i, attr_payload_len):
                attr = attr_payloads[m]["attribute"]
                inline_attributes[attr] = attr_payloads[m]["valid"]["value"]
            inline_object = inline_obj(
                _configuration=configuration, **inline_attributes
            )
            inline_metadata_obj = wrap_attribute_payload_metadata(
                value=inline_object, message=VALID_message
            )
            valid_payload = inline_metadata_obj

        # Iterate negative payloads for attribute at index `i`
        for payload in attr_payloads[i]["negative"]:
            inline_attributes: Dict = {}
            inline_attributes[attr_negative_payload] = payload["value"]
            # Consider valid value for attributes before the one at index `i`
            for j in range(0, i):
                attr = attr_payloads[j]["attribute"]
                inline_attributes[attr] = attr_payloads[j]["valid"]["value"]
            # Consider valid value for attributes after the one at index `i`
            for k in range(i + 1, attr_payload_len):
                attr = attr_payloads[k]["attribute"]
                inline_attributes[attr] = attr_payloads[k]["valid"]["value"]

            # Form inline object
            inline_object = inline_obj(
                _configuration=configuration, **inline_attributes
            )
            # Bubble up negative payload attribute details like constraint and message.
            inline_metadata_obj = wrap_attribute_payload_metadata(
                value=inline_object, attribute=attr_negative_payload, metadata=payload
            )
            negative_payloads.append(inline_metadata_obj)

    # Wrap positive and negative payloads into a dict useful for merging
    # Add parent attribute in case of merging attributes of a nested object
    attr_payloads = wrap_attribute_payloads_metadata(
        parent_attribute, INLINE_OBJ, valid_payload, negative_payloads
    )

    return attr_payloads


def merge_sibling_mixed_attributes_obj(
    parent_attr_obj: Dict,
    child_attr_obj: Dict,
    parent_obj: object,
    parent_attribute: str = None,
    configuration=None,
    data_dir=None,
) -> List:
    """
    Merge sibling attributes(primitive, array, objects) of an object by merging child object into parent object.
    """
    valid_payload = None
    negative_payloads = []

    # Form an all positive(valid) object
    child_attribute = get_attribute_values(
        child_attr_obj["valid"],
        data_dir=data_dir,
        additional_info=child_attr_obj["valid"].get("additional_info"),
    )
    attributes = get_attribute_values(
        parent_attr_obj["valid"],
        data_dir=data_dir,
        additional_info=parent_attr_obj["valid"].get("additional_info"),
    )
    attributes[parent_attribute] = child_attribute
    parent_object = parent_obj(_configuration=configuration, **attributes)

    inline_metadata_obj = wrap_attribute_payload_metadata(
        value=parent_object, message=VALID_message
    )
    valid_payload = inline_metadata_obj

    # parent negative
    # child positive
    for item in parent_attr_obj["negative"]:
        attribute = item["attribute"]
        attributes = get_attribute_values(
            item, data_dir=data_dir, additional_info=item.get("additional_info")
        )
        attributes[parent_attribute] = get_attribute_values(
            child_attr_obj["valid"],
            data_dir=data_dir,
            additional_info=child_attr_obj["valid"].get("additional_info"),
        )
        parent_object = parent_obj(_configuration=configuration, **attributes)
        # print(parent_object)
        parent_metadata_obj = wrap_attribute_payload_metadata(
            value=parent_object, attribute=attribute, metadata=item
        )
        negative_payloads.append(parent_metadata_obj)

    # parent positive
    # child negative
    for item in child_attr_obj["negative"]:
        attribute = item["attribute"]
        child_attribute = get_attribute_values(
            item, data_dir=data_dir, additional_info=item.get("additional_info")
        )
        attributes = get_attribute_values(
            parent_attr_obj["valid"],
            data_dir=data_dir,
            additional_info=parent_attr_obj["valid"].get("additional_info"),
        )
        attributes[parent_attribute] = child_attribute
        parent_object = parent_obj(_configuration=configuration, **attributes)

        parent_metadata_obj = wrap_attribute_payload_metadata(
            value=parent_object, attribute=attribute, metadata=item
        )
        negative_payloads.append(parent_metadata_obj)

    # Wrap positive and negative payloads into a dict useful for merging
    # Add parent attribute in case of merging attributes of a nested object
    attr_payloads = wrap_attribute_payloads_metadata(
        parent_attribute, INLINE_OBJ, valid_payload, negative_payloads
    )

    return attr_payloads


def get_attribute_values(obj, data_dir=None, additional_info=None):
    """
    Get attribute values (valid & negative) from object. Use data_store property if attribute is an object or else extract values directly(primitive)
    """
    if obj:
        if "value" in obj and hasattr(obj["value"], "_data_store"):
            return copy.deepcopy(obj["value"]._data_store)
        elif "value" in obj and isinstance(obj["value"], io.IOBase):
            # If value is file object, replace it with a new file for each composed payload
            # as the generator api calling logic closes file object(s) after sending them
            file_handle: Dict = get_file_payloads(
                data_dir, file_type=additional_info["file_type"]
            )
            return file_handle["file_handle"]
        else:
            return copy.deepcopy(obj["value"])
    return {}


def get_attribute_payloads_obj(
    validations: Dict, openapi_types: Dict, data_dir: str
) -> List:
    """
    Generate (fuzzed) values based on various validation constraints for each attribute
    """
    attribute_payloads = []
    for k, v in validations.items():
        # 'v' is a dict of validation constraints for given attribute 'k'
        pytype = get_python_type(k, data_dir, openapi_types)
        if pytype == "str" or pytype == "int":
            attribute_payload = get_attribute_payloads_primitive(k, v, pytype)
            attribute_payloads.append(attribute_payload)

    return attribute_payloads


def get_attribute_payloads_primitive(
    attribute: str, validations: Dict, pytype: str
) -> Dict:
    """
    Generate (fuzzed) values based on various validation constraints for each attribute
    """
    negative_attr_payloads = []
    valid_attr_payload = None
    attribute_type = None
    if pytype == "str":
        valid_attr_payload = get_attribute_positive_payload_str(attribute, validations)
        negative_attr_payloads = get_attribute_negative_payloads_str(
            attribute, validations
        )
        attribute_type = STR
    if pytype == "int":
        valid_attr_payload = get_attribute_positive_payload_int(attribute, validations)
        negative_attr_payloads = get_attribute_negative_payloads_int(
            attribute, validations
        )
        attribute_type = INT

    attribute_payload = wrap_attribute_payloads_metadata(
        attribute, attribute_type, valid_attr_payload, negative_attr_payloads
    )

    return attribute_payload


def get_attribute_positive_payload_str(
    attribute: str, validation_constraints: Dict
) -> Dict:
    """
    Prepare positive payload for given attribute
    """
    max_length = None
    pattern = None
    for k1, v1 in validation_constraints.items():
        if k1 == "max_length":
            max_length = v1
        if k1 == "regex":
            pattern = v1["pattern"]

    value = fuzzer.get_valid_str(max_length, pattern)
    payload_metadata = wrap_attribute_payload_metadata(
        value=value, attribute=attribute, message=VALID_message
    )
    return payload_metadata


def get_attribute_positive_payload_int(
    attribute: str, validation_constraints: Dict
) -> Dict:
    """
    Prepare positive payload for given attribute
    """
    min_length = None
    max_length = None
    # valid_request_detail['attribute'] = attribute
    for k1, v1 in validation_constraints.items():
        if k1 == "minimum":
            min_length = v1
        if k1 == "maximum":
            max_length = v1

    value = fuzzer.get_valid_int(min_length, max_length)
    payload_metadata = wrap_attribute_payload_metadata(
        value=value, attribute=attribute, message=VALID_message
    )
    return payload_metadata


def get_attribute_negative_payloads_str(
    attribute: str, validation_constraints: Dict
) -> List[Dict]:
    """
    Prepare negative payloads for given attribute
    """
    neg_attr_details = []
    for k1, v1 in validation_constraints.items():
        if k1 == "max_length":
            value = fuzzer.get_length_fuzz_str(v1)
            message = f"Invalid value for {attribute}, length must be less than or equal to {v1}"
            constraint = "Max Length"
            payload_metadata = wrap_attribute_payload_metadata(
                value=value, attribute=attribute, message=message, constraint=constraint
            )
            neg_attr_details.append(payload_metadata)
        if k1 == "regex":
            regex = v1["pattern"]
            value = fuzzer.get_regex_fuzz_str(regex)
            message = (
                f"Invalid value for {attribute}, must match regular expression {regex}"
            )
            constraint = "Pattern"
            payload_metadata = wrap_attribute_payload_metadata(
                value=value, attribute=attribute, message=message, constraint=constraint
            )
            neg_attr_details.append(payload_metadata)
    return neg_attr_details


def get_attribute_payloads_file(
    attribute: str, data_dir, valid_file_types=None
) -> List[Dict]:
    """
    Prepare file payloads
    """
    neg_attr_payloads = []
    # File type picked from spec
    valid_file_type = None
    if len(valid_file_types) > 0:
        valid_file_type = valid_file_types[0]

    file_payloads: Dict = get_file_payloads(data_dir, valid_file_type)

    valid_file_payload = file_payloads["valid"]
    negative_file_payloads = file_payloads["negative"]

    valid_attr_payload = wrap_attribute_payload_metadata(
        value=valid_file_payload["file_handle"],
        attribute=attribute,
        message="Upload valid file type: " + valid_file_payload["file_type"],
        additional_info={"file_type": valid_file_type},
    )

    for negative_file_payload in negative_file_payloads:
        file_handle = negative_file_payload["file_handle"]
        file_type = negative_file_payload["file_type"]
        negative_attr_payload = wrap_attribute_payload_metadata(
            value=file_handle,
            attribute=attribute,
            message="Upload incorrect file type: " + file_type,
            constraint="file type",
            additional_info={"file_type": file_type},
        )
        neg_attr_payloads.append(negative_attr_payload)

    attribute_payloads = wrap_attribute_payloads_metadata(
        attribute, FILE_ATTRIBUTE_TYPE, valid_attr_payload, neg_attr_payloads
    )

    return attribute_payloads


def get_file_payloads(data_dir, valid_file_type=None, file_type=None) -> Dict:
    """
    Return generated file handles
    """
    # Get file handle for given file_type
    if file_type:
        file_handle = get_generated_file_handles(data_dir, file_type)
        return file_handle

    # File type picked from spec(after parsing) or the default
    elif valid_file_type:
        return prepare_file_payloads(valid_file_type, data_dir)


def prepare_file_payloads(in_file_type: str, data_dir: str) -> List[Dict]:
    valid_negative_file_payloads: Dict = {}
    negative_file_payloads = []
    valid_file_handle = None
    # Generate all file handles and separate out valid & negative ones.
    file_handles = get_generated_file_handles(data_dir, file_type=None)
    for file_handle in file_handles:
        if in_file_type == file_handle["file_type"]:
            valid_file_handle = file_handle
        else:
            negative_file_payloads.append(file_handle)

    valid_negative_file_payloads["valid"] = valid_file_handle
    valid_negative_file_payloads["negative"] = negative_file_payloads

    return valid_negative_file_payloads


def get_attribute_negative_payloads_int(
    attribute: str, validation_constraints: Dict
) -> List[Dict]:
    """
    Prepare negative payloads for given attribute
    """
    neg_attr_details = []
    for k1, v1 in validation_constraints.items():
        if k1 == "minimum":
            value = fuzzer.get_min_int(v1)
            message = "Min length violation"
            constraint = "Min Length"
            payload_metadata = wrap_attribute_payload_metadata(
                value=value, attribute=attribute, message=message, constraint=constraint
            )
            neg_attr_details.append(payload_metadata)
        if k1 == "maximum":
            value = fuzzer.get_max_int(v1)
            message = "Max length violation"
            constraint = "Max length"
            payload_metadata = wrap_attribute_payload_metadata(
                value=value, attribute=attribute, message=message, constraint=constraint
            )
            neg_attr_details.append(payload_metadata)
    return neg_attr_details


def process_validation_obj(validations: Dict) -> Dict:
    """
    Process validation dict such that string key is extracted from tuple key
    """
    # Pre-processing validations dict {(key1, ): 'value'} to extract string key from tuple based key
    # TODO: Check if below processing logic will hold if more than one attribute is present in inline object
    validationS: Dict = {k[0]: v for k, v in validations.items()}

    # print(validationS)
    return validationS


def extract_class(param):
    """
    Extracts class name from module name. Class name happens to be capitalized version of module name
    Args:
        param: inline_objectX string

    Returns:
    Convert inline_objectX to InlineObjectX
    """
    return to_camel_case(param)


def to_camel_case(param: str) -> str:
    """
    Convert given string from snake case to camel case
    """
    return param.replace("_", " ").title().replace(" ", "")


def get_module_name(file_name: str) -> str:
    """
    Get module name from python file name by trimming .py extension
    """
    return os.path.splitext(file_name)[0]


def get_all_endpoint_paths(api_obj) -> List:
    """
    Get all endpoint paths for given api client instance
    """

    endpoint_settings = get_endpoint_objs(api_obj)
    return [item.settings["endpoint_path"] for item in endpoint_settings]


def get_endpoint_obj(endpoint_path: str, api_instances: List[object]) -> List[object]:
    """
    Get endpoint object for given endpoint path from list of all api instances
    """
    for api_instance in api_instances:
        endpoint_objs = get_endpoint_objs(api_instance)
        for item in endpoint_objs:
            if item.settings["endpoint_path"] == endpoint_path:
                return (api_instance, item)
    return None


def get_api_operation_id(endpoint_obj: object):
    """
    Get operation id from given endpoint object
    """
    return endpoint_obj.settings["operation_id"]


def get_api_http_method(endpoint_obj: object):
    """
    Get operation id from given endpoint object
    """
    return endpoint_obj.settings["http_method"]


def get_api_params_map(endpoint_obj: object, filter_key=None) -> Dict:
    """
    Get params map from given endpoint object
    """
    if filter_key:
        return endpoint_obj.params_map[filter_key]
    return endpoint_obj.params_map()


def get_api_validations(endpoint_obj: object) -> Dict:
    """
    Get validations from given endpoint object
    """
    return endpoint_obj.validations


def get_api_param_types(endpoint_obj: object) -> Dict:
    """
    Get openapi type information from given endpoint object
    """
    return endpoint_obj.openapi_types


def get_endpoint_obj_names(api_obj) -> List:
    """
    Get endpoint object attribute names from api client instance
    """
    return list(filter(lambda a: "_endpoint" in a, dir(api_obj)))


def get_endpoint_objs(api_obj) -> List:
    """
    Get endpoint objects from api client instance
    """
    endpoint_obj_names = get_endpoint_obj_names(api_obj)
    return [getattr(api_obj, item) for item in endpoint_obj_names]


def get_api_instances(api_client: object, data_dir: str, pkg_name: str) -> List:
    """
    Prepare list of api instances from generated openapi files
    """
    api_instance_lis = []
    api_path = get_api_dir(data_dir)
    for file_name in os.listdir(api_path):
        # Skip __init__.py
        if file_name in SKIP_FILES:
            continue
        # Extract module name from file name
        api_module = get_module_name(file_name)
        # Get class name from module name
        klass = to_camel_case(api_module)
        # Instantiate class
        api_instance = getattr(get_api_module(api_module, pkg_name), klass)(api_client)
        api_instance_lis.append(api_instance)

    return api_instance_lis


def extract_payloads(attribute_payloads: List[Dict]) -> Tuple[List, List[List]]:
    """
    Extract negative payloads from attribute payload dict
    """
    payloads: List = []
    request_metadata: List = []
    for item in attribute_payloads["negative"]:
        request_metadata.append(
            {
                "message": item.get("message"),
                "constraint": item.get("constraint"),
                "attribute": item.get("attribute"),
            }
        )
        payloads.append(item["value"])
    return (request_metadata, payloads)


def get_openapi_spec(spec_path: str):
    """
    Get openapi in dict form
    """
    parser = ResolvingParser(spec_path)
    spec = parser.specification
    return spec


def get_path_params(payload: List, path_params: List) -> Dict:
    """
    Return a dict of path params. Ideally in the openapi model, path parameters appear at the top(in order)
    """
    if len(payload) < len(path_params):
        raise Exception(
            "Could not extract path parameter values from payload. Payload could be malformed"
        )

    return dict(zip(path_params, payload))


def extract_path_params(api_path):
    """
    Extract path params from api path. For example extract `petName` from http://localhost:80/pets/v1/{petName}
    """
    match_groups = [
        x.group().replace("{", "").replace("}", "")
        for x in re.finditer(
            r"{(.*?)}",
            api_path,
        )
    ]
    return match_groups


def _invoke_apis(
    run_id: str,
    api_path: str,
    spec_path: str,
    data_dir: str,
    run_dir: str,
    gen_package_name: str,
    auth_headers: List[Dict],
) -> List[Dict]:
    """
    Invoker apis with negative payloads for each attribute in request(body and path params)
    """
    configuration = init_configuration(gen_package_name)
    api_client_module = get_api_client_module(gen_package_name)
    exceptions_module = get_exceptions_module(gen_package_name)
    response_list: List[Dict] = []
    request_metadata: List[Dict] = []
    with api_client_module.ApiClient(configuration) as api_client:

        spec = get_openapi_spec(spec_path)

        # Extract path params from api path. Needed to form path params dict for request validation
        path_param_keys = extract_path_params(api_path)

        # Create an instances of the API class
        api_instances = get_api_instances(api_client, data_dir, gen_package_name)

        # Testing operationId to api function mapping
        api_instance, endpoint_obj = get_endpoint_obj(api_path, api_instances)
        api_func_name = get_api_operation_id(endpoint_obj)

        input_params: Dict = get_api_params_map(endpoint_obj, "required")
        # Get validations on the endpoint object itself. These are usually applicable for the primitives
        validations: Dict = get_api_validations(endpoint_obj)
        openapi_types: Dict = get_api_param_types(endpoint_obj)

        logger.info(
            f"Preparing fuzzed payloads with run_id: {run_id} for api: {api_path}"
        )
        combined_fuzzed_payloads = get_json_payloads(
            input_params,
            openapi_types,
            validations,
            spec=spec,
            path=api_path,
            configuration=configuration,
            data_dir=data_dir,
            pkg_name=gen_package_name,
        )

        request_metadata, attribute_payloads = extract_payloads(
            combined_fuzzed_payloads
        )
        # print(attribute_payloads)

        host_url = configuration.get_host_from_settings(index=None)
        # This mimetype is for response validation. TODO: Need to pick these from actual responses(har file ?)
        mimetype = "application/json"
        http_method = get_api_http_method(endpoint_obj).lower()

        # Pass fuzzed payloads one at a time
        response_data = None
        response_status = None
        response_headers = None
        logger.info(
            f"Sending fuzzed requests with run_id: {run_id} for api: {api_path}"
        )

        # Counter to keep track of how many tests ran(payloads were sent)
        payload_count = len(attribute_payloads)
        counter = 0

        for req_metadata, attribute_payload in zip(
            request_metadata, attribute_payloads
        ):
            # Set additional headers

            # Set request_id header
            # Generate and  attach unique request id for each request
            # Use it to capture request proxied through zap
            request_id = uuid.uuid4().hex
            api_client.set_default_header(REQUEST_ID, request_id)

            api_client.set_default_header(DATA_DIR, run_dir)

            # Set auth headers
            for auth_header in auth_headers:
                for header_name, header_value in auth_header.items():
                    api_client.set_default_header(header_name, header_value)

            req_metadata[REQUEST_ID] = request_id

            try:
                logger.info(
                    f"Sending request: {attribute_payload} with run_id: {run_id} for request_id: {request_id}"
                )

                # If payload is a list
                if isinstance(attribute_payload, list):
                    api_function = getattr(api_instance, api_func_name)
                    response: urllib3.HTTPResponse = api_function(
                        *attribute_payload,
                        _request_timeout=READ_TIMEOUT,
                        _preload_content=False,
                        _check_return_type=False,
                    )
                    response_data = response.data
                    response_status = response.status
                else:
                    # If payload is primitive
                    response: urllib3.HTTPResponse = getattr(
                        api_instance, api_func_name
                    )(
                        attribute_payload,
                        _request_timeout=READ_TIMEOUT,
                        _preload_content=False,
                        _check_return_type=False,
                    )
                    response_data = response.data
                    response_status = response.status
                    response_headers = response.headers

                counter = counter + 1
            except exceptions_module.ApiValueError as ae:
                logger.error(f"Api Value Error:  {str(ae)}")
                counter = counter + 1
            except exceptions_module.ApiException as api_exception:
                logger.error(f"Api Exception Error: {str(api_exception)}")
                response_data = api_exception.body
                response_status = api_exception.status
                response_headers = api_exception.headers
                counter = counter + 1
            except exceptions_module.ApiAttributeError as ae:
                logger.error(f"Api Attribute Error: {str(ae)}")
                counter = counter + 1
            except Exception:
                counter = counter + 1
                logger.exception(f"Test Invocation failed for request_id: {request_id}")

            # Form response object for each request
            full_api_path = urljoin(host_url, api_path)

            # Now that we are storing the har(http archive) file.
            # These details can be picked up from har data itself in conformance.py file
            response_obj = {
                REQUEST_ID: request_id,
                "full_api_path": full_api_path,
                # "path_params": path_params,
                "mimetype": mimetype,
                "http_method": http_method,
                "response_headers": response_headers,
                "response_data": response_data,
                "response_status": response_status,
            }
            response_list.append(response_obj)

        logger.info(f"Payloads generated: {payload_count}, sent: {counter}")
        if counter == payload_count:
            logger.info(f"All generated payloads were sent")

    return (request_metadata, response_list)


if __name__ == "__main__":
    api_path = "/users/v1/{username}/email"
    _invoke_apis(api_path, TEST_SPEC_PATH)
