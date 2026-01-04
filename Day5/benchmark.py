"""
Performance benchmarking for Day 5 solution.

Usage:
    python benchmark.py
"""

import time
import sys
from typing import List

# Import the solution functions
sys.path.append(".")
from day5 import parse_input, solve_part1, solve_part2


def time_function(func, *args, **kwargs):
    """Time a function execution and return (duration, result)."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return end_time - start_time, result


def benchmark_solution():
    """Benchmark the Day 5 solution."""
    print(f"🎯 Day 5 Performance Benchmark")
    print("=" * 40)

    try:
        # Load input data
        print("📂 Loading input data...")
        data = parse_input("input.txt")
        print(f"   Loaded {len(data)} lines")

        # Benchmark Part 1
        print("\n🧪 Benchmarking Part 1...")
        part1_time, part1_result = time_function(solve_part1, data)
        print(f"   Result: {part1_result}")
        print(f"   Time: {part1_time*1000:.2f}ms")

        # Benchmark Part 2
        print("\n🧪 Benchmarking Part 2...")
        part2_time, part2_result = time_function(solve_part2, data)
        print(f"   Result: {part2_result}")
        print(f"   Time: {part2_time*1000:.2f}ms")

        # Summary
        total_time = part1_time + part2_time
        print("\n" + "=" * 40)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 40)
        print(f"Part 1: {part1_time*1000:6.2f}ms")
        print(f"Part 2: {part2_time*1000:6.2f}ms")
        print(f"Total:  {total_time*1000:6.2f}ms")

        if total_time < 0.001:
            print("⚡ Excellent performance!")
        elif total_time < 0.01:
            print("✅ Good performance!")
        elif total_time < 0.1:
            print("👍 Acceptable performance")
        else:
            print("⏰ Consider optimization opportunities")

    except Exception as e:
        print(f"❌ Benchmark failed: {e}")


if __name__ == "__main__":
    benchmark_solution()
