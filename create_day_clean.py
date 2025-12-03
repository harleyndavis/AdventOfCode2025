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
        with open(template_path, "r", encoding="utf-8") as f:
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
    with open(day_folder / f"day{day_num}.py", "w", encoding="utf-8") as f:
        f.write(solution_content)


def create_input_files(day_folder: Path) -> None:
    """Create empty input files."""
    # Main input file
    with open(day_folder / "input.txt", "w", encoding="utf-8") as f:
        f.write("# Paste your puzzle input here\n")

    # Test input file
    with open(day_folder / "test.txt", "w", encoding="utf-8") as f:
        f.write("# Paste test input here\n")


def create_readme(day_folder: Path, day_num: int) -> None:
    """Create README from template."""
    template_path = Path("templates") / "README_template.md"

    if template_path.exists():
        # Read template and substitute values
        with open(template_path, "r", encoding="utf-8") as f:
            template_content = f.read()
        readme_content = template_content.replace("{day_num}", str(day_num))
    else:
        # Simple fallback
        readme_content = f"""# Day {day_num}: [Problem Title]

## Problem Description
[Add problem description here]

## Solution
[Add solution explanation here]

## Usage
```bash
python day{day_num}.py
```
"""

    # Write README file
    with open(day_folder / "README.md", "w", encoding="utf-8") as f:
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
