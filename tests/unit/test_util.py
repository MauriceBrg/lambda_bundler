"""Tests for the lambda_bundler.util module."""
import tempfile
import unittest

import lambda_bundler.util as target_module

class UtilTestCases(unittest.TestCase):
    """Test cases for the util module"""

    def test_hash_string(self):
        """Asserts hash_string returns the correct sha256 hexdigest"""

        test_string = "test"
        expected_hash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

        self.assertEqual(expected_hash, target_module.hash_string(test_string))

    def test_get_content_of_files(self):
        """Asserts get_content_of_files reads the correct files"""

        content_1 = "a"
        content_2 = "b"

        with tempfile.TemporaryDirectory() as input_directory:

            # Set up test files
            with open(input_directory + "file1", "w") as handle:
                handle.write(content_1)

            with open(input_directory + "file2", "w") as handle:
                handle.write(content_2)

            expected_result = [content_1, content_2]

            actual_result = target_module.get_content_of_files(
                input_directory + "file1",
                input_directory + "file2"
            )

        self.assertEqual(expected_result, actual_result)

if __name__ == "__main__":
    unittest.main()
