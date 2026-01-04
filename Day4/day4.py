"""
Advent of Code 2025 - Day 4

Problem: [Brief description of the problem]

Usage:
    python Day4/day4.py
    python Day4/day4.py ./Day4/test_input.txt
"""

import sys
from typing import List, Optional
import time


def parse_input(filename: str) -> List[List[str]]:
    """Parse the input file and return processed data.

    Args:
        filename: Path to the input file

    Returns:
        List of lists of characters (2D grid)

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input format is invalid
    """
    try:
        with open(filename, "r") as f:
            lines = [list(line.strip()) for line in f if line.strip()]
        return lines
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")
    except Exception as e:
        raise ValueError(f"Error parsing input: {{e}}")


def solve_part1(data: List[List[str]]) -> int:
    """Solve part 1 of the problem.

    Args:
        data: 2D grid of characters

    Returns:
        Solution for part 1
    """
    if not data:
        return 0

    rows, cols = len(data), len(data[0])
    result = 0

    for i in range(rows):
        for j in range(cols):
            if data[i][j] == "@":
                result += removable_at_symbols(data, i, j, rows, cols)

    return result


def removable_at_symbols(
    data: List[List[str]], i: int, j: int, rows: int, cols: int
) -> int:
    """Count surrounding '@' symbols and return 1 if less than 4, 0 otherwise.

    Args:
        data: 2D grid of characters
        i: Row index
        j: Column index
        rows: Total number of rows in the grid
        cols: Total number of columns in the grid

    Returns:
        1 if "removable", less than 4 '@' symbols around position, 0 otherwise
    """
    # Filter before function call instead of checking here
    # if data[i][j] != "@":
    #   return 0

    # Check all 8 directions around the current position
    at_count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for di, dj in directions:
        ni, nj = i + di, j + dj
        # Check if the position is within bounds
        if 0 <= ni < rows and 0 <= nj < cols:
            if data[ni][nj] == "@":
                at_count += 1

            # Suggested optimization, did not improve performance in testing
            if at_count >= 4:
                return 0  # No need to count further

    # If there are less than four '@' around, return 1
    return 1


def solve_part2(data: List[List[str]]) -> int:
    """Solve part 2 of the problem.

    Args:
        data: 2D grid of characters

    Returns:
        Solution for part 2
    """
    if not data:
        return 0

    rows, cols = len(data), len(data[0])
    result = 0
    pass_result = -1  # set to negative one to enter the loop first time.
    while pass_result != 0:
        pass_result = 0  # resetting for this pass
        for i in range(rows):
            for j in range(cols):
                if data[i][j] != "@":
                    continue
                item_result = removable_at_symbols(data, i, j, rows, cols)
                if item_result:
                    # remove item
                    data[i][j] = "."

                pass_result += item_result

        result += pass_result

    return result


def solve_part2_tracking_at_cells(data: List[List[str]]) -> int:
    if not data:
        return 0

    rows, cols = len(data), len(data[0])

    # Build initial set of '@' positions
    at_positions = set()
    for i in range(rows):
        for j in range(cols):
            if data[i][j] == "@":
                at_positions.add((i, j))

    result = 0
    while True:
        removals = []

        # Only check existing '@' positions
        for i, j in at_positions:
            if removable_at_symbols(data, i, j, rows, cols):
                removals.append((i, j))

        if not removals:
            break

        # Remove cells and update tracking set
        for i, j in removals:
            data[i][j] = "."
            at_positions.remove((i, j))

        result += len(removals)

    return result


def solve_part2_differential(data: List[List[str]]) -> int:
    """Solve part 2 using differential updates - only recheck cells affected by removals.

    Args:
        data: 2D grid of characters

    Returns:
        Solution for part 2
    """
    if not data:
        return 0

    rows, cols = len(data), len(data[0])

    # Build initial set of '@' positions
    at_positions = set()
    for i in range(rows):
        for j in range(cols):
            if data[i][j] == "@":
                at_positions.add((i, j))

    # Initially check all '@' positions
    cells_to_check = set(at_positions)
    result = 0

    while cells_to_check:
        removals = []
        next_check = set()

        # Only check cells that might have changed status
        for i, j in cells_to_check:
            if (i, j) in at_positions and removable_at_symbols(data, i, j, rows, cols):
                removals.append((i, j))

        if not removals:
            break

        # Remove cells and determine which neighbors need rechecking
        for i, j in removals:
            data[i][j] = "."
            at_positions.remove((i, j))

            # Add neighbors to recheck list (they might become removable now)
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:  # Skip center cell
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and (ni, nj) in at_positions:
                        next_check.add((ni, nj))

        cells_to_check = next_check
        result += len(removals)

    return result


def main() -> None:
    """Main entry point."""
    # Get filename from command line argument, or use default
    filename: str = sys.argv[1] if len(sys.argv) > 1 else "test_input.txt"

    try:
        # Parse input
        data = parse_input(filename)

        # Solve both parts
        # Time part 1
        start_time = time.time()
        part1_result = solve_part1(data)
        part1_time = time.time() - start_time

        # Time part 2
        start_time = time.time()
        part2_result = solve_part2(data)
        part2_time = time.time() - start_time

        # Output results
        print(f"🎯 Day 4 Results:")
        print(f"   Part 1: {part1_result} (Time: {part1_time:.6f} seconds)")
        print(f"   Part 2: {part2_result} (Time: {part2_time:.6f} seconds)")

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
