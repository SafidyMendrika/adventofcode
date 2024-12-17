
import regex as re
import time
import copy
from itertools import product
from dataclasses import dataclass


def extract_str_data(file_path : str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def get_line(input_data: str) -> list:
    line = []
    for i, digit in enumerate(input_data):
        if i % 2 == 0:
            line.extend([int(i // 2)] * int(digit))
        else:
            line.extend(['.'] * int(digit))
    return line

def solution_one(path : str) -> int:
    input_data = extract_str_data(path)
    temp_line = get_line(input_data)
    length = len(temp_line) - 1
    
    stop = length - temp_line.count('.')
    
    dot_index = temp_line.index('.')
    
    while length > 0:
        if length == stop:
            break
        
        if isinstance(temp_line[length], int):
            temp_line[dot_index], temp_line[length] = temp_line[length], '.'
            dot_index = temp_line.index('.')
        
        length -= 1
    
    checksum = sum(
        i * val for i, val in enumerate(temp_line) 
        if isinstance(val, int)
    )
    
    return checksum