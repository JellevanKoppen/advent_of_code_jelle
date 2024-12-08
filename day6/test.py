import sys
from collections import defaultdict
import multiprocessing as mp
from functools import partial


def find_guard(grid):
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "^":
                return x, y


def simulate(grid, gx, gy):
    visited = defaultdict(int)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    current_dir = directions[2]
    rows, cols = len(grid), len(grid[0])

    grid[gx][gy] = "x"
    x, y = gx, gy
    while True:
        while True:
            x += current_dir[0]
            y += current_dir[1]
            if x < 0 or x >= rows or y < 0 or y >= cols:
                return True
            if grid[x][y] == "#":
                x -= current_dir[0]
                y -= current_dir[1]
                break
            grid[x][y] = "x"
            visited[(x, y)] += 1
            if visited[(x, y)] > 4:
                return False

        if current_dir == directions[0]:
            current_dir = directions[2]
        elif current_dir == directions[1]:
            current_dir = directions[3]
        elif current_dir == directions[3]:
            current_dir = directions[0]
        else:
            current_dir = directions[1]


def count_x(grid):
    return sum(row.count("x") for row in grid)


def process_indices(indices, og_grid, gx, gy):
    count = 0
    grid = [row[:] for row in og_grid]

    for i in indices:
        grid[i[0]][i[1]] = "#"
        if not simulate(grid, gx, gy):
            count += 1
        grid[i[0]][i[1]] = "."
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] == "x":
                    grid[x][y] = "."
    return count


def count_options(grid, og_grid, gx, gy, possible_indices):
    chunk_size = len(possible_indices) // 10 + (len(possible_indices) % 10 > 0)
    chunks = [
        possible_indices[i : i + chunk_size]
        for i in range(0, len(possible_indices), chunk_size)
    ]

    with mp.Pool(processes=10) as pool:
        process_func = partial(process_indices, og_grid=og_grid, gx=gx, gy=gy)
        results = pool.map(process_func, chunks)

    return sum(results)


def main():
    print("test")
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        return

    file_name = sys.argv[1]

    with open(file_name) as f:
        grid = [list(line.strip()) for line in f]

    og_grid = [row[:] for row in grid]
    gx, gy = find_guard(grid)
    simulate(grid, gx, gy)
    
    count = count_x(grid)
    print(count)
    # reset guard
    grid[gx][gy] = "^"
    # posible indices are the ones with x
    possible_indices = [
        (x, y)
        for x, row in enumerate(grid)
        for y, cell in enumerate(row)
        if cell == "x"
    ]
    grid = [row[:] for row in og_grid]
    count = count_options(grid, og_grid, gx, gy, possible_indices)
    print(count)


if __name__ == "__main__":
    main()