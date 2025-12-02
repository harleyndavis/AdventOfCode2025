# Advent of Code 2025

My solutions for Advent of Code 2025 programming challenges.

My goal for this is to solve the problems myself, using code completion and inline Copilot as needed.
After a solution is reached, using Claude to further develop or optimize the solution.

Part of the second step involves exercises perhaps unrelated to Advent Of Code just to practice, like developing this README.

## Solutions

| Day | Title | Description | Solution | Tests |
|-----|-------|-------------|----------|-------|
| 1 | [Secret Entrance](./Day1/README.md) | Circular position tracking with zero crossing optimization | [day1.py](./Day1/day1.py) | ✅ 24/24 |
| 2 | TBD | _Coming soon..._ | | |
| 3 | TBD | _Coming soon..._ | | |
| 4 | TBD | _Coming soon..._ | |
| 5 | TBD | _Coming soon..._ | |
| 6 | TBD | _Coming soon..._ | |
| 7 | TBD | _Coming soon..._ | |
| 8 | TBD | _Coming soon..._ | |
| 9 | TBD | _Coming soon..._ | |
| 10 | TBD | _Coming soon..._ | |
| 11 | TBD | _Coming soon..._ | |
| 12 | TBD | _Coming soon..._ | |

### Quick Start

```bash
# Run any day's solution
python Day1/day1.py [input_file]
python Day2/day2.py [input_file]
# etc.

# Run tests for a specific day
cd Day1 && python test_day1.py

# Run with virtual environment (if configured)
.venv/Scripts/python.exe Day1/day1.py
```

### Development Setup

**Requirements:**
- Python 3.10+
- Virtual environment (`.venv` configured)
- pytest (for running tests)

**Development Tools:**
- Type hints with full type safety
- Comprehensive unit testing
- Black formatter for code style
- Modular function architecture

**Recommended VS Code Extensions:**
- Python
- Black Formatter

### Project Structure

```
AdventOfCode2025/
├── README.md            # Main project documentation
├── .gitignore          # Git ignore patterns
├── .venv/              # Python virtual environment
├── Day1/
│   ├── day1.py          # Main solution (type-hinted, modular)
│   ├── test_day1.py     # Comprehensive unit tests (24 tests)
│   ├── benchmark.py     # Performance benchmarks
│   ├── extreme_benchmark.py # Stress testing with massive datasets
│   ├── README.md        # Detailed day documentation
│   ├── input.txt        # Puzzle input
│   └── test_input.txt   # Test data
└── .vscode/             # VS Code configuration (optional)
    └── launch.json      # Debug configurations
```

## Progress Tracking

### Solutions
- ✅ **Day 1:** Complete with optimization, type hints, and comprehensive testing
- ⏳ **Day 2:** _Pending..._
- ⏳ **Day 3:** _Pending..._

### Development Quality Standards

**Code Quality Checklist per Day:**
- ✅ **Type Safety:** Full type hints with Python 3.10+
- ✅ **Modular Design:** Clean function extraction  
- ✅ **Comprehensive Testing:** Unit tests with edge cases
- ✅ **Documentation:** Clear README with usage examples
- ✅ **Error Handling:** Graceful failure modes
- ✅ **Performance:** Algorithmic optimization where applicable

**Day 1 Metrics:**
- **Functions:** 4 clean, testable functions
- **Type Coverage:** 100% type-hinted
- **Test Coverage:** 24 tests, 100% pass rate
- **Performance:** O(m) vs O(D) optimization achieved

## Contributing

This is a personal Advent of Code repository, but feel free to:
- Suggest optimizations
- Point out bugs
- Share alternative approaches

## License

MIT License - Feel free to use these solutions for learning purposes.
