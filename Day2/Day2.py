import sys
from typing import List


def read_file(filename: str) -> List[tuple[int, int]]:
    """Read ID ranges from file and return as list of tuples.

    Args:
        filename: Path to input file containing ID ranges

    Returns:
        List of tuples representing ID ranges

    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    id_ranges: List[tuple[int, int]] = []

    with open(filename, "r") as file:
        # Read the entire file content and strip whitespace
        content = file.read().strip()
        if not content:
            return id_ranges

        # Split by commas to get individual ranges
        ranges = content.split(",")

        for range in ranges:
            range = range.strip()
            if not range:  # Skip empty parts
                continue

            # Split each range on "-" to get start and end
            start_str, end_str = range.split("-", 1)

            start = int(start_str.strip())
            end = int(end_str.strip())
            id_ranges.append((start, end))

    return id_ranges


def sum_invalid_ids(id_range: tuple[int, int]) -> int:
    """Sum IDs in range that are invalid.
    An invalid ID is defined as one that contains any duplicated sequence of digits.
    The sequence can be dupilicated multiple times.
    Examples: 55, 555, 1212, 1212121212, 123123123

    Args:
        id_range: Tuple of (start, end) representing ID range

    Returns:
        Sum of invalid IDs in the range
    """
    start, end = id_range
    total_sum = 0

    for id_num in range(start, end + 1):
        if is_invalid_id(id_num):
            total_sum += id_num

    return total_sum


def is_invalid_id(id_num: int) -> bool:
    """Check if an ID contains any duplicated sequence of digits.

    Args:
        id_num: The ID number to check

    Returns:
        True if the ID contains duplicated sequences, False otherwise
    """
    id_str = str(id_num)
    length = len(id_str)

    # Check all possible pattern lengths from 1 to half the string length
    for pattern_len in range(1, length // 2 + 1):
        pattern = id_str[:pattern_len]

        # Check if the entire string can be formed by repeating this pattern
        if length % pattern_len == 0:  # Length must be divisible by pattern length
            repetitions = length // pattern_len
            if repetitions >= 2:  # Must repeat at least twice
                repeated_pattern = pattern * repetitions
                if repeated_pattern == id_str:
                    return True

    return False


def main() -> None:
    """Main entry point."""
    # Get filename from command line argument, or use default
    filename: str = sys.argv[1] if len(sys.argv) > 1 else "./Day2/input.txt"

    try:
        id_ranges: List[tuple[int, int]] = read_file(filename)
        total_duplicate_sequences: int = 0
        for range in id_ranges:
            total_duplicate_sequences += sum_invalid_ids(range)
        print(
            f"Total sum of IDs with duplicated sequences: {total_duplicate_sequences}"
        )

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
