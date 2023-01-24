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
