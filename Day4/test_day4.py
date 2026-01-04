"""
Unit tests for Day 4 solution.

To run tests:
    python test_day4.py
"""

import tempfile
import os
import sys

# Add current directory to path to import day4 module
sys.path.append(".")
from day4 import (
    parse_input,
    solve_part1,
    solve_part2,
    removable_at_symbols,
)


def run_test(test_name, test_func):
    """Helper to run individual tests and report results."""
    try:
        test_func()
        print(f"✅ {test_name}")
        return True
    except AssertionError as e:
        print(f"❌ {test_name}: {e}")
        return False
    except Exception as e:
        print(f"❌ {test_name}: Unexpected error - {e}")
        return False


def test_parse_input():
    """Test parsing input file."""
    # Create a temporary test file
    test_data = "..@@.@@@@.\n@@@.@.@.@@\n@@@@@.@.@@\n"

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write(test_data)
        temp_filename = f.name

    try:
        result = parse_input(temp_filename)
        expected = ["..@@.@@@@.", "@@@.@.@.@@", "@@@@@.@.@@"]
        assert result == expected, f"Expected {expected}, got {result}"
    finally:
        os.unlink(temp_filename)


def test_parse_input_file_not_found():
    """Test parsing non-existent file raises FileNotFoundError."""
    try:
        parse_input("nonexistent_file.txt")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        pass  # Expected behavior


def test_surrounding_at_symbols_lt_four():
    """Test the surrounding_at_symbols_lt_four function."""
    # Test grid with known '@' positions
    test_grid = [
        [".", ".", "@", "@", "."],
        ["@", "@", "@", ".", "@"],
        ["@", "@", "@", "@", "@"],
        ["@", ".", "@", "@", "@"],
        ["@", "@", ".", "@", "@"],
    ]

    # Test position (1, 1) - should have many '@' symbols around it
    result = removable_at_symbols(test_grid, 1, 1, 5, 5)
    # Count '@' symbols around position (1, 1)
    # Positions to check: (0,0)=., (0,1)=., (0,2)=@, (1,0)=@, (1,2)=@, (2,0)=@, (2,1)=@, (2,2)=@
    # That's 6 '@' symbols, so result should be 0 (not less than 4)
    assert result == 0, f"Expected 0 for position with many '@' symbols, got {result}"

    # Test position (0, 0) - corner position with fewer '@' symbols
    result = removable_at_symbols(test_grid, 0, 0, 5, 5)
    # Positions to check: (0,1)=., (1,0)=@, (1,1)=@
    # That's 2 '@' symbols, so result should be 1 (less than 4)
    assert result == 1, f"Expected 1 for position with few '@' symbols, got {result}"

    # Test position (0, 1) - edge position
    result = removable_at_symbols(test_grid, 0, 1, 5, 5)
    # Positions to check: (0,0)=., (0,2)=@, (1,0)=@, (1,1)=@, (1,2)=@
    # That's 4 '@' symbols, so result should be 0 (not less than 4)
    assert (
        result == 0
    ), f"Expected 0 for position with exactly 4 '@' symbols, got {result}"


def test_surrounding_at_symbols_edge_cases():
    """Test edge cases for surrounding_at_symbols_lt_four function."""
    # Single character grid
    single_grid = [["@"]]
    result = removable_at_symbols(single_grid, 0, 0, 1, 1)
    assert result == 1, f"Expected 1 for single character grid, got {result}"

    # Empty positions around
    sparse_grid = [[".", ".", "."], [".", "@", "."], [".", ".", "."]]
    result = removable_at_symbols(sparse_grid, 1, 1, 3, 3)
    assert (
        result == 1
    ), f"Expected 1 for position with no '@' symbols around, got {result}"


def test_solve_part1_with_test_input():
    """Test solve_part1 with the actual test input file."""
    if os.path.exists("test_input.txt"):
        data = parse_input("test_input.txt")
        result = solve_part1(data)
        assert result == 13, f"Expected 13 for test input, got {result}"
    else:
        print("⚠️  test_input.txt not found, skipping test")


def test_solve_part1_simple_case():
    """Test solve_part1 with a simple known case."""
    # Create a simple test case
    test_data = [[".", ".", "."], [".", "@", "."], [".", ".", "."]]

    result = solve_part1(test_data)
    # All 9 positions should have less than 4 '@' symbols around them
    # Position (1,1) has 0 '@' symbols around it
    # All edge and corner positions also have less than 4 '@' symbols
    expected = 9  # All positions should count
    assert result == expected, f"Expected {expected} for simple case, got {result}"


def test_solve_part1_dense_case():
    """Test solve_part1 with a dense '@' case."""
    test_data = [["@", "@", "@"], ["@", "@", "@"], ["@", "@", "@"]]

    result = solve_part1(test_data)
    # Corner positions (0,0), (0,2), (2,0), (2,2) should have 3 '@' symbols each (< 4)
    # Edge positions (0,1), (1,0), (1,2), (2,1) should have 5 '@' symbols each (>= 4)
    # Center position (1,1) should have 8 '@' symbols (>= 4)
    # So only the 4 corner positions should count
    expected = 4
    assert result == expected, f"Expected {expected} for dense case, got {result}"


def test_solve_part2_placeholder():
    """Test solve_part2 (currently returns 0)."""
    test_data = [[".", ".", "."], [".", "@", "."], [".", ".", "."]]
    result = solve_part2(test_data)
    assert result == 0, f"Expected 0 for part 2 placeholder, got {result}"


def main():
    """Run all tests."""
    print("🧪 Running Day 4 Tests...")
    print("=" * 50)

    tests = [
        ("Parse Input", test_parse_input),
        ("Parse Input - File Not Found", test_parse_input_file_not_found),
        ("Surrounding @ Symbols - Basic Cases", test_surrounding_at_symbols_lt_four),
        ("Surrounding @ Symbols - Edge Cases", test_surrounding_at_symbols_edge_cases),
        ("Solve Part 1 - Test Input (Expected: 13)", test_solve_part1_with_test_input),
        ("Solve Part 1 - Simple Case", test_solve_part1_simple_case),
        ("Solve Part 1 - Dense Case", test_solve_part1_dense_case),
        ("Solve Part 2 - Placeholder", test_solve_part2_placeholder),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1

    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"❌ {total - passed} tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
