"""Extended benchmark with more complex test cases."""

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


def benchmark_with_larger_numbers():
    """Test with larger numbers that have longer digit sequences."""
    print("Testing with larger numbers (6-8 digits)...")

    # Create test cases with longer patterns
    test_cases = [
        111111,  # 6 digits, all same
        123123,  # 6 digits, pattern length 3
        12121212,  # 8 digits, pattern length 2
        123412341234,  # 12 digits, pattern length 4
        999999999,  # 9 digits, all same
        987654321,  # 9 digits, no pattern
    ]

    print("\nLarge number verification:")
    for test_num in test_cases:
        orig_result = is_invalid_id_original(test_num)
        opt_result = is_invalid_id_optimized(test_num)
        print(
            f"  {test_num}: Original={orig_result}, Optimized={opt_result}, Match={'✓' if orig_result == opt_result else '✗'}"
        )

    # Benchmark with range of larger numbers
    test_range = range(100000, 200000)

    start = time.perf_counter()
    orig_count = sum(1 for num in test_range if is_invalid_id_original(num))
    orig_time = time.perf_counter() - start

    start = time.perf_counter()
    opt_count = sum(1 for num in test_range if is_invalid_id_optimized(num))
    opt_time = time.perf_counter() - start

    print(f"\nLarger numbers benchmark (100K-200K):")
    print(f"Original: {orig_time:.4f}s, found {orig_count} invalid IDs")
    print(f"Optimized: {opt_time:.4f}s, found {opt_count} invalid IDs")
    print(f"Speed improvement: {orig_time / opt_time:.2f}x")


def test_memory_efficiency():
    """Test memory usage patterns."""
    print("\nTesting with numbers that stress string operations...")

    # Test cases that require checking many pattern lengths
    stress_cases = [
        12345678901234567890,  # Very long number
        111111111111,  # Long repeated pattern
        123456789012,  # Long no-pattern number
    ]

    for case in stress_cases:
        start = time.perf_counter()
        orig_result = is_invalid_id_original(case)
        orig_time = time.perf_counter() - start

        start = time.perf_counter()
        opt_result = is_invalid_id_optimized(case)
        opt_time = time.perf_counter() - start

        print(f"Number: {case}")
        print(f"  Original: {orig_time*1000:.3f}ms, result: {orig_result}")
        print(f"  Optimized: {opt_time*1000:.3f}ms, result: {opt_result}")
        print(f"  Speedup: {orig_time/opt_time:.2f}x")


def main():
    benchmark_with_larger_numbers()
    test_memory_efficiency()


if __name__ == "__main__":
    main()
