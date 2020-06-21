"""
Tests for the lambda_bundler.bundler module.
"""
import os
import tempfile
import unittest
import unittest.mock

import lambda_bundler.bundler as target_module

class TestBundler(unittest.TestCase):
    """
    Test Cases for the python dependencies.
    """

    def test_build_lambda_deployment_package(self):
        """
        Asserts that the build process works with includes and excludes.
        """

        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "lambda_bundler"
        )

        with tempfile.TemporaryDirectory() as output_directory:

            artifact_path = target_module.build_lambda_deployment_package(
                code_directories=[path],
                output_path=output_directory+"/package.zip"
            )

            self.assertTrue(artifact_path.endswith(".zip"))

    def test_build_python_requirements_asset(self):
        """
        NOTE: This is technically an integration test!
        Assert the build_python_requirements_asset function is able to build a .zip for
        a simple requirements.txt
        """

        requirements_file_content = "pytz==2020.1"

        with tempfile.TemporaryDirectory() as input_directory,\
            tempfile.TemporaryDirectory() as output_directory:

            # Set up the requirements.txt
            with open(input_directory + "requirements.txt", "w") as handle:
                handle.write(requirements_file_content)

            # Build the Asset
            asset = target_module.build_python_requirements_asset(
                requirements_file_path=input_directory + "requirements.txt",
                output_directory_path=output_directory
            )

            self.assertIn(".zip", asset, msg="Should return the path of a .zip")


if __name__ == "__main__":
    unittest.main()
