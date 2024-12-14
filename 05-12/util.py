
import regex as re

def extract_str_data(file_path : str):
    with open(file_path, 'r') as file:
        return file.read()
    

def get_rules_and_execution_order(input_data):
    arr_rules = []
    arr_rule_execution = []
    
    for line in input_data.split('\n'):
        if '|' in line:
            arr_rules.append(line)
        elif line.strip() and ',' in line:
            arr_rule_execution.append(line)
    
    return arr_rules, arr_rule_execution

# Part 1 - Solution
def solution_one(path : str):
    input_data = extract_str_data(path)
    arr_rules, arr_rule_execution = get_rules_and_execution_order(input_data)
    
    arr_temp = []

    for line in arr_rule_execution:
        rule_correct = True
        pages = line.split(',')
        
        for index in range(1, len(pages)):
            for previous_index in range(index):
                rule = f"{pages[index]}|{pages[previous_index]}"
                if rule in arr_rules:
                    rule_correct = False
                    break
            
            if not rule_correct:
                break
        
        if rule_correct:
            arr_temp.append(line)
    
    result = sum(
        int(line.split(',')[len(line.split(',')) // 2])
        for line in arr_temp
    )
    
    return result

# Part 2 - Solution
def solution_two(path : str):
    input_data = extract_str_data(path)
    arr_rules, arr_rule_execution = get_rules_and_execution_order(input_data)
    
    arr_wrong_rules = {}
    
    for line in arr_rule_execution:
        rule_correct = True
        rules_violated = []
        pages = line.split(',')
        
        for index in range(1, len(pages)):
            for previous_index in range(index):
                rule = f"{pages[index]}|{pages[previous_index]}"
                if rule in arr_rules:
                    rules_violated.append(rule)
                    rule_correct = False
        
        if not rule_correct:
            arr_wrong_rules[line] = rules_violated
    
    def in_correct_order(x, y):
        return f"{x}|{y}" in arr_rules
    
    result = 0
    for update in arr_wrong_rules:
        pages = update.split(',')
        
        def compare(a, b):
            if in_correct_order(a, b):
                return -1
            elif in_correct_order(b, a):
                return 1
            return 0
        
        for i in range(len(pages)):
            for j in range(0, len(pages) - i - 1):
                if compare(pages[j], pages[j + 1]) > 0:
                    pages[j], pages[j + 1] = pages[j + 1], pages[j]
        
        middle_index = len(pages) // 2
        result += int(pages[middle_index])
    
    return result