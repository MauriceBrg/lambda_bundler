"""This module contains code to install dependencies in a target directory"""
import subprocess
import sys
import typing

def install_dependencies(path_to_requirements: str, path_to_target_directory: str) -> str:
    """
    Installs the dependencies from path_to_requirements.txt into path_to_target_directory.

    :param path_to_requirements: Path to the requirements.txt with the dependencies.
    :type path_to_requirements: str
    :param path_to_target_directory: Path to the target directory to install them in.
    :type path_to_target_directory: str
    :return: Output of the install command.
    :rtype: str
    """

    # Use the pip module to recursively (-r) install all packages from
    # path_to_requirements into (-t) path_to_target_directory while
    # ignoring already installed packages (-I)
    call = [sys.executable, "-m", "pip", "install", "-r", path_to_requirements,
            "-t", path_to_target_directory, "-I"]
    return subprocess.check_output(call)

def merge_requirement_files(*file_contents: typing.List[str]) -> str:
    """
    Merges the content of multiple requirements.txt files into one in a reproducible
    manner and returns it. This means empty lines will be removed and the output is
    the data for a new requirements.txt file based on the input.

    :return: A merged version of the content of the requirement files.
    :rtype: str
    """
    
    output_list = []
    for content in file_contents:
        output_list += [line.strip() for line in content.split("\n") if line.strip() != ""]
    
    return "\n".join(sorted(output_list))