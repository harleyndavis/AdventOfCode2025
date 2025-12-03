"""
Visual GUI for Day 2 Solution - Pattern Detection Matrix

This creates an interactive GUI that shows:
- Pattern detection matrix visualization
- Real-time number processing
- Pattern analysis statistics
- Step-by-step algorithm demonstration
- Range processing progress

Usage:
    python pattern_gui.py
    python pattern_gui.py --file custom_input.txt
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import threading
import time
from typing import List, Tuple, Optional, Dict
import sys
import os
from collections import defaultdict, deque

# Import our solution functions
sys.path.append(".")
from Day2 import read_file, is_invalid_id, sum_invalid_ids


class PatternDetectionGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Advent of Code Day 2 - Pattern Detection Matrix")
        self.root.geometry("1400x900")

        # Processing state
        self.id_ranges: List[Tuple[int, int]] = []
        self.current_range_index = 0
        self.current_number = 0
        self.is_processing = False
        self.processing_thread = None

        # Animation settings
        self.animation_speed = 100  # milliseconds between numbers
        self.step_mode = False
        self.auto_advance = True

        # Statistics
        self.stats = {
            "total_processed": 0,
            "invalid_count": 0,
            "valid_count": 0,
            "pattern_types": defaultdict(int),
            "processing_time": 0,
            "current_sum": 0,
        }

        # Pattern analysis state
        self.current_analysis = {
            "number": "",
            "length": 0,
            "current_pattern_len": 0,
            "pattern_states": {},  # {position: color}
            "found_pattern": None,
            "is_invalid": False,
        }

        # Colors
        self.colors = {
            "unchecked": "#ECEFF1",  # Light gray
            "analyzing": "#FFF176",  # Yellow
            "pattern_match": "#81C784",  # Green
            "pattern_fail": "#E57373",  # Red
            "valid": "#64B5F6",  # Blue
            "invalid": "#FF8A65",  # Orange
            "background": "#263238",  # Dark blue-gray
            "text": "#FFFFFF",  # White
        }

        self.setup_ui()
        self.setup_matplotlib()

    def setup_ui(self):
        """Create the main UI layout."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Top control panel
        self.setup_controls(main_frame)

        # Content area (3 columns)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Left panel: Statistics and controls
        left_frame = ttk.LabelFrame(
            content_frame, text="Statistics & Analysis", padding=10
        )
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        self.setup_stats_panel(left_frame)

        # Center panel: Pattern Matrix
        center_frame = ttk.LabelFrame(
            content_frame, text="Pattern Detection Matrix", padding=5
        )
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.setup_matrix_panel(center_frame)

        # Right panel: Number Queue and Details
        right_frame = ttk.LabelFrame(content_frame, text="Processing Queue", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        self.setup_queue_panel(right_frame)

    def setup_controls(self, parent):
        """Setup control buttons and file selection."""
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # File selection
        file_frame = ttk.Frame(control_frame)
        file_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(file_frame, text="Input File:").pack(side=tk.LEFT, padx=(0, 5))

        self.file_var = tk.StringVar(value="input.txt")
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var, width=30)
        self.file_entry.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Button(file_frame, text="Load", command=self.load_file).pack(side=tk.LEFT)

        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)

        self.start_btn = ttk.Button(
            button_frame, text="Start Processing", command=self.start_processing
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = ttk.Button(
            button_frame, text="Pause", command=self.pause_processing, state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.step_btn = ttk.Button(
            button_frame, text="Step", command=self.step_processing, state=tk.DISABLED
        )
        self.step_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = ttk.Button(
            button_frame, text="Reset", command=self.reset_processing
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

    def setup_stats_panel(self, parent):
        """Setup statistics display panel."""
        # Current number display
        current_frame = ttk.LabelFrame(parent, text="Current Analysis", padding=5)
        current_frame.pack(fill=tk.X, pady=(0, 10))

        self.current_number_label = ttk.Label(
            current_frame, text="Number: --", font=("Courier", 14, "bold")
        )
        self.current_number_label.pack(anchor=tk.W)

        self.pattern_status_label = ttk.Label(current_frame, text="Status: Ready")
        self.pattern_status_label.pack(anchor=tk.W)

        self.pattern_info_label = ttk.Label(current_frame, text="Pattern: --")
        self.pattern_info_label.pack(anchor=tk.W)

        # Statistics display
        stats_frame = ttk.LabelFrame(parent, text="Processing Statistics", padding=5)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        self.stats_labels = {}
        for stat in ["total_processed", "invalid_count", "valid_count", "current_sum"]:
            label = ttk.Label(stats_frame, text=f"{stat.replace('_', ' ').title()}: 0")
            label.pack(anchor=tk.W)
            self.stats_labels[stat] = label

        # Speed controls
        speed_frame = ttk.LabelFrame(parent, text="Animation Controls", padding=5)
        speed_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(speed_frame, text="Speed:").pack(anchor=tk.W)
        self.speed_var = tk.IntVar(value=self.animation_speed)
        speed_scale = ttk.Scale(
            speed_frame,
            from_=10,
            to=1000,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            command=self.update_speed,
        )
        speed_scale.pack(fill=tk.X, pady=5)

        # Mode controls
        self.step_mode_var = tk.BooleanVar()
        step_check = ttk.Checkbutton(
            speed_frame,
            text="Step-by-step mode",
            variable=self.step_mode_var,
            command=self.toggle_step_mode,
        )
        step_check.pack(anchor=tk.W)

        # Pattern type distribution
        pattern_frame = ttk.LabelFrame(parent, text="Pattern Distribution", padding=5)
        pattern_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for pattern chart
        self.pattern_canvas = tk.Canvas(pattern_frame, height=150, bg="white")
        self.pattern_canvas.pack(fill=tk.BOTH, expand=True, pady=5)

    def setup_matrix_panel(self, parent):
        """Setup the pattern detection matrix visualization."""
        # Matrix will be created with matplotlib
        self.matrix_frame = parent

    def setup_queue_panel(self, parent):
        """Setup the processing queue display."""
        # Range progress
        range_frame = ttk.LabelFrame(parent, text="Range Progress", padding=5)
        range_frame.pack(fill=tk.X, pady=(0, 10))

        self.range_label = ttk.Label(range_frame, text="Range: --")
        self.range_label.pack(anchor=tk.W)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            range_frame, variable=self.progress_var, maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=5)

        # Recent numbers queue
        queue_frame = ttk.LabelFrame(parent, text="Recent Numbers", padding=5)
        queue_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox with scrollbar
        list_frame = ttk.Frame(queue_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.queue_listbox = tk.Listbox(list_frame, height=15, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.queue_listbox.yview
        )
        self.queue_listbox.config(yscrollcommand=scrollbar.set)

        self.queue_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Detailed analysis
        detail_frame = ttk.LabelFrame(parent, text="Pattern Details", padding=5)
        detail_frame.pack(fill=tk.X, pady=(10, 0))

        self.detail_text = tk.Text(
            detail_frame, height=6, width=25, wrap=tk.WORD, font=("Courier", 9)
        )
        detail_scroll = ttk.Scrollbar(
            detail_frame, orient=tk.VERTICAL, command=self.detail_text.yview
        )
        self.detail_text.config(yscrollcommand=detail_scroll.set)

        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        detail_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def setup_matplotlib(self):
        """Setup matplotlib figure for pattern matrix."""
        self.fig = Figure(figsize=(8, 6), facecolor="white")
        self.ax = self.fig.add_subplot(111)

        # Initial empty matrix
        self.matrix_data = np.zeros((10, 10))  # Will resize based on number length
        self.im = self.ax.imshow(self.matrix_data, cmap="viridis", aspect="equal")

        self.ax.set_title("Pattern Detection Matrix", fontsize=14, fontweight="bold")
        self.ax.set_xlabel("Pattern Position")
        self.ax.set_ylabel("Number Position")

        # Add to GUI
        self.canvas = FigureCanvasTkAgg(self.fig, self.matrix_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # File operations
    def browse_file(self):
        """Browse for input file."""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if filename:
            self.file_var.set(filename)

    def load_file(self):
        """Load ID ranges from file."""
        try:
            filename = self.file_var.get()
            self.id_ranges = read_file(filename)

            total_numbers = sum(end - start + 1 for start, end in self.id_ranges)
            messagebox.showinfo(
                "File Loaded",
                f"Loaded {len(self.id_ranges)} ranges with {total_numbers:,} total numbers",
            )

            self.reset_processing()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    # Processing control
    def start_processing(self):
        """Start processing the loaded ranges."""
        if not self.id_ranges:
            messagebox.showwarning("No Data", "Please load an input file first")
            return

        if not self.is_processing:
            self.is_processing = True
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.DISABLED if not self.step_mode else tk.NORMAL)

            # Start processing thread
            self.processing_thread = threading.Thread(
                target=self.process_ranges, daemon=True
            )
            self.processing_thread.start()

    def pause_processing(self):
        """Pause/resume processing."""
        if self.is_processing:
            self.is_processing = False
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.step_btn.config(state=tk.NORMAL)
        else:
            self.start_processing()

    def step_processing(self):
        """Process one step."""
        if hasattr(self, "_step_event"):
            self._step_event.set()

    def reset_processing(self):
        """Reset processing state."""
        self.is_processing = False
        self.current_range_index = 0
        self.current_number = 0

        # Reset statistics
        self.stats = {
            "total_processed": 0,
            "invalid_count": 0,
            "valid_count": 0,
            "pattern_types": defaultdict(int),
            "processing_time": 0,
            "current_sum": 0,
        }

        self.update_stats_display()
        self.clear_matrix()
        self.queue_listbox.delete(0, tk.END)
        self.detail_text.delete("1.0", tk.END)

        # Reset buttons
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.step_btn.config(state=tk.DISABLED)

    # Processing logic
    def process_ranges(self):
        """Main processing loop."""
        start_time = time.time()

        for range_idx, (start, end) in enumerate(self.id_ranges):
            if not self.is_processing:
                break

            self.current_range_index = range_idx
            range_size = end - start + 1

            # Update range display
            self.root.after(0, self.update_range_display, start, end)

            for i, number in enumerate(range(start, end + 1)):
                if not self.is_processing:
                    break

                self.current_number = number

                # Process this number
                self.root.after(0, self.analyze_number, number)

                # Update progress
                progress = (i + 1) / range_size * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))

                # Wait for animation or step
                if self.step_mode_var.get():
                    self._step_event = threading.Event()
                    self._step_event.wait()
                else:
                    time.sleep(self.animation_speed / 1000.0)

        end_time = time.time()
        self.stats["processing_time"] = end_time - start_time

        # Processing complete
        self.root.after(0, self.processing_complete)

    def analyze_number(self, number):
        """Analyze a single number and update visualization."""
        # Update current number display
        self.current_number_label.config(text=f"Number: {number}")
        self.pattern_status_label.config(text="Status: Analyzing...")

        # Perform pattern detection with visualization
        is_invalid = self.visualize_pattern_detection(number)

        # Update statistics
        self.stats["total_processed"] += 1
        if is_invalid:
            self.stats["invalid_count"] += 1
            self.stats["current_sum"] += number

            # Determine pattern type
            pattern_type = self.get_pattern_type(number)
            self.stats["pattern_types"][pattern_type] += 1

            status = f"Status: INVALID - {pattern_type}"
            color = self.colors["invalid"]
        else:
            self.stats["valid_count"] += 1
            status = "Status: Valid"
            color = self.colors["valid"]

        self.pattern_status_label.config(text=status)

        # Add to queue display
        queue_text = f"{number}: {'INVALID' if is_invalid else 'valid'}"
        self.queue_listbox.insert(0, queue_text)

        # Keep only recent 50 items
        if self.queue_listbox.size() > 50:
            self.queue_listbox.delete(tk.END)

        # Color the item
        self.queue_listbox.itemconfig(0, {"fg": "red" if is_invalid else "blue"})

        self.update_stats_display()
        self.update_pattern_chart()

    def visualize_pattern_detection(self, number):
        """Visualize the pattern detection algorithm step by step."""
        number_str = str(number)
        length = len(number_str)

        # Create matrix for this number
        max_pattern_len = length // 2
        if max_pattern_len == 0:
            return False

        # Initialize matrix
        matrix = np.zeros((length, max_pattern_len))

        # Check each pattern length
        found_pattern = False
        pattern_info = ""

        for pattern_len in range(1, max_pattern_len + 1):
            if length % pattern_len == 0:
                # Highlight current pattern being tested
                self.pattern_info_label.config(
                    text=f"Testing pattern length: {pattern_len}"
                )

                # Check if pattern repeats
                is_repeated = True
                pattern = number_str[:pattern_len]

                for i in range(pattern_len, length):
                    pos_in_pattern = i % pattern_len

                    if number_str[i] == number_str[pos_in_pattern]:
                        matrix[i][pattern_len - 1] = 1  # Match
                    else:
                        matrix[i][pattern_len - 1] = -1  # No match
                        is_repeated = False

                if (
                    is_repeated and pattern_len < length
                ):  # Don't count the whole number as a pattern
                    found_pattern = True
                    pattern_info = (
                        f"Pattern '{pattern}' repeats {length // pattern_len} times"
                    )
                    # Mark the successful pattern
                    matrix[:, pattern_len - 1] = 2
                    break

        self.update_matrix_display(matrix, number_str)
        self.pattern_info_label.config(
            text=pattern_info if found_pattern else "No pattern found"
        )

        # Update detail text
        self.update_detail_text(number, found_pattern, pattern_info)

        return found_pattern

    def update_matrix_display(self, matrix, number_str):
        """Update the matplotlib matrix display."""
        self.ax.clear()

        # Create colormap: -1=red (no match), 0=white (not checked), 1=yellow (match), 2=green (pattern found)
        colors = ["red", "white", "yellow", "green"]
        from matplotlib.colors import ListedColormap

        cmap = ListedColormap(colors)

        # Adjust matrix values for colormap (shift from [-1,2] to [0,3])
        display_matrix = matrix + 1

        im = self.ax.imshow(display_matrix, cmap=cmap, aspect="equal", vmin=0, vmax=3)

        self.ax.set_title(
            f"Pattern Analysis: {number_str}", fontsize=12, fontweight="bold"
        )
        self.ax.set_xlabel("Pattern Length")
        self.ax.set_ylabel("Character Position")

        # Add number characters as y-axis labels
        self.ax.set_yticks(range(len(number_str)))
        self.ax.set_yticklabels(list(number_str))

        # Add pattern length as x-axis labels
        if matrix.shape[1] > 0:
            self.ax.set_xticks(range(matrix.shape[1]))
            self.ax.set_xticklabels(range(1, matrix.shape[1] + 1))

        self.canvas.draw()

    # UI update methods
    def update_range_display(self, start, end):
        """Update range information display."""
        self.range_label.config(text=f"Range: {start:,} - {end:,}")

    def update_stats_display(self):
        """Update statistics labels."""
        for stat, label in self.stats_labels.items():
            value = self.stats[stat]
            if stat == "current_sum":
                text = f"{stat.replace('_', ' ').title()}: {value:,}"
            else:
                text = f"{stat.replace('_', ' ').title()}: {value}"
            label.config(text=text)

    def update_pattern_chart(self):
        """Update pattern distribution chart."""
        self.pattern_canvas.delete("all")

        if not self.stats["pattern_types"]:
            return

        # Simple bar chart
        canvas_width = self.pattern_canvas.winfo_width()
        canvas_height = self.pattern_canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        patterns = list(self.stats["pattern_types"].keys())
        counts = list(self.stats["pattern_types"].values())

        if not patterns:
            return

        max_count = max(counts)
        bar_width = canvas_width // len(patterns)

        for i, (pattern, count) in enumerate(zip(patterns, counts)):
            x = i * bar_width
            height = (count / max_count) * (canvas_height - 20)
            y = canvas_height - height

            # Draw bar
            self.pattern_canvas.create_rectangle(
                x + 2,
                y,
                x + bar_width - 2,
                canvas_height - 10,
                fill="lightblue",
                outline="blue",
            )

            # Add label
            if bar_width > 30:  # Only show label if there's space
                self.pattern_canvas.create_text(
                    x + bar_width // 2,
                    canvas_height - 5,
                    text=pattern[:8],
                    anchor=tk.S,
                    font=("Arial", 8),
                )

    def update_detail_text(self, number, is_invalid, pattern_info):
        """Update detailed analysis text."""
        self.detail_text.insert(tk.END, f"\\n--- {number} ---\\n")
        self.detail_text.insert(tk.END, f"Length: {len(str(number))}\\n")
        self.detail_text.insert(
            tk.END, f"Result: {'INVALID' if is_invalid else 'Valid'}\\n"
        )
        if pattern_info:
            self.detail_text.insert(tk.END, f"Pattern: {pattern_info}\\n")

        # Auto-scroll to bottom
        self.detail_text.see(tk.END)

        # Keep only recent entries (limit to ~100 lines)
        lines = int(self.detail_text.index("end-1c").split(".")[0])
        if lines > 100:
            self.detail_text.delete("1.0", "25.0")  # Remove first 25 lines

    def clear_matrix(self):
        """Clear the matrix display."""
        self.ax.clear()
        self.ax.set_title("Pattern Detection Matrix - Ready", fontsize=12)
        self.ax.set_xlabel("Pattern Length")
        self.ax.set_ylabel("Character Position")
        self.canvas.draw()

    # Utility methods
    def get_pattern_type(self, number):
        """Determine the type of pattern in an invalid number."""
        number_str = str(number)
        length = len(number_str)

        for pattern_len in range(1, length // 2 + 1):
            if length % pattern_len == 0:
                pattern = number_str[:pattern_len]
                repetitions = length // pattern_len

                if pattern * repetitions == number_str:
                    if pattern_len == 1:
                        return f"All {pattern}s"
                    else:
                        return f"'{pattern}' x{repetitions}"

        return "Unknown"

    def update_speed(self, value):
        """Update animation speed."""
        self.animation_speed = int(float(value))

    def toggle_step_mode(self):
        """Toggle step-by-step mode."""
        self.step_mode = self.step_mode_var.get()
        if self.step_mode and self.is_processing:
            self.step_btn.config(state=tk.NORMAL)
        else:
            self.step_btn.config(state=tk.DISABLED)

    def processing_complete(self):
        """Handle processing completion."""
        self.is_processing = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.step_btn.config(state=tk.DISABLED)

        # Show completion message
        messagebox.showinfo(
            "Complete",
            f"Processing complete!\\n"
            f"Total processed: {self.stats['total_processed']:,}\\n"
            f"Invalid IDs: {self.stats['invalid_count']:,}\\n"
            f"Sum: {self.stats['current_sum']:,}\\n"
            f"Time: {self.stats['processing_time']:.2f} seconds",
        )


def main():
    """Main entry point."""
    root = tk.Tk()
    app = PatternDetectionGUI(root)

    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            print(__doc__)
            return
        elif sys.argv[1] == "--file" and len(sys.argv) > 2:
            app.file_var.set(sys.argv[2])
            app.load_file()
        else:
            app.file_var.set(sys.argv[1])
            app.load_file()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\\nExiting...")


if __name__ == "__main__":
    main()
