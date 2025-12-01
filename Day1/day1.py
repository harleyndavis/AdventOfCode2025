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
        None (reads from './Day1/input.txt')
    Returns:
        None (modifies currentValue in place)
    Side Effects:
        - Reads from file system
        - Modifies the currentValue variable
    """

with open('./Day1/input.txt', 'r') as file:
    password = 0
    content = file.read()
    currentValue = 50
    for line in content.splitlines():
        direction = 1 if line[0] == 'R' else -1
        distance = int(line[1:])
        while distance > 0:
            currentValue += direction
            distance -= 1

            if currentValue < 0:
                currentValue = 99
            if currentValue > 99:
                currentValue = 0

        if currentValue == 0:
            password += 1

    print(password)