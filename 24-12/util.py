from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple
from itertools import combinations
import re

class Operation(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

@dataclass
class Gate:
    inputs: List[str]
    output: str
    operation: Operation

def parse_input(input_text: str) -> Tuple[Dict[str, bool], List[Gate]]:
    parts = input_text.strip().split("\n\n")
    value_map = {}
    for line in parts[0].split("\n"):
        key, value = line.split(": ")
        value_map[key] = bool(int(value))
    
    gates = []
    for line in parts[1].split("\n"):
        match = re.match(r"(\w+)\s+(AND|OR|XOR)\s+(\w+)\s+->\s+(\w+)", line)
        if match:
            input1, op, input2, output = match.groups()
            gates.append(Gate(
                inputs=[input1, input2],
                output=output,
                operation=Operation(op)
            ))
    
    return value_map, gates

def apply_operation(op: Operation, a: bool, b: bool) -> bool:
    if op == Operation.AND:
        return a and b
    elif op == Operation.OR:
        return a or b
    else:  # XOR
        return a != b

def process_gates(current_map: Dict[str, bool], gates: List[Gate], swaps: Dict[str, str] = None) -> Dict[str, bool]:
    current_map = current_map.copy()
    gates_to_process = gates.copy()
    
    while gates_to_process:
        processable = []
        remaining = []
        
        for gate in gates_to_process:
            if all(input_key in current_map for input_key in gate.inputs):
                processable.append(gate)
            else:
                remaining.append(gate)
        
        if not processable:
            break
            
        for gate in processable:
            a = current_map[gate.inputs[0]]
            b = current_map[gate.inputs[1]]
            value = apply_operation(gate.operation, a, b)
            
            output = gate.output
            if swaps and output in swaps:
                output = swaps[output]
                
            current_map[output] = value
        
        gates_to_process = remaining
    
    return current_map

def get_binary_string(value_map: Dict[str, bool], prefix: str) -> str:
    return ''.join(
        str(int(value_map[key])) 
        for key in sorted(
            (k for k in value_map if k.startswith(prefix)), 
            reverse=True
        )
    )

def get_number_from_bits(value_map: Dict[str, bool], prefix: str) -> int:
    bits = []
    for key in sorted(k for k in value_map if k.startswith(prefix)):
        bits.append('1' if value_map[key] else '0')
    return int(''.join(reversed(bits)), 2)

def try_swap_combination(value_map: Dict[str, bool], gates: List[Gate], swap_pairs: List[Tuple[str, str]]) -> bool:
    swaps = {}
    for a, b in swap_pairs:
        swaps[a] = b
        swaps[b] = a
    
    result = process_gates(value_map, gates, swaps)
    
    x_val = get_number_from_bits(value_map, 'x')
    y_val = get_number_from_bits(value_map, 'y')
    z_val = get_number_from_bits(result, 'z')
    
    return z_val == x_val + y_val

def solution_one(input_text: str) -> str:
    value_map, gates = parse_input(input_text)
    result_map = process_gates(value_map, gates)
    bitstring = get_binary_string(result_map, 'z')
    return str(int(bitstring, 2))

def solution_two(input_text: str) -> str:
    value_map, gates = parse_input(input_text)
    
    all_outputs = {gate.output for gate in gates}
    potential_pairs = list(combinations(all_outputs, 2))
    
    for pairs_combo in combinations(potential_pairs, 4):
        if try_swap_combination(value_map, gates, pairs_combo):
            swapped_wires = sorted(set(wire for pair in pairs_combo for wire in pair))
            return ','.join(swapped_wires)
    
    return ""