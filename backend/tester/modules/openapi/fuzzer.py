import rstr
from typing import Dict, List
import copy
import random
from backend.tester.modules.openapi.metadata_wrapper import (
    wrap_attribute_payload_metadata,
)


max_num_limit = 999999999999999

# TODO: Add following tests:
# 1. Required items
# 2. Unique items(array)


def get_length_fuzz_str(length: int) -> str:
    """
    Test max_length:
    Return payload that exceed given length(max_length)
    """
    return rstr.rstr("abc", length, length + 1)


def get_regex_fuzz_str(regex: str) -> str:
    """
    Test regex:
    Return payload that's built from a regex but includes an special char not present in given regex
    """
    # TODO: Improve below logic to create words with more special chars(those that aren't part of given pattern!)
    return rstr.xeger(regex)


def get_valid_str(max_length: int, pattern: str) -> str:
    """
    Generate payloads that adhere to given constraints
    """
    return "valid"


def get_valid_int(minimum: int, maximum: int) -> int:
    """
    Generate an integer betweem minimum and maximum limits
    """
    return random.randrange(minimum, maximum)


def get_max_int(maximum: int) -> int:
    """
    Generate an integer greater than maximum limit
    """
    return random.randrange(maximum, max_num_limit)


def get_min_int(minimum: int) -> int:
    """
    Generate an integer below minimum limit
    """
    return random.randrange(0, minimum)


def get_max_number(maximum: int) -> int:
    """
    Generate an number(float/double) greater than maximum limit
    """
    return random.randrange(maximum, max_num_limit)


def get_min_number(minimum: int) -> int:
    """
    Generate a number(float/double) below minimum limit
    """
    return random.randrange(0, minimum)


def get_valid_number(minimum: int, maximum: int) -> int:
    """
    Generate an float/double betweem minimum and maximum limits
    """
    return random.uniform(minimum, maximum)


def get_array_payloads(attribute_payloads: Dict, validation: Dict) -> List:
    """
    Generate arrays that fall outside given constraints given valid and negative payloads
    TODO: Use array constraints (minLength, maxLength) to form invalid arrays
    """

    attribute_payloads_copy = copy.deepcopy(attribute_payloads)

    # Enclose valid value in an array
    valid_value = attribute_payloads["valid"]["value"]
    encl_valid_value = [valid_value]
    attribute_payloads_copy["valid"]["value"] = encl_valid_value

    # Enclose each negative value in an array
    negative_values = attribute_payloads["negative"]
    attribute = attribute_payloads["attribute"]
    encl_negative_values = []
    for item in negative_values:
        item_copy = copy.deepcopy(item)
        item_copy["value"] = [item["value"]]
        encl_negative_values.append(item_copy)

    min_items = validation.get((attribute,)).get("min_items")
    max_items = validation.get((attribute,)).get("max_items")

    # Add few more tests(min and max array items)
    if min_items:
        min_array_items_payload = get_min_array(min_items, attribute, valid_value)
        encl_negative_values.append(min_array_items_payload)
    if max_items:
        max_array_items_payload = get_max_array(max_items, attribute, valid_value)
        encl_negative_values.append(max_array_items_payload)

    attribute_payloads_copy["negative"] = encl_negative_values

    return attribute_payloads_copy


def get_min_array(min_items: int, attribute: str, value) -> List:
    """
    Generate array of items less that minItems
    """
    min_payloads = []
    if min_items > 1:
        for i in range(0, min_items - 1):
            min_payloads.append(value)

    message = "Array min items violation"
    constraint = "Array minItems"
    payload_metadata = wrap_attribute_payload_metadata(
        value=min_payloads, attribute=attribute, message=message, constraint=constraint
    )
    return payload_metadata


def get_max_array(max_items: int, attribute: str, value) -> List:
    """
    Generate array of items more than maxItems
    """
    max_payloads = []
    for i in range(0, max_items + 1):
        max_payloads.append(value)

    message = "Array max items violation"
    constraint = "Array maxItems"
    payload_metadata = wrap_attribute_payload_metadata(
        value=max_payloads, attribute=attribute, message=message, constraint=constraint
    )
    return payload_metadata
