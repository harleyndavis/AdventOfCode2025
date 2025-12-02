"""
Visual GUI for Day 1 Solution - Dial Visualization

This creates an interactive GUI that shows:
- A circular dial (positions 0-99)
- Current position indicator
- Step-by-step movement animation
- Command processing display
- Zero crossing counter
- Speed controls for animation

Usage:
    python gui_visualizer.py
    python gui_visualizer.py --file custom_input.txt
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import time
import threading
from typing import List, Tuple, Optional
import sys
import os

# Import our solution functions
sys.path.append(".")
from day1 import parse_command, START_POSITION, POSITION_RANGE


class DialVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Advent of Code Day 1 - Circular Dial Visualizer")
        self.root.geometry("1000x700")

        # Animation state
        self.current_position = START_POSITION
        self.zero_crossings = 0
        self.commands: List[str] = []
        self.current_command_index = 0
        self.is_animating = False
        self.animation_speed = 50  # milliseconds between steps
        self.step_mode = False  # True for step-by-step, False for smooth

        # Timing
        self.start_time = None
        self.end_time = None

        # Colors
        self.dial_color = "#2C3E50"
        self.position_color = "#E74C3C"
        self.zero_color = "#27AE60"
        self.path_color = "#3498DB"

        self.setup_ui()
        self.load_default_data()

    def setup_ui(self):
        """Create the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Control panel (left side)
        self.setup_controls(main_frame)

        # Dial visualization (right side)
        self.setup_dial(main_frame)

        # Status bar (bottom)
        self.setup_status(main_frame)

    def setup_controls(self, parent):
        """Setup control panel."""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(
            row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10)
        )

        # File controls
        ttk.Button(control_frame, text="Load File", command=self.load_file).pack(
            fill=tk.X, pady=(0, 5)
        )
        ttk.Button(
            control_frame, text="Load Test Data", command=self.load_test_data
        ).pack(fill=tk.X, pady=(0, 10))

        # Animation controls
        ttk.Label(control_frame, text="Animation").pack(anchor=tk.W)

        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.play_btn = ttk.Button(
            button_frame, text="▶ Play", command=self.start_animation
        )
        self.play_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.pause_btn = ttk.Button(
            button_frame,
            text="⏸ Pause",
            command=self.pause_animation,
            state=tk.DISABLED,
        )
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(button_frame, text="⏹ Reset", command=self.reset_animation).pack(
            side=tk.LEFT
        )

        # Speed control
        ttk.Label(control_frame, text="Speed (ms per step)").pack(
            anchor=tk.W, pady=(10, 0)
        )
        self.speed_var = tk.IntVar(value=self.animation_speed)
        speed_scale = ttk.Scale(
            control_frame,
            from_=10,
            to=500,
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
        )
        speed_scale.pack(fill=tk.X, pady=(0, 5))
        speed_scale.configure(command=self.update_speed)

        # Step mode checkbox
        self.step_mode_var = tk.BooleanVar(value=self.step_mode)
        ttk.Checkbutton(
            control_frame,
            text="Step Mode (vs Smooth)",
            variable=self.step_mode_var,
            command=self.toggle_step_mode,
        ).pack(anchor=tk.W, pady=(10, 0))

        # Statistics
        stats_frame = ttk.LabelFrame(control_frame, text="Statistics", padding="5")
        stats_frame.pack(fill=tk.X, pady=(10, 0))

        self.stats_text = tk.Text(stats_frame, height=8, width=25, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.BOTH, expand=True)

        # Command display
        cmd_frame = ttk.LabelFrame(control_frame, text="Current Command", padding="5")
        cmd_frame.pack(fill=tk.X, pady=(10, 0))

        self.command_label = ttk.Label(
            cmd_frame, text="Ready", font=("Arial", 12, "bold")
        )
        self.command_label.pack()

    def setup_dial(self, parent):
        """Setup the circular dial visualization."""
        dial_frame = ttk.LabelFrame(
            parent, text="Circular Position Dial (0-99)", padding="10"
        )
        dial_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        dial_frame.columnconfigure(0, weight=1)
        dial_frame.rowconfigure(0, weight=1)

        # Canvas for drawing
        self.canvas = tk.Canvas(dial_frame, width=500, height=500, bg="white")
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Instructions
        instructions = ttk.Label(
            dial_frame,
            text="🔴 Red dot = Current Position\n🟢 Green = Position 0\n🔵 Blue trail = Path taken",
            justify=tk.CENTER,
        )
        instructions.grid(row=1, column=0, pady=(10, 0))

        # Bind canvas resize event to redraw
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Initial draw after a small delay to ensure canvas is ready
        self.root.after(100, self.draw_dial)

    def setup_status(self, parent):
        """Setup status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(
            row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0)
        )

        self.status_label = ttk.Label(status_frame, text="Ready to visualize")
        self.status_label.pack(side=tk.LEFT)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            status_frame, variable=self.progress_var, length=200
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))

    def draw_dial(self):
        """Draw the circular dial with position markers."""
        self.canvas.delete("all")

        # Force canvas update to get actual dimensions
        self.canvas.update()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Ensure minimum size
        if width < 100 or height < 100:
            width = height = 500

        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2 - 60  # More padding

        # Draw outer circle
        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline=self.dial_color,
            width=3,
        )

        # Draw position markers and numbers
        for i in range(100):  # All positions
            # Calculate angle: position 0 at top, clockwise
            angle = (i / 100) * 2 * math.pi - math.pi / 2

            # Draw marker lines - different styles for different intervals
            if i % 10 == 0:
                # Major markers every 10 positions - thick and long
                x1 = center_x + (radius - 3) * math.cos(angle)
                y1 = center_y + (radius - 3) * math.sin(angle)
                x2 = center_x + (radius - 30) * math.cos(angle)
                y2 = center_y + (radius - 30) * math.sin(angle)
                self.canvas.create_line(x1, y1, x2, y2, fill=self.dial_color, width=4)
            elif i % 5 == 0:
                # Medium markers every 5 positions
                x1 = center_x + (radius - 5) * math.cos(angle)
                y1 = center_y + (radius - 5) * math.sin(angle)
                x2 = center_x + (radius - 20) * math.cos(angle)
                y2 = center_y + (radius - 20) * math.sin(angle)
                self.canvas.create_line(x1, y1, x2, y2, fill=self.dial_color, width=2)
            elif i % 1 == 0:
                # Small markers for every position
                x1 = center_x + (radius - 5) * math.cos(angle)
                y1 = center_y + (radius - 5) * math.sin(angle)
                x2 = center_x + (radius - 12) * math.cos(angle)
                y2 = center_y + (radius - 12) * math.sin(angle)
                self.canvas.create_line(x1, y1, x2, y2, fill="#BDC3C7", width=1)

            # Draw numbers for every 10th position
            if i % 10 == 0:
                text_x = center_x + (radius - 45) * math.cos(angle)
                text_y = center_y + (radius - 45) * math.sin(angle)

                # Special styling for position 0
                if i == 0:
                    font_size = 14
                    font_weight = "bold"
                    color = self.zero_color
                    # Add background circle for 0
                    self.canvas.create_oval(
                        text_x - 12,
                        text_y - 12,
                        text_x + 12,
                        text_y + 12,
                        fill="white",
                        outline=self.zero_color,
                        width=2,
                    )
                else:
                    font_size = 12
                    font_weight = "bold"
                    color = self.dial_color
                    # Add subtle background for other numbers
                    self.canvas.create_oval(
                        text_x - 10,
                        text_y - 10,
                        text_x + 10,
                        text_y + 10,
                        fill="white",
                        outline="#BDC3C7",
                        width=1,
                    )

                self.canvas.create_text(
                    text_x,
                    text_y,
                    text=str(i),
                    font=("Arial", font_size, font_weight),
                    fill=color,
                )

        # Highlight position 0 with a special marker
        angle_0 = -math.pi / 2
        x_0 = center_x + (radius - 25) * math.cos(angle_0)
        y_0 = center_y + (radius - 25) * math.sin(angle_0)
        self.canvas.create_oval(
            x_0 - 10,
            y_0 - 10,
            x_0 + 10,
            y_0 + 10,
            fill=self.zero_color,
            outline="darkgreen",
            width=3,
            tags="zero_marker",
        )

        # Add center dot
        self.canvas.create_oval(
            center_x - 3,
            center_y - 3,
            center_x + 3,
            center_y + 3,
            fill=self.dial_color,
            outline=self.dial_color,
        )

        # Draw current position
        self.draw_current_position()

    def draw_current_position(self):
        """Draw the current position indicator."""
        # Remove old position marker
        self.canvas.delete("position")

        # Get actual canvas dimensions
        self.canvas.update()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Ensure minimum size
        if width < 100 or height < 100:
            width = height = 500

        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2 - 60

        # Calculate angle for current position (0 is at top, clockwise)
        angle = (self.current_position / 100) * 2 * math.pi - math.pi / 2

        # Position on the dial
        dial_x = center_x + (radius - 15) * math.cos(angle)
        dial_y = center_y + (radius - 15) * math.sin(angle)

        # Draw pointer line from center
        self.canvas.create_line(
            center_x,
            center_y,
            dial_x,
            dial_y,
            fill=self.position_color,
            width=4,
            tags="position",
        )

        # Draw position dot
        self.canvas.create_oval(
            dial_x - 8,
            dial_y - 8,
            dial_x + 8,
            dial_y + 8,
            fill=self.position_color,
            outline="darkred",
            width=2,
            tags="position",
        )

        # Position text - place it outside the dial
        text_radius = radius + 25
        text_x = center_x + text_radius * math.cos(angle)
        text_y = center_y + text_radius * math.sin(angle)

        # Create background for text
        self.canvas.create_oval(
            text_x - 15,
            text_y - 12,
            text_x + 15,
            text_y + 12,
            fill="white",
            outline=self.position_color,
            width=2,
            tags="position",
        )

        # Position number
        self.canvas.create_text(
            text_x,
            text_y,
            text=str(self.current_position),
            font=("Arial", 11, "bold"),
            fill=self.position_color,
            tags="position",
        )

    def update_stats(self):
        """Update the statistics display."""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)

        # Calculate elapsed time if animation is running
        elapsed_str = ""
        if self.is_animating and self.start_time:
            elapsed = time.perf_counter() - self.start_time
            if elapsed < 60:
                elapsed_str = f"\nElapsed: {elapsed:.1f}s"
            else:
                minutes = int(elapsed // 60)
                seconds = elapsed % 60
                elapsed_str = f"\nElapsed: {minutes}m {seconds:.1f}s"
        elif self.end_time and self.start_time:
            total_time = self.end_time - self.start_time
            if total_time < 60:
                elapsed_str = f"\nTotal: {total_time:.2f}s"
            else:
                minutes = int(total_time // 60)
                seconds = total_time % 60
                elapsed_str = f"\nTotal: {minutes}m {seconds:.1f}s"

        stats = f"""Position: {self.current_position}
Zero Crossings: {self.zero_crossings}
Commands Loaded: {len(self.commands)}
Current Command: {self.current_command_index + 1}
Remaining: {len(self.commands) - self.current_command_index}

Animation: {'Running' if self.is_animating else 'Stopped'}
Speed: {self.animation_speed}ms
Mode: {'Step-by-step' if self.step_mode else 'Smooth'}{elapsed_str}"""

        self.stats_text.insert(1.0, stats)
        self.stats_text.config(state=tk.DISABLED)

    def load_file(self):
        """Load commands from a file."""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=".",
        )

        if filename:
            try:
                with open(filename, "r") as f:
                    self.commands = [line.strip() for line in f if line.strip()]
                self.reset_animation()
                self.status_label.config(
                    text=f"Loaded {len(self.commands)} commands from {os.path.basename(filename)}"
                )
                messagebox.showinfo(
                    "Success", f"Loaded {len(self.commands)} commands successfully!"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def load_test_data(self):
        """Load sample test data."""
        self.commands = ["R10", "L5", "R60", "L25", "R100", "L150"]
        self.reset_animation()
        self.status_label.config(text="Loaded sample test commands")

    def load_default_data(self):
        """Load default input file if it exists."""
        if os.path.exists("input.txt"):
            try:
                with open("input.txt", "r") as f:
                    self.commands = [line.strip() for line in f if line.strip()]
                self.status_label.config(
                    text=f"Loaded {len(self.commands)} commands from input.txt"
                )
            except Exception as e:
                self.load_test_data()
        else:
            self.load_test_data()

    def start_animation(self):
        """Start the animation."""
        if not self.commands:
            messagebox.showwarning("No Data", "Please load commands first!")
            return

        if self.current_command_index >= len(self.commands):
            self.reset_animation()

        self.is_animating = True
        self.play_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)

        # Record start time
        self.start_time = time.perf_counter()
        self.end_time = None

        # Start animation in a separate thread to avoid blocking UI
        self.animate_next_step()

    def pause_animation(self):
        """Pause the animation."""
        self.is_animating = False
        self.play_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)

    def reset_animation(self):
        """Reset animation to beginning."""
        self.is_animating = False
        self.current_position = START_POSITION
        self.zero_crossings = 0
        self.current_command_index = 0

        # Reset timing
        self.start_time = None
        self.end_time = None

        self.play_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)

        # Clear canvas and redraw
        self.canvas.delete("path")
        self.draw_current_position()
        self.update_stats()
        self.update_progress()

        self.command_label.config(text="Ready")
        self.status_label.config(text="Reset to starting position")

    def animate_next_step(self):
        """Animate the next step in the sequence."""
        if not self.is_animating or self.current_command_index >= len(self.commands):
            if self.current_command_index >= len(self.commands):
                # Record end time and calculate duration
                self.end_time = time.perf_counter()
                duration = self.end_time - self.start_time if self.start_time else 0

                self.status_label.config(text="Animation complete!")

                # Format duration nicely
                if duration < 1:
                    duration_str = f"{duration*1000:.1f} milliseconds"
                elif duration < 60:
                    duration_str = f"{duration:.2f} seconds"
                else:
                    minutes = int(duration // 60)
                    seconds = duration % 60
                    duration_str = f"{minutes}m {seconds:.1f}s"

                mode_str = "Step-by-step" if self.step_mode else "Smooth"

                messagebox.showinfo(
                    "Animation Complete! 🎉",
                    f"Animation finished!\n\n"
                    f"📍 Final position: {self.current_position}\n"
                    f"🎯 Total zero crossings: {self.zero_crossings}\n"
                    f"📊 Commands processed: {len(self.commands)}\n"
                    f"⏱️  Total time: {duration_str}\n"
                    f"🎮 Mode: {mode_str}\n"
                    f"⚡ Speed: {self.animation_speed}ms per step",
                )
            self.pause_animation()
            return

        # Get current command
        command = self.commands[self.current_command_index]
        try:
            direction, distance = parse_command(command)
        except Exception as e:
            messagebox.showerror(
                "Invalid Command", f"Error parsing command '{command}': {e}"
            )
            self.pause_animation()
            return

        self.command_label.config(
            text=f"{command} (Step {self.current_command_index + 1}/{len(self.commands)})"
        )

        if self.step_mode:
            # Step-by-step mode: move one position at a time
            self.animate_single_step(direction, distance)
        else:
            # Smooth mode: jump directly to final position
            self.animate_command_directly(direction, distance)

    def animate_single_step(self, direction: int, distance: int):
        """Animate moving one step at a time."""
        if distance <= 0:
            # Command finished, move to next
            self.current_command_index += 1
            self.update_progress()
            self.root.after(self.animation_speed, self.animate_next_step)
            return

        # Move one step
        old_position = self.current_position
        self.current_position += direction

        # Handle wrapping
        if self.current_position < 0:
            self.current_position = POSITION_RANGE - 1
        elif self.current_position >= POSITION_RANGE:
            self.current_position = 0

        # Check for zero crossing
        if self.current_position == 0:
            self.zero_crossings += 1

        # Draw path
        self.draw_movement_path(old_position, self.current_position)
        self.draw_current_position()
        self.update_stats()

        # Continue with remaining distance
        self.root.after(
            self.animation_speed,
            lambda: self.animate_single_step(direction, distance - 1),
        )

    def animate_command_directly(self, direction: int, distance: int):
        """Animate jumping directly to final position after calculating crossings."""
        # Calculate result using our optimized method
        crossings = self.calculate_zero_crossings_visual(
            self.current_position, direction, distance
        )

        # Update position
        new_position = (self.current_position + direction * distance) % POSITION_RANGE
        old_position = self.current_position

        # Draw path
        self.draw_movement_path(old_position, new_position)

        # Update state
        self.current_position = new_position
        self.zero_crossings += crossings

        self.draw_current_position()
        self.update_stats()

        # Move to next command
        self.current_command_index += 1
        self.update_progress()
        self.root.after(self.animation_speed, self.animate_next_step)

    def calculate_zero_crossings_visual(
        self, position: int, direction: int, distance: int
    ) -> int:
        """Calculate zero crossings with visual feedback."""
        if distance == 0:
            return 0

        zero_crossings = 0

        if direction > 0:  # Moving right
            if position == 0:
                distance_to_first_zero = 100
            else:
                distance_to_first_zero = 100 - position
        else:  # Moving left
            if position == 0:
                distance_to_first_zero = 100
            else:
                distance_to_first_zero = position

        if distance >= distance_to_first_zero:
            zero_crossings += 1
            remaining_distance = distance - distance_to_first_zero
            zero_crossings += remaining_distance // 100

        return zero_crossings

    def draw_movement_path(self, from_pos: int, to_pos: int):
        """Draw a path showing movement."""
        self.canvas.update()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100 or height < 100:
            width = height = 500

        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2 - 60

        # Calculate angles
        from_angle = (from_pos / 100) * 2 * math.pi - math.pi / 2
        to_angle = (to_pos / 100) * 2 * math.pi - math.pi / 2

        # Calculate positions on the dial circle
        path_radius = radius * 0.8
        from_x = center_x + path_radius * math.cos(from_angle)
        from_y = center_y + path_radius * math.sin(from_angle)
        to_x = center_x + path_radius * math.cos(to_angle)
        to_y = center_y + path_radius * math.sin(to_angle)

        # Draw path line with arrow
        self.canvas.create_line(
            from_x, from_y, to_x, to_y, fill=self.path_color, width=3, tags="path"
        )

        # Add small circle at destination
        self.canvas.create_oval(
            to_x - 3,
            to_y - 3,
            to_x + 3,
            to_y + 3,
            fill=self.path_color,
            outline=self.path_color,
            tags="path",
        )

    def update_progress(self):
        """Update progress bar."""
        if self.commands:
            progress = (self.current_command_index / len(self.commands)) * 100
            self.progress_var.set(progress)

    def update_speed(self, value):
        """Update animation speed."""
        self.animation_speed = int(float(value))

    def toggle_step_mode(self):
        """Toggle between step-by-step and smooth animation."""
        self.step_mode = self.step_mode_var.get()

    def on_canvas_resize(self, event):
        """Handle canvas resize events."""
        # Redraw the dial when canvas is resized
        self.root.after(10, self.draw_dial)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Visual GUI for Day 1 Circular Dial")
    parser.add_argument("--file", help="Input file to load", default=None)

    args = parser.parse_args()

    # Create GUI
    root = tk.Tk()
    app = DialVisualizer(root)

    # Load specified file if provided
    if args.file and os.path.exists(args.file):
        try:
            with open(args.file, "r") as f:
                app.commands = [line.strip() for line in f if line.strip()]
            app.reset_animation()
            app.status_label.config(
                text=f"Loaded {len(app.commands)} commands from {args.file}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load {args.file}: {e}")

    # Handle window closing
    def on_closing():
        app.is_animating = False
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start GUI
    root.mainloop()


if __name__ == "__main__":
    main()
