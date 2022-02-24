import json
import re
from typing import Dict, List

from misc.log_pattern import RegexPattern
from log.factory import Logger
from utils.constants import SAVED_REGEX_FILE, SENSITIVE_DATA_REGEX, OTHER_REGEX

logger = Logger(__name__)


def find_login_occurrence(line, pattern):
    return len(re.findall(pattern, line))


def _find_sensitive_data(line, sensitive_data_regex_match: Dict, sensitive_data_regex_map: List[Dict]):
    for item in sensitive_data_regex_map:
        regexp = item["value"]
        regex_key = item["key"]
        # Search(each line of file) and break on first match
        # TODO: Explore the difference b/w re.search vs re.findall. Is there a chance of missing out valid matches
        result = re.search(regexp, line)
        if result:
            print("Match for " + regex_key + " and value " + result.group(0))
            logger.info(f"Match found for regex key {regex_key} and value {result.group(0)}")
            sensitive_data_regex_match[regex_key] = True

    return is_sensitive_data_match_satisfied(sensitive_data_regex_match)


def find_sensitive_data(path: str, regex_pattern: RegexPattern):
    sensitive_data_regex_map: List[Dict] = regex_pattern.get_sensitive_data_regex()

    sensitive_data_regex_match = {}
    sensitive_data_match_satisfied = False
    init_sensitive_data_regex_match(sensitive_data_regex_match, sensitive_data_regex_map)

    # Read file line by line and perform regex match
    with open(path, 'r') as f:
        for line in f:

            # Count login success and failure counts as per user attempts
            # login_success_count = find_login_occurrence(line, login_pattern)
            # login_failed_count = find_login_occurrence(line, logout_pattern)

            # Skip matching further log lines once all sensitive regexes have matched/found
            if not sensitive_data_match_satisfied:
                sensitive_data_match_satisfied = _find_sensitive_data(line, sensitive_data_regex_match,
                                                                      sensitive_data_regex_map)


def is_sensitive_data_match_satisfied(sensitive_data_regex_match):
    match_count = 0
    for _, is_matched in sensitive_data_regex_match.items():
        if is_matched:
            match_count = match_count + 1

    # Return if all sensitive regexp are already found in lines that have passed.
    # This information can be used to skip matching further lines
    if len(sensitive_data_regex_match) == match_count:
        return True

    return False


def init_sensitive_data_regex_match(sensitive_data_regex_match: Dict, sensitive_data_regex_map: List[Dict]):
    """
    Init regex match found to false
    :param sensitive_data_regex_match: Regex_to_is_match_dict
    :param sensitive_data_regex_list: Input regex list
    """
    for item in sensitive_data_regex_map:
        regex_key = item["key"]
        sensitive_data_regex_match[regex_key] = False


def read_regex_patterns():
    """
    Return RegexPattern object that consists of list of sensitive and other regexes
    :return:
    """
    with open(SAVED_REGEX_FILE, 'r') as fp:
        data = json.load(fp)
        sensitive_data_regex = data[SENSITIVE_DATA_REGEX]
        other_regex = data[OTHER_REGEX]
        regex_pattern = RegexPattern(sensitive_data_regex=sensitive_data_regex, other_regex=other_regex)
    return regex_pattern


if __name__ == "__main__":
    regex_pattern = read_regex_patterns()
    test_file_path = "/home/kali/Desktop/scripbox_response.raw"
    find_sensitive_data(test_file_path, regex_pattern)
