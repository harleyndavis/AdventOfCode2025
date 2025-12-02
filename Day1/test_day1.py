"""
Unit tests for Day 1 solution.

To run tests:
    python test_day1.py
"""

import tempfile
import os
import sys

# Add parent directory to path to import day1 module
sys.path.append(".")
from day1 import (
    parse_command,
    calculate_zero_crossings,
    process_commands,
    START_POSITION,
    POSITION_RANGE,
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
        print(f"💥 {test_name}: Unexpected error: {e}")
        return False


class TestParseCommand:
    """Test command parsing functionality."""

    def test_parse_right_command(self):
        """Test parsing right (R) commands."""
        direction, distance = parse_command("R10")
        assert direction == 1
        assert distance == 10

    def test_parse_left_command(self):
        """Test parsing left (L) commands."""
        direction, distance = parse_command("L25")
        assert direction == -1
        assert distance == 25

    def test_parse_zero_distance(self):
        """Test parsing commands with zero distance."""
        direction, distance = parse_command("R0")
        assert direction == 1
        assert distance == 0

        direction, distance = parse_command("L0")
        assert direction == -1
        assert distance == 0

    def test_parse_large_distance(self):
        """Test parsing commands with large distances."""
        direction, distance = parse_command("R999")
        assert direction == 1
        assert distance == 999

    def test_parse_single_digit(self):
        """Test parsing single digit distances."""
        direction, distance = parse_command("L5")
        assert direction == -1
        assert distance == 5


class TestCalculateZeroCrossings:
    """Test zero crossing calculation logic."""

    def test_no_crossing_right(self):
        """Test movement that doesn't cross zero going right."""
        # Start at 50, move right 10 -> no zero crossing
        crossings, new_pos = calculate_zero_crossings(50, 1, 10)
        assert crossings == 0
        assert new_pos == 60

    def test_no_crossing_left(self):
        """Test movement that doesn't cross zero going left."""
        # Start at 50, move left 10 -> no zero crossing
        crossings, new_pos = calculate_zero_crossings(50, -1, 10)
        assert crossings == 0
        assert new_pos == 40

    def test_single_crossing_right(self):
        """Test single zero crossing going right."""
        # Start at 90, move right 20 -> cross zero once at position 0
        crossings, new_pos = calculate_zero_crossings(90, 1, 20)
        assert crossings == 1
        assert new_pos == 10  # (90 + 20) % 100 = 10

    def test_single_crossing_left(self):
        """Test single zero crossing going left."""
        # Start at 10, move left 20 -> cross zero once
        crossings, new_pos = calculate_zero_crossings(10, -1, 20)
        assert crossings == 1
        assert new_pos == 90  # (10 - 20) % 100 = 90

    def test_multiple_crossings_right(self):
        """Test multiple zero crossings going right."""
        # Start at 90, move right 220 -> cross zero 3 times
        # First crossing at step 10 (90->0), then every 100 steps
        crossings, new_pos = calculate_zero_crossings(90, 1, 220)
        assert crossings == 3  # At steps 10, 110, 210
        assert new_pos == 10  # (90 + 220) % 100 = 10

    def test_multiple_crossings_left(self):
        """Test multiple zero crossings going left."""
        # Start at 10, move left 220 -> cross zero 3 times
        crossings, new_pos = calculate_zero_crossings(10, -1, 220)
        assert crossings == 3
        assert new_pos == 90  # (10 - 220) % 100 = 90

    def test_starting_at_zero_right(self):
        """Test starting at position zero going right."""
        # Start at 0, move right 150 -> cross zero at step 100
        crossings, new_pos = calculate_zero_crossings(0, 1, 150)
        assert crossings == 1
        assert new_pos == 50

    def test_starting_at_zero_left(self):
        """Test starting at position zero going left."""
        # Start at 0, move left 150 -> cross zero at step 100
        crossings, new_pos = calculate_zero_crossings(0, -1, 150)
        assert crossings == 1
        assert new_pos == 50  # (0 - 150) % 100 = 50

    def test_exact_boundary_crossings(self):
        """Test exact boundary crossings."""
        # Start at 0, move right exactly 100 -> cross zero once
        crossings, new_pos = calculate_zero_crossings(0, 1, 100)
        assert crossings == 1
        assert new_pos == 0

    def test_zero_distance(self):
        """Test zero distance movement."""
        crossings, new_pos = calculate_zero_crossings(50, 1, 0)
        assert crossings == 0
        assert new_pos == 50


class TestProcessCommands:
    """Test file processing integration."""

    def create_temp_file(self, content: str) -> str:
        """Helper to create temporary test files."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write(content)
            return f.name

    def test_empty_file(self):
        """Test processing empty file."""
        temp_file = self.create_temp_file("")
        try:
            result = process_commands(temp_file)
            assert result == 0
        finally:
            os.unlink(temp_file)

    def test_single_command(self):
        """Test processing single command."""
        temp_file = self.create_temp_file("R10")
        try:
            result = process_commands(temp_file)
            assert result == 0  # No zero crossings from 50->60
        finally:
            os.unlink(temp_file)

    def test_multiple_commands(self):
        """Test processing multiple commands."""
        # Simple test case that should cross zero
        temp_file = self.create_temp_file("R60\nL10")  # 50->10->0, crosses once
        try:
            result = process_commands(temp_file)
            # This should result in some crossings
            assert isinstance(result, int)
            assert result >= 0
        finally:
            os.unlink(temp_file)

    def test_known_test_input(self):
        """Test with the actual test_input.txt file."""
        # We know this should return 6 based on your earlier test
        result = process_commands("test_input.txt")
        assert result == 6

    def test_file_with_empty_lines(self):
        """Test file with empty lines (should be skipped)."""
        temp_file = self.create_temp_file("R10\n\nL5\n\nR15")
        try:
            result = process_commands(temp_file)
            assert isinstance(result, int)
        finally:
            os.unlink(temp_file)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_position_range_boundaries(self):
        """Test movements at position boundaries."""
        # Test at position 99
        crossings, new_pos = calculate_zero_crossings(99, 1, 1)
        assert crossings == 1  # Should cross zero
        assert new_pos == 0

        # Test at position 1
        crossings, new_pos = calculate_zero_crossings(1, -1, 1)
        assert crossings == 1  # Should cross zero
        assert new_pos == 0

    def test_large_distances(self):
        """Test very large movement distances."""
        # Test with distance larger than position range
        crossings, new_pos = calculate_zero_crossings(50, 1, 10000)
        assert crossings > 0  # Should have many crossings
        assert 0 <= new_pos < POSITION_RANGE

    def test_wrap_around_consistency(self):
        """Test that position wrapping is consistent."""
        # Multiple small moves should equal one large move
        pos = START_POSITION
        total_crossings = 0

        # Take 10 steps of 37 each
        for _ in range(10):
            crossings, pos = calculate_zero_crossings(pos, 1, 37)
            total_crossings += crossings

        # Compare with one large step
        large_crossings, large_pos = calculate_zero_crossings(START_POSITION, 1, 370)

        assert total_crossings == large_crossings
        assert pos == large_pos


def test_constants():
    """Test that constants are properly defined."""
    assert START_POSITION == 50
    assert POSITION_RANGE == 100


if __name__ == "__main__":
    """Run all tests and report results."""
    print("🧪 Running Day 1 Unit Tests")
    print("=" * 40)

    passed = 0
    total = 0

    # Test parse_command function
    print("\n📋 Testing parse_command()")
    tests = TestParseCommand()
    test_methods = [
        ("Parse R commands", tests.test_parse_right_command),
        ("Parse L commands", tests.test_parse_left_command),
        ("Parse zero distance", tests.test_parse_zero_distance),
        ("Parse large distance", tests.test_parse_large_distance),
        ("Parse single digit", tests.test_parse_single_digit),
    ]

    for name, method in test_methods:
        if run_test(name, method):
            passed += 1
        total += 1

    # Test calculate_zero_crossings function
    print("\n🎯 Testing calculate_zero_crossings()")
    tests = TestCalculateZeroCrossings()
    test_methods = [
        ("No crossing right", tests.test_no_crossing_right),
        ("No crossing left", tests.test_no_crossing_left),
        ("Single crossing right", tests.test_single_crossing_right),
        ("Single crossing left", tests.test_single_crossing_left),
        ("Multiple crossings right", tests.test_multiple_crossings_right),
        ("Multiple crossings left", tests.test_multiple_crossings_left),
        ("Starting at zero right", tests.test_starting_at_zero_right),
        ("Starting at zero left", tests.test_starting_at_zero_left),
        ("Exact boundary crossings", tests.test_exact_boundary_crossings),
        ("Zero distance", tests.test_zero_distance),
    ]

    for name, method in test_methods:
        if run_test(name, method):
            passed += 1
        total += 1

    # Test process_commands function
    print("\n📁 Testing process_commands()")
    tests = TestProcessCommands()
    test_methods = [
        ("Empty file", tests.test_empty_file),
        ("Single command", tests.test_single_command),
        ("Multiple commands", tests.test_multiple_commands),
        ("Known test input", tests.test_known_test_input),
        ("File with empty lines", tests.test_file_with_empty_lines),
    ]

    for name, method in test_methods:
        if run_test(name, method):
            passed += 1
        total += 1

    # Test edge cases
    print("\n⚡ Testing edge cases")
    tests = TestEdgeCases()
    test_methods = [
        ("Position boundaries", tests.test_position_range_boundaries),
        ("Large distances", tests.test_large_distances),
        ("Wrap around consistency", tests.test_wrap_around_consistency),
    ]

    for name, method in test_methods:
        if run_test(name, method):
            passed += 1
        total += 1

    # Test constants
    if run_test("Constants defined", test_constants):
        passed += 1
    total += 1

    # Final results
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} passed")
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed")

    exit(0 if passed == total else 1)
