"""
Tests for the lambda_bundler.bundler module.
"""
import unittest
from unittest.mock import patch, ANY

import lambda_bundler.bundler as target_module

class TestBundler(unittest.TestCase):
    """
    Test Cases for the python dependencies.
    """

    def setUp(self):
        self.module = "lambda_bundler.bundler."

    def test_build_layer_package(self):
        """Asserts build_layer_package orchestrates the functions as expected."""

        with patch(self.module + "dependencies.collect_and_merge_requirements") as collect_mock, \
            patch(self.module + "dependencies.create_or_return_zipped_dependencies") as zip_mock:

            zip_mock.return_value = "some/path.zip"

            result = target_module.build_layer_package(
                ["abc"]
            )

            collect_mock.assert_called_with("abc")

            zip_mock.assert_called_with(
                requirements_information=ANY,
                output_directory_path=ANY,
                prefix_in_zip="python"
            )

            self.assertEqual("some/path.zip", result)

if __name__ == "__main__":
    unittest.main()
