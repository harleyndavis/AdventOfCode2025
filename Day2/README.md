# Day 2: Invalid ID Detection

## Problem Description
Find the sum of all invalid IDs within given ranges. An invalid ID is defined as one that contains any duplicated sequence of digits that repeats at least twice.

### Examples of Invalid IDs:
- `55` (single digit repeated)
- `1212` (two digits repeated)
- `123123` (three digits repeated)
- `555` (single digit repeated 3 times)
- `1212121212` (pattern repeated multiple times)

## Solution Overview

The solution reads ID ranges from an input file and checks each ID in those ranges for repeated digit patterns. The core algorithm checks if any substring pattern can be repeated to form the entire ID.

## Performance Optimization Work

### Original Implementation
The initial `is_invalid_id()` function worked by:
1. Converting the number to a string
2. Testing all possible pattern lengths (1 to half the string length)
3. Creating a repeated pattern string via multiplication (`pattern * repetitions`)
4. Comparing the repeated pattern to the original string

### Optimization Applied
**Character-by-character comparison** instead of string concatenation:
- Eliminated expensive string multiplication operations
- Used direct array indexing: `id_str[i] != id_str[i % pattern_len]`
- Reduced memory allocations for temporary strings

### Benchmark Results

#### Synthetic Data Benchmarking
- **Small numbers (1-100K)**: Minimal performance difference
- **Large numbers (10+ digits)**: **2-4x speedup** for pattern-heavy data
- **Memory efficiency**: Significantly reduced memory allocation overhead

#### Real Advent of Code Data Benchmarking
Using actual `input.txt` and `test_input.txt`:
- **Test input**: 106 numbers, largest 10 digits - performance identical
- **Full input**: 2.26M numbers, largest 10 digits - performance nearly identical (0.95x)
- **Final answer**: 50,793,864,718

#### Key Insights from Real Data
1. Most IDs in the actual dataset are **valid** (no repeated patterns)
2. Both implementations spend most time determining "no pattern exists"
3. Optimization benefits are most apparent with pattern-heavy datasets
4. Real-world performance maintained while improving memory efficiency

## Files

- `Day2.py` - Main solution with optimized `is_invalid_id()` function
- `input.txt` - Full puzzle input (32 ranges, 2.26M numbers)
- `test_input.txt` - Test data (11 ranges, 106 numbers)
- `benchmark_optimization.py` - Synthetic data performance comparison
- `extended_benchmark.py` - Large number stress testing
- `real_data_benchmark.py` - Benchmarking with actual puzzle input

## Usage

```bash
# Run with default input
python Day2.py

# Run with test input
python Day2.py test_input.txt

# Run performance benchmarks
python real_data_benchmark.py
```

## Algorithm Complexity

- **Time Complexity**: O(n * m * √m) where n is the range size and m is the average number length
- **Space Complexity**: O(m) for string representation of each number
- **Optimization Impact**: Reduces constant factors and memory allocation overhead