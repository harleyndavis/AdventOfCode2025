"""Benchmark using actual Day2 input files."""

import sys
import time
from typing import List, Callable


def read_file(filename: str) -> List[tuple[int, int]]:
    """Read ID ranges from file and return as list of tuples."""
    id_ranges: List[tuple[int, int]] = []

    with open(filename, "r") as file:
        content = file.read().strip()
        if not content:
            return id_ranges

        ranges = content.split(",")

        for range_str in ranges:
            range_str = range_str.strip()
            if not range_str:
                continue

            start_str, end_str = range_str.split("-", 1)
            start = int(start_str.strip())
            end = int(end_str.strip())
            id_ranges.append((start, end))

    return id_ranges


def is_invalid_id_original(id_num: int) -> bool:
    """Original implementation."""
    id_str = str(id_num)
    length = len(id_str)

    for pattern_len in range(1, length // 2 + 1):
        pattern = id_str[:pattern_len]

        if length % pattern_len == 0:
            repetitions = length // pattern_len
            if repetitions >= 2:
                repeated_pattern = pattern * repetitions
                if repeated_pattern == id_str:
                    return True
    return False


def is_invalid_id_optimized(id_num: int) -> bool:
    """Optimized implementation with direct character comparison."""
    id_str = str(id_num)
    length = len(id_str)

    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:
            is_repeated = True
            for i in range(pattern_len, length):
                if id_str[i] != id_str[i % pattern_len]:
                    is_repeated = False
                    break
            if is_repeated:
                return True
    return False


def sum_invalid_ids_with_function(id_range: tuple[int, int], invalid_func: Callable[[int], bool]) -> int:
    """Sum IDs in range that are invalid using the specified function."""
    start, end = id_range
    total_sum = 0

    for id_num in range(start, end + 1):
        if invalid_func(id_num):
            total_sum += id_num

    return total_sum


def benchmark_with_real_data(filename: str, function_name: str, invalid_func: Callable[[int], bool]) -> tuple[float, int]:
    """Benchmark using real input data."""
    id_ranges = read_file(filename)
    
    start_time = time.perf_counter()
    total_sum = 0
    
    for id_range in id_ranges:
        total_sum += sum_invalid_ids_with_function(id_range, invalid_func)
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    print(f"{function_name} ({filename}): {duration:.4f}s, sum = {total_sum}")
    return duration, total_sum


def analyze_input_characteristics(filename: str):
    """Analyze the characteristics of the input ranges."""
    id_ranges = read_file(filename)
    
    total_numbers = 0
    largest_range = 0
    largest_number = 0
    
    print(f"\nAnalyzing {filename}:")
    print(f"Number of ranges: {len(id_ranges)}")
    
    for start, end in id_ranges:
        range_size = end - start + 1
        total_numbers += range_size
        largest_range = max(largest_range, range_size)
        largest_number = max(largest_number, end)
        
    print(f"Total numbers to check: {total_numbers:,}")
    print(f"Largest range size: {largest_range:,}")
    print(f"Largest number: {largest_number:,} ({len(str(largest_number))} digits)")


def main():
    """Run benchmarks with actual input files."""
    print("Benchmarking is_invalid_id() with real Day2 input data")
    print("=" * 60)
    
    # Analyze input characteristics
    analyze_input_characteristics("test_input.txt")
    analyze_input_characteristics("input.txt")
    
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    # Test with test_input.txt first (smaller dataset)
    print("\n--- TEST INPUT ---")
    test_orig_time, test_orig_sum = benchmark_with_real_data("test_input.txt", "Original", is_invalid_id_original)
    test_opt_time, test_opt_sum = benchmark_with_real_data("test_input.txt", "Optimized", is_invalid_id_optimized)
    
    print(f"\nTest input results match: {'✓' if test_orig_sum == test_opt_sum else '✗ MISMATCH!'}")
    if test_opt_time > 0:
        print(f"Test input speedup: {test_orig_time / test_opt_time:.2f}x")
    
    # Test with full input.txt
    print("\n--- FULL INPUT ---")
    orig_time, orig_sum = benchmark_with_real_data("input.txt", "Original", is_invalid_id_original)
    opt_time, opt_sum = benchmark_with_real_data("input.txt", "Optimized", is_invalid_id_optimized)
    
    print(f"\nFull input results match: {'✓' if orig_sum == opt_sum else '✗ MISMATCH!'}")
    if opt_time > 0:
        print(f"Full input speedup: {orig_time / opt_time:.2f}x")
    
    print(f"\nFinal answer: {orig_sum}")


if __name__ == "__main__":
    main()