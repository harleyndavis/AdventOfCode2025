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
        raise FileNotFoundError(f"Input file '{filename}' not found")
    except Exception as e:
        raise ValueError(f"Error parsing input: {e}")


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


def solve_part1_optimized(data: List[str]) -> int:
    """Optimized version of part 1 solution.

    Optimizations applied:
    - Single-pass digit extraction with position tracking
    - Reduced string operations
    - Integer arithmetic instead of string concatenation

    Args:
        data: Parsed input data

    Returns:
        Solution for part 1
    """
    total_output_joltage = 0

    for line in data:
        # Extract digits with their positions in one pass
        digit_positions = []
        for i, char in enumerate(line):
            if char.isdigit():
                digit_positions.append((int(char), i))

        # Get digits excluding the last one
        available_digits = digit_positions[:-1]
        max_digit, max_position = max(available_digits, key=lambda x: x[0])

        # Find the largest value after the max_position
        remaining_digits = [
            digit for digit, pos in digit_positions if pos > max_position
        ]

        if remaining_digits:
            second_max = max(remaining_digits)
            # Concatenate using integer arithmetic (faster than string operations)
            concatenated_value = max_digit * 10 + second_max
            total_output_joltage += concatenated_value

    return total_output_joltage


def solve_part2_optimized(data: List[str]) -> int:
    """Optimized version of part 2 solution.

    Optimizations applied:
    - Single-pass digit position extraction
    - Reduced substring operations
    - Direct index calculations
    - Integer arithmetic instead of string concatenation

    Args:
        data: Parsed input data

    Returns:
        Solution for part 2
    """
    result = 0

    for line in data:
        length = len(line)

        # Extract all digit positions once
        digit_positions = []
        for i, char in enumerate(line):
            if char.isdigit():
                digit_positions.append((int(char), i))

        final_digits = []
        last_index = -1

        # Process iterations more efficiently
        for i in range(11, -1, -1):
            end_pos = length - i

            # Skip if we're beyond the line or past our last position
            if end_pos <= last_index + 1:
                continue

            # Find digits in range [last_index + 1, end_pos)
            valid_digits = [
                digit for digit, pos in digit_positions if last_index < pos < end_pos
            ]

            if valid_digits:
                max_digit = max(valid_digits)
                final_digits.append(max_digit)

                # Update last_index to the position of this max digit
                for digit, pos in digit_positions:
                    if digit == max_digit and last_index < pos < end_pos:
                        last_index = pos
                        break
            else:
                # If no digits found in this range, we might be done
                break

        # Convert final digits to number using integer arithmetic
        if final_digits:
            final_value = 0
            for digit in final_digits:
                final_value = final_value * 10 + digit
            result += final_value

    return result


def solve_combined_optimized(data: List[str]) -> tuple[int, int]:
    """Combined optimized solution for both parts in a single pass.

    This processes each line once and calculates both results simultaneously,
    sharing digit extraction and reducing overall computational overhead.

    Args:
        data: Parsed input data

    Returns:
        Tuple of (part1_result, part2_result)
    """
    part1_total = 0
    part2_total = 0

    for line in data:
        length = len(line)

        # Single pass digit extraction with positions
        digit_positions = []
        for i, char in enumerate(line):
            if char.isdigit():
                digit_positions.append((int(char), i))

        # PART 1 CALCULATION
        # Get digits excluding the last one
        available_digits = digit_positions[:-1]
        if available_digits:
            max_digit, max_position = max(available_digits, key=lambda x: x[0])

            # Find the largest value after the max_position
            remaining_digits = [
                digit for digit, pos in digit_positions if pos > max_position
            ]

            if remaining_digits:
                second_max = max(remaining_digits)
                concatenated_value = max_digit * 10 + second_max
                part1_total += concatenated_value

        # PART 2 CALCULATION
        final_digits = []
        last_index = -1

        for i in range(11, -1, -1):
            end_pos = length - i

            if end_pos <= last_index + 1:
                continue

            # Find digits in range efficiently
            valid_digits = [
                digit for digit, pos in digit_positions if last_index < pos < end_pos
            ]

            if valid_digits:
                max_digit = max(valid_digits)
                final_digits.append(max_digit)

                # Update position
                for digit, pos in digit_positions:
                    if digit == max_digit and last_index < pos < end_pos:
                        last_index = pos
                        break
            else:
                break

        # Convert to number
        if final_digits:
            final_value = 0
            for digit in final_digits:
                final_value = final_value * 10 + digit
            part2_total += final_value

    return part1_total, part2_total


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
    import argparse
    import time

    parser = argparse.ArgumentParser(description="Advent of Code Day 3 Solution")
    parser.add_argument(
        "filename",
        nargs="?",
        default="input.txt",
        help="Input file path (default: input.txt)",
    )
    parser.add_argument(
        "--test", action="store_true", help="Use test input (./Day3/test_input.txt)"
    )
    parser.add_argument(
        "--optimized", action="store_true", help="Use optimized functions"
    )
    parser.add_argument(
        "--combined", action="store_true", help="Use combined optimized solution"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Compare original vs optimized performance",
    )
    parser.add_argument(
        "--part", type=int, choices=[1, 2], help="Run only specific part"
    )

    args = parser.parse_args()

    # Determine input file
    if args.test:
        filename = "test_input.txt"
        print("Using test input...")
    else:
        filename = args.filename
        print(f"Using input file: {filename}")

    try:
        # Parse input
        data = parse_input(filename)

        if args.combined:
            # Use the combined optimized solution
            print("\n🚀 Using combined optimized solution...")
            start = time.perf_counter()
            result1, result2 = solve_combined_optimized(data)
            end = time.perf_counter()
            print(f"🎯 Day 3 Results (Combined Optimized):")
            print(f"   Part 1: {result1}")
            print(f"   Part 2: {result2}")
            print(f"   Execution time: {(end - start) * 1000:.2f}ms")

        elif args.benchmark:
            # Compare performance between original and optimized
            print("\n📊 Benchmarking original vs optimized solutions...")

            # Test Part 1
            print("\n🔹 Part 1 Comparison:")
            start = time.perf_counter()
            result1_orig = solve_part1(data)
            time_orig_1 = time.perf_counter() - start

            start = time.perf_counter()
            result1_opt = solve_part1_optimized(data)
            time_opt_1 = time.perf_counter() - start

            print(f"   Original:  {result1_orig:>10} ({time_orig_1*1000:>6.2f}ms)")
            print(f"   Optimized: {result1_opt:>10} ({time_opt_1*1000:>6.2f}ms)")
            print(f"   Speedup: {time_orig_1/time_opt_1:.2f}x")
            print(f"   ✅ Results match: {result1_orig == result1_opt}")

            # Test Part 2
            print("\n🔹 Part 2 Comparison:")
            start = time.perf_counter()
            result2_orig = solve_part2(data)
            time_orig_2 = time.perf_counter() - start

            start = time.perf_counter()
            result2_opt = solve_part2_optimized(data)
            time_opt_2 = time.perf_counter() - start

            print(f"   Original:  {result2_orig:>10} ({time_orig_2*1000:>6.2f}ms)")
            print(f"   Optimized: {result2_opt:>10} ({time_opt_2*1000:>6.2f}ms)")
            print(f"   Speedup: {time_orig_2/time_opt_2:.2f}x")
            print(f"   ✅ Results match: {result2_orig == result2_opt}")

            # Test Combined
            print("\n🔹 Combined vs Separate:")
            start = time.perf_counter()
            comb1, comb2 = solve_combined_optimized(data)
            time_combined = time.perf_counter() - start

            total_separate = time_opt_1 + time_opt_2
            print(f"   Separate optimized: {total_separate*1000:>6.2f}ms")
            print(f"   Combined optimized: {time_combined*1000:>6.2f}ms")
            print(f"   Combined speedup: {total_separate/time_combined:.2f}x")
            print(
                f"   ✅ Combined results match: {comb1 == result1_opt and comb2 == result2_opt}"
            )

        elif args.optimized:
            # Use optimized functions
            print("\n🚀 Using optimized solutions...")
            if args.part is None or args.part == 1:
                start = time.perf_counter()
                result1 = solve_part1_optimized(data)
                time1 = time.perf_counter() - start
                print(f"   Part 1 (optimized): {result1} ({time1*1000:.2f}ms)")

            if args.part is None or args.part == 2:
                start = time.perf_counter()
                result2 = solve_part2_optimized(data)
                time2 = time.perf_counter() - start
                print(f"   Part 2 (optimized): {result2} ({time2*1000:.2f}ms)")

        else:
            # Use original functions
            print("\n🎯 Day 3 Results (Original):")
            if args.part is None or args.part == 1:
                start = time.perf_counter()
                result1 = solve_part1(data)
                time1 = time.perf_counter() - start
                print(f"   Part 1: {result1} ({time1*1000:.2f}ms)")

            if args.part is None or args.part == 2:
                start = time.perf_counter()
                result2 = solve_part2(data)
                time2 = time.perf_counter() - start
                print(f"   Part 2: {result2} ({time2*1000:.2f}ms)")

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
