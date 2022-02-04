from typing import Dict, List


def wrap_attribute_payloads_metadata(
    attribute: str, attribute_type: str, valid_payload: Dict, negative_payloads: List
) -> Dict:
    """
    Wrap positive(valid) and negative payloads into a dict
    """
    attr_payloads_metadata_obj = {}
    attr_payloads_metadata_obj["attribute"] = attribute
    attr_payloads_metadata_obj["attributeType"] = attribute_type
    attr_payloads_metadata_obj["valid"] = valid_payload
    attr_payloads_metadata_obj["negative"] = negative_payloads
    return attr_payloads_metadata_obj


def wrap_attribute_payload_metadata(
    value=None, attribute=None, metadata=None, **kwargs
):
    """
    Wrap given attribute value inside a metadata dict. Item may either be a primitive(str or int) or inline object
    """
    metadata_obj = {}
    metadata_obj["value"] = value
    metadata_obj["attribute"] = attribute
    # Use passed metadata if it exists:
    if metadata:
        if "attribute" in metadata:
            metadata_obj["attribute"] = metadata.get("attribute")
        if "remarks" in metadata:
            metadata_obj["remarks"] = metadata.get("remarks")
        if "constraint" in metadata:
            metadata_obj["constraint"] = metadata.get("constraint")
        return metadata_obj
    else:
        for k, v in kwargs.items():
            metadata_obj[k] = v
        return metadata_obj
