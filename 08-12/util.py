
import regex as re
import time
import copy
from itertools import product
from dataclasses import dataclass


def extract_str_data(file_path : str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def extract_antennas(input_data: str) -> dict:
    rows = [line for line in input_data.split('\n') if line.strip()]
    signal_sources = {}
    
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell != '.':
                if cell not in signal_sources:
                    signal_sources[cell] = []
                signal_sources[cell].append({'x': x, 'y': y})
    
    return {
        'signalSources': signal_sources, 
        'gridWidth': len(rows[0]), 
        'gridHeight': len(rows)
    }

def calculate_distance(pos1 : dict, pos2 : dict) -> float:
    return ((pos1['x'] - pos2['x'])**2 + (pos1['y'] - pos2['y'])**2)**0.5

def find_antinodes(first : dict, second : dict) -> list[dict]:
    dx = second['x'] - first['x']
    dy = second['y'] - first['y']
    
    dist = calculate_distance(first, second)
    
    antinodes = [
        {
            'x': first['x'] + 2 * dx,
            'y': first['y'] + 2 * dy
        },
        {
            'x': second['x'] - 2 * dx,
            'y': second['y'] - 2 * dy
        }
    ]
    
    return antinodes

def process_antennas(path : str, part : int=1) -> int:
    input_data = extract_str_data(path)
    extracted = extract_antennas(input_data)
    signal_sources = extracted['signalSources']
    grid_width = extracted['gridWidth']
    grid_height = extracted['gridHeight']
    
    activated_nodes = set()
    
    def is_inside_grid(node):
        return (0 <= node['x'] < grid_width and 
                0 <= node['y'] < grid_height)
    
    for freq, positions in signal_sources.items():
        for i in range(len(positions)):
            for j in range(i+1, len(positions)):
                first = positions[i]
                second = positions[j]
                
                dx = second['x'] - first['x']
                dy = second['y'] - first['y']
                
                if part == 1:
                    antinodes = [
                        {
                            'x': first['x'] + 2 * dx,
                            'y': first['y'] + 2 * dy
                        },
                        {
                            'x': second['x'] - 2 * dx,
                            'y': second['y'] - 2 * dy
                        }
                    ]
                    
                    for antinode in antinodes:
                        if is_inside_grid(antinode):
                            activated_nodes.add((antinode['x'], antinode['y']))
                
                elif part == 2:
                    activated_nodes.add((first['x'], first['y']))
                    activated_nodes.add((second['x'], second['y']))
                    
                    multiplier = 2
                    
                    while True:
                        nodes = [
                            {
                                'x': first['x'] + multiplier * dx,
                                'y': first['y'] + multiplier * dy
                            },
                            {
                                'x': second['x'] - multiplier * dx,
                                'y': second['y'] - multiplier * dy
                            }
                        ]
                        
                        inside_grid = False
                        for node in nodes:
                            if is_inside_grid(node):
                                activated_nodes.add((node['x'], node['y']))
                                inside_grid = True
                        
                        if not inside_grid:
                            break
                        
                        multiplier += 1
    
    if part == 2:
        for freq1, positions1 in signal_sources.items():
            for freq2, positions2 in signal_sources.items():
                if freq1 == freq2:
                    continue
                
                for pos1 in positions1:
                    for pos2 in positions2:
                        activated_nodes.add((pos1['x'], pos1['y']))
    
    return len(activated_nodes)