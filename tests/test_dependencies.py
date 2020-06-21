"""Test cases for lambu.dependencies"""

import unittest

import lambu.dependencies as target_module

class DependenciesTestCases(unittest.TestCase):

    def test_merge_requirements(self):
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
