
import regex as re
import time
import copy
from itertools import product


def extract_str_data(file_path : str) -> str:
    with open(file_path, 'r') as file:
        return file.read()
    
def generate_combinations(symbols : str, times : int) -> list[list[str]]:
    number_of_combinations = len(symbols) ** times
    combinations = []
    
    for i in range(number_of_combinations):
        combination = []
        temp = i
        
        for _ in range(times):
            combination.append(symbols[temp % len(symbols)])
            temp = temp // len(symbols)
        
        combinations.append(combination)
    
    return combinations

def calculate(combination : str, arr : list, target_number : int, part : int = 1) -> bool:

    sum_value = arr[0]
    
    for i in range(1, len(arr)):
        if combination[i - 1] == '*':
            sum_value *= arr[i]
        elif combination[i - 1] == '+':
            sum_value += arr[i]
        else:  
            if part == 2:
                sum_value = int(str(sum_value) + str(arr[i]))
    
    return sum_value == target_number

def parse_lines(input_data : str) -> list[str]:

    return input_data.strip().split('\n')

def solution_one(path : str) -> int:
    input_data = extract_str_data(path)

    lines = parse_lines(input_data)
    amount = 0
    
    for line in lines:
        target_number = int(line.split(':')[0])
        arr = list(map(int, line.split(':')[1].strip().split()))
        
        symbols = ['*', '+']
        times = len(arr) - 1
        combinations = generate_combinations(symbols, times)
        
        for combination in combinations:
            if calculate(combination, arr, target_number):
                amount += target_number
                break
    
    return amount

def solution_two(path : str) -> int:
    input_data = extract_str_data(path)

    lines = parse_lines(input_data)
    amount = 0
    
    for line in lines:
        target_number = int(line.split(':')[0])
        arr = list(map(int, line.split(':')[1].strip().split()))
        
        symbols = ['*', '+', '||']
        times = len(arr) - 1
        combinations = generate_combinations(symbols, times)
        
        for combination in combinations:
            if calculate(combination, arr, target_number, 2):
                amount += target_number
                break
    
    return amount