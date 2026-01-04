"""
Test suite for Day 5 solution.

Usage:
    python test_day5.py
"""

import unittest
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the solution
sys.path.append(str(Path(__file__).parent))
from day5 import parse_input, solve_part1, solve_part2, preprocess_input


class TestDay5(unittest.TestCase):
    """Test cases for Day 5 solution."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_data = [
            "3-5",
            "10-14",
            "16-20",
            "12-18",
            "",
            "1",
            "5",
            "8",
            "11",
            "17",
            "32",
        ]

    def test_parse_input(self):
        """Test input parsing."""
        try:
            data = parse_input("test_input.txt")
            # Should have parsed the file successfully
            self.assertIsInstance(data, list)
            self.assertGreater(len(data), 0)
        except FileNotFoundError:
            self.skipTest("Test input file not found")

    def test_solve_part1_example(self):
        """Test part 1 with example data."""
        expected = 3  # Based on the provided expected result
        ranges, ids_to_check = preprocess_input(self.test_data)
        result = solve_part1(ranges, ids_to_check)
        self.assertEqual(result, expected)

    def test_solve_part2_example(self):
        """Test part 2 with example data."""
        # TODO: Update with expected result when part 2 is known
        ranges, ids_to_check = preprocess_input(self.test_data)
        result = solve_part2(ranges, ids_to_check)
        self.assertIsInstance(result, int)

    def test_solve_part1_file(self):
        """Test part 1 with test input file."""
        try:
            data = parse_input("test_input.txt")
            ranges, ids_to_check = preprocess_input(data)
            result = solve_part1(ranges, ids_to_check)
            # Expected result is 3 based on the problem description
            self.assertEqual(result, 3)
        except FileNotFoundError:
            self.skipTest("Test input file not found")

    def test_solve_part2_file(self):
        """Test part 2 with test input file."""
        try:
            data = parse_input("test_input.txt")
            ranges, ids_to_check = preprocess_input(data)
            result = solve_part2(ranges, ids_to_check)
            # TODO: Add assertion for expected result when part 2 is implemented
            self.assertIsInstance(result, int)
        except FileNotFoundError:
            self.skipTest("Test input file not found")

    def test_preprocess_input_example(self):
        """Test preprocess_input with example data."""
        ranges, ids_to_check = preprocess_input(self.test_data)

        # Expected merged ranges: (3,5), (10,20) - the 10-14, 16-20, and 12-18 should merge
        expected_ranges = [(3, 5), (10, 20)]
        expected_ids = [1, 5, 8, 11, 17, 32]

        self.assertEqual(ranges, expected_ranges)
        self.assertEqual(ids_to_check, expected_ids)

    def test_preprocess_input_file(self):
        """Test preprocess_input with test input file."""
        try:
            data = parse_input("test_input.txt")
            ranges, ids_to_check = preprocess_input(
                data
            )  # Should return tuples for ranges and list for IDs
            self.assertIsInstance(ranges, list)
            self.assertIsInstance(ids_to_check, list)

            # All ranges should be tuples of (start, end)
            for range_tuple in ranges:
                self.assertIsInstance(range_tuple, tuple)
                self.assertEqual(len(range_tuple), 2)
                self.assertLessEqual(range_tuple[0], range_tuple[1])  # start <= end

            # All IDs should be integers
            for id_val in ids_to_check:
                self.assertIsInstance(id_val, int)

        except FileNotFoundError:
            self.skipTest("Test input file not found")


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
