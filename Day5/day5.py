"""
Advent of Code 2025 - Day 5

Problem: [Brief description of the problem]

Usage:
    python Day5/day5.py
    python Day5/day5.py ./Day5/test_input.txt
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
            lines = [
                line.strip()
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
        return lines
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")
    except Exception as e:
        raise ValueError(f"Error parsing input: {e}")


def solve_part1(ranges: List[tuple], ids_to_check: List[int]) -> int:
    """Solve part 1 of the problem.
       Check to see if the IDs to check fall within any of the given ranges.

    Args:
        ranges: List of ID ranges
        ids_to_check: List of IDs to check against the ranges
    Returns:
        Solution for part 1
    """
    result = 0

    for id in ids_to_check:
        for start, end in ranges:
            if start <= id <= end:
                result += 1
                break

    return result


def solve_part2(ranges: List[tuple], ids_to_check: List[int]) -> int:
    """Solve part 2 of the problem.

    Args:
        data: Parsed input data

    Returns:
        Solution for part 2
    """
    # TODO: Implement part 2 solution
    result = 0

    for id in ids_to_check:
        # Process each line
        pass

    return result


def preprocess_input(data):
    """Process input data to seperate the id ranges from the IDs to check.
       Reads through the data generating a series of ranges and a series of IDs to check.
       The ranges in the input are given first, followed by a blank line, then the IDs to check.
       The ranges are in the format "start-end", and the IDs to check are single integers.
       The ranges can contain overlaps. We will want to combine overlapping ranges for efficiency.
    Args:
        data: Parsed input data
    Returns:
        ranges: List of tuples representing the ID ranges
        ids_to_check: List of IDs to check against the ranges
    """
    ranges = []
    ids_to_check = []
    blank_line_found = False

    for line in data:
        if not blank_line_found:
            # Parse range in format "start-end"
            if "-" in line:
                start, end = map(int, line.split("-"))
                ranges.append((start, end))
            else:
                # Found the blank line separator - this line is the first ID
                blank_line_found = True
                ids_to_check.append(int(line))
        else:
            # Parse single ID to check
            ids_to_check.append(int(line))

    # Combine overlapping ranges for efficiency
    ranges.sort()
    merged_ranges = []
    for start, end in ranges:
        if merged_ranges and start <= merged_ranges[-1][1]:
            # Overlapping ranges, merge them
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))
        else:
            merged_ranges.append((start, end))

    return merged_ranges, ids_to_check


def main() -> None:
    """Main entry point."""
    # Get filename from command line argument, or use default
    filename: str = sys.argv[1] if len(sys.argv) > 1 else "./Day5/input.txt"

    try:
        # Parse input
        data = parse_input(filename)

        ranges, ids_to_check = preprocess_input(data)

        # Solve both parts
        part1_result = solve_part1(ranges, ids_to_check)
        part2_result = solve_part2(ranges, ids_to_check)

        # Output results
        print(f"🎯 Day 5 Results:")
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
