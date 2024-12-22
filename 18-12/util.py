from collections import deque

class Solution:
    def __init__(self, filename):
        self.corrupted_cords = [(int(line.split(',')[1]), int(line.split(',')[0]),) 
                               for line in open(filename,'r').read().split('\n')]
    
    def generate_map(self, map_bound, bytes_fallen):
        map_ = []
        for i in range(map_bound):
            row = []
            for j in range(map_bound):
                if (i,j,) in self.corrupted_cords[:bytes_fallen]:
                    row.append('#')
                else:
                    row.append('.')
            map_.append(row)
        return map_
    
    def show_map(self, map_):
        for row in map_:
            print("".join(row))
    
    def shortest_path(self, map_, map_bound, start, end):
        directions = [(-1,0),(1,0),(0,-1),(0,1)] 
        queue = deque([(start[0], start[1], 0)])
        visited = set()
        while queue:
            x, y, dist = queue.popleft()
            if (x,y) == end:
                return dist
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < map_bound and 0 <= ny < map_bound and map_[nx][ny] == '.' and (nx,ny) not in visited:
                    queue.append((nx, ny, dist+1))
                    visited.add((nx,ny))
   
        return -1

    def solution_one(self, bytes_fallen, map_bound, start, end):

        map_ = self.generate_map(map_bound, bytes_fallen)
        print('Part 1:', self.shortest_path(map_, map_bound, start, end))
    
    def solution_two(self, bytes_fallen, map_bound, start, end):

        map_ = self.generate_map(map_bound, bytes_fallen)
        for cord in self.corrupted_cords[bytes_fallen:]:
            map_[cord[0]][cord[1]] = '#'  
            if self.shortest_path(map_, map_bound, start, end) == -1:  
                print('Part 2:', f'{cord[1]},{cord[0]}')
                break