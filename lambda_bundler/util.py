"""Contains several utility functions for the lambda_bundler."""
import functools
import hashlib
import logging
import os
import pathlib
import shutil
import tempfile
import typing
import zipfile

LOGGER = logging.getLogger("lambda_bundler")

DEFAULT_EXCLUDE_LIST = [
    "__pycache__"
]

BUILD_DIR_ENV = "LAMBDA_BUNDLER_BUILD_DIR"

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

def extend_zip(path_to_zip: str, code_directories: typing.List[str],
               exclude_patterns: typing.List[str] = None) -> None:
    """
    This functions extends an existing zip archive with code from the code_directories
    while ignoring the exclude_patterns.

    :param path_to_zip: The path to the zip file to edit.
    :type path_to_zip: str
    :param code_directories: A list of directories that should be included in the zip.
    :type code_directories: typing.List[str]
    :param exclude_patterns: A list of glob patterns to exclude from the zip, defaults to None
    :type exclude_patterns: typing.List[str], optional
    :return: Nothing.
    :rtype: None
    """

    # Build the exclude patterns
    exclude_patterns = exclude_patterns or []
    exclude_patterns = exclude_patterns + DEFAULT_EXCLUDE_LIST
    ignore_during_copy = shutil.ignore_patterns(*exclude_patterns)

    # Create a working directory, copy all source directories there with the exclude list
    with tempfile.TemporaryDirectory() as working_directory, \
        zipfile.ZipFile(path_to_zip, mode="a") as zip_file:

        LOGGER.debug("Copying code to staging directory.")
        for directory in code_directories:

            LOGGER.debug("Copying '%s'", directory)
            # Get the name of the directory -> "path/to/directory" would return "directory"
            source_directory_name = os.path.basename(directory)

            # This is the directory that will ultimately be zipped
            target_directory = os.path.join(working_directory, source_directory_name)

            # Copy the source directory to the working directory
            shutil.copytree(directory, target_directory, ignore=ignore_during_copy)

        LOGGER.debug("Extending '%s' with code from the staging directory", path_to_zip)
        # Now add the contents of the working directory to the EXISTING zip
        # inspired by https://stackoverflow.com/a/11751948/6485881
        # and https://stackoverflow.com/a/18295769/6485881
        empty_dirs = []
        for root, directories, files in os.walk(working_directory):

            # Add regular files
            for name in files:
                zip_file.write(
                    filename=os.path.join(root, name),
                    arcname=os.path.join(root.replace(working_directory, ""), name),
                    compress_type=zipfile.ZIP_DEFLATED
                )

            # Handle empty directories, those are annoying in zips
            empty_dirs = [directory for directory in directories
                          if os.listdir(os.path.join(root, directory)) == []]
            for empty_dir in empty_dirs:
                zip_file.write(
                    filename=os.path.join(root, empty_dir),
                    arcname=os.path.join(root.replace(working_directory, ""), empty_dir),
                    compress_type=zipfile.ZIP_STORED
                )
        LOGGER.debug("Zip extended.")

def get_build_dir() -> str:
    """
    Returns the path to the build directory.

    :return: Path to the build directory.
    :rtype: str
    """
    return os.environ.get(
        BUILD_DIR_ENV,
        os.path.join(tempfile.gettempdir(), "lambda_bundler_builds")
    )

def _create_or_return_empty_zip() -> str:
    path_to_empty_zip = os.path.join(get_build_dir(), "empty.zip")
    if not os.path.exists(path_to_empty_zip):
        # Create an empty file
        LOGGER.debug("Creating empty.zip")
        pathlib.Path(path_to_empty_zip).touch()
    return path_to_empty_zip

def return_empty_if_skip_install(function: typing.Callable,
                                 environment_variale_name="LAMBDA_BUNDLER_SKIP_INSTALL") -> typing.Callable:
    """
    Decorator that returns an empty zip if the installation should be skipped.

    :param function: Function to decorate.
    :type function: typing.Callable
    :param environment_variale_name: Name of the environment variable to evaluate, defaults to "LAMBDA_BUNDLER_SKIP_INSTALL"
    :type environment_variale_name: str, optional
    :return: The decorated function.
    :rtype: typing.Callable
    """

    @functools.wraps(function)
    def wrapped(*args, **kwargs):

        skip_install_value = os.environ.get(environment_variale_name, "false")

        if skip_install_value.lower() in ["true", "t", "1", "y", "yes"]:
            LOGGER.info("Skipping installation of dependencies.")
            return _create_or_return_empty_zip()

        # No skip
        return function(*args, **kwargs)

    return wrapped
