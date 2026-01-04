"""
Comprehensive benchmarking suite for Day 3 solution.

Tests both actual input files and generated test data to analyze:
- Performance characteristics of both part 1 and part 2 algorithms
- Scalability with different input sizes
- Edge case handling
- Data pattern sensitivity

Usage:
    python benchmark_day3.py
    python benchmark_day3.py --detailed
"""

import time
import random
import string
from typing import List, Tuple, Dict, Any
from collections import defaultdict
import statistics
import sys
import os

# Import Day 3 solution functions
sys.path.append(".")
from day3 import parse_input, solve_part1, solve_part2


class Day3Benchmarker:
    def __init__(self):
        self.results = {
            "file_tests": {},
            "generated_tests": {},
            "performance_analysis": {},
            "edge_cases": {},
        }

    def run_comprehensive_benchmark(self, detailed=False):
        """Run complete benchmark suite."""
        print("🚀 Day 3 Comprehensive Benchmarking Suite")
        print("=" * 60)

        # Test actual input files
        self.test_actual_files()

        # Test generated data
        self.test_generated_data()

        # Test edge cases
        self.test_edge_cases()

        # Performance analysis
        self.analyze_performance()

        if detailed:
            self.detailed_analysis()

        # Summary
        self.print_summary()

    def test_actual_files(self):
        """Test with actual Day 3 input files."""
        print("\\n📁 Testing Actual Input Files")
        print("-" * 40)

        files_to_test = [("test_input.txt", "Test Input"), ("input.txt", "Full Input")]

        for filename, description in files_to_test:
            if os.path.exists(filename):
                print(f"\\n🔍 {description} ({filename}):")
                result = self.benchmark_file(filename)
                self.results["file_tests"][filename] = result
                self.print_file_result(result)
            else:
                print(f"❌ {filename} not found")

    def benchmark_file(self, filename: str) -> Dict[str, Any]:
        """Benchmark a single file."""
        try:
            # Parse input
            start_time = time.perf_counter()
            data = parse_input(filename)
            parse_time = time.perf_counter() - start_time

            # Part 1
            start_time = time.perf_counter()
            part1_result = solve_part1(data)
            part1_time = time.perf_counter() - start_time

            # Part 2
            start_time = time.perf_counter()
            part2_result = solve_part2(data)
            part2_time = time.perf_counter() - start_time

            return {
                "lines_count": len(data),
                "total_chars": sum(len(line) for line in data),
                "avg_line_length": statistics.mean(len(line) for line in data),
                "parse_time": parse_time,
                "part1_time": part1_time,
                "part2_time": part2_time,
                "part1_result": part1_result,
                "part2_result": part2_result,
                "total_time": parse_time + part1_time + part2_time,
            }
        except Exception as e:
            return {"error": str(e)}

    def print_file_result(self, result: Dict[str, Any]):
        """Print file benchmark results."""
        if "error" in result:
            print(f"  ❌ Error: {result['error']}")
            return

        print(f"  📊 Lines: {result['lines_count']:,}")
        print(f"  📏 Total chars: {result['total_chars']:,}")
        print(f"  📐 Avg line length: {result['avg_line_length']:.1f}")
        print(f"  ⏱️  Parse time: {result['parse_time']*1000:.3f}ms")
        print(
            f"  🎯 Part 1: {result['part1_result']:,} ({result['part1_time']*1000:.3f}ms)"
        )
        print(
            f"  🎯 Part 2: {result['part2_result']:,} ({result['part2_time']*1000:.3f}ms)"
        )
        print(f"  ⚡ Total time: {result['total_time']*1000:.3f}ms")

    def test_generated_data(self):
        """Test with various generated data patterns."""
        print("\\n🧪 Testing Generated Data Patterns")
        print("-" * 40)

        test_cases = [
            ("small_random", self.generate_random_lines, 10, 20),
            ("medium_random", self.generate_random_lines, 100, 50),
            ("large_random", self.generate_random_lines, 1000, 100),
            ("digit_heavy", self.generate_digit_heavy_lines, 100, 80),
            ("mixed_content", self.generate_mixed_lines, 100, 60),
            ("long_lines", self.generate_long_lines, 50, 200),
            ("short_lines", self.generate_short_lines, 200, 10),
            ("pattern_based", self.generate_pattern_lines, 100, 50),
        ]

        for test_name, generator_func, line_count, line_length in test_cases:
            print(f"\\n🔬 {test_name.replace('_', ' ').title()}:")
            data = generator_func(line_count, line_length)
            result = self.benchmark_generated_data(data, test_name)
            self.results["generated_tests"][test_name] = result
            self.print_generated_result(result)

    def generate_random_lines(self, count: int, length: int) -> List[str]:
        """Generate random alphanumeric lines."""
        lines = []
        for _ in range(count):
            line = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            lines.append(line)
        return lines

    def generate_digit_heavy_lines(self, count: int, length: int) -> List[str]:
        """Generate lines with mostly digits."""
        lines = []
        for _ in range(count):
            # 80% digits, 20% letters
            chars = []
            for _ in range(length):
                if random.random() < 0.8:
                    chars.append(random.choice(string.digits))
                else:
                    chars.append(random.choice(string.ascii_letters))
            lines.append("".join(chars))
        return lines

    def generate_mixed_lines(self, count: int, length: int) -> List[str]:
        """Generate mixed content lines."""
        lines = []
        for _ in range(count):
            # Mix of digits, letters, and some special chars
            chars = []
            for _ in range(length):
                rand = random.random()
                if rand < 0.5:
                    chars.append(random.choice(string.digits))
                elif rand < 0.8:
                    chars.append(random.choice(string.ascii_letters))
                else:
                    chars.append(random.choice(".,;:!?"))
            lines.append("".join(chars))
        return lines

    def generate_long_lines(self, count: int, base_length: int) -> List[str]:
        """Generate very long lines."""
        lines = []
        for _ in range(count):
            length = base_length + random.randint(0, base_length)
            line = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            lines.append(line)
        return lines

    def generate_short_lines(self, count: int, max_length: int) -> List[str]:
        """Generate short lines."""
        lines = []
        for _ in range(count):
            length = random.randint(1, max_length)
            line = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            lines.append(line)
        return lines

    def generate_pattern_lines(self, count: int, length: int) -> List[str]:
        """Generate lines with specific patterns."""
        lines = []
        patterns = [
            lambda: "".join([str(i % 10) for i in range(length)]),  # Sequential
            lambda: "1234567890" * (length // 10)
            + "1234567890"[: length % 10],  # Repeating
            lambda: "9" * length,  # All same digit
            lambda: "".join(
                [str(9 - i % 10) for i in range(length)]
            ),  # Reverse sequential
        ]

        for _ in range(count):
            pattern = random.choice(patterns)
            lines.append(pattern())
        return lines

    def benchmark_generated_data(
        self, data: List[str], test_name: str
    ) -> Dict[str, Any]:
        """Benchmark generated data."""
        try:
            # Measure part 1
            start_time = time.perf_counter()
            part1_result = solve_part1(data)
            part1_time = time.perf_counter() - start_time

            # Measure part 2
            start_time = time.perf_counter()
            part2_result = solve_part2(data)
            part2_time = time.perf_counter() - start_time

            # Calculate statistics
            digit_counts = [sum(1 for c in line if c.isdigit()) for line in data]

            return {
                "test_name": test_name,
                "lines_count": len(data),
                "total_chars": sum(len(line) for line in data),
                "avg_line_length": statistics.mean(len(line) for line in data),
                "digit_density": statistics.mean(digit_counts)
                / statistics.mean(len(line) for line in data),
                "part1_time": part1_time,
                "part2_time": part2_time,
                "part1_result": part1_result,
                "part2_result": part2_result,
                "lines_per_second_p1": len(data) / part1_time if part1_time > 0 else 0,
                "lines_per_second_p2": len(data) / part2_time if part2_time > 0 else 0,
            }
        except Exception as e:
            return {"error": str(e), "test_name": test_name}

    def print_generated_result(self, result: Dict[str, Any]):
        """Print generated data benchmark results."""
        if "error" in result:
            print(f"  ❌ Error: {result['error']}")
            return

        print(f"  📊 Lines: {result['lines_count']:,}")
        print(f"  📏 Avg length: {result['avg_line_length']:.1f}")
        print(f"  🔢 Digit density: {result['digit_density']:.2%}")
        print(
            f"  🎯 Part 1: {result['part1_result']:,} ({result['part1_time']*1000:.3f}ms, {result['lines_per_second_p1']:.0f} lines/s)"
        )
        print(
            f"  🎯 Part 2: {result['part2_result']:,} ({result['part2_time']*1000:.3f}ms, {result['lines_per_second_p2']:.0f} lines/s)"
        )

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        print("\\n🔍 Testing Edge Cases")
        print("-" * 40)

        edge_cases = [
            ("empty_lines", []),
            ("single_char", ["1", "a", "9"]),
            ("no_digits", ["abcdef", "xyz", "hello"]),
            ("all_digits", ["123456", "999999", "000000"]),
            ("single_digit", ["1", "2", "3", "4", "5"]),
            ("very_long", ["1" * 1000 + "2" * 1000]),
            ("mixed_lengths", ["1", "12", "123", "1234", "12345"]),
            ("special_chars", ["1!2@3#", "a$b%c^", "9&8*7("]),
        ]

        for case_name, data in edge_cases:
            print(f"\\n🧩 {case_name.replace('_', ' ').title()}:")
            try:
                result = self.benchmark_generated_data(data, case_name)
                self.results["edge_cases"][case_name] = result

                if "error" not in result:
                    print(f"  ✅ Part 1: {result['part1_result']:,}")
                    print(f"  ✅ Part 2: {result['part2_result']:,}")
                else:
                    print(f"  ❌ {result['error']}")

            except Exception as e:
                print(f"  ❌ Exception: {e}")
                self.results["edge_cases"][case_name] = {"error": str(e)}

    def analyze_performance(self):
        """Analyze performance patterns."""
        print("\\n📈 Performance Analysis")
        print("-" * 40)

        # Collect timing data
        part1_times = []
        part2_times = []
        line_counts = []

        for result in self.results["generated_tests"].values():
            if "error" not in result:
                part1_times.append(result["part1_time"])
                part2_times.append(result["part2_time"])
                line_counts.append(result["lines_count"])

        if part1_times and part2_times:
            analysis = {
                "part1_avg_time": statistics.mean(part1_times),
                "part1_median_time": statistics.median(part1_times),
                "part1_std_time": (
                    statistics.stdev(part1_times) if len(part1_times) > 1 else 0
                ),
                "part2_avg_time": statistics.mean(part2_times),
                "part2_median_time": statistics.median(part2_times),
                "part2_std_time": (
                    statistics.stdev(part2_times) if len(part2_times) > 1 else 0
                ),
                "performance_ratio": statistics.mean(
                    [p2 / p1 for p1, p2 in zip(part1_times, part2_times) if p1 > 0]
                ),
            }

            self.results["performance_analysis"] = analysis

            print(f"\\n⏱️  Part 1 Performance:")
            print(f"  Average: {analysis['part1_avg_time']*1000:.3f}ms")
            print(f"  Median: {analysis['part1_median_time']*1000:.3f}ms")
            print(f"  Std Dev: {analysis['part1_std_time']*1000:.3f}ms")

            print(f"\\n⏱️  Part 2 Performance:")
            print(f"  Average: {analysis['part2_avg_time']*1000:.3f}ms")
            print(f"  Median: {analysis['part2_median_time']*1000:.3f}ms")
            print(f"  Std Dev: {analysis['part2_std_time']*1000:.3f}ms")

            print(f"\\n🔄 Part 2 vs Part 1 Performance:")
            print(f"  Ratio: {analysis['performance_ratio']:.2f}x")

    def detailed_analysis(self):
        """Provide detailed analysis of results."""
        print("\\n🔬 Detailed Analysis")
        print("-" * 40)

        # Digit density vs performance correlation
        print("\\n📊 Digit Density Impact:")
        for test_name, result in self.results["generated_tests"].items():
            if "error" not in result and "digit_density" in result:
                print(
                    f"  {test_name}: {result['digit_density']:.2%} digits → "
                    f"P1: {result['part1_time']*1000:.2f}ms, "
                    f"P2: {result['part2_time']*1000:.2f}ms"
                )

        # Line length impact
        print("\\n📏 Line Length Impact:")
        length_performance = []
        for result in self.results["generated_tests"].values():
            if "error" not in result:
                length_performance.append(
                    (
                        result["avg_line_length"],
                        result["part1_time"],
                        result["part2_time"],
                    )
                )

        length_performance.sort(key=lambda x: x[0])
        for length, p1_time, p2_time in length_performance:
            print(
                f"  Avg length {length:.0f}: P1 {p1_time*1000:.2f}ms, P2 {p2_time*1000:.2f}ms"
            )

    def print_summary(self):
        """Print benchmark summary."""
        print("\\n" + "=" * 60)
        print("📋 BENCHMARK SUMMARY")
        print("=" * 60)

        # File test summary
        if self.results["file_tests"]:
            print("\\n📁 Actual Files:")
            for filename, result in self.results["file_tests"].items():
                if "error" not in result:
                    print(
                        f"  {filename}: {result['lines_count']:,} lines, "
                        f"{result['total_time']*1000:.1f}ms total"
                    )

        # Generated test summary
        if self.results["generated_tests"]:
            print("\\n🧪 Generated Data Tests:")
            fastest_p1 = min(
                (
                    r
                    for r in self.results["generated_tests"].values()
                    if "error" not in r
                ),
                key=lambda x: x["part1_time"],
            )
            fastest_p2 = min(
                (
                    r
                    for r in self.results["generated_tests"].values()
                    if "error" not in r
                ),
                key=lambda x: x["part2_time"],
            )

            print(
                f"  Fastest Part 1: {fastest_p1['test_name']} ({fastest_p1['part1_time']*1000:.2f}ms)"
            )
            print(
                f"  Fastest Part 2: {fastest_p2['test_name']} ({fastest_p2['part2_time']*1000:.2f}ms)"
            )

        # Edge cases summary
        edge_success = sum(
            1 for r in self.results["edge_cases"].values() if "error" not in r
        )
        edge_total = len(self.results["edge_cases"])
        print(f"\\n🔍 Edge Cases: {edge_success}/{edge_total} passed")

        print("\\n✅ Benchmark Complete!")


def main():
    """Main entry point."""
    detailed = "--detailed" in sys.argv or "-d" in sys.argv

    benchmarker = Day3Benchmarker()
    benchmarker.run_comprehensive_benchmark(detailed=detailed)


if __name__ == "__main__":
    main()
