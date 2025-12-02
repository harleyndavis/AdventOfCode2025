"""
Demo script for the GUI Visualizer

This shows different ways to use the visual dial interface.
"""

import os
import sys


def create_demo_files():
    """Create some demo input files for testing."""

    # Simple demo
    with open("demo_simple.txt", "w") as f:
        f.write("R10\nL5\nR60\nL25\n")

    # Crossing demo - designed to hit zero multiple times
    with open("demo_crossings.txt", "w") as f:
        f.write("R50\nR50\nL25\nL75\nR100\nL200\n")

    # Large movements demo
    with open("demo_large.txt", "w") as f:
        f.write("R500\nL300\nR1000\nL750\n")


def print_usage():
    """Print usage instructions."""
    print("🎯 GUI Visualizer Demo")
    print("=" * 40)
    print()
    print("The GUI visualizer has been created! Here's how to use it:")
    print()
    print("📋 Basic Usage:")
    print("  python gui_visualizer.py                    # Run with default data")
    print("  python gui_visualizer.py --file input.txt  # Load your puzzle input")
    print()
    print("🎮 GUI Features:")
    print("  • Circular dial showing positions 0-99")
    print("  • Real-time position tracking with red dot")
    print("  • Zero crossing counter")
    print("  • Two animation modes:")
    print("    - Step Mode: Watch every single step (naive approach)")
    print("    - Smooth Mode: Jump to final positions (optimized approach)")
    print("  • Speed controls (10ms to 500ms per step)")
    print("  • Load custom input files")
    print("  • Progress tracking")
    print()
    print("🔴 Red Dot = Current position")
    print("🟢 Green Circle = Position 0 (zero crossing point)")
    print("🔵 Blue Lines = Movement paths")
    print()
    print("💡 Tips:")
    print("  • Use Step Mode to see the naive O(n) approach in action")
    print("  • Use Smooth Mode to see the optimized O(1) approach")
    print("  • Try different speeds to see the performance difference")
    print("  • Load your actual puzzle input to see it visualized!")
    print()
    print("📁 Demo files created:")
    print("  • demo_simple.txt - Basic movements")
    print("  • demo_crossings.txt - Multiple zero crossings")
    print("  • demo_large.txt - Large distance movements")
    print()


def main():
    """Main demo function."""
    create_demo_files()
    print_usage()

    print("🚀 Starting GUI visualizer...")
    print("   (Close the GUI window when you're done exploring)")
    print()

    # Try to start with the simple demo
    os.system("python gui_visualizer.py --file demo_simple.txt")


if __name__ == "__main__":
    main()
