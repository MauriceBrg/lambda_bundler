"""
Contains functions to bundle python dependencies.
"""

import hashlib
import os
import shutil
import tempfile
import typing

import lambda_bundler.dependencies as dependencies

__DEFAULT_EXCLUDE_LIST = [
    "__pycache__"
]


def build_lambda_deployment_package(code_directories: typing.List[str], output_path: str,
                                    exclude_patterns: typing.List[str] = None,
                                    include_directories: typing.List[str] = None) -> str:
    """
    TODO Document this
    """

    # Create a list of patterns to ignore during the initial copy
    exclude_patterns = exclude_patterns or []
    exclude_patterns = exclude_patterns + __DEFAULT_EXCLUDE_LIST
    ignore_during_copy = shutil.ignore_patterns(*exclude_patterns)

    include_directories = include_directories or []

    # TODO: Implement whitelist functionality!

    with tempfile.TemporaryDirectory() as working_directory:

        for directory in code_directories:

            # Get the name of the directory -> "path/to/directory" would return "directory"
            source_directory_name = os.path.basename(directory)

            # This is the directory that will ultimately be zipped
            target_directory = working_directory + "/" + source_directory_name

            # Copy the source directory to the working directory
            shutil.copytree(directory, target_directory, ignore=ignore_during_copy)

        # Remove all directories that are not on the include list

        # Zip the directory after removing a potential .zip suffix
        output_path_without_suffix = output_path[:-4] if output_path.endswith(".zip") else output_path
        shutil.make_archive(output_path_without_suffix, "zip", working_directory)

        return output_path_without_suffix + ".zip"


def build_python_requirements_asset(requirements_file_path: str, output_directory_path: str) -> str:
    """
    Creates a zipped version of the requirements from a Python requirements.txt file that's suitable for use
    in a Lambda layer.

    :param requirements_file_path: Path to the requirements file that is the basis of this asset.
    :param output_directory_path: Path to the directory where the output will be stored.
    :return: The Path to the zip archive.
    """

    requirements_path_hash = hashlib.sha256(requirements_file_path.encode("utf-8")).hexdigest()

    with tempfile.TemporaryDirectory() as working_directory:

        # TODO This isn't very efficient, a more permanent solution should have a static cache directory for downloads

        requirements_file_in_temp_directory = f"{working_directory}/requirements.txt"

        # Copy the requirements file to the temporary directory
        shutil.copyfile(requirements_file_path, requirements_file_in_temp_directory)

        # Create the python subdirectory
        install_target = f"{working_directory}/python"
        os.makedirs(install_target, exist_ok=True)

        # Install the dependencies
        dependencies.install_dependencies(
            path_to_requirements=requirements_file_in_temp_directory,
            path_to_target_directory=install_target
        )

        output_path = f"{output_directory_path}/python_requirements_{requirements_path_hash}"

        # Zip the temporary directory
        shutil.make_archive(output_path, "zip", working_directory)

        return f"{output_path}.zip"