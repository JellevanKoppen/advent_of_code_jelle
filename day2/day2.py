from copy import deepcopy

def get_puzzle_input():
    reports = []
    with open("input", 'r') as file_input:
        lines = file_input.readlines()
        for line in lines:
            report = []
            numbers = line.rstrip('\n').split(" ")
            for number in numbers:
                report.append(int(number))
            reports.append(report)         
    return reports

def analyse_report(report: list, log=False):

    if report[0] > report[1]:
        report.reverse()

    for i in range(0, len(report)-1):
        if report[i] >= report[i+1]:
            if log:
                print(f"{report[i]} is bigger or equal then {report[i+1]}, check failed.")
            return False
        delta = report[i+1] - report[i]
        if delta > 3:
            if log:
                print(f"Delta of reports {report[i+1]} - {report[i]} > 3 ({delta}), check failed.")
            return False
    
    return True

def analyse_report_with_dampener(report: list):

    print(f"Re-analysing report {report}")

    for i in range(0, len(report)):
        dampened_report = deepcopy(report)
        result = dampened_report.pop(i)
        print(f"popping {result}")
        is_safe = analyse_report(dampened_report, log=True)
        if is_safe:
            print(f"Report scan successfull after applying problem dampener.")
            return True
    
    return False


def exercise_1():
    reports = get_puzzle_input()

    safe_counter = 0

    for report in reports:
        is_safe = analyse_report(report)
        if is_safe:
            safe_counter += 1
    
    print(f"Amount of safe reports: {safe_counter}")

def exercise_2():
    reports = get_puzzle_input()

    safe_counter = 0
    dampened_report_counter = 0

    for report in reports:
        is_safe = analyse_report(report)
        if is_safe:
            safe_counter += 1
        else:
            is_safe = analyse_report_with_dampener(report)
            if is_safe:
                dampened_report_counter += 1

    total_safe_reports = dampened_report_counter + safe_counter
    
    print(f"Amount of safe reports: {safe_counter}, with dampening {dampened_report_counter} reports became safe. Total ({total_safe_reports})")

def main():
    # exercise_1()  # 686
    exercise_2()  # 710 (too low), 757 (too high)
    
    

main()