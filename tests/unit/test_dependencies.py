"""Test cases for lambda_bundler.dependencies"""
import os
import pathlib
import shutil
import tempfile
import unittest

from unittest.mock import patch

import lambda_bundler.dependencies as target_module

class DependenciesTestCases(unittest.TestCase):
    """Tests for the lambda_bundler.dependencies module"""

    def setUp(self):
        self.module = "lambda_bundler.dependencies."

    def test_merge_requirement_files(self):
        """Assert that merge_requirement_files handles whitespaces and ordering."""
        file_1 = """
        abc
        ghj
        """

        file_2 = """
        def

        """

        expected_output = "\n".join(["abc", "def", "ghj"])

        actual_output = target_module.merge_requirement_files(file_1, file_2)

        self.assertEqual(expected_output, actual_output)

    def test_collect_and_merge_requirements(self):
        """Assert collect_and_merge_requirements calls the correct functions"""

        with patch(self.module + "util.get_content_of_files") as get_mock, \
            patch(self.module + "merge_requirement_files") as merge_mock:

            get_mock.return_value = ["a"]
            merge_mock.return_value = "merged"

            list_of_files = ["file1", "file2"]
            self.assertEqual("merged", target_module.collect_and_merge_requirements(*list_of_files))

            get_mock.assert_called_with(*list_of_files)
            merge_mock.assert_called_with("a")

    def test_create_zipped_dependencies(self):
        """Asserts that create_zipped_dependencies works as expected"""

        with tempfile.TemporaryDirectory() as working_directory, \
            tempfile.TemporaryDirectory() as assertion_directory, \
            patch(self.module + "util.hash_string") as hash_mock, \
            patch(self.module + "install_dependencies") as install_mock:

            hash_mock.return_value = "bla"
            requirements = "pytz"

            output_path = target_module.create_zipped_dependencies(
                requirements_information=requirements,
                output_directory_path=working_directory
            )

            hash_mock.assert_called_with(requirements)
            install_mock.assert_called_with(
                path_to_requirements=os.path.join(working_directory, "bla", "requirements.txt"),
                path_to_target_directory=os.path.join(working_directory, "bla")
            )

            self.assertTrue(output_path.endswith("bla.zip"))

            # If we extract it, there should be a requirements txt at the root
            shutil.unpack_archive(output_path, assertion_directory)
            self.assertTrue(
                os.path.exists(
                    os.path.join(assertion_directory, "requirements.txt")
                )
            )

    def test_create_zipped_dependencies_with_prefix(self):
        """Asserts that create_zipped_dependencies works as expected and honors the prefix"""

        with tempfile.TemporaryDirectory() as working_directory, \
            tempfile.TemporaryDirectory() as assertion_directory, \
            patch(self.module + "util.hash_string") as hash_mock, \
            patch(self.module + "install_dependencies") as install_mock:

            hash_mock.return_value = "bla"
            requirements = "pytz"

            output_path = target_module.create_zipped_dependencies(
                requirements_information=requirements,
                output_directory_path=working_directory,
                prefix_in_zip="python"
            )

            hash_mock.assert_called_with(requirements + "python")
            install_mock.assert_called_with(
                path_to_requirements=os.path.join(working_directory, "bla", "python", "requirements.txt"),
                path_to_target_directory=os.path.join(working_directory, "bla", "python")
            )

            self.assertTrue(output_path.endswith("bla.zip"))

            # If we extract it, there should be a requirements txt at the root
            shutil.unpack_archive(output_path, assertion_directory)
            self.assertTrue(
                os.path.exists(
                    os.path.join(assertion_directory, "python", "requirements.txt")
                )
            )

    def test_create_zipped_dependencies_with_pre_existing_build_dir(self):
        """Asserts that create_zipped_dependencies works as expected"""

        with tempfile.TemporaryDirectory() as working_directory, \
            tempfile.TemporaryDirectory() as assertion_directory, \
            patch(self.module + "util.hash_string") as hash_mock, \
            patch(self.module + "install_dependencies") as install_mock, \
            patch(self.module + "LOGGER.warning") as warning_logger:

            # Create the build dir beforehand, the code should still work and log a warning
            pathlib.Path(os.path.join(working_directory, "bla")).mkdir()

            hash_mock.return_value = "bla"
            requirements = "pytz"

            output_path = target_module.create_zipped_dependencies(
                requirements_information=requirements,
                output_directory_path=working_directory
            )

            hash_mock.assert_called_with(requirements)
            install_mock.assert_called_with(
                path_to_requirements=os.path.join(working_directory, "bla", "requirements.txt"),
                path_to_target_directory=os.path.join(working_directory, "bla")
            )
            warning_logger.assert_called_once()

            self.assertTrue(output_path.endswith("bla.zip"))

            # If we extract it, there should be a requirements txt at the root
            shutil.unpack_archive(output_path, assertion_directory)
            self.assertTrue(
                os.path.exists(
                    os.path.join(assertion_directory, "requirements.txt")
                )
            )

    def test_create_or_return_zipped_dependencies(self):
        """Assert that create_or_return_zipped_dependencies works as intended"""

        with patch(self.module + "util.hash_string") as hash_mock, \
            patch(self.module + "os.path.exists") as exists_mock, \
            patch(self.module + "create_zipped_dependencies") as zip_mock:

            hash_mock.return_value = "a"
            exists_mock.return_value = True
            zip_mock.return_value = "zipped"

            # Already existing

            result = target_module.create_or_return_zipped_dependencies(
                requirements_information="bla",
                output_directory_path="/some_path/"
            )

            self.assertEqual("/some_path/a.zip", result)

            # Create new
            exists_mock.return_value = False

            result = target_module.create_or_return_zipped_dependencies(
                requirements_information="bla",
                output_directory_path="/some_path/"
            )

            self.assertEqual("zipped", result)

if __name__ == "__main__":
    unittest.main()
