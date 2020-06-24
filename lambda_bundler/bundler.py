"""
Contains functions to bundle python dependencies.
"""

import typing

import lambda_bundler.dependencies as dependencies
import lambda_bundler.util as util

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
        output_directory_path=util.get_build_dir(),
        prefix_in_zip="python"
    )

def build_lambda_package(code_directories: typing.List[str],
                         requirement_files: typing.List[str] = None,
                         exclude_patterns: typing.List[str] = None) -> str:
    """
    This function builds a lambda deployment package out of one or
    more code directories and optionally bundles dependencies in
    the package.

    :param code_directories: List of paths to the code directories.
    :type code_directories: typing.List[str]
    :param requirement_files: List of paths to requirement files, defaults to None
    :type requirement_files: typing.List[str], optional
    :param exclude_patterns: Glob patterns of files to exclude from the code_directories, defaults to None
    :type exclude_patterns: typing.List[str], optional
    :return: Path to the .zip archive.
    :rtype: str
    """
    if requirement_files is None:

        return dependencies.build_lambda_package_without_dependencies(
            code_directories=code_directories,
            exclude_patterns=exclude_patterns
        )

    return dependencies.build_lambda_package_with_dependencies(
        code_directories=code_directories,
        requirement_files=requirement_files,
        exclude_patterns=exclude_patterns
    )
