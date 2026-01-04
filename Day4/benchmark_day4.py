"""
Benchmark script for Day 4 Advent of Code solution.

This script runs the Day 4 solution multiple times and provides detailed
timing statistics including min, max, median, and mean runtimes.

Usage:
    python Day4/benchmark_day4.py
    python Day4/benchmark_day4.py ./Day4/input.txt
    python Day4/benchmark_day4.py --runs 10
"""

import sys
import time
import statistics
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse

# Add the Day4 directory to path so we can import day4
sys.path.append(str(Path(__file__).parent))
from day4 import (
    parse_input,
    solve_part1,
    solve_part2,
    solve_part2_tracking_at_cells,
    solve_part2_differential,
)


def deep_copy_2d_list(data: List[List[str]]) -> List[List[str]]:
    """Create a deep copy of a 2D list."""
    return [row[:] for row in data]


def benchmark_function(func, data: List[List[str]], runs: int = 5) -> Dict[str, Any]:
    """Benchmark a function over multiple runs.

    Args:
        func: Function to benchmark
        data: Input data for the function
        runs: Number of benchmark runs

    Returns:
        Dictionary containing timing statistics
    """
    times = []
    results = []

    # Warmup run (not timed)
    warmup_data = (
        deep_copy_2d_list(data)
        if isinstance(data, list) and data and isinstance(data[0], list)
        else data
    )
    result = func(warmup_data)

    # Timed runs
    for _ in range(runs):
        # Create fresh deep copy of data for each run (important for part 2)
        if isinstance(data, list) and data and isinstance(data[0], list):
            test_data = deep_copy_2d_list(data)  # Deep copy for 2D lists
        else:
            test_data = data.copy() if isinstance(data, list) else data

        start_time = time.perf_counter()
        result = func(test_data)
        end_time = time.perf_counter()

        times.append(end_time - start_time)
        results.append(result)

    # Verify all results are consistent
    if not all(r == results[0] for r in results):
        print(f"⚠️ Warning: Inconsistent results detected: {set(results)}")

    return {
        "result": results[0],
        "times": times,
        "min_time": min(times),
        "max_time": max(times),
        "mean_time": statistics.mean(times),
        "median_time": statistics.median(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
        "total_time": sum(times),
        "runs": runs,
    }


def format_time(seconds: float) -> str:
    """Format time in human-readable units."""
    if seconds >= 1:
        return f"{seconds:.3f}s"
    elif seconds >= 0.001:
        return f"{seconds*1000:.3f}ms"
    else:
        return f"{seconds*1000000:.3f}μs"


def print_benchmark_results(name: str, stats: Dict[str, Any]) -> None:
    """Print formatted benchmark results."""
    print(f"\n📊 {name} Benchmark Results:")
    print(f"   Result: {stats['result']}")
    print(f"   Runs: {stats['runs']}")
    print(f"   Min time:    {format_time(stats['min_time'])}")
    print(f"   Max time:    {format_time(stats['max_time'])}")
    print(f"   Mean time:   {format_time(stats['mean_time'])}")
    print(f"   Median time: {format_time(stats['median_time'])}")
    print(f"   Std dev:     {format_time(stats['std_dev'])}")
    print(f"   Total time:  {format_time(stats['total_time'])}")

    # Performance insights
    variance_pct = (
        (stats["std_dev"] / stats["mean_time"]) * 100 if stats["mean_time"] > 0 else 0
    )
    if variance_pct > 20:
        print(f"   ⚠️ High variance: {variance_pct:.1f}%")
    elif variance_pct > 10:
        print(f"   ⚡ Moderate variance: {variance_pct:.1f}%")
    else:
        print(f"   ✅ Low variance: {variance_pct:.1f}%")


def format_table_row(optimization_name: str, stats: Dict[str, Any]) -> str:
    """Format benchmark results as a table row for README."""
    mean_time = format_time(stats["mean_time"])
    min_time = format_time(stats["min_time"])
    max_time = format_time(stats["max_time"])
    range_str = f"{min_time}-{max_time}"

    variance_pct = (
        (stats["std_dev"] / stats["mean_time"]) * 100 if stats["mean_time"] > 0 else 0
    )

    return f"| {optimization_name} | {mean_time} | {range_str} | {variance_pct:.1f}% |"


def print_table_output(
    part1_stats: Optional[Dict[str, Any]] = None,
    part2_stats: Optional[Dict[str, Any]] = None,
    optimization_name: str = "Current Implementation",
) -> None:
    """Print results in table format for README."""
    print(f"\n📋 Table Format for README:")

    if part1_stats:
        print(format_table_row(f"{optimization_name}", part1_stats))
    if part2_stats:
        print(format_table_row(f"{optimization_name}", part2_stats))

    print(f"\n💡 Copy the above table rows to your README.md")


def main():
    """Main benchmarking function."""
    parser = argparse.ArgumentParser(description="Benchmark Day 4 solution")
    parser.add_argument(
        "filename",
        nargs="?",
        default="input.txt",
        help="Input file to benchmark (default: input.txt)",
    )
    parser.add_argument(
        "--runs", type=int, default=5, help="Number of benchmark runs (default: 5)"
    )
    parser.add_argument(
        "--test", action="store_true", help="Use test_input.txt instead of input.txt"
    )
    parser.add_argument(
        "--part1", action="store_true", help="Run only Part 1 benchmark"
    )
    parser.add_argument(
        "--part2", action="store_true", help="Run only Part 2 benchmark"
    )
    parser.add_argument(
        "--table", action="store_true", help="Output results in table format for README"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Current Implementation",
        help="Optimization name for table output (default: Current Implementation)",
    )
    parser.add_argument(
        "--tracking",
        action="store_true",
        help="Use the tracking @ cells optimization for Part 2",
    )
    parser.add_argument(
        "--differential",
        action="store_true",
        help="Use the differential updates optimization for Part 2",
    )

    args = parser.parse_args()

    # Determine input file
    if args.test:
        filename = "test_input.txt"
    else:
        filename = args.filename

    # Determine which parts to run
    run_part1 = not args.part2  # Run part1 unless --part2 is specified
    run_part2 = not args.part1  # Run part2 unless --part1 is specified

    # If both flags are specified, run both (default behavior)
    if args.part1 and args.part2:
        run_part1 = run_part2 = True

    parts_to_run = []
    if run_part1:
        parts_to_run.append("Part 1")
    if run_part2:
        parts_to_run.append("Part 2")

    print(f"🚀 Benchmarking Day 4 Solution")
    print(f"   Input file: {filename}")
    print(f"   Number of runs: {args.runs}")
    print(f"   Parts to run: {', '.join(parts_to_run)}")

    try:
        # Parse input once
        print("\n📁 Loading input data...")
        data = parse_input(filename)
        print(f"   Grid size: {len(data)} rows × {len(data[0]) if data else 0} columns")
        print(f"   Total cells: {sum(len(line) for line in data)}")

        # Count '@' symbols for context
        at_count = sum(line.count("@") for line in data)
        dot_count = sum(line.count(".") for line in data)
        print(f"   '@' symbols: {at_count}")
        print(f"   '.' symbols: {dot_count}")

        # Benchmark Part 1
        part1_stats = None
        if run_part1:
            print("\n🔥 Benchmarking Part 1...")
            part1_stats = benchmark_function(solve_part1, data, args.runs)
            print_benchmark_results("Part 1", part1_stats)

        # Benchmark Part 2
        part2_stats = None
        if run_part2:
            print("\n🔥 Benchmarking Part 2...")
            # Choose which Part 2 function to use
            if args.differential:
                part2_func = solve_part2_differential
                print("   Using differential updates optimization")
            elif args.tracking:
                part2_func = solve_part2_tracking_at_cells
                print("   Using tracking @ cells optimization")
            else:
                part2_func = solve_part2
            part2_stats = benchmark_function(part2_func, data, args.runs)
            print_benchmark_results("Part 2", part2_stats)

        # Overall summary
        if part1_stats and part2_stats:
            total_time = part1_stats["mean_time"] + part2_stats["mean_time"]
            print(f"\n🎯 Overall Performance:")
            print(f"   Combined mean time: {format_time(total_time)}")
            print(
                f"   Part 1 proportion: {(part1_stats['mean_time']/total_time)*100:.1f}%"
            )
            print(
                f"   Part 2 proportion: {(part2_stats['mean_time']/total_time)*100:.1f}%"
            )
        elif part1_stats:
            total_time = part1_stats["mean_time"]
            print(f"\n🎯 Part 1 Only Performance:")
            print(f"   Mean time: {format_time(total_time)}")
        elif part2_stats:
            total_time = part2_stats["mean_time"]
            print(f"\n🎯 Part 2 Only Performance:")
            print(f"   Mean time: {format_time(total_time)}")
        else:
            print(f"\n⚠️ No parts were benchmarked")
            return

        # Performance classification
        if total_time < 0.001:  # < 1ms
            print(f"   🚀 Performance: Excellent")
        elif total_time < 0.01:  # < 10ms
            print(f"   ⚡ Performance: Very Good")
        elif total_time < 0.1:  # < 100ms
            print(f"   ✅ Performance: Good")
        elif total_time < 1.0:  # < 1s
            print(f"   ⚠️ Performance: Acceptable")
        else:
            print(f"   🐌 Performance: Needs Optimization")

        # Suggest optimization if needed
        if part2_stats and part2_stats["mean_time"] > 0.1:  # Part 2 > 100ms
            print(f"\n💡 Optimization Suggestions:")
            print(
                f"   - Part 2 is the bottleneck ({format_time(part2_stats['mean_time'])})"
            )
            print(
                f"   - Consider using mutable data structures instead of string slicing"
            )
            print(f"   - Implement early exit in neighbor counting")
            print(f"   - Track only affected cells between iterations")

        # Output table format if requested
        if args.table:
            print_table_output(part1_stats, part2_stats, args.name)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
