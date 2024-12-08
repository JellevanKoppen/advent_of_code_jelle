from copy import deepcopy

def get_puzzle_input(file_name):
    puzzle_input = ""
    with open(file_name, 'r') as file_input:
        puzzle_input = file_input.read().splitlines()  
    return puzzle_input

def define_if_possible(answer, numbers, amount_of_multiplications):
    max_amount_of_operators = len(numbers) - 1

    result = numbers[0]
    for i in range(1, len(numbers)):
        if i < amount_of_multiplications:
            print(f"Multiplying {result} * {numbers[i]}")
            result *= numbers[i]
        else:
            print(f"Adding {result} + {numbers[i]}")
            result += numbers[i]
    if result == answer:
        print(f"Found answer: {numbers} = {result} (amount of *'s left to right: {amount_of_multiplications})")
        return True
    else:
        print(f"Result not equal {result} {answer}")
    
    if amount_of_multiplications > max_amount_of_operators:
        print("returning, max amount is reached")
        return False
    
    amount_of_multiplications += 1

    return define_if_possible(answer, numbers, amount_of_multiplications)
    

def exercise_1(puzzle_input):
    total_sum = 0
    for line in puzzle_input:
        answer, equation = line.split(':')
        answer = int(answer)
        numbers = [int(x) for x in equation.strip().split(" ")]
        print(numbers)

        is_possible = define_if_possible(answer, numbers, 0)
        print(is_possible)
        if is_possible:
            total_sum += answer
        
    print(total_sum)
    

def main():
    puzzle_input = get_puzzle_input('input')
    exercise_1(puzzle_input) # 88612406721 (too low)
main()
