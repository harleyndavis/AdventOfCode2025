#!/usr/bin/env python3
"""
Quick setup and utility scripts for Advent of Code

Usage:
    python setup.py day <num>        # Create new day template
    python setup.py test <num>       # Run tests for specific day
    python setup.py benchmark <num>  # Run benchmarks for specific day
    python setup.py all-tests        # Run all tests
"""

import os
import sys
import subprocess
from pathlib import Path


def create_day(day_num: int) -> None:
    """Create a new day using the template generator."""
    subprocess.run([sys.executable, "create_day.py", str(day_num)])


def run_day_tests(day_num: int) -> None:
    """Run tests for a specific day."""
    day_folder = Path(f"Day{day_num}")
    if not day_folder.exists():
        print(f"❌ Day{day_num} folder not found")
        return

    test_file = day_folder / f"test_day{day_num}.py"
    if not test_file.exists():
        print(f"❌ Test file for Day{day_num} not found")
        return

    print(f"🧪 Running tests for Day {day_num}...")
    os.chdir(day_folder)
    result = subprocess.run([sys.executable, f"test_day{day_num}.py"])
    os.chdir("..")

    if result.returncode == 0:
        print(f"✅ Day {day_num} tests passed!")
    else:
        print(f"❌ Day {day_num} tests failed")


def run_day_benchmark(day_num: int) -> None:
    """Run benchmark for a specific day."""
    day_folder = Path(f"Day{day_num}")
    if not day_folder.exists():
        print(f"❌ Day{day_num} folder not found")
        return

    benchmark_file = day_folder / "benchmark.py"
    if not benchmark_file.exists():
        print(f"❌ Benchmark file for Day{day_num} not found")
        return

    print(f"📊 Running benchmark for Day {day_num}...")
    os.chdir(day_folder)
    subprocess.run([sys.executable, "benchmark.py"])
    os.chdir("..")


def run_all_tests() -> None:
    """Run tests for all available days."""
    day_folders = [
        f for f in Path(".").iterdir() if f.is_dir() and f.name.startswith("Day")
    ]
    day_folders.sort(key=lambda x: int(x.name[3:]))

    if not day_folders:
        print("❌ No day folders found")
        return

    print("🧪 Running all tests...")
    print("=" * 50)

    results = {}

    for day_folder in day_folders:
        day_num = int(day_folder.name[3:])
        test_file = day_folder / f"test_day{day_num}.py"

        if test_file.exists():
            print(f"\\n📁 Day {day_num}:")
            os.chdir(day_folder)
            result = subprocess.run(
                [sys.executable, f"test_day{day_num}.py"],
                capture_output=True,
                text=True,
            )
            os.chdir("..")

            if result.returncode == 0:
                results[day_num] = "✅ PASSED"
                print(f"   ✅ Tests passed")
            else:
                results[day_num] = "❌ FAILED"
                print(f"   ❌ Tests failed")
        else:
            results[day_num] = "⚠️  NO TESTS"
            print(f"\\n📁 Day {day_num}: ⚠️  No test file found")

    # Summary
    print("\\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for status in results.values() if "PASSED" in status)
    total = len(results)

    for day_num in sorted(results.keys()):
        print(f"Day {day_num:2d}: {results[day_num]}")

    print("=" * 50)
    print(f"📈 Overall: {passed}/{total} days with passing tests")


def run_solution(day_num: int, input_file: str = None) -> None:
    """Run the solution for a specific day."""
    day_folder = Path(f"Day{day_num}")
    if not day_folder.exists():
        print(f"❌ Day{day_num} folder not found")
        return

    solution_file = day_folder / f"day{day_num}.py"
    if not solution_file.exists():
        print(f"❌ Solution file for Day{day_num} not found")
        return

    print(f"🚀 Running Day {day_num} solution...")

    cmd = [sys.executable, f"Day{day_num}/day{day_num}.py"]
    if input_file:
        cmd.append(input_file)

    subprocess.run(cmd)


def show_help() -> None:
    """Show help information."""
    print(
        """
🎄 Advent of Code Setup Utility
================================

Commands:
  day <num>           Create new day template
  test <num>          Run tests for specific day  
  benchmark <num>     Run benchmark for specific day
  run <num> [file]    Run solution for specific day
  all-tests           Run tests for all days
  help                Show this help

Examples:
  python setup.py day 3                    # Create Day 3 template
  python setup.py test 1                   # Run Day 1 tests
  python setup.py run 2                    # Run Day 2 with default input
  python setup.py run 2 custom_input.txt   # Run Day 2 with custom input
  python setup.py benchmark 1              # Run Day 1 benchmark
  python setup.py all-tests                # Run all available tests
"""
    )


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "day":
        if len(sys.argv) < 3:
            print("❌ Usage: python setup.py day <number>")
            return
        try:
            day_num = int(sys.argv[2])
            create_day(day_num)
        except ValueError:
            print("❌ Day number must be an integer")

    elif command == "test":
        if len(sys.argv) < 3:
            print("❌ Usage: python setup.py test <number>")
            return
        try:
            day_num = int(sys.argv[2])
            run_day_tests(day_num)
        except ValueError:
            print("❌ Day number must be an integer")

    elif command == "benchmark":
        if len(sys.argv) < 3:
            print("❌ Usage: python setup.py benchmark <number>")
            return
        try:
            day_num = int(sys.argv[2])
            run_day_benchmark(day_num)
        except ValueError:
            print("❌ Day number must be an integer")

    elif command == "run":
        if len(sys.argv) < 3:
            print("❌ Usage: python setup.py run <number> [input_file]")
            return
        try:
            day_num = int(sys.argv[2])
            input_file = sys.argv[3] if len(sys.argv) > 3 else None
            run_solution(day_num, input_file)
        except ValueError:
            print("❌ Day number must be an integer")

    elif command == "all-tests":
        run_all_tests()

    elif command in ["help", "-h", "--help"]:
        show_help()

    else:
        print(f"❌ Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()
