import bleach
from typing import List


def bleach_list(list_str: List[str]) -> list:
    """Sanitizes a list of strings with bleach.clean()

    Args:
        list_str (List[str]): A list containing only str elements.

    Returns:
        list: A sanitized list.
    """
    for item in list_str:
        list_str[list_str.index(item)] = bleach.clean(item)
    return list_str


def remove_matching_elements(list_str: List[str], match: str) -> list:
    """Removes every element from a list that matches a given string.

    Args:
        list_str (List[str]): A list containing only str elements.
        match (str): A string to match.

    Returns:
        list: A list without matching elements.
    """
    for item in list_str:
        if item == match:
            list_str.remove(item)
    return list_str


def format_string(input: str) -> str:
    """removes all weird escape characters, excess spaces and the like from the inputted data.

    Args:
        input (str): a possibly unformatted input string

    Returns:
        str: formatted, sanitized output
    """
    input.replace("\n", "")
    input = input.replace("\\", "")
    input = input.replace("\t", "")
    input = input.replace("\r", "")
    input = input.replace("\b", "")
    input = input.replace("\f", "")

    input = " ".join(input.split())
    input = bleach.clean(input)
    return input


def remove_url_parameters(input_url: str) -> str:
    """
    removes url parameters by cutting off everything after before a '?' symbol
    Args:
        input_url (str): url to remove parameters from

    Returns:
        str: clean url
    """
    if input_url.find("?") > -1:
        return input_url[0 : input_url.find("?")]
    else:
        return input_url
