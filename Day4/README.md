# Day 4: [Problem Title]

**Problem:** [Brief description of the problem]

## Solution Overview

- **Input:** [Description of input format]
- **Output:** [Description of expected output]
- **Algorithm:** [Brief algorithm description]

## Usage

```bash
# Use default input file
python Day4/day4.py

# Use custom input file
python Day4/day4.py ./Day4/test_input.txt

# Use any file path
python Day4/day4.py "path/to/your/file.txt"
```

## Input Format

[Describe the expected input format]

Example:
```
[Sample input]
```

## Algorithm Explanation

### Part 1
**Problem**: Count how many '@' symbols are removable, ie have fewer than 4 '@' neighbors in their 8-directional neighborhood.

**Initial Algorithm**:
1. Iterate through every cell in the grid (`data`)
2. For each position `(i, j)`, call `removable_at_symbols()`
3. This helper function:
   - Returns 0 immediately if current cell is not '@'
   - Checks all 8 adjacent directions: up, down, left, right, and 4 diagonals
   - Counts how many neighbors contain '@' symbols
   - Returns 1 if count < 4 (meaning this '@' is "removable"), 0 otherwise
4. Sum all the 1s returned to get total count of removable '@' symbols

**Example**: In a 3x3 area around position (i,j):
```
@ @ .    <- If center @ has only 2 neighbors,
. @ @    <- it counts as 1 toward the total
. . .
```

**Time Complexity**: O(rows × cols) - single pass through grid, constant work per cell 

**Benchmarking**

For the following results ran 100 tests each time to try and account for variable load.
They are in order and do build off each other when improvements are found.

| Optimization | Average Time | Range | Variance | Notes|
|--------------|--------------|-------|----------|----------|
| Pre-optimization | 18.021ms | 17.667ms-21.388ms | 2.4% |
| Early Exit in `removable_at_symbols()` | 15.763ms | 15.223ms-19.734ms | 4.3% |
| Pre-check for '@' | 14.751ms | 14.105ms-18.851ms | 5.8% |
| Simplify Final Return in `removable_at_symbols()` | 14.347ms | 13.914ms-16.340ms | 2.2% |
| Only Calculate Rows/Cols Once | 13.818ms | 13.233ms-17.963ms | 6.1% |
| Pre-compute grid dimensions and use edge detection | 18.216ms | 17.545ms-25.710ms | 5.3% | This had less operations, but had function call overhead. |
| Changed to 2d list | 13.658ms | 13.377ms-14.309ms | 1.2% | Did not expect much if any improvements, this well be more noticeable improvements to part 2. |

### Part 2  
[Explain part 2 approach]

## Complexity Analysis

- **Time Complexity:** O(?) 
- **Space Complexity:** O(?)

**Benchmarking**
Some of the Part 1 benchmarking may not be accounted for in these results. This is also running 100 different tests to account for system load.

| Optimization | Average Time | Range | Variance | Notes|
|--------------|--------------|-------|----------|----------|
| Pre-optimization | 251.027ms | 241.109ms-268.389ms | 4.2% |
| Changed to 2d list | 171.203ms | 167.517ms-183.483ms | 1.4% | Speed up as we were recreating strings to modify each position. |
| Tracking @ Cells | 247.868ms | 241.547ms-261.201ms | 2.5% | Looks like Set overhead might be slower then just checking the whole array. |
| Differential Updates | 63.380ms | 57.878ms-75.724ms | 6.1% | Despite also using sets, this reduces the checks by only checking positions that could have changed. |

## Development Notes

[Any interesting notes about the solution approach, optimizations, or lessons learned]

[← Back to Main README](../README.md)