"""
Stress testing and performance analysis for Day 3 solution.

Focuses on:
- Large dataset performance
- Memory usage patterns
- Algorithm complexity analysis
- Real vs synthetic data comparison
- Scalability testing

Usage:
    python stress_test_day3.py
    python stress_test_day3.py --extreme
"""

import time
import random
import string
import sys
import psutil
import os
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Import Day 3 solution functions
sys.path.append(".")
from day3 import parse_input, solve_part1, solve_part2


class Day3StressTester:
    def __init__(self):
        self.process = psutil.Process()
        self.results = {
            "scalability": [],
            "memory_usage": [],
            "algorithm_analysis": {},
            "real_vs_synthetic": {},
        }

    def run_stress_tests(self, extreme_mode=False):
        """Run comprehensive stress tests."""
        print("🔥 Day 3 Stress Testing Suite")
        print("=" * 50)

        # Scalability testing
        self.test_scalability(extreme_mode)

        # Memory usage analysis
        self.analyze_memory_usage()

        # Algorithm complexity
        self.analyze_algorithm_complexity()

        # Real vs synthetic comparison
        self.compare_real_vs_synthetic()

        # Generate performance charts
        self.generate_charts()

        print("\\n✅ Stress testing complete!")

    def test_scalability(self, extreme_mode=False):
        """Test algorithm scalability with increasing data sizes."""
        print("\\n📊 Scalability Analysis")
        print("-" * 30)

        if extreme_mode:
            line_counts = [10, 50, 100, 500, 1000, 5000, 10000, 25000]
            line_lengths = [50, 100, 200, 500, 1000]
        else:
            line_counts = [10, 50, 100, 500, 1000, 2000]
            line_lengths = [50, 100, 200]

        for line_count in line_counts:
            for line_length in line_lengths:
                print(f"\\n🧪 Testing {line_count:,} lines × {line_length} chars")

                # Generate test data with guaranteed digits
                test_data = self.generate_scalability_data(line_count, line_length)

                # Measure performance and memory
                result = self.measure_performance_and_memory(test_data)
                result.update(
                    {
                        "line_count": line_count,
                        "line_length": line_length,
                        "total_chars": line_count * line_length,
                    }
                )

                self.results["scalability"].append(result)
                self.print_scalability_result(result)

    def generate_scalability_data(self, line_count: int, line_length: int) -> List[str]:
        """Generate data optimized for scalability testing."""
        lines = []
        for _ in range(line_count):
            # Ensure each line has digits (60% digits, 40% letters)
            line_chars = []
            digit_count = max(1, int(line_length * 0.6))  # At least 1 digit

            # Add digits
            for _ in range(digit_count):
                line_chars.append(random.choice(string.digits))

            # Add letters for remaining positions
            for _ in range(line_length - digit_count):
                line_chars.append(random.choice(string.ascii_letters))

            # Shuffle to distribute digits throughout line
            random.shuffle(line_chars)
            lines.append("".join(line_chars))

        return lines

    def measure_performance_and_memory(self, data: List[str]) -> Dict[str, Any]:
        """Measure both performance and memory usage."""
        # Initial memory
        initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB

        # Part 1 timing and memory
        start_time = time.perf_counter()
        start_memory = self.process.memory_info().rss / 1024 / 1024

        try:
            part1_result = solve_part1(data)
            part1_time = time.perf_counter() - start_time
            part1_memory = self.process.memory_info().rss / 1024 / 1024 - start_memory
        except Exception as e:
            return {"error": f"Part 1 error: {e}"}

        # Part 2 timing and memory
        start_time = time.perf_counter()
        start_memory = self.process.memory_info().rss / 1024 / 1024

        try:
            part2_result = solve_part2(data)
            part2_time = time.perf_counter() - start_time
            part2_memory = self.process.memory_info().rss / 1024 / 1024 - start_memory
        except Exception as e:
            return {"error": f"Part 2 error: {e}"}

        return {
            "part1_time": part1_time,
            "part2_time": part2_time,
            "part1_memory": part1_memory,
            "part2_memory": part2_memory,
            "part1_result": part1_result,
            "part2_result": part2_result,
            "lines_per_sec_p1": len(data) / part1_time if part1_time > 0 else 0,
            "lines_per_sec_p2": len(data) / part2_time if part2_time > 0 else 0,
            "chars_per_sec_p1": (
                sum(len(line) for line in data) / part1_time if part1_time > 0 else 0
            ),
            "chars_per_sec_p2": (
                sum(len(line) for line in data) / part2_time if part2_time > 0 else 0
            ),
        }

    def print_scalability_result(self, result: Dict[str, Any]):
        """Print scalability test results."""
        if "error" in result:
            print(f"  ❌ {result['error']}")
            return

        print(
            f"  ⏱️  Part 1: {result['part1_time']*1000:.2f}ms "
            f"({result['lines_per_sec_p1']:.0f} lines/s, {result['chars_per_sec_p1']:.0f} chars/s)"
        )
        print(
            f"  ⏱️  Part 2: {result['part2_time']*1000:.2f}ms "
            f"({result['lines_per_sec_p2']:.0f} lines/s, {result['chars_per_sec_p2']:.0f} chars/s)"
        )
        print(
            f"  🧠 Memory: P1 {result['part1_memory']:.2f}MB, P2 {result['part2_memory']:.2f}MB"
        )

    def analyze_memory_usage(self):
        """Analyze memory usage patterns."""
        print("\\n🧠 Memory Usage Analysis")
        print("-" * 30)

        # Test memory growth with data size
        sizes = [100, 500, 1000, 2000, 5000]
        memory_results = []

        for size in sizes:
            data = self.generate_scalability_data(size, 100)

            # Monitor memory during execution
            baseline_memory = self.process.memory_info().rss / 1024 / 1024

            solve_part1(data)
            p1_memory = self.process.memory_info().rss / 1024 / 1024

            solve_part2(data)
            p2_memory = self.process.memory_info().rss / 1024 / 1024

            memory_results.append(
                {
                    "size": size,
                    "baseline": baseline_memory,
                    "after_p1": p1_memory,
                    "after_p2": p2_memory,
                    "p1_growth": p1_memory - baseline_memory,
                    "p2_growth": p2_memory - baseline_memory,
                }
            )

        # Print memory analysis
        for result in memory_results:
            print(
                f"  📏 {result['size']:,} lines: "
                f"P1 +{result['p1_growth']:.2f}MB, P2 +{result['p2_growth']:.2f}MB"
            )

        self.results["memory_usage"] = memory_results

    def analyze_algorithm_complexity(self):
        """Analyze algorithmic complexity characteristics."""
        print("\\n⚡ Algorithm Complexity Analysis")
        print("-" * 40)

        # Test with different line lengths (character processing complexity)
        print("\\n🔤 Character Processing Complexity:")
        lengths = [10, 25, 50, 100, 200, 500]
        complexity_results = []

        for length in lengths:
            data = self.generate_scalability_data(100, length)  # Fixed 100 lines
            result = self.measure_performance_and_memory(data)

            if "error" not in result:
                complexity_results.append(
                    {
                        "length": length,
                        "part1_time": result["part1_time"],
                        "part2_time": result["part2_time"],
                        "time_per_char_p1": result["part1_time"] / (100 * length),
                        "time_per_char_p2": result["part2_time"] / (100 * length),
                    }
                )

                print(
                    f"  Length {length:3d}: "
                    f"P1 {result['part1_time']*1000:.2f}ms, "
                    f"P2 {result['part2_time']*1000:.2f}ms "
                    f"({result['part1_time']/(100*length)*1000000:.2f}μs/char P1, "
                    f"{result['part2_time']/(100*length)*1000000:.2f}μs/char P2)"
                )

        # Test with different line counts (data processing complexity)
        print("\\n📊 Data Volume Complexity:")
        counts = [50, 100, 200, 500, 1000, 2000]

        for count in counts:
            data = self.generate_scalability_data(
                count, 100
            )  # Fixed 100 chars per line
            result = self.measure_performance_and_memory(data)

            if "error" not in result:
                print(
                    f"  Lines {count:4d}: "
                    f"P1 {result['part1_time']*1000:.2f}ms, "
                    f"P2 {result['part2_time']*1000:.2f}ms "
                    f"({result['part1_time']/count*1000:.3f}ms/line P1, "
                    f"{result['part2_time']/count*1000:.3f}ms/line P2)"
                )

        self.results["algorithm_analysis"] = {
            "char_complexity": complexity_results,
            "scaling_factor": self.calculate_scaling_factor(),
        }

    def calculate_scaling_factor(self) -> Dict[str, float]:
        """Calculate how performance scales with data size."""
        if len(self.results["scalability"]) < 2:
            return {}

        # Find matching line lengths to compare counts
        scaling = {"part1": [], "part2": []}

        for length in [50, 100, 200]:
            length_results = [
                r
                for r in self.results["scalability"]
                if r.get("line_length") == length and "error" not in r
            ]

            if len(length_results) >= 2:
                # Calculate scaling between smallest and largest
                smallest = min(length_results, key=lambda x: x["line_count"])
                largest = max(length_results, key=lambda x: x["line_count"])

                size_ratio = largest["line_count"] / smallest["line_count"]
                time_ratio_p1 = largest["part1_time"] / smallest["part1_time"]
                time_ratio_p2 = largest["part2_time"] / smallest["part2_time"]

                scaling["part1"].append(time_ratio_p1 / size_ratio)
                scaling["part2"].append(time_ratio_p2 / size_ratio)

        return {
            "part1_scaling": np.mean(scaling["part1"]) if scaling["part1"] else 0,
            "part2_scaling": np.mean(scaling["part2"]) if scaling["part2"] else 0,
        }

    def compare_real_vs_synthetic(self):
        """Compare performance on real vs synthetic data."""
        print("\\n🎯 Real vs Synthetic Data Comparison")
        print("-" * 40)

        # Test real data
        try:
            real_data = parse_input("input.txt")
            real_result = self.measure_performance_and_memory(real_data)
            real_result["data_type"] = "Real AoC Input"

            print("\\n📄 Real Input Performance:")
            if "error" not in real_result:
                print(f"  Lines: {len(real_data):,}")
                print(
                    f"  Part 1: {real_result['part1_time']*1000:.2f}ms ({real_result['lines_per_sec_p1']:.0f} lines/s)"
                )
                print(
                    f"  Part 2: {real_result['part2_time']*1000:.2f}ms ({real_result['lines_per_sec_p2']:.0f} lines/s)"
                )

        except Exception as e:
            real_result = {"error": f"Real data error: {e}"}
            print(f"  ❌ Real data test failed: {e}")

        # Test synthetic data with same characteristics
        if "error" not in real_result:
            synthetic_data = self.generate_scalability_data(len(real_data), 100)
            synthetic_result = self.measure_performance_and_memory(synthetic_data)
            synthetic_result["data_type"] = "Synthetic Data"

            print("\\n🧪 Synthetic Data Performance:")
            if "error" not in synthetic_result:
                print(f"  Lines: {len(synthetic_data):,}")
                print(
                    f"  Part 1: {synthetic_result['part1_time']*1000:.2f}ms ({synthetic_result['lines_per_sec_p1']:.0f} lines/s)"
                )
                print(
                    f"  Part 2: {synthetic_result['part2_time']*1000:.2f}ms ({synthetic_result['lines_per_sec_p2']:.0f} lines/s)"
                )

                # Comparison
                print("\\n📊 Real vs Synthetic Comparison:")
                p1_ratio = real_result["part1_time"] / synthetic_result["part1_time"]
                p2_ratio = real_result["part2_time"] / synthetic_result["part2_time"]
                print(f"  Part 1 ratio (real/synthetic): {p1_ratio:.2f}x")
                print(f"  Part 2 ratio (real/synthetic): {p2_ratio:.2f}x")

            self.results["real_vs_synthetic"] = {
                "real": real_result,
                "synthetic": synthetic_result,
            }

    def generate_charts(self):
        """Generate performance visualization charts."""
        print("\\n📈 Generating Performance Charts")
        print("-" * 35)

        if not self.results["scalability"]:
            print("  ⚠️  No scalability data available for charts")
            return

        try:
            # Prepare data for plotting
            valid_results = [r for r in self.results["scalability"] if "error" not in r]

            if len(valid_results) < 2:
                print("  ⚠️  Insufficient data for meaningful charts")
                return

            # Extract data for plotting
            line_counts = [r["line_count"] for r in valid_results]
            part1_times = [
                r["part1_time"] * 1000 for r in valid_results
            ]  # Convert to ms
            part2_times = [r["part2_time"] * 1000 for r in valid_results]

            # Create performance chart
            plt.figure(figsize=(12, 8))

            # Subplot 1: Performance vs Line Count
            plt.subplot(2, 2, 1)
            plt.scatter(
                line_counts, part1_times, alpha=0.7, label="Part 1", color="blue"
            )
            plt.scatter(
                line_counts, part2_times, alpha=0.7, label="Part 2", color="red"
            )
            plt.xlabel("Number of Lines")
            plt.ylabel("Processing Time (ms)")
            plt.title("Performance vs Data Size")
            plt.legend()
            plt.grid(True, alpha=0.3)

            # Subplot 2: Lines per Second
            lines_per_sec_p1 = [r["lines_per_sec_p1"] for r in valid_results]
            lines_per_sec_p2 = [r["lines_per_sec_p2"] for r in valid_results]

            plt.subplot(2, 2, 2)
            plt.scatter(
                line_counts, lines_per_sec_p1, alpha=0.7, label="Part 1", color="blue"
            )
            plt.scatter(
                line_counts, lines_per_sec_p2, alpha=0.7, label="Part 2", color="red"
            )
            plt.xlabel("Number of Lines")
            plt.ylabel("Lines per Second")
            plt.title("Throughput Analysis")
            plt.legend()
            plt.grid(True, alpha=0.3)

            # Subplot 3: Memory Usage
            if self.results["memory_usage"]:
                mem_sizes = [r["size"] for r in self.results["memory_usage"]]
                mem_p1 = [r["p1_growth"] for r in self.results["memory_usage"]]
                mem_p2 = [r["p2_growth"] for r in self.results["memory_usage"]]

                plt.subplot(2, 2, 3)
                plt.plot(mem_sizes, mem_p1, "bo-", label="Part 1", alpha=0.7)
                plt.plot(mem_sizes, mem_p2, "ro-", label="Part 2", alpha=0.7)
                plt.xlabel("Number of Lines")
                plt.ylabel("Memory Growth (MB)")
                plt.title("Memory Usage Pattern")
                plt.legend()
                plt.grid(True, alpha=0.3)

            # Subplot 4: Performance Ratio
            performance_ratios = [
                r["part2_time"] / r["part1_time"] for r in valid_results
            ]

            plt.subplot(2, 2, 4)
            plt.scatter(line_counts, performance_ratios, alpha=0.7, color="green")
            plt.xlabel("Number of Lines")
            plt.ylabel("Part 2 / Part 1 Time Ratio")
            plt.title("Algorithm Complexity Comparison")
            plt.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig("day3_performance_analysis.png", dpi=300, bbox_inches="tight")
            plt.close()

            print("  ✅ Charts saved as 'day3_performance_analysis.png'")

        except ImportError:
            print("  ⚠️  matplotlib not available - skipping chart generation")
        except Exception as e:
            print(f"  ❌ Chart generation failed: {e}")


def main():
    """Main entry point."""
    extreme_mode = "--extreme" in sys.argv or "-x" in sys.argv

    tester = Day3StressTester()
    tester.run_stress_tests(extreme_mode=extreme_mode)


if __name__ == "__main__":
    main()
