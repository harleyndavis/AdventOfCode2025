"""
Advent of Code 2025 - Day 3

Problem: [Brief description of the problem]

Usage:
    python Day3/day3.py
    python Day3/day3.py ./Day3/test_input.txt
"""

import sys
from typing import List, Optional


def parse_input(filename: str) -> List[str]:
    """Parse the input file and return processed data.

    Args:
        filename: Path to the input file

    Returns:
        List of processed input lines

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input format is invalid
    """
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{{filename}}' not found")
    except Exception as e:
        raise ValueError(f"Error parsing input: {{e}}")


def solve_part1(data: List[str]) -> int:
    """Solve part 1 of the problem.

    Args:
        data: Parsed input data

    Returns:
        Solution for part 1
    """
    # TODO: Implement part 1 solution
    total_output_joltage = 0

    for line in data:
        # Process each line

        # Find the first maximum value and its position
        digits = [int(char) for char in line if char.isdigit()]
        if digits:
            max_value = max(digits[:-1])
            max_position = line.index(str(max_value))
        else:
            max_value = -1
            max_position = -1

        # Find the largest value after the max_position
        remaining_digits = [
            int(char) for char in line[max_position + 1 :] if char.isdigit()
        ]
        if remaining_digits:
            second_max = max(remaining_digits)
        else:
            second_max = -1

        # Concatenate max_value and second_max to form a two-digit number
        if max_value != -1 and second_max != -1:
            concatenated_value = int(str(max_value) + str(second_max))
            total_output_joltage += concatenated_value

    return total_output_joltage


def find_n_smallest(line: str, n: int) -> List[int]:
    digits = [int(char) for char in line if char.isdigit()]
    return sorted(digits)[:n]


def solve_part2(data: List[str]) -> int:
    """Solve part 2 of the problem.

    Args:
        data: Parsed input data

    Returns:
        Solution for part 2
    """
    result = 0

    for line in data:
        length = len(line)
        final_value: str = ""
        last_index: int = -1
        for i in range(11, -1, -1):
            # Get the first (length - i) characters
            substring = line[last_index + 1 : length - i]
            digits = [int(char) for char in substring if char.isdigit()]

            max_value = max(digits)
            # Find the index of the max_value in the original line
            last_index = substring.index(str(max_value)) + last_index + 1

            final_value += str(max_value)

        result += int(final_value)

    return result


def main() -> None:
    """Main entry point."""
    # Get filename from command line argument, or use default
    filename: str = sys.argv[1] if len(sys.argv) > 1 else "./Day3/input.txt"

    try:
        # Parse input
        data = parse_input(filename)

        # Solve both parts
        part1_result = solve_part1(data)
        part2_result = solve_part2(data)

        # Output results
        print(f"🎯 Day 3 Results:")
        print(f"   Part 1: {part1_result}")
        print(f"   Part 2: {part2_result}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
