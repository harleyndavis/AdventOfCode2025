# Day 1: Secret Entrance

**Problem:** Process movement commands on a circular track (positions 0-99) and count how many times position 0 is crossed.

## Solution Overview

- **Input:** Text file with movement commands (R/L followed by distance)
- **Output:** Count of zero crossings
- **Algorithm:** Mathematical O(1) approach instead of step-by-step simulation

## Key Features

- ✅ **Optimized Algorithm:** O(m) complexity where m = number of commands (vs O(D) where D = sum of all distances)
- ✅ **Command Line Arguments:** Flexible input file specification
- ✅ **Error Handling:** Graceful handling of missing files and invalid input
- ✅ **Code Quality:** Formatted with Black, follows PEP 8 standards

## Usage

```bash
# Use default input file (./Day1/input.txt)
python Day1/day1.py

# Specify custom input file
python Day1/day1.py ./Day1/test.txt

# Use any file path
python Day1/day1.py "path/to/your/file.txt"
```

## Input Format

Each line contains a movement command:
- `R` followed by a number (move right/positive)
- `L` followed by a number (move left/negative)

Example:
```
R10
L5
R100
L25
```

## Algorithm Explanation

Instead of simulating each step (O(D) complexity), we calculate zero crossings mathematically:

1. **Calculate distance to next zero crossing** based on current position and direction
2. **Count crossings** if movement distance exceeds that threshold
3. **Add additional crossings** for complete 100-position loops
4. **Update position** using modular arithmetic

This transforms a potentially expensive step-by-step simulation into constant-time calculations per command.

## Complexity Analysis

- **Original approach:** O(D) where D = sum of all movement distances
- **Optimized approach:** O(m) where m = number of commands
- **Improvement:** Massive speedup for large distances (e.g., 10M steps → 10 operations)

## Mathematical Approach Details

### Zero Crossing Logic

**Moving Right (R commands):**
- Cross zero when going from position 99 → 0
- Distance to next zero: `100 - current_position` (or 100 if already at 0)

**Moving Left (L commands):**
- Cross zero when going from position 1 → 0  
- Distance to next zero: `current_position` (or 100 if already at 0)

### Complete Loop Handling

After reaching the first zero crossing, every additional 100 steps results in another zero crossing.

```python
# Pseudocode
if distance >= distance_to_first_zero:
    crossings += 1  # First crossing
    remaining = distance - distance_to_first_zero
    crossings += remaining // 100  # Additional complete loops
```

## Development Notes

This solution showcases the transformation from a naive O(n) simulation to an optimized mathematical approach, demonstrating algorithmic thinking and performance optimization principles.

[← Back to Main README](../README.md)