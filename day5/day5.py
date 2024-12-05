from copy import deepcopy

def get_puzzle_input(file_name):
    puzzle_input = ""
    with open(file_name, 'r') as file_input:
        puzzle_input = file_input.read().splitlines()  
    return puzzle_input

def get_instructions(puzzle_input):
    retrieving_order = True
    orders = []
    instructions = []
    for line in puzzle_input:
        if line == "":
            retrieving_order = False
            continue
        if retrieving_order:
            orders.append(line)
        else:
            instructions.append([int(x) for x in line.split(",")])
    return orders,instructions


def check_order_list(orders, number):
    """ Returns the numbers that have to come before this number """
    precessors = []
    for order in orders:
        first, second = order.split('|')
        if int(second) == number:
            precessors.append(int(first))
    return precessors


def are_precessors_in_list(instruction, precessors):

    for precessor in precessors:
        if precessor in instruction:
            return precessor  # This value should be lower in the list
    return False

def verify_correct(orders, instruction):
    """ Check if steps are correctly placed in instruction """

    for _ in instruction:
        step = instruction.pop(0)
        precessors = check_order_list(orders, step)
        precessor = are_precessors_in_list(instruction, precessors)
        if precessor:
            return step, precessor
        
    return None, None

def get_middle_item_of_list(list):
    return list[int(len(list) / 2)]

def exercise_1(puzzle_input):
    incorrect_instructions = []
    orders, instructions = get_instructions(puzzle_input)
    total = 0
    amount_of_correct = 0
    for instruction in instructions:
        is_correct = verify_correct(orders, deepcopy(instruction))
        if is_correct:
            amount_of_correct += 1
            middle_item = get_middle_item_of_list(instruction)
            total += middle_item
            print(f"Correct lines: {amount_of_correct} {total} (+{middle_item}) Instruction: {instruction}")
        else:
            incorrect_instructions.append(instruction)
    
def swap_instructions(step, precessor, instruction):
    step_index = 0
    precessor_indexes = []
    for i in range(0, len(instruction)):
        if instruction[i] == step:
            step_index = i
            break
        
    for i in range(0, len(instruction)):
        if instruction[i] == precessor:
            precessor_indexes.append(i)
    
    for precessor_index in precessor_indexes:
        if precessor_index > step_index:  # Only affect precessors after the step
            elem = instruction.pop(precessor_index)
            instruction.insert(step_index, elem)
            print(f"popped {elem} from index {precessor_index} ({precessor}) and inserted in {step_index}")
    
    return instruction

def exercise_2(puzzle_input):
    orders, instructions = get_instructions(puzzle_input)
    correct_instructions = []
    for instruction in instructions:
        finished = False
        while not finished:
            step, precessor = verify_correct(orders, deepcopy(instruction))
            if step is None and precessor is None:
                finished = True
                continue  
            instruction = swap_instructions(step, precessor, instruction)
        correct_instructions.append(instruction)
    
    total = 0
    for instruction in correct_instructions:
        middle_item = get_middle_item_of_list(instruction)
        total += middle_item
        print(f"Total: {total} (+{middle_item})")
    

def main():
    puzzle_input = get_puzzle_input('input')
    exercise_1(puzzle_input)  # 6498
    new_puzzle_input = get_puzzle_input('split_input')
    exercise_2(new_puzzle_input)  # 5017

main()
