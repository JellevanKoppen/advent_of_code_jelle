import re

def get_puzzle_input():
    puzzle_input = ""
    with open("input", 'r') as file_input:
        puzzle_input = file_input.read()         
    return puzzle_input


def extract_numbers(input):
    output = re.findall(r'\d+', input)
    return (int(output[0]), int(output[1]))


def exercise_1(puzzle_input):
    pattern = r"mul\(\d+,\d+\)"

    results = re.findall(pattern, puzzle_input)
    total_sum = 0

    for item in results:
        result = extract_numbers(item)
        product = result[0] * result[1]
        total_sum += product
        print(f"{result} ({product}) ({total_sum})")



def exercise_2(puzzle_input):
    dos = puzzle_input.split("do()")
    dos_split = [do.split("don't()")[0] for do in dos]

    new_puzzle_input = ""
    for piece in dos_split:
        new_puzzle_input += piece
    
    exercise_1(new_puzzle_input)
    

def main():
    puzzle_input = get_puzzle_input()
    # exercise_1(puzzle_input)
    exercise_2(puzzle_input)

main()
