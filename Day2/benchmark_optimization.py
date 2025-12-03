"""Benchmark script to test is_invalid_id() optimizations."""

import time
from typing import Callable


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


def is_invalid_id_slicing(id_num: int) -> bool:
    """Alternative implementation using string slicing."""
    id_str = str(id_num)
    length = len(id_str)

    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:
            pattern = id_str[:pattern_len]
            is_repeated = True
            for i in range(pattern_len, length, pattern_len):
                if id_str[i : i + pattern_len] != pattern:
                    is_repeated = False
                    break
            if is_repeated:
                return True
    return False


def is_invalid_id_all(id_num: int) -> bool:
    """Implementation using all() with generator."""
    id_str = str(id_num)
    length = len(id_str)

    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:
            pattern = id_str[:pattern_len]
            if all(
                id_str[i : i + pattern_len] == pattern
                for i in range(0, length, pattern_len)
            ):
                return True
    return False


def benchmark_function(
    func: Callable[[int], bool], test_range: range, name: str
) -> float:
    """Benchmark a function over a range of values."""
    start_time = time.perf_counter()

    invalid_count = 0
    for num in test_range:
        if func(num):
            invalid_count += 1

    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"{name}: {duration:.4f}s, found {invalid_count} invalid IDs")
    return duration


def main():
    """Run benchmarks comparing different implementations."""
    print("Benchmarking is_invalid_id() optimizations")
    print("=" * 50)

    # Test with a range that includes various patterns
    test_range = range(1, 100000)

    print(f"Testing range: {test_range.start} to {test_range.stop - 1}")
    print()

    # First verify all implementations give same results
    test_cases = [55, 1212, 123123, 555, 1234, 7777, 121212]
    print("Verification test:")
    for test_num in test_cases:
        results = [
            is_invalid_id_original(test_num),
            is_invalid_id_optimized(test_num),
            is_invalid_id_slicing(test_num),
            is_invalid_id_all(test_num),
        ]
        all_same = all(r == results[0] for r in results)
        print(f"  {test_num}: {results[0]} - {'✓' if all_same else '✗ MISMATCH'}")

    print("\nPerformance benchmark:")

    # Benchmark each implementation
    original_time = benchmark_function(is_invalid_id_original, test_range, "Original")
    optimized_time = benchmark_function(
        is_invalid_id_optimized, test_range, "Optimized (char comparison)"
    )
    slicing_time = benchmark_function(
        is_invalid_id_slicing, test_range, "String slicing"
    )
    all_time = benchmark_function(is_invalid_id_all, test_range, "Using all()")

    print("\nSpeed improvements:")
    print(f"Optimized vs Original: {original_time / optimized_time:.2f}x faster")
    print(f"Slicing vs Original: {original_time / slicing_time:.2f}x faster")
    print(f"All() vs Original: {original_time / all_time:.2f}x faster")


if __name__ == "__main__":
    main()
