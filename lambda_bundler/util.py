import hashlib
import typing

def get_content_of_files(*list_of_paths: typing.List[str]) -> typing.List[str]:
    """
    Returns a list with the content of each file in list_of_paths.

    :return: A list of strings with the content of each file in list_of_paths.
    :rtype: typing.List[str]
    """

    contents = []

    for path in list_of_paths:
        with open(path) as file_handle:
            contents.append(file_handle.read())

    return contents

def hash_string(string_to_hash: str) -> str:
    """
    Returns the sha256 hexdigest of string_to_hash.

    :param string_to_hash: Input to the sha256 hash function
    :type string_to_hash: str
    :return: Hexdigest of string_to_hash.
    :rtype: str
    """
    
    return hashlib.sha256(string_to_hash.encode("utf-8")).hexdigest()