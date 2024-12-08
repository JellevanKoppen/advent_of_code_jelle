from time import sleep

o_hits = 0
initial_guard_location = None
initial_guard_direction = None

def get_puzzle_input(file_name):
    puzzle_input = ""
    with open(file_name, 'r') as file_input:
        puzzle_input = file_input.read().splitlines()  
    return puzzle_input

def convert_to_matrix(puzzle_input):
    matrix = []
    for line in puzzle_input:
        matrix.append(list(line))
    return matrix

def get_guard_coordinates(puzzle_input):
    guard_identifiers = "^<>v"
    for y in range(0, len(puzzle_input)):
        row = puzzle_input[y]
        for x in range(0, len(row)):
            column = row[x]
            if column in guard_identifiers:
                return(x,y)
            
def mark_guard_location(map, guard_location):
    x,y = guard_location
    map[y][x] = "X"

def place_guard_on_map(map, guard_direction, guard_location):
    x,y = guard_location
    map[y][x] = guard_direction

def get_coordinates(map, coordinates):
    x,y = coordinates
    return map[y][x]

def set_next_step(map, guard_location, guard_direction):
    global o_hits
    x_outer_bound = len(map[0]) - 1
    y_outer_bound = len(map) - 1
    guard_x, guard_y = guard_location
    next_direction = ""
    if guard_direction == "^":
        # Move up
        if guard_y == 0:
            return True  # Guard moved out of map
        guard_y -= 1
        next_direction = ">"
    elif guard_direction == ">":
        # Move right
        if guard_x == x_outer_bound:
            return True  # Guard moved out of map
        guard_x += 1
        next_direction = "v"
    elif guard_direction == "<":
        # Move left
        if guard_x == 0:
            return True  # Guard moved out of map
        guard_x -= 1
        next_direction = "^"
    elif guard_direction == "v":
        # Move down
        if guard_y == y_outer_bound:
            return True  # Guard moved out of map
        guard_y += 1
        next_direction = "<"
    else:
        raise RuntimeError(f"Received wrong guard direction {guard_direction}")

    assumed_next_step = get_coordinates(map, (guard_x, guard_y))

    if assumed_next_step == "#":
        # Obstacle detected, turn right instead
        place_guard_on_map(map, next_direction, guard_location)
    elif assumed_next_step == "O":
        print(f"O - hit!")
        o_hits += 1
        if o_hits >= 4:
            # Guard hit same obstacle 4 times, assume guard is in loop
            return True
        place_guard_on_map(map, next_direction, guard_location)
    else:
        # No obstacle detected, place guard on next tile
        place_guard_on_map(map, guard_direction, (guard_x, guard_y))

    return False

def print_map(map):
    readable_map = [''.join(row) for row in map]
    for y in readable_map:
        print(y)

def count_steps(map):
    x_counter = 0
    for y in map:
        for x in y:
            if x == "X":
                x_counter += 1
    return x_counter

def find_obstacle(map, obstacle_nr):
    global initial_guard_location
    initial_x, initial_y = initial_guard_location
    obstacles_found = 0
    for y in range(0, len(map)):
        row = map[y]
        for x in range(0, len(row)):
            if x == initial_x and y == initial_y:
                continue
            if row[x] == "X":
                # Obstacle found
                obstacles_found += 1
                if obstacles_found == obstacle_nr:
                    return (x,y)
    return None

def get_next_possible_obstacle(obstacle_nr):
    global initial_guard_location
    path_history = get_puzzle_input('path_history')
    guard_map = convert_to_matrix(path_history)
    next_obstacle = find_obstacle(guard_map, obstacle_nr)
    return next_obstacle

def exercise_1(puzzle_input):
    is_finished = False
    map = convert_to_matrix(puzzle_input)
    while not is_finished:
        guard_location = get_guard_coordinates(map)
        guard_direction = get_coordinates(map, guard_location)
        mark_guard_location(map, guard_location)
        is_finished = set_next_step(map, guard_location, guard_direction)
    steps = count_steps(map)
    print(f"Guard took {steps} steps")
    
def place_obstacle(map, coordinates):
    x, y = coordinates
    print(f"Placing obstacle at {x},{y}")
    map[y][x] = "O"
    
def remove_obstacle(map, coordinates):
    x, y = coordinates
    map[y][x] = "."

def remove_guard_from_map(map):
    guard_location = get_guard_coordinates(map)
    x, y = guard_location
    map[y][x] = "."

def exercise_2(puzzle_input):
    global o_hits
    global initial_guard_direction
    global initial_guard_location

    map = convert_to_matrix(puzzle_input)

    obstacle_nr = 461

    initial_guard_location = get_guard_coordinates(map)
    initial_guard_direction = get_coordinates(map, initial_guard_location)
    infinite_loops_found = 0
    obstacle = get_next_possible_obstacle(obstacle_nr)

    while obstacle:
        print(f"Placing obstacle nr {obstacle_nr}")
        place_obstacle(map, obstacle)
        place_guard_on_map(map, initial_guard_direction, initial_guard_location)

        o_hits = 0
        is_finished = False
        step_counter = 0
        while not is_finished:
            step_counter += 1
            guard_location = get_guard_coordinates(map)
            guard_direction = get_coordinates(map, guard_location)
            mark_guard_location(map, guard_location)
            is_finished = set_next_step(map, guard_location, guard_direction)
            if step_counter > 20000:
                infinite_loops_found += 1
                print("indirect infinite loop found by repetition")
                remove_guard_from_map(map)
                is_finished = True

        if o_hits >= 4:
            infinite_loops_found += 1
            print(f"Infinite loop found! ({infinite_loops_found})")

        remove_obstacle(map, obstacle)
        obstacle_nr += 1
        obstacle = get_next_possible_obstacle(obstacle_nr)

    
    print(f"Infinite loops found {infinite_loops_found}")
    

def main():
    puzzle_input = get_puzzle_input('input')
    # exercise_1(puzzle_input)
    exercise_2(puzzle_input) #1392 (too low) > 1575

main()
