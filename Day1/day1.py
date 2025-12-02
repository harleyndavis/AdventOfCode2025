"""
Processes movement commands from an input file to update a current position value.
Reads a file containing movement commands where each line starts with 'R' (right/positive)
or 'L' (left/negative) followed by a numeric distance. Starting from position 50,
the function moves step by step in the specified direction for the given distance.
The position wraps around in a circular manner:
- If position goes below 0, it wraps to 99
- If position goes above 99, it wraps to 0
This creates a circular buffer/ring of positions from 0-99 where movement continues
seamlessly across boundaries.
Args:
    filename (command line argument): Path to input file (defaults to './Day1/input.txt')
Returns:
    None (prints password count)
Side Effects:
    - Reads from file system
    - Prints result to stdout
"""

import sys
from typing import List

# Constants for clarity
START_POSITION: int = 50
POSITION_RANGE: int = 100


def parse_command(line: str) -> tuple[int, int]:
    """Parse movement command into direction and distance.

    Args:
        line: Command line like 'R10' or 'L25'

    Returns:
        tuple of (direction, distance) where direction is 1 for R, -1 for L
    """
    direction: int = 1 if line[0] == "R" else -1
    distance: int = int(line[1:])
    return direction, distance


def calculate_zero_crossings(
    position: int, direction: int, distance: int
) -> tuple[int, int]:
    """Calculate zero crossings and new position for a movement.

    Args:
        position: Current position (0-99)
        direction: Movement direction (1 for right, -1 for left)
        distance: Distance to move

    Returns:
        tuple of (zero_crossings, new_position)
    """
    zero_crossings: int = 0

    if direction == 1:  # Moving right (positive direction)
        # Distance from current position to next 0 (going right)
        if position == 0:
            distance_to_first_zero: int = POSITION_RANGE
        else:
            distance_to_first_zero: int = POSITION_RANGE - position

        if distance >= distance_to_first_zero:
            # We'll cross at least one zero
            zero_crossings += 1
            remaining_distance: int = distance - distance_to_first_zero
            # Each additional 100 steps crosses zero again
            zero_crossings += remaining_distance // POSITION_RANGE

    else:  # Moving left (negative direction)
        # Distance from current position to next 0 (going left)
        if position == 0:
            distance_to_first_zero: int = POSITION_RANGE
        else:
            distance_to_first_zero: int = position

        if distance >= distance_to_first_zero:
            # We'll cross at least one zero
            zero_crossings += 1
            remaining_distance: int = distance - distance_to_first_zero
            # Each additional 100 steps crosses zero again
            zero_crossings += remaining_distance // POSITION_RANGE

    # Calculate new position
    new_position: int = (position + direction * distance) % POSITION_RANGE
    return zero_crossings, new_position


def process_commands(filename: str) -> int:
    """Process all movement commands and return total zero crossings.

    Args:
        filename: Path to input file

    Returns:
        Total number of zero crossings

    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If command format is invalid
    """
    with open(filename, "r") as file:
        content: str = file.read()
        total_crossings: int = 0
        position: int = START_POSITION

        for line in content.splitlines():
            if not line.strip():  # Skip empty lines
                continue

            direction, distance = parse_command(line)
            crossings, position = calculate_zero_crossings(
                position, direction, distance
            )
            total_crossings += crossings

        return total_crossings


def main() -> None:
    """Main entry point."""
    # Get filename from command line argument, or use default
    filename: str = sys.argv[1] if len(sys.argv) > 1 else "./Day1/input.txt"

    try:
        zero_crossings: int = process_commands(filename)
        print(f"Password: {zero_crossings}")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
