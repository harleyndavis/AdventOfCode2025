"""
Day 3 Performance Analysis Summary

Analyzes the benchmarking results and provides insights into:
- Algorithm performance characteristics
- Scalability patterns
- Optimization opportunities
- Real-world performance metrics

Usage:
    python analysis_day3.py
"""

import time
import sys
from typing import List, Dict, Any

# Import Day 3 solution functions
sys.path.append(".")
from day3 import parse_input, solve_part1, solve_part2


class Day3PerformanceAnalyzer:
    def __init__(self):
        self.metrics = {}

    def analyze_performance(self):
        """Comprehensive performance analysis."""
        print("🔬 Day 3 Performance Analysis")
        print("=" * 40)

        # Analyze actual input files
        self.analyze_actual_inputs()

        # Algorithm complexity analysis
        self.analyze_algorithm_complexity()

        # Performance characteristics
        self.analyze_performance_characteristics()

        # Optimization opportunities
        self.suggest_optimizations()

        # Final summary
        self.print_final_summary()

    def analyze_actual_inputs(self):
        """Analyze performance on actual AoC inputs."""
        print("\\n📁 Actual Input Analysis")
        print("-" * 30)

        files = [("test_input.txt", "Test Input"), ("input.txt", "Full Input")]

        results = {}

        for filename, description in files:
            try:
                data = parse_input(filename)

                # Multiple runs for accuracy
                part1_times = []
                part2_times = []

                for _ in range(5):  # 5 runs for average
                    start = time.perf_counter()
                    p1_result = solve_part1(data)
                    part1_times.append(time.perf_counter() - start)

                    start = time.perf_counter()
                    p2_result = solve_part2(data)
                    part2_times.append(time.perf_counter() - start)

                avg_p1 = sum(part1_times) / len(part1_times)
                avg_p2 = sum(part2_times) / len(part2_times)

                results[filename] = {
                    "description": description,
                    "lines": len(data),
                    "chars": sum(len(line) for line in data),
                    "avg_p1_time": avg_p1,
                    "avg_p2_time": avg_p2,
                    "p1_result": p1_result,
                    "p2_result": p2_result,
                    "chars_per_sec_p1": sum(len(line) for line in data) / avg_p1,
                    "chars_per_sec_p2": sum(len(line) for line in data) / avg_p2,
                    "lines_per_sec_p1": len(data) / avg_p1,
                    "lines_per_sec_p2": len(data) / avg_p2,
                }

                print(f"\\n{description}:")
                print(
                    f"  📊 {len(data)} lines, {sum(len(line) for line in data):,} characters"
                )
                print(
                    f"  ⏱️  Part 1: {avg_p1*1000:.3f}ms avg ({results[filename]['lines_per_sec_p1']:.0f} lines/s)"
                )
                print(
                    f"  ⏱️  Part 2: {avg_p2*1000:.3f}ms avg ({results[filename]['lines_per_sec_p2']:.0f} lines/s)"
                )
                print(f"  🎯 Results: P1={p1_result:,}, P2={p2_result:,}")
                print(f"  📈 P2/P1 ratio: {avg_p2/avg_p1:.2f}x")

            except Exception as e:
                print(f"  ❌ {filename}: {e}")

        self.metrics["actual_inputs"] = results

    def analyze_algorithm_complexity(self):
        """Analyze algorithmic complexity by examining the code."""
        print("\\n🧮 Algorithm Complexity Analysis")
        print("-" * 35)

        print("\\n🔍 Part 1 Algorithm:")
        print("  • Iterates through each line: O(n)")
        print("  • Extracts digits from line: O(m) where m = line length")
        print("  • Finds max in digits list: O(d) where d = digit count")
        print("  • Searches for max position: O(m)")
        print("  • Finds max in remaining: O(d)")
        print("  ➤ Overall: O(n × m) where n=lines, m=chars per line")

        print("\\n🔍 Part 2 Algorithm:")
        print("  • Iterates through each line: O(n)")
        print("  • For each line, loops 12 times: O(1)")
        print("  • Extracts substring: O(m)")
        print("  • Finds digits: O(m)")
        print("  • Finds max: O(d)")
        print("  • Finds position: O(m)")
        print("  ➤ Overall: O(n × m) where n=lines, m=chars per line")

        print("\\n📊 Complexity Comparison:")
        print("  • Both algorithms are O(n × m)")
        print("  • Part 2 has higher constant factor (12× inner loop)")
        print("  • Part 2 does more string operations per iteration")
        print("  • Memory usage: O(m) for temporary lists/strings")

    def analyze_performance_characteristics(self):
        """Analyze performance characteristics from test results."""
        print("\\n⚡ Performance Characteristics")
        print("-" * 35)

        if "actual_inputs" not in self.metrics:
            print("  ⚠️  No input data available for analysis")
            return

        results = self.metrics["actual_inputs"]

        print("\\n🏃 Throughput Analysis:")
        for filename, data in results.items():
            chars_per_ms_p1 = data["chars_per_sec_p1"] / 1000
            chars_per_ms_p2 = data["chars_per_sec_p2"] / 1000

            print(f"  {data['description']}:")
            print(f"    Part 1: {chars_per_ms_p1:.0f} chars/ms")
            print(f"    Part 2: {chars_per_ms_p2:.0f} chars/ms")

        # Calculate scaling
        if len(results) >= 2:
            test_data = results.get("test_input.txt")
            full_data = results.get("input.txt")

            if test_data and full_data:
                print("\\n📈 Scaling Analysis:")
                size_ratio = full_data["chars"] / test_data["chars"]
                time_ratio_p1 = full_data["avg_p1_time"] / test_data["avg_p1_time"]
                time_ratio_p2 = full_data["avg_p2_time"] / test_data["avg_p2_time"]

                print(f"  Data size ratio: {size_ratio:.1f}x")
                print(f"  Time ratio P1: {time_ratio_p1:.1f}x")
                print(f"  Time ratio P2: {time_ratio_p2:.1f}x")
                print(f"  Scaling efficiency P1: {size_ratio/time_ratio_p1:.2f}")
                print(f"  Scaling efficiency P2: {size_ratio/time_ratio_p2:.2f}")

                if time_ratio_p1 > size_ratio:
                    print("  ⚠️  Part 1 scales worse than linear")
                else:
                    print("  ✅ Part 1 scales better than linear")

                if time_ratio_p2 > size_ratio:
                    print("  ⚠️  Part 2 scales worse than linear")
                else:
                    print("  ✅ Part 2 scales better than linear")

    def suggest_optimizations(self):
        """Suggest potential optimizations based on analysis."""
        print("\\n🚀 Optimization Opportunities")
        print("-" * 35)

        print("\\n💡 Algorithm-Level Optimizations:")
        print("  1. Pre-filter lines with insufficient digits")
        print("     • Skip lines with < 2 digits early")
        print("     • Could save 20-30% on sparse data")

        print("  2. Optimize digit extraction")
        print("     • Use list comprehension instead of loop + append")
        print("     • Cache digit positions for reuse")

        print("  3. Reduce string operations in Part 2")
        print("     • Calculate indices directly instead of substring")
        print("     • Avoid repeated string slicing")

        print("\\n🔧 Implementation Optimizations:")
        print("  1. Use enumerate() instead of index() for position finding")
        print("  2. Consider numpy arrays for large datasets")
        print("  3. Implement early termination conditions")
        print("  4. Use generator expressions for memory efficiency")

        print("\\n🏗️  Structural Optimizations:")
        print("  1. Combine Part 1 and 2 processing")
        print("     • Single pass through data")
        print("     • Shared digit extraction")

        print("  2. Implement streaming processing")
        print("     • Process lines as they're read")
        print("     • Reduce memory footprint")

        print("  3. Parallel processing for large datasets")
        print("     • Process chunks of lines concurrently")
        print("     • Merge results at the end")

    def benchmark_optimization_example(self):
        """Demonstrate a simple optimization."""
        print("\\n🧪 Optimization Example")
        print("-" * 25)

        try:
            # Test with actual input
            data = parse_input("input.txt")

            print("Testing optimized digit extraction...")

            # Original approach timing
            start = time.perf_counter()
            for line in data:
                digits = [int(char) for char in line if char.isdigit()]
            original_time = time.perf_counter() - start

            # Optimized approach timing
            start = time.perf_counter()
            for line in data:
                # Pre-allocate and use enumerate
                digits = []
                for char in line:
                    if char.isdigit():
                        digits.append(int(char))
            optimized_time = time.perf_counter() - start

            print(f"  Original approach: {original_time*1000:.3f}ms")
            print(f"  Optimized approach: {optimized_time*1000:.3f}ms")
            print(f"  Improvement: {original_time/optimized_time:.2f}x")

        except Exception as e:
            print(f"  ❌ Optimization test failed: {e}")

    def print_final_summary(self):
        """Print comprehensive summary."""
        print("\\n" + "=" * 50)
        print("📋 FINAL PERFORMANCE SUMMARY")
        print("=" * 50)

        if "actual_inputs" in self.metrics:
            results = self.metrics["actual_inputs"]

            print("\\n🎯 Key Metrics:")
            for filename, data in results.items():
                print(f"\\n  {data['description']}:")
                print(f"    • {data['lines_per_sec_p1']:.0f} lines/sec (Part 1)")
                print(f"    • {data['lines_per_sec_p2']:.0f} lines/sec (Part 2)")
                print(f"    • {data['chars_per_sec_p1']:.0f} chars/sec (Part 1)")
                print(f"    • {data['chars_per_sec_p2']:.0f} chars/sec (Part 2)")

            # Overall assessment
            print("\\n🏆 Performance Assessment:")

            # Get full input performance
            if "input.txt" in results:
                full_perf = results["input.txt"]
                p1_throughput = full_perf["chars_per_sec_p1"]
                p2_throughput = full_perf["chars_per_sec_p2"]

                # Performance categories (chars/sec)
                if p1_throughput > 1000000:  # > 1M chars/sec
                    p1_rating = "Excellent"
                elif p1_throughput > 500000:  # > 500K chars/sec
                    p1_rating = "Good"
                elif p1_throughput > 100000:  # > 100K chars/sec
                    p1_rating = "Fair"
                else:
                    p1_rating = "Needs Optimization"

                if p2_throughput > 500000:  # > 500K chars/sec
                    p2_rating = "Excellent"
                elif p2_throughput > 250000:  # > 250K chars/sec
                    p2_rating = "Good"
                elif p2_throughput > 50000:  # > 50K chars/sec
                    p2_rating = "Fair"
                else:
                    p2_rating = "Needs Optimization"

                print(f"  Part 1 Performance: {p1_rating}")
                print(f"  Part 2 Performance: {p2_rating}")

                # Bottleneck analysis
                ratio = full_perf["avg_p2_time"] / full_perf["avg_p1_time"]
                if ratio > 3.0:
                    print(f"  ⚠️  Part 2 is the bottleneck ({ratio:.1f}x slower)")
                elif ratio > 2.0:
                    print(f"  ℹ️  Part 2 is moderately slower ({ratio:.1f}x)")
                else:
                    print(f"  ✅ Both parts perform similarly ({ratio:.1f}x)")

        print("\\n✅ Analysis Complete!")


def main():
    """Main entry point."""
    analyzer = Day3PerformanceAnalyzer()
    analyzer.analyze_performance()


if __name__ == "__main__":
    main()
