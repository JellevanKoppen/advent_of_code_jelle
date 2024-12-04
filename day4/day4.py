from copy import deepcopy

def get_puzzle_input():
    puzzle_input = ""
    with open("input", 'r') as file_input:
        puzzle_input = file_input.read().splitlines()      
    return puzzle_input

def delete_offset(puzzle_input):
    offset = 0
    puzzle_output = []
    for line in puzzle_input:
        if offset == 3:
            offset = 0  # Reset offset
        else:
            offset += 1
            puzzle_output.append(line[:-offset])
    return puzzle_output

def has_xmas(sub_line):
    return sub_line == "XMAS" or sub_line == "SAMX"

def is_correction_needed(line, offset, mirrored=False):
    # Offset is the part of the string that was the edge of the puzzle input
    # Check if left of the offset and right of the offset, not mistakenly the word XMAS was formed

    if mirrored:
        # Check for [X-MAS]
        if offset >= 3 and offset + 1 <= len(line):
            if has_xmas(line[offset-3:offset+1]):
                return True
    else:
        # Check for [X-MAS]
        if offset + 4 <= len(line):
            if has_xmas(line[offset:offset+4]):
                return True

    # Check for [XM-AS]
    if offset >= 1 and offset + 3 <= len(line):
        if has_xmas(line[offset-1:offset+3]):
            return True

    # Check for [XMA-S]
    if offset >= 2 and offset + 2 <= len(line):
        if has_xmas(line[offset-2:offset+2]):
            return True
    
    return False

def check_for_xmas(puzzle_input, offset = False, mirror=False):
    xmas = 0
    offset_count = 0
    correction_needed = False
    for line in puzzle_input:
        if offset:
            correction_needed = is_correction_needed(line, offset_count, mirror)
            offset_count+=1
        xmas += line.count("XMAS")
        xmas += line.count("SAMX") # Reverse
        if correction_needed:
            xmas -= 1
    return xmas

def convert_to_matrix(puzzle_input):
    matrix = []
    for line in puzzle_input:
        matrix.append(list(line))
    return matrix

def shift_matrix(matrix: list):
    shifter = 0
    for row in matrix:
        counter = 0
        while counter < shifter:
            row.append(row.pop(0))
            counter += 1
        shifter += 1
    return matrix

def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]

def matrix_to_puzzle_input(matrix):
    return [''.join(row) for row in matrix]

def exercise_1(puzzle_input):
    # check horizontally
    total_horizontal = check_for_xmas(puzzle_input)
    
    # convert puzzle to matrix
    puzzle_matrix = convert_to_matrix(puzzle_input)

    # check vertically
    puzzle_matrix_transposed = transpose_matrix(deepcopy(puzzle_matrix))
    puzzle_input_vertical = matrix_to_puzzle_input(puzzle_matrix_transposed)
    total_vertical = check_for_xmas(puzzle_input_vertical)

    # check diagonally (clockwise)
    shifted_matrix = shift_matrix(deepcopy(puzzle_matrix))
    shifted_transposed_matrix = transpose_matrix(shifted_matrix)
    puzzle_input_diagonal = matrix_to_puzzle_input(shifted_transposed_matrix)
    puzzle_input_diagonal.reverse()

    with open('temp1', 'w+') as file:
        for line in puzzle_input_diagonal:
            file.write(line + '\n')

    total_diagonal_clockwise = check_for_xmas(puzzle_input_diagonal, offset=True)

    # check diagonally (counter_clockwise)
    puzzle_matrix.reverse()
    shifted_matrix = shift_matrix(deepcopy(puzzle_matrix))
    shifted_matrix.reverse()
    shifted_transposed_matrix = transpose_matrix(shifted_matrix)
    puzzle_input_diagonal = matrix_to_puzzle_input(shifted_transposed_matrix)
    total_diagonal_counter_clockwise = check_for_xmas(puzzle_input_diagonal, offset=True, mirror=True)

    with open('temp2', 'w+') as file:
        for line in puzzle_input_diagonal:
            file.write(line + '\n')

    print(f"{total_horizontal}, {total_vertical}, {total_diagonal_clockwise}, {total_diagonal_counter_clockwise}")
    print(f"Grand total: {sum([total_diagonal_counter_clockwise, total_diagonal_clockwise, total_horizontal, total_vertical])}")

def exercise_2(puzzle_input):

    puzzle_matrix = convert_to_matrix(puzzle_input)
    mas_counter = 0
    for row_index in range(1, len(puzzle_matrix)-1):
        prev_row = puzzle_matrix[row_index-1]
        row = puzzle_matrix[row_index]
        next_row = puzzle_matrix[row_index+1]
        for elem_index in range(1, len(row)-1):
            first_half = False
            second_half = False
            if row[elem_index] == "A":
                if prev_row[elem_index-1] == "M" and next_row[elem_index+1] == "S" or prev_row[elem_index-1] == "S" and next_row[elem_index+1] == "M":
                    first_half = True
                if next_row[elem_index-1] == "M" and prev_row[elem_index+1] == "S" or next_row[elem_index-1] == "S" and prev_row[elem_index+1] == "M":
                    second_half = True
                
                if first_half and second_half:
                    mas_counter += 1
    
    print(f"X-MAS counter: {mas_counter}")

def create_test_output(puzzle_input):

    index = 0
    puzzle_output = []
    puzzle_matrix = convert_to_matrix(puzzle_input)

    for line in puzzle_matrix:
        line[index] = "_"
        line[len(line)-1] = "*"
        index += 1
        puzzle_output.append(line)

    # puzzle_output = shift_matrix(puzzle_output)
    # puzzle_output = transpose_matrix(puzzle_output)
    puzzle_output.reverse()
    po2 = []
    index = 0
    for line in puzzle_output:
        line[index] = "$"
        index +=1
        po2.append(line)

    output = matrix_to_puzzle_input(po2)
    output.reverse()

    with open('test_output', 'w') as file:
        for line in output:
            file.write(line + '\n')
    return output


def main():
    puzzle_input = get_puzzle_input()
    # test_output = create_test_output(puzzle_input)
    exercise_1(puzzle_input)  # 2397
    exercise_2(puzzle_input)  # 1824

main()