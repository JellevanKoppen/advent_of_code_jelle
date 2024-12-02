def get_puzzle_input():
    list_a = []
    list_b = []
    with open("input", 'r') as file_input:
        lines = file_input.readlines()
        for line in lines:
            numbers = line.rstrip('\n').split("   ")
            list_a.append(int(numbers[0]))
            list_b.append(int(numbers[1]))
            
    return list_a, list_b

def exercise_1():
    list_a, list_b = get_puzzle_input()

    list_a.sort()
    list_b.sort()

    total_difference = 0

    for i in range(0, len(list_a)):
        max_val = max(list_a[i], list_b[i])
        min_val = min(list_a[i], list_b[i])
        difference = max_val - min_val
        total_difference += difference
        print(f"{max_val} - {min_val} = {difference} ({total_difference})")


    print(total_difference)
    print(f"total length A {len(list_a)}, B {len(list_b)}, ")

def exercise_2():
    list_a, list_b = get_puzzle_input()

    similarity_score = 0

    for a_number in list_a:
        occurrences = 0
        for b_number in list_b:
            if b_number == a_number:
                occurrences += 1
        
        similarity = a_number * occurrences
        similarity_score += similarity

        print(f"{a_number} occured {occurrences} times in list B ({similarity}). ({similarity_score})")





def main():
    # exercise_1()
    exercise_2()
    
    

main()