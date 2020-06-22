"""
Contains functions to bundle python dependencies.
"""

import os
import shutil
import tempfile
import typing

import lambda_bundler.dependencies as dependencies
import lambda_bundler.util as util

def _get_build_dir() -> str:
    return os.environ.get(
        "LAMBDA_BUNDLER_BUILD_DIR",
        os.path.join(tempfile.gettempdir(), "lambda_bundler_builds")
    )

def build_layer_package(requirement_files: typing.List[str]) -> str:
    """
    Builds the zip archive for a lambda layer from a list of requirement files.

    :param requirement_files: List of paths to requirement files.
    :type requirement_files: typing.List[str]
    :return: Path to the packaged zip.
    :rtype: str
    """

    collected_dependencies = dependencies.collect_and_merge_requirements(
        *requirement_files
    )

    return dependencies.create_or_return_zipped_dependencies(
        requirements_information=collected_dependencies,
        output_directory_path=_get_build_dir(),
        prefix_in_zip="python"
    )

def build_lambda_package(code_directories: typing.List[str],
                         requirement_files: typing.List[str] = None,
                         exclude_patterns: typing.List[str] = None) -> str:

    # TODO: Handle case where no requirements are set
    collected_dependencies = dependencies.collect_and_merge_requirements(
        *requirement_files
    )

    requirements_zip = dependencies.create_or_return_zipped_dependencies(
        requirements_information=collected_dependencies,
        output_directory_path=_get_build_dir(),
    )

    target_zip_name = util.hash_string("".join(code_directories)) + ".zip"
    zip_path = os.path.join(_get_build_dir(), target_zip_name)

    shutil.copyfile(
        src=requirements_zip,
        dst=zip_path
    )

    util.extend_zip(
        path_to_zip=zip_path,
        code_directories=code_directories,
        exclude_patterns=exclude_patterns
    )

    return zip_path
