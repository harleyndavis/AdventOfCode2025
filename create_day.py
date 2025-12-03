#!/usr/bin/env python3
"""
Advent of Code Day Template Generator

This script creates a new day folder with the essential files using templates.

Usage:
    python create_day.py <day_number>
    python create_day.py 3
"""

import sys
from pathlib import Path


def create_day_structure(day_num: int, base_path: str = ".") -> None:
    """Create the day structure with essential files."""
    day_folder = Path(base_path) / f"Day{day_num}"
    
    # Create day folder
    day_folder.mkdir(exist_ok=True)
    
    # Create main solution file from template
    create_main_solution(day_folder, day_num)
    
    # Create empty input files
    create_input_files(day_folder)
    
    # Create README from template
    create_readme(day_folder, day_num)
    
    print(f"Created Day{day_num} structure:")
    print(f"   {day_folder}/")
    print(f"   day{day_num}.py")
    print(f"   README.md")
    print(f"   input.txt")
    print(f"   test.txt")
def create_main_solution(day_folder: Path, day_num: int) -> None:
    """Create the main solution file from template."""
    template_path = Path("templates") / "day_template.py"
    
    if template_path.exists():
        # Read template and substitute values
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        solution_content = template_content.replace("{day_num}", str(day_num))
    else:
        # Simple fallback if no template
        solution_content = f'''#!/usr/bin/env python3
"""
Advent of Code 2025 - Day {day_num}
"""

def parse_input(filename):
    """Parse input file and return data."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def part1(data):
    """Solve part 1."""
    # TODO: Implement solution
    return 0


def part2(data):
    """Solve part 2."""
    # TODO: Implement solution
    return 0


def main():
    """Main function."""
    # Test input
    test_data = parse_input('test.txt')
    print(f"Test Part 1: {{part1(test_data)}}")
    print(f"Test Part 2: {{part2(test_data)}}")
    
    # Actual input
    data = parse_input('input.txt')
    print(f"Part 1: {{part1(data)}}")
    print(f"Part 2: {{part2(data)}}")


if __name__ == "__main__":
    main()
'''
    
    # Write solution file
    with open(day_folder / f"day{day_num}.py", 'w', encoding='utf-8') as f:
        f.write(solution_content)


def create_input_files(day_folder: Path) -> None:
    """Create empty input files."""
    # Main input file
    with open(day_folder / "input.txt", "w", encoding='utf-8') as f:
        f.write("# Paste your puzzle input here\n")

    # Test input file
    with open(day_folder / "test.txt", "w", encoding='utf-8') as f:
        f.write("# Paste test input here\n")


def create_readme(day_folder: Path, day_num: int) -> None:
    """Create README from template."""
    template_path = Path("templates") / "README_template.md"
    
    if template_path.exists():
        # Read template and substitute values
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        readme_content = template_content.replace("{day_num}", str(day_num))
    else:
        # Simple fallback
        readme_content = f'''# Day {day_num}: [Problem Title]

## Problem Description
[Add problem description here]

## Solution
[Add solution explanation here]

## Usage
```bash
python day{day_num}.py
```
'''
    
    # Write README file
    with open(day_folder / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python create_day.py <day_number>")
        sys.exit(1)
    
    try:
        day_num = int(sys.argv[1])
    except ValueError:
        print("Error: Day number must be an integer")
        sys.exit(1)
    
    if not (1 <= day_num <= 25):
        print("Error: Day number must be between 1 and 25")
        sys.exit(1)

    day_folder = Path(f"Day{day_num}")
    if day_folder.exists():
        response = input(f"Day{day_num} folder already exists. Overwrite? (y/N): ")
        if response.lower() != "y":
            print("Cancelled")
            sys.exit(1)

    print(f"Creating Day {day_num} template...")
    create_day_structure(day_num)
    print(f"\nDay {day_num} created successfully!")


if __name__ == "__main__":
    main()

import tempfile
import os
import sys
from typing import List

# Add parent directory to path for imports
sys.path.append(".")
from day{day_num} import parse_input, solve_part1, solve_part2


class TestDay{day_num}:
    """Test cases for Day {day_num} solution."""
    
    def test_parse_input(self) -> None:
        """Test input parsing."""
        # Create temporary test file
        test_data = "test line 1\\ntest line 2\\n\\ntest line 3"
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(test_data)
            temp_filename = f.name
        
        try:
            result = parse_input(temp_filename)
            expected = ["test line 1", "test line 2", "test line 3"]
            assert result == expected, f"Expected {{expected}}, got {{result}}"
            print("✅ test_parse_input passed")
        finally:
            os.unlink(temp_filename)
    
    def test_solve_part1_sample(self) -> None:
        """Test part 1 with sample data."""
        sample_data = [
            "sample input line 1",
            "sample input line 2"
        ]
        
        result = solve_part1(sample_data)
        expected = 0  # TODO: Update with expected result
        
        assert result == expected, f"Part 1: Expected {{expected}}, got {{result}}"
        print("✅ test_solve_part1_sample passed")
    
    def test_solve_part2_sample(self) -> None:
        """Test part 2 with sample data."""
        sample_data = [
            "sample input line 1", 
            "sample input line 2"
        ]
        
        result = solve_part2(sample_data)
        expected = 0  # TODO: Update with expected result
        
        assert result == expected, f"Part 2: Expected {{expected}}, got {{result}}"
        print("✅ test_solve_part2_sample passed")
    
    def test_edge_cases(self) -> None:
        """Test edge cases."""
        # Empty input
        empty_result1 = solve_part1([])
        empty_result2 = solve_part2([])
        
        assert empty_result1 == 0, f"Part 1 empty input: Expected 0, got {{empty_result1}}"
        assert empty_result2 == 0, f"Part 2 empty input: Expected 0, got {{empty_result2}}"
        print("✅ test_edge_cases passed")


def run_all_tests() -> None:
    """Run all tests and report results."""
    test_instance = TestDay{day_num}()
    tests = [
        test_instance.test_parse_input,
        test_instance.test_solve_part1_sample,
        test_instance.test_solve_part2_sample,
        test_instance.test_edge_cases,
    ]
    
    passed = 0
    total = len(tests)
    
    print(f"🧪 Running Day {day_num} Tests")
    print("=" * 30)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {{test.__name__}} failed: {{e}}")
    
    print("=" * 30)
    print(f"📊 Results: {{passed}}/{{total}} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
'''

    with open(day_folder / f"test_day{day_num}.py", 'w', encoding='utf-8') as f:
        f.write(content)


def create_input_files(day_folder: Path) -> None:
    """Create placeholder input files."""
    # Main input file (placeholder)
    with open(day_folder / "input.txt", "w") as f:
        f.write("# Paste your actual puzzle input here\n")

    # Test input file with sample data
    with open(day_folder / "test_input.txt", "w") as f:
        f.write("sample input line 1\\nsample input line 2\\n")


def create_readme(day_folder: Path, day_num: int) -> None:
    """Create README template."""
    content = f"""# Day {day_num}: [Problem Title]

**Problem:** [Brief description of the problem]

## Solution Overview

- **Input:** [Description of input format]
- **Output:** [Description of expected output]
- **Algorithm:** [Brief algorithm description]

## Key Features

- ✅ **Clean Architecture:** Modular functions with clear separation
- ✅ **Type Safety:** Full type hints for better code quality
- ✅ **Error Handling:** Graceful handling of edge cases
- ✅ **Comprehensive Testing:** Unit tests for all major functions
- ✅ **Performance:** [Complexity analysis if applicable]

## Usage

```bash
# Use default input file
python Day{day_num}/day{day_num}.py

# Use custom input file
python Day{day_num}/day{day_num}.py ./Day{day_num}/test_input.txt

# Use any file path
python Day{day_num}/day{day_num}.py "path/to/your/file.txt"
```

## Testing

Run the test suite:

```bash
cd Day{day_num}
python test_day{day_num}.py
```

## Input Format

[Describe the expected input format]

Example:
```
[Sample input]
```

## Algorithm Explanation

### Part 1
[Explain part 1 approach]

### Part 2  
[Explain part 2 approach]

## Complexity Analysis

- **Time Complexity:** O(?) 
- **Space Complexity:** O(?)

## Development Notes

[Any interesting notes about the solution approach, optimizations, or lessons learned]

[← Back to Main README](../README.md)
"""

    with open(day_folder / "README.md", 'w', encoding='utf-8') as f:
        f.write(content)


def create_benchmark_file(day_folder: Path, day_num: int) -> None:
    """Create benchmark template (optional)."""
    content = f'''"""
Performance benchmarking for Day {day_num} solution.

Usage:
    python benchmark.py
"""

import time
import sys
from typing import List

# Import the solution functions
sys.path.append(".")
from day{day_num} import parse_input, solve_part1, solve_part2


def time_function(func, *args, **kwargs):
    """Time a function execution and return (duration, result)."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    return end_time - start_time, result


def benchmark_solution():
    """Benchmark the Day {day_num} solution."""
    print(f"🎯 Day {day_num} Performance Benchmark")
    print("=" * 40)
    
    try:
        # Load input data
        print("📂 Loading input data...")
        data = parse_input("input.txt")
        print(f"   Loaded {{len(data)}} lines")
        
        # Benchmark Part 1
        print("\n🧪 Benchmarking Part 1...")
        part1_time, part1_result = time_function(solve_part1, data)
        print(f"   Result: {{part1_result}}")
        print(f"   Time: {{part1_time*1000:.2f}}ms")
        
        # Benchmark Part 2
        print("\n🧪 Benchmarking Part 2...")
        part2_time, part2_result = time_function(solve_part2, data)
        print(f"   Result: {{part2_result}}")
        print(f"   Time: {{part2_time*1000:.2f}}ms")
        
        # Summary
        total_time = part1_time + part2_time
        print("\\n" + "=" * 40)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 40)
        print(f"Part 1: {{part1_time*1000:6.2f}}ms")
        print(f"Part 2: {{part2_time*1000:6.2f}}ms")
        print(f"Total:  {{total_time*1000:6.2f}}ms")
        
        if total_time < 0.001:
            print("⚡ Excellent performance!")
        elif total_time < 0.01:
            print("✅ Good performance!")
        elif total_time < 0.1:
            print("👍 Acceptable performance")
        else:
            print("⏰ Consider optimization opportunities")
            
    except Exception as e:
        print(f"❌ Benchmark failed: {{e}}")


if __name__ == "__main__":
    benchmark_solution()
'''

    with open(day_folder / "benchmark.py", 'w', encoding='utf-8') as f:
        f.write(content)


def update_main_readme(day_num: int) -> None:
    """Update the main README to include the new day."""
    readme_path = Path("README.md")

    if not readme_path.exists():
        print("⚠️  Main README.md not found, skipping update")
        return

    try:
        with open(readme_path, "r") as f:
            content = f.read()

        # Find the solutions table and add new day
        day_line = f"| {day_num} | TBD | _Coming soon..._ | | |"

        if day_line in content:
            # Replace the TBD entry
            new_day_line = f"| {day_num} | [Day {day_num}](./Day{day_num}/README.md) | [Brief description] | [day{day_num}.py](./Day{day_num}/day{day_num}.py) | ⏳ |"
            content = content.replace(day_line, new_day_line)

            with open(readme_path, "w") as f:
                f.write(content)
            print(f"✅ Updated main README.md with Day {day_num}")
        else:
            print(f"⚠️  Could not find Day {day_num} entry in main README.md")

    except Exception as e:
        print(f"⚠️  Could not update main README.md: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Create Advent of Code day template")
    parser.add_argument("day", type=int, help="Day number (1-25)")
    parser.add_argument("--path", default=".", help="Base path for day creation")

    args = parser.parse_args()

    if not (1 <= args.day <= 25):
        print("❌ Day number must be between 1 and 25")
        sys.exit(1)

    day_folder = Path(args.path) / f"Day{args.day}"
    if day_folder.exists():
        response = input(f"⚠️  Day{args.day} folder already exists. Overwrite? (y/N): ")
        if response.lower() != "y":
            print("❌ Cancelled")
            sys.exit(1)

    print(f"🚀 Creating Day {args.day} template...")
    create_day_structure(args.day, args.path)
    update_main_readme(args.day)

    print(f"\\n🎉 Day {args.day} template created successfully!")
    print(f"\\n📝 Next steps:")
    print(f"   1. Read the problem at https://adventofcode.com/2025/day/{args.day}")
    print(f"   2. Update Day{args.day}/README.md with problem description")
    print(f"   3. Add your puzzle input to Day{args.day}/input.txt")
    print(f"   4. Update test cases in Day{args.day}/test_day{args.day}.py")
    print(f"   5. Implement the solution in Day{args.day}/day{args.day}.py")
    print(f"   6. Run tests: cd Day{args.day} && python test_day{args.day}.py")


if __name__ == "__main__":
    main()
