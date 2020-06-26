"""
Integration tests for the lambda bundler

NOTE: These download packages and thus require internet access!
"""
import os
import shutil
import tempfile
import unittest

from lambda_bundler import build_lambda_package, build_layer_package

BUILD_DIR_ENV = "LAMBDA_BUNDLER_BUILD_DIR"

class LayerTestCases(unittest.TestCase):
    """Test cases for build_layer_package"""

    def test_simple_requirement_file(self):
        """A Test case for a single requirement file"""

        with tempfile.TemporaryDirectory() as assertion_directory, \
            tempfile.TemporaryDirectory() as build_directory, \
            tempfile.TemporaryDirectory() as source_directory:

            os.environ[BUILD_DIR_ENV] = build_directory

            path_to_requirement = os.path.join(source_directory, "requirements.txt")

            with open(path_to_requirement, "w") as handle:

                handle.write("pytz==2020.01")

            path_to_output = build_layer_package(
                requirement_files=[path_to_requirement]
            )

            # Assert a zip archive is returned
            self.assertTrue(path_to_output.endswith(".zip"))

            shutil.unpack_archive(path_to_output, assertion_directory)

            # Assert a pytz directory exists
            self.assertTrue(os.path.exists(
                os.path.join(assertion_directory, "python", "pytz")
            ))

    def test_multiple_requirement_files(self):
        """A Test case for multiple requirement files"""

        with tempfile.TemporaryDirectory() as assertion_directory, \
            tempfile.TemporaryDirectory() as build_directory, \
            tempfile.TemporaryDirectory() as source_directory:

            os.environ[BUILD_DIR_ENV] = build_directory

            path_to_requirement_1 = os.path.join(source_directory, "requirements_1.txt")
            path_to_requirement_2 = os.path.join(source_directory, "requirements_2.txt")

            with open(path_to_requirement_1, "w") as handle_1, \
                open(path_to_requirement_2, "w") as handle_2:

                handle_1.write("pytz==2020.01")
                handle_2.write("certifi==2020.6.20")

            path_to_output = build_layer_package(
                requirement_files=[path_to_requirement_1, path_to_requirement_2]
            )

            # Assert a zip archive is returned
            self.assertTrue(path_to_output.endswith(".zip"))

            shutil.unpack_archive(path_to_output, assertion_directory)

            # Assert a pytz directory exists
            self.assertTrue(os.path.exists(
                os.path.join(assertion_directory, "python", "pytz")
            ))
            self.assertTrue(os.path.exists(
                os.path.join(assertion_directory, "python", "certifi")
            ))
