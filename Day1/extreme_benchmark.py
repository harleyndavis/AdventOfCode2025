"""
Extreme performance benchmark to showcase the dramatic difference
between O(n) and O(1) approaches with very large datasets.
"""

import time
import tempfile
import os
from day1 import process_commands


def create_extreme_test_file():
    """Create a test file with extremely large distances."""
    commands = [
        "R1000000",  # 1 million steps
        "L500000",  # 500k steps
        "R2000000",  # 2 million steps
        "L750000",  # 750k steps
        "R10000000",  # 10 million steps!
    ]

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("\n".join(commands))
        return f.name, commands


def main():
    print("🚀 EXTREME Performance Benchmark")
    print("=" * 50)
    print("Testing with MASSIVE distances that would be impossible with O(n)...")

    temp_file, commands = create_extreme_test_file()

    try:
        total_distance = sum(int(cmd[1:]) for cmd in commands)
        print(f"\n📊 Total distance to simulate: {total_distance:,} steps")
        print(
            f"📊 With O(n), this would take ~{total_distance/1000000:.1f} million operations"
        )
        print(f"📊 With our O(1), this takes only {len(commands)} operations")

        print(f"\n⏱️  Running optimized algorithm...")
        start_time = time.perf_counter()
        result = process_commands(temp_file)
        end_time = time.perf_counter()

        duration = (end_time - start_time) * 1000  # Convert to milliseconds

        print(f"✅ Result: {result} zero crossings")
        print(f"⚡ Time taken: {duration:.2f}ms")
        print(f"🎯 Performance: {total_distance/duration:.0f} steps per millisecond")

        # Estimate how long naive approach would take
        estimated_naive_time = (
            total_distance / 1000000
        ) * 60  # Rough estimate: 1M steps = 60ms
        estimated_hours = estimated_naive_time / 1000 / 3600

        print(f"\n🐌 Estimated O(n) time: ~{estimated_naive_time/1000:.1f} seconds")
        if estimated_hours > 1:
            print(f"🐌 That's approximately {estimated_hours:.1f} hours!")

        speedup_factor = estimated_naive_time / duration
        print(f"🚀 Estimated speedup: ~{speedup_factor:,.0f}x faster!")

        print(f"\n🎉 This showcases why algorithmic optimization matters!")
        print(f"💡 O(1) vs O(n) makes the impossible possible!")

    finally:
        os.unlink(temp_file)


if __name__ == "__main__":
    main()
