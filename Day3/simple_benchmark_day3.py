"""
Performance benchmarking for Day 3 solution - simplified version.

Analyzes performance characteristics without external dependencies.
Includes both actual input files and generated test data.

Usage:
    python simple_benchmark_day3.py
    python simple_benchmark_day3.py --detailed
"""

import time
import random
import string
import sys
import statistics
from typing import List, Tuple, Dict, Any

# Import Day 3 solution functions
sys.path.append(".")
from day3 import parse_input, solve_part1, solve_part2


class Day3SimpleBenchmark:
    def __init__(self):
        self.results = {
            "file_tests": {},
            "scalability_tests": [],
            "pattern_tests": {},
            "performance_summary": {},
        }

    def run_benchmark(self, detailed=False):
        """Run comprehensive performance benchmark."""
        print("⚡ Day 3 Performance Benchmark")
        print("=" * 45)

        # Test actual files
        self.test_actual_files()

        # Scalability testing
        self.test_scalability()

        # Pattern-based testing
        self.test_data_patterns()

        if detailed:
            self.detailed_analysis()

        # Summary
        self.print_summary()

    def test_actual_files(self):
        """Test performance on actual input files."""
        print("\\n📁 Actual Input Files Performance")
        print("-" * 35)

        files = [("test_input.txt", "Test Input"), ("input.txt", "Full Input")]

        for filename, description in files:
            try:
                print(f"\\n🔍 {description}:")
                data = parse_input(filename)
                result = self.benchmark_data(data, filename)
                self.results["file_tests"][filename] = result
                self.print_benchmark_result(result)

            except FileNotFoundError:
                print(f"  ❌ {filename} not found")
            except Exception as e:
                print(f"  ❌ Error: {e}")

    def test_scalability(self):
        """Test performance scalability with increasing data sizes."""
        print("\\n📊 Scalability Testing")
        print("-" * 25)

        # Test different data sizes
        test_configs = [
            (50, 50, "Small"),
            (100, 100, "Medium"),
            (500, 100, "Large Lines"),
            (200, 200, "Long Lines"),
            (1000, 50, "Many Short"),
            (100, 500, "Few Long"),
        ]

        for line_count, line_length, description in test_configs:
            print(f"\\n🧪 {description} ({line_count} lines × {line_length} chars):")

            # Generate test data with guaranteed digits
            test_data = self.generate_robust_test_data(line_count, line_length)

            result = self.benchmark_data(
                test_data, f"generated_{description.lower().replace(' ', '_')}"
            )
            result.update(
                {
                    "line_count": line_count,
                    "line_length": line_length,
                    "description": description,
                }
            )

            self.results["scalability_tests"].append(result)
            self.print_benchmark_result(result)

    def generate_robust_test_data(self, line_count: int, line_length: int) -> List[str]:
        """Generate test data that's guaranteed to work with the algorithm."""
        lines = []

        for _ in range(line_count):
            line_chars = []

            # Ensure we have enough digits (at least 2 per line)
            digit_positions = random.sample(
                range(line_length), min(line_length, max(2, line_length // 3))
            )

            # Fill line with letters first
            for i in range(line_length):
                if i in digit_positions:
                    line_chars.append(random.choice(string.digits))
                else:
                    line_chars.append(random.choice(string.ascii_letters))

            lines.append("".join(line_chars))

        return lines

    def test_data_patterns(self):
        """Test performance with different data patterns."""
        print("\\n🎨 Data Pattern Analysis")
        print("-" * 28)

        patterns = {
            "digit_heavy": lambda: self.generate_digit_heavy_data(200, 100),
            "digit_sparse": lambda: self.generate_digit_sparse_data(200, 100),
            "alternating": lambda: self.generate_alternating_data(200, 100),
            "clustered_digits": lambda: self.generate_clustered_data(200, 100),
            "sequential_digits": lambda: self.generate_sequential_data(200, 100),
        }

        for pattern_name, generator in patterns.items():
            print(f"\\n🔬 {pattern_name.replace('_', ' ').title()}:")

            try:
                test_data = generator()
                result = self.benchmark_data(test_data, pattern_name)
                result["pattern_type"] = pattern_name

                self.results["pattern_tests"][pattern_name] = result
                self.print_benchmark_result(result)

            except Exception as e:
                print(f"  ❌ Error with {pattern_name}: {e}")

    def generate_digit_heavy_data(self, lines: int, length: int) -> List[str]:
        """Generate data with high digit density."""
        result = []
        for _ in range(lines):
            chars = []
            for _ in range(length):
                if random.random() < 0.7:  # 70% digits
                    chars.append(random.choice(string.digits))
                else:
                    chars.append(random.choice(string.ascii_letters))
            result.append("".join(chars))
        return result

    def generate_digit_sparse_data(self, lines: int, length: int) -> List[str]:
        """Generate data with low digit density."""
        result = []
        for _ in range(lines):
            chars = []
            digit_count = 0
            for _ in range(length):
                if digit_count < 2 or (
                    random.random() < 0.2 and digit_count < length // 4
                ):  # At least 2 digits, max 25%
                    chars.append(random.choice(string.digits))
                    digit_count += 1
                else:
                    chars.append(random.choice(string.ascii_letters))
            random.shuffle(chars)  # Mix positions
            result.append("".join(chars))
        return result

    def generate_alternating_data(self, lines: int, length: int) -> List[str]:
        """Generate data with alternating digit/letter pattern."""
        result = []
        for _ in range(lines):
            chars = []
            for i in range(length):
                if i % 2 == 0:
                    chars.append(random.choice(string.digits))
                else:
                    chars.append(random.choice(string.ascii_letters))
            result.append("".join(chars))
        return result

    def generate_clustered_data(self, lines: int, length: int) -> List[str]:
        """Generate data with clustered digits."""
        result = []
        for _ in range(lines):
            chars = ["a"] * length  # Fill with letters

            # Add digit clusters
            cluster_count = random.randint(2, 4)
            for _ in range(cluster_count):
                cluster_size = random.randint(2, 6)
                start_pos = random.randint(0, max(0, length - cluster_size))

                for i in range(cluster_size):
                    if start_pos + i < length:
                        chars[start_pos + i] = random.choice(string.digits)

            result.append("".join(chars))
        return result

    def generate_sequential_data(self, lines: int, length: int) -> List[str]:
        """Generate data with sequential digit patterns."""
        result = []
        for _ in range(lines):
            chars = []
            for i in range(length):
                if i < length // 2:
                    chars.append(str((i % 10)))  # Sequential digits
                else:
                    chars.append(random.choice(string.ascii_letters))
            result.append("".join(chars))
        return result

    def benchmark_data(self, data: List[str], data_name: str) -> Dict[str, Any]:
        """Benchmark the solution on given data."""
        try:
            # Calculate data characteristics
            total_chars = sum(len(line) for line in data)
            digit_counts = []
            for line in data:
                digit_count = sum(1 for c in line if c.isdigit())
                digit_counts.append(digit_count)

            avg_digits_per_line = statistics.mean(digit_counts) if digit_counts else 0
            digit_density = (
                avg_digits_per_line / (total_chars / len(data)) if data else 0
            )

            # Benchmark Part 1
            start_time = time.perf_counter()
            part1_result = solve_part1(data)
            part1_time = time.perf_counter() - start_time

            # Benchmark Part 2
            start_time = time.perf_counter()
            part2_result = solve_part2(data)
            part2_time = time.perf_counter() - start_time

            return {
                "data_name": data_name,
                "line_count": len(data),
                "total_chars": total_chars,
                "avg_line_length": total_chars / len(data) if data else 0,
                "digit_density": digit_density,
                "avg_digits_per_line": avg_digits_per_line,
                "part1_time": part1_time,
                "part2_time": part2_time,
                "part1_result": part1_result,
                "part2_result": part2_result,
                "lines_per_second_p1": len(data) / part1_time if part1_time > 0 else 0,
                "lines_per_second_p2": len(data) / part2_time if part2_time > 0 else 0,
                "chars_per_second_p1": (
                    total_chars / part1_time if part1_time > 0 else 0
                ),
                "chars_per_second_p2": (
                    total_chars / part2_time if part2_time > 0 else 0
                ),
                "performance_ratio": part2_time / part1_time if part1_time > 0 else 0,
            }

        except Exception as e:
            return {"data_name": data_name, "error": str(e)}

    def print_benchmark_result(self, result: Dict[str, Any]):
        """Print benchmark results in a formatted way."""
        if "error" in result:
            print(f"  ❌ Error: {result['error']}")
            return

        print(f"  📊 {result['line_count']:,} lines, {result['total_chars']:,} chars")
        print(
            f"  🔢 {result['digit_density']:.1%} digit density, {result['avg_digits_per_line']:.1f} digits/line"
        )
        print(
            f"  🎯 Part 1: {result['part1_result']:,} ({result['part1_time']*1000:.2f}ms)"
        )
        print(
            f"  🎯 Part 2: {result['part2_result']:,} ({result['part2_time']*1000:.2f}ms)"
        )
        print(
            f"  ⚡ Throughput: {result['lines_per_second_p1']:.0f}/{result['lines_per_second_p2']:.0f} lines/s (P1/P2)"
        )
        print(f"  📈 P2/P1 ratio: {result['performance_ratio']:.2f}x")

    def detailed_analysis(self):
        """Provide detailed performance analysis."""
        print("\\n🔬 Detailed Performance Analysis")
        print("-" * 35)

        # Collect all successful results
        all_results = []

        for result in self.results["file_tests"].values():
            if "error" not in result:
                all_results.append(result)

        for result in self.results["scalability_tests"]:
            if "error" not in result:
                all_results.append(result)

        for result in self.results["pattern_tests"].values():
            if "error" not in result:
                all_results.append(result)

        if not all_results:
            print("  ⚠️  No successful results for analysis")
            return

        # Performance statistics
        part1_times = [r["part1_time"] for r in all_results]
        part2_times = [r["part2_time"] for r in all_results]
        ratios = [r["performance_ratio"] for r in all_results]

        print("\\n⏱️  Performance Statistics:")
        print(
            f"  Part 1 - Avg: {statistics.mean(part1_times)*1000:.2f}ms, "
            f"Min: {min(part1_times)*1000:.2f}ms, Max: {max(part1_times)*1000:.2f}ms"
        )
        print(
            f"  Part 2 - Avg: {statistics.mean(part2_times)*1000:.2f}ms, "
            f"Min: {min(part2_times)*1000:.2f}ms, Max: {max(part2_times)*1000:.2f}ms"
        )
        print(
            f"  P2/P1 Ratio - Avg: {statistics.mean(ratios):.2f}x, "
            f"Min: {min(ratios):.2f}x, Max: {max(ratios):.2f}x"
        )

        # Digit density correlation
        print("\\n🔢 Digit Density vs Performance:")
        density_performance = [
            (r["digit_density"], r["part1_time"], r["part2_time"])
            for r in all_results
            if "digit_density" in r
        ]
        density_performance.sort(key=lambda x: x[0])

        for density, p1_time, p2_time in density_performance:
            print(
                f"  {density:.1%} digits → P1: {p1_time*1000:.2f}ms, P2: {p2_time*1000:.2f}ms"
            )

        # Line length correlation
        print("\\n📏 Line Length vs Performance:")
        length_performance = [
            (r["avg_line_length"], r["part1_time"], r["part2_time"])
            for r in all_results
            if "avg_line_length" in r
        ]
        length_performance.sort(key=lambda x: x[0])

        for length, p1_time, p2_time in length_performance:
            print(
                f"  {length:.0f} chars → P1: {p1_time*1000:.2f}ms, P2: {p2_time*1000:.2f}ms"
            )

    def print_summary(self):
        """Print performance summary."""
        print("\\n" + "=" * 45)
        print("📋 PERFORMANCE SUMMARY")
        print("=" * 45)

        # Best performers
        all_valid = []

        for source, results in [
            ("File Tests", self.results["file_tests"].values()),
            ("Scalability", self.results["scalability_tests"]),
            ("Patterns", self.results["pattern_tests"].values()),
        ]:
            for result in results:
                if "error" not in result:
                    result["source"] = source
                    all_valid.append(result)

        if all_valid:
            # Fastest by throughput (lines per second)
            fastest_p1 = max(all_valid, key=lambda x: x["lines_per_second_p1"])
            fastest_p2 = max(all_valid, key=lambda x: x["lines_per_second_p2"])

            print(f"\\n🏆 Best Throughput:")
            print(
                f"  Part 1: {fastest_p1['data_name']} ({fastest_p1['lines_per_second_p1']:.0f} lines/s)"
            )
            print(
                f"  Part 2: {fastest_p2['data_name']} ({fastest_p2['lines_per_second_p2']:.0f} lines/s)"
            )

            # Most efficient (best P2/P1 ratio)
            most_efficient = min(all_valid, key=lambda x: x["performance_ratio"])
            least_efficient = max(all_valid, key=lambda x: x["performance_ratio"])

            print(f"\\n⚖️  Efficiency Range:")
            print(
                f"  Best: {most_efficient['data_name']} ({most_efficient['performance_ratio']:.2f}x)"
            )
            print(
                f"  Worst: {least_efficient['data_name']} ({least_efficient['performance_ratio']:.2f}x)"
            )

            # Overall statistics
            total_tests = len(all_valid)
            avg_p1_throughput = statistics.mean(
                [r["lines_per_second_p1"] for r in all_valid]
            )
            avg_p2_throughput = statistics.mean(
                [r["lines_per_second_p2"] for r in all_valid]
            )

            print(f"\\n📊 Overall Statistics:")
            print(f"  Tests completed: {total_tests}")
            print(f"  Avg throughput P1: {avg_p1_throughput:.0f} lines/s")
            print(f"  Avg throughput P2: {avg_p2_throughput:.0f} lines/s")

        print("\\n✅ Benchmark Complete!")


def main():
    """Main entry point."""
    detailed = "--detailed" in sys.argv or "-d" in sys.argv

    benchmark = Day3SimpleBenchmark()
    benchmark.run_benchmark(detailed=detailed)


if __name__ == "__main__":
    main()
