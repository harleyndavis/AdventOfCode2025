# Day 5: Cafeteria

**Problem:** Inventory Management System - Fresh vs Spoiled Ingredients

## Solution Overview

- **Input:** Fresh ingredient ID ranges, blank line separator, available ingredient IDs to check
- **Output Part 1:** Count of available ingredient IDs that are fresh (fall within any range)
- **Output Part 2:** Total count of all ingredient IDs considered fresh by the ranges
- **Algorithm:** Range parsing, overlapping range merging, inclusive range matching

## Usage

```bash
# Use default input file
python Day5/day5.py

# Use custom input file
python Day5/day5.py ./Day5/test_input.txt

# Use any file path
python Day5/day5.py "path/to/your/file.txt"
```

## Input Format

The database consists of:
1. Fresh ingredient ID ranges (inclusive, format: `start-end`)
2. A blank line separator  
3. Available ingredient IDs to check (one per line)

Example:
```
3-5
10-14
16-20
12-18

1
5
8
11
17
32
```

## Algorithm Explanation

### Part 1: Count Fresh Available Ingredients
1. Parse ranges and available IDs from input
2. Sort and merge overlapping ranges for efficiency
3. For each available ID, check if it falls within any range (inclusive)
4. Count matching IDs

**Example Analysis:**
- ID 1: spoiled (not in any range)
- ID 5: fresh (in range 3-5) ✓
- ID 8: spoiled (not in any range)  
- ID 11: fresh (in range 10-14) ✓
- ID 17: fresh (in ranges 16-20 and 12-18) ✓
- ID 32: spoiled (not in any range)

**Result:** 3 fresh ingredients

### Part 2: Count All Possible Fresh IDs
1. Use the same merged ranges from Part 1
2. For each range, count all IDs it contains: `end - start + 1` 
3. Sum the counts from all ranges

**Example Analysis:**
- Ranges after merging: (3,5), (10,20)
- Range (3,5): contains IDs 3,4,5 = 3 IDs
- Range (10,20): contains IDs 10,11,12,13,14,15,16,17,18,19,20 = 11 IDs  
- Total: 3 + 11 = **14 fresh ingredient IDs**

## Critical Bug Fix: Missing First ID

### The Problem
Initial implementation returned 732 for Part 1 (too low by 1). The issue was in the `preprocess_input()` function's blank line detection logic.
Issue was due to ripping out blank lines even though that was an important formatting in the input.

### Root Cause
```python
# BUGGY CODE:
for line in data:
    if not blank_line_found:
        if "-" in line:
            start, end = map(int, line.split("-"))
            ranges.append((start, end))
        else:
            # Found the blank line separator
            blank_line_found = True  # ❌ BUG: Don't process this line!
    else:
        ids_to_check.append(int(line))
```

When the first non-range line (first ID) was encountered, the code would:
1. Set `blank_line_found = True`
2. **Skip processing that line as an ID**
3. Continue to next iteration

Result: The first ID in the list was completely ignored.

### The Fix
```python
# FIXED CODE:
for line in data:
    if not blank_line_found:
        if "-" in line:
            start, end = map(int, line.split("-"))
            ranges.append((start, end))
        else:
            # Found the blank line separator - this line is the first ID
            blank_line_found = True
            ids_to_check.append(int(line))  # ✅ Process this line!
    else:
        ids_to_check.append(int(line))
```

### Detection Method
Created a test case `test_input_all.txt` with a range covering all IDs:
```
1-32
1
5
8
11
17
32
```
- Expected: 6 (all IDs fresh)
- Before fix: 5 (missing first ID)  
- After fix: 6 ✓

## Complexity Analysis

- **Time Complexity:** O(R log R + I×R) where R = number of ranges, I = number of IDs
  - Range sorting: O(R log R)
  - Range merging: O(R)  
  - ID checking: O(I×R) in worst case (no merging benefit)
- **Space Complexity:** O(R + I) for storing ranges and IDs

## Development Notes

### Key Insights
1. **Ranges are inclusive:** "3-5" means IDs 3, 4, and 5 are all fresh
2. **Overlapping ranges:** An ID is fresh if it appears in ANY range
3. **Range merging optimization:** Combines overlapping ranges to reduce checking time
4. **Part 1 vs Part 2:** Different counting methods but same range processing

### Testing Strategy
- **Unit tests:** Verified range parsing, merging, and ID matching logic
- **Edge case testing:** Created comprehensive test cases including all-inclusive ranges
- **Debugging:** Used custom test files to isolate parsing issues

### Lessons Learned
- **Always test edge cases:** The "missing first ID" bug only appeared with comprehensive testing
- **Validate assumptions:** Initial assumption that 732 was correct led to extensive debugging
- **Incremental testing:** Creating targeted test cases helped isolate the specific parsing issue

[← Back to Main README](../README.md)