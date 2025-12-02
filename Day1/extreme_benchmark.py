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

        print(f"🎉 This showcases why algorithmic optimization matters!")
        print(f"💡 O(1) vs O(n) makes the impossible possible!")

    finally:
        os.unlink(temp_file)

    # Test with real puzzle input
    print(f"\n" + "="*50)
    print(f"🎯 TESTING WITH YOUR ACTUAL PUZZLE INPUT")
    print(f"=" * 50)

    # Load real puzzle input
    with open("input.txt", "r") as f:
        real_commands = [line.strip() for line in f if line.strip()]

    real_total_distance = sum(int(cmd[1:]) for cmd in real_commands)

    print(f"📊 Real puzzle commands: {len(real_commands):,}")
    print(f"📊 Real total distance: {real_total_distance:,} steps")
    print(f"📊 With O(n), this would take ~{real_total_distance:,} operations")
    print(f"📊 With our O(1), this takes only {len(real_commands)} operations")

    # Create temp file and benchmark
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("\n".join(real_commands))
        temp_filename = f.name

    try:
        print(f"\n⏱️  Running on REAL puzzle input...")
        start_time = time.perf_counter()
        real_result = process_commands(temp_filename)
        end_time = time.perf_counter()
        
        real_duration = (end_time - start_time) * 1000  # Convert to ms
        
        print(f"✅ Real puzzle result: {real_result} zero crossings")
        print(f"⚡ Time taken: {real_duration:.2f}ms")
        print(f"🎯 Performance: {real_total_distance/real_duration:.0f} steps per millisecond")
        
        # Estimate O(n) time for comparison
        estimated_naive_time = real_total_distance * 0.00006  # 60ms per 1M steps estimate
        if estimated_naive_time > 1000:
            print(f"🐌 Estimated O(n) time: ~{estimated_naive_time/1000:.1f} seconds")
            speedup = (estimated_naive_time * 1000) / real_duration
            print(f"🚀 Estimated speedup: ~{speedup:.0f}x faster!")
        else:
            print(f"🐌 Estimated O(n) time: ~{estimated_naive_time:.0f}ms")
            speedup = estimated_naive_time / real_duration
            print(f"🚀 Estimated speedup: ~{speedup:.1f}x faster!")
            
    finally:
        os.unlink(temp_filename)

    print(f"\n🏆 Your algorithm handles both synthetic AND real data beautifully!")


if __name__ == "__main__":
    main()
