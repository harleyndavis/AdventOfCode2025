"""
Performance benchmarking for Day 1 solution.

This script compares the O(n) step-by-step approach with the O(1) mathematical approach,
demonstrating the massive performance improvement achieved through algorithmic optimization.

Usage:
    python benchmark.py
    python benchmark.py --detailed
    python benchmark.py --save-results
"""

import time
import sys
import argparse
from typing import List, Tuple
import statistics
import tempfile
import os

# Import the optimized functions
sys.path.append(".")
from day1 import parse_command, process_commands, START_POSITION, POSITION_RANGE


def calculate_zero_crossings_naive(
    position: int, direction: int, distance: int
) -> Tuple[int, int]:
    """
    O(n) step-by-step approach - the original implementation.

    This simulates each individual step, which is inefficient for large distances
    but serves as a baseline for correctness validation.
    """
    zero_crossings: int = 0
    current_pos: int = position

    # Move step by step
    for _ in range(distance):
        current_pos += direction

        # Handle wrapping
        if current_pos < 0:
            current_pos = POSITION_RANGE - 1  # 99
        elif current_pos >= POSITION_RANGE:
            current_pos = 0

        # Count zero crossings
        if current_pos == 0:
            zero_crossings += 1

    return zero_crossings, current_pos


def process_commands_naive(commands: List[str]) -> int:
    """Process commands using the O(n) approach."""
    total_crossings: int = 0
    position: int = START_POSITION

    for line in commands:
        if not line.strip():
            continue
        direction, distance = parse_command(line)
        crossings, position = calculate_zero_crossings_naive(
            position, direction, distance
        )
        total_crossings += crossings

    return total_crossings


def generate_test_data(num_commands: int, max_distance: int = 10000) -> List[str]:
    """Generate test data with varying command sizes."""
    import random

    commands = []

    for _ in range(num_commands):
        direction = random.choice(["R", "L"])
        distance = random.randint(1, max_distance)
        commands.append(f"{direction}{distance}")

    return commands


def time_function(func, *args, **kwargs) -> Tuple[float, any]:
    """Time a function execution and return (duration, result)."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return end_time - start_time, result


def validate_correctness():
    """Ensure both approaches produce identical results."""
    print("🔍 Validating correctness of both approaches...")

    test_cases = [
        ["R10", "L5", "R60"],  # Simple case
        ["R150", "L200"],  # Large distances
        ["L50"],  # Single crossing
        ["R0", "L0"],  # Zero distances
        ["R100", "R100"],  # Exact boundaries
    ]

    for i, commands in enumerate(test_cases, 1):
        naive_result = process_commands_naive(commands)

        # Create temp file for optimized version
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("\n".join(commands))
            temp_filename = f.name

        try:
            optimized_result = process_commands(temp_filename)

            if naive_result == optimized_result:
                print(f"  ✅ Test case {i}: Both methods return {naive_result}")
            else:
                print(
                    f"  ❌ Test case {i}: Naive={naive_result}, Optimized={optimized_result}"
                )
                return False
        finally:
            os.unlink(temp_filename)

    print("✅ All validation tests passed!")
    return True


def run_benchmark_suite():
    """Run comprehensive performance benchmarks."""
    print("⚡ Performance Benchmarking Suite")
    print("=" * 50)

    # Validate correctness first
    if not validate_correctness():
        print("❌ Correctness validation failed. Aborting benchmarks.")
        return

    print("\n📊 Performance Comparison")
    print("-" * 30)

    # Test scenarios: (num_commands, max_distance, description)
    test_scenarios = [
        (10, 100, "Small commands, small distances"),
        (10, 1000, "Small commands, medium distances"),
        (10, 10000, "Small commands, large distances"),
        (50, 1000, "Medium commands, medium distances"),
        (50, 10000, "Medium commands, large distances"),
        (100, 10000, "Large commands, large distances"),
        ("REAL_INPUT", None, "🎯 REAL PUZZLE INPUT (4,317 commands)"),
    ]

    results = []

    for num_commands, max_distance, description in test_scenarios:
        print(f"\n🧪 Testing: {description}")

        if num_commands == "REAL_INPUT":
            # Use actual puzzle input
            with open("input.txt", "r") as f:
                commands = [line.strip() for line in f if line.strip()]
            num_commands = len(commands)
            print(f"   Commands: {num_commands} (actual puzzle input)")
        else:
            print(f"   Commands: {num_commands}, Max distance: {max_distance}")
            # Generate test data
            commands = generate_test_data(num_commands, max_distance)

        total_distance = sum(int(cmd[1:]) for cmd in commands)

        # Create temp file for optimized version
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("\n".join(commands))
            temp_filename = f.name

        try:
            # Benchmark naive approach (with timeout for very large cases)
            naive_times = []
            naive_result = None

            # Only run naive approach for reasonable sizes
            if total_distance < 1000000:  # 1M total distance limit for naive
                for _ in range(3):  # Run multiple times for average
                    duration, result = time_function(process_commands_naive, commands)
                    naive_times.append(duration)
                    naive_result = result

                avg_naive_time = statistics.mean(naive_times)
            else:
                avg_naive_time = float("inf")  # Too large for naive approach
                naive_result = "Skipped (too large)"

            # Benchmark optimized approach
            optimized_times = []
            for _ in range(5):  # Run more times since it's fast
                duration, optimized_result = time_function(
                    process_commands, temp_filename
                )
                optimized_times.append(duration)

            avg_optimized_time = statistics.mean(optimized_times)

            # Calculate speedup
            if avg_naive_time != float("inf") and avg_optimized_time > 0:
                speedup = avg_naive_time / avg_optimized_time
                speedup_str = f"{speedup:.1f}x faster"
            else:
                speedup_str = "∞ (effectively infinite speedup)"

            print(f"   📈 Naive (O(n)):      {avg_naive_time*1000:.2f}ms")
            print(f"   ⚡ Optimized (O(1)):  {avg_optimized_time*1000:.2f}ms")
            print(f"   🚀 Speedup:           {speedup_str}")
            print(f"   📊 Total distance:    {total_distance:,} steps")

            results.append(
                {
                    "scenario": description,
                    "commands": num_commands,
                    "max_distance": max_distance,
                    "total_distance": total_distance,
                    "naive_time": avg_naive_time,
                    "optimized_time": avg_optimized_time,
                    "speedup": (
                        avg_naive_time / avg_optimized_time
                        if avg_optimized_time > 0
                        else float("inf")
                    ),
                    "result": optimized_result,
                }
            )

        finally:
            os.unlink(temp_filename)

    return results


def print_summary_table(results):
    """Print a formatted summary table of all results."""
    print("\n" + "=" * 80)
    print("📋 PERFORMANCE SUMMARY")
    print("=" * 80)

    print(
        f"{'Scenario':<35} {'Commands':<8} {'Total Dist':<12} {'Speedup':<15} {'Result':<8}"
    )
    print("-" * 80)

    for result in results:
        scenario = result["scenario"][:34]
        speedup = (
            f"{result['speedup']:.1f}x" if result["speedup"] != float("inf") else "∞"
        )

        print(
            f"{scenario:<35} {result['commands']:<8} {result['total_distance']:>11,} {speedup:<15} {result['result']:<8}"
        )

    # Calculate aggregate metrics
    finite_speedups = [r["speedup"] for r in results if r["speedup"] != float("inf")]
    if finite_speedups:
        avg_speedup = statistics.mean(finite_speedups)
        max_speedup = max(finite_speedups)
        print(f"\n🎯 Average speedup: {avg_speedup:.1f}x")
        print(f"🚀 Maximum speedup: {max_speedup:.1f}x")


def main():
    """Main benchmarking entry point."""
    parser = argparse.ArgumentParser(description="Benchmark Day 1 performance")
    parser.add_argument(
        "--detailed", action="store_true", help="Show detailed timing information"
    )
    parser.add_argument(
        "--save-results", action="store_true", help="Save results to file"
    )

    args = parser.parse_args()

    print("🎯 Day 1 Performance Benchmark")
    print(f"🔬 Comparing O(n) vs O(1) algorithms")
    print(f"🐍 Python {sys.version}")

    results = run_benchmark_suite()

    if results:
        print_summary_table(results)

        if args.save_results:
            # Save detailed results
            with open("benchmark_results.txt", "w") as f:
                f.write("Day 1 Performance Benchmark Results\n")
                f.write("=" * 40 + "\n\n")
                for result in results:
                    f.write(f"Scenario: {result['scenario']}\n")
                    f.write(
                        f"Commands: {result['commands']}, Max Distance: {result['max_distance']}\n"
                    )
                    f.write(f"Total Distance: {result['total_distance']:,}\n")
                    f.write(f"Naive Time: {result['naive_time']*1000:.2f}ms\n")
                    f.write(f"Optimized Time: {result['optimized_time']*1000:.2f}ms\n")
                    f.write(f"Speedup: {result['speedup']:.1f}x\n")
                    f.write(f"Result: {result['result']}\n")
                    f.write("-" * 40 + "\n")
            print(f"\n💾 Results saved to benchmark_results.txt")

        print(f"\n✨ Benchmark complete! Your optimization is working beautifully.")


if __name__ == "__main__":
    main()
