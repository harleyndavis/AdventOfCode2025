"""
Processes movement commands from an input file to update a current position value.
Reads a file containing movement commands where each line starts with 'R' (right/positive)
or 'L' (left/negative) followed by a numeric distance. Starting from position 50,
the function moves step by step in the specified direction for the given distance.
The position wraps around in a circular manner:
- If position goes below 0, it wraps to 99
- If position goes above 99, it wraps to 0
This creates a circular buffer/ring of positions from 0-99 where movement continues
seamlessly across boundaries.
Args:
    filename (command line argument): Path to input file (defaults to './Day1/input.txt')
Returns:
    None (prints password count)
Side Effects:
    - Reads from file system
    - Prints result to stdout
"""

import sys

# Get filename from command line argument, or use default
filename = sys.argv[1] if len(sys.argv) > 1 else "./Day1/input.txt"

try:
    with open(filename, "r") as file:
        zero_crossings = 0
        content = file.read()
        position = 50
        for line in content.splitlines():
            direction = 1 if line[0] == "R" else -1
            distance = int(line[1:])

            # # Move step by step to handle wrapping
            # # O(n) approach, not efficient for large distances
            # # Greatly improves efficiency to calculate mathematically
            # while distance > 0:
            #     currentValue += direction
            #     distance -= 1

            #     if currentValue < 0:
            #         currentValue = 99
            #     if currentValue > 99:
            #         currentValue = 0

            #     if currentValue == 0:
            #         password += 1

            # Calculate mathematically instead of step by step
            # O(1) approach.
            if direction == 1:  # Moving right (positive direction)
                # Calculate how many times we'd pass position 0

                # Distance from current position to next 0 (going right)
                if position == 0:
                    # Already at 0, first crossing is after 100 steps
                    distance_to_first_zero = 100
                else:
                    # Distance to wrap around to 0: (100 - currentValue)
                    distance_to_first_zero = 100 - position

                if distance >= distance_to_first_zero:
                    # We'll cross at least one zero
                    zero_crossings += 1
                    remaining_distance = distance - distance_to_first_zero
                    # Each additional 100 steps crosses zero again
                    zero_crossings += remaining_distance // 100

            else:  # Moving left (negative direction)
                # We pass 0 when going from 1 to 0
                # Distance from current position to next 0 (going left)
                if position == 0:
                    # Already at 0, first crossing is after 100 steps left (to 0 again)
                    distance_to_first_zero = 100
                else:
                    # Distance to reach 0 going left: currentValue steps
                    distance_to_first_zero = position

                if distance >= distance_to_first_zero:
                    # We'll cross at least one zero
                    zero_crossings += 1
                    remaining_distance = distance - distance_to_first_zero
                    # Each additional 100 steps crosses zero again
                    zero_crossings += remaining_distance // 100

            # Update position for next iteration
            position = (position + direction * distance) % 100

        print("Password: " + str(zero_crossings))

except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)
