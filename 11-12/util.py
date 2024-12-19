
import regex as re
import time
import copy
from itertools import product
from dataclasses import dataclass


def extract_str_data(file_path : str) -> str:
    with open(file_path, 'r') as file:
        return file.read().strip()
    

def blink(stone_group : list[str]) -> list[str]: 
    result = []
    for stone in stone_group:
        result.extend(blink_stone(stone))
    
    return result

def blink_stone (stone : str) -> list[str]:
    result = [stone]

    has_rules = False
    if "0" == result[0]:
        result[0] = result[0].replace("0", "1")
        has_rules = True


    if len(result[0]) % 2 == 0:
        mid = len(result[0]) // 2
        result = [str(int(result[0][:mid])) ,str(int(result[0][mid:]))]
        has_rules = True

    if not has_rules : 
        result[0] = str(int(result[0]) * 2024)

    return result
    
def solution_one(path : str,blink_times : int = 1)-> int :
    data = extract_str_data(path)

    result = re.split(r"\s+",data)
    for _ in range(blink_times):    
        print('n = ', _)
        result = blink(result)
        print('n done ', _)
        print(result)


    # print(result)
    return len(result)
  