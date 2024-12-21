from dataclasses import dataclass
from typing import Set, List, Dict, Tuple

@dataclass
class WarehouseState:
    walls: Set[Tuple[int, int]]
    boxes: Set[Tuple[int, int]]
    robot: Tuple[int, int]

@dataclass
class MoveData:
    directions: Dict[str, Tuple[int, int]]
    move_sequence: List[Tuple[int, int]]

def extract_str_data(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()

def parse_move_data(moves_str: str) -> MoveData:
    directions = {
        "^": (-1, 0),  
        "v": (1, 0),  
        "<": (0, -1), 
        ">": (0, 1)   
    }
    clean_moves = moves_str.replace("\n", "")
    return MoveData(
        directions=directions,
        move_sequence=[directions[x] for x in clean_moves]
    )

def add_pos(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> Tuple[int, int]:
    return (pos1[0] + pos2[0], pos1[1] + pos2[1])

def parse_warehouse_state(layout_str: str, part2: bool) -> WarehouseState:
    walls = set()
    boxes = set()
    robot = (0, 0)
    
    for i, line in enumerate(layout_str.split("\n")):
        for j, char in enumerate(line):
            pos = (i, j)
            
            match char:
                case "#":
                    if part2:
                        walls.update({pos, (pos[0], pos[1] + 1)})
                    else:
                        walls.add(pos)
                case "O":
                    boxes.add(pos)
                case "@":
                    robot = pos
    
    return WarehouseState(walls=walls, boxes=boxes, robot=robot)

def process_moves(state: WarehouseState, move_data: MoveData, part2: bool) -> int:
    boxes = state.boxes.copy()
    robot = state.robot
    
    for move in move_data.move_sequence:
        to_move = set()
        to_check = [add_pos(robot, move)]
        
        while to_check:
            curr_pos = to_check.pop()
            left_pos = (curr_pos[0], curr_pos[1] - 1)
            is_right_side = part2 and left_pos in boxes
            
            if curr_pos in boxes or is_right_side:
                to_move.add(left_pos if is_right_side else curr_pos)
                to_check.append(add_pos(curr_pos, move))
                
                if part2 and move[0] != 0: 
                    other_pos = left_pos if is_right_side else (curr_pos[0], curr_pos[1] + 1)
                    to_check.append(add_pos(other_pos, move))
            elif curr_pos in state.walls:
                break
        else: 
            
            boxes -= to_move
            boxes |= {add_pos(pos, move) for pos in to_move}
            robot = add_pos(robot, move)
    
    return sum(pos[0] * 100 + pos[1] for pos in boxes)

def solution_one(file_path: str) -> int:
    data = extract_str_data(file_path)
    layout, moves = data.strip().split("\n\n")
    
    move_data = parse_move_data(moves)
    warehouse_state = parse_warehouse_state(layout, False)
    
    return process_moves(warehouse_state, move_data, False)

def solution_two(file_path: str) -> int:
    data = extract_str_data(file_path)
    layout, moves = data.strip().split("\n\n")
    
    move_data = parse_move_data(moves)
    warehouse_state = parse_warehouse_state(layout, True)
    
    return process_moves(warehouse_state, move_data, True)
