"""This module contains code to install dependencies in a target directory"""
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import typing

import lambda_bundler.util as util

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

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


def collect_and_merge_requirements(*requirement_files: typing.List[str]) -> str:
    """
    Reads the content of all requirement files in requirement_files and merges it
    into a single list of requirements in the form of a string that is returned.

    :return: Merged requirements in the form of a multiline string.
    :rtype: str
    """

    file_contents = util.get_content_of_files(*requirement_files)

    return merge_requirement_files(*file_contents)

def create_zipped_dependencies(requirements_information: str,
                               output_directory_path: str,
                               prefix_in_zip: str = None) -> str:
    """
    This function creates a zip archive that holds the python dependencies
    passed to this function via the requirements_information argument. The
    output will be stored in output_directory_path with a unique name and
    returned. If prefix_in_zip is set, requirements will be installed in a
    subdirectory of the zip (useful for Lambda layers which require a
    python prefix).


    :param requirements_information: The content of the requirements.txt
    :type requirements_information: str
    :param output_directory_path: The directory to build the requirements and store the result in.
    :type output_directory_path: str
    :param prefix_in_zip: Optional prefix in the zip file, defaults to None
    :type prefix_in_zip: str, optional
    :return: Path to the finished zip archive.
    :rtype: str
    """

    directory_name = util.hash_string(requirements_information)

    build_directory = os.path.join(output_directory_path, directory_name)

    # Check if directory exists
    if os.path.exists(build_directory):
        LOGGER.warning("Build-directory '%s' already exists, probably from a failed" \
                       "build - deleting it!", build_directory)
        shutil.rmtree(build_directory)

    # If the prefix is set, we create the install directory with it
    install_directory = build_directory
    if prefix_in_zip is not None:
        install_directory = os.path.join(install_directory, prefix_in_zip)

    # Now we have a clean space and can create our build directory
    pathlib.Path(install_directory).mkdir(parents=True, exist_ok=True)

    # Create the requirements.txt in the install_directory
    requirements_path = os.path.join(install_directory, "requirements.txt")
    with open(requirements_path, "w") as handle:
        handle.write(requirements_information)

    # Install the dependencies to the target directory
    install_dependencies(
        path_to_requirements=requirements_path,
        path_to_target_directory=install_directory
    )

    output_file_name = build_directory if build_directory[-1] != "/" else build_directory[:-1]
    # Zip the temporary directory
    shutil.make_archive(output_file_name, "zip", build_directory)

    # Delete the build directory
    shutil.rmtree(build_directory)

    return f"{output_file_name}.zip"
