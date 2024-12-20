#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_WIDTH 1000
#define MAX_HEIGHT 1000

typedef struct {
    int x;
    int y;
} Point;

typedef struct {
    char data[MAX_HEIGHT][MAX_WIDTH];
    int width;
    int height;
} Grid;

typedef struct {
    Point* points;
    int size;
    int capacity;
} VisitedSet;

VisitedSet* createVisitedSet(int initial_capacity) {
    VisitedSet* set = malloc(sizeof(VisitedSet));
    set->points = malloc(sizeof(Point) * initial_capacity);
    set->size = 0;
    set->capacity = initial_capacity;
    return set;
}

void freeVisitedSet(VisitedSet* set) {
    free(set->points);
    free(set);
}

void addPoint(VisitedSet* set, Point p) {
    if (set->size >= set->capacity) {
        set->capacity *= 2;
        set->points = realloc(set->points, sizeof(Point) * set->capacity);
    }
    set->points[set->size++] = p;
}

bool isPointInSet(VisitedSet* set, Point p) {
    for (int i = 0; i < set->size; i++) {
        if (set->points[i].x == p.x && set->points[i].y == p.y) {
            return true;
        }
    }
    return false;
}

bool isPosInGrid(Grid* grid, Point pos) {
    return pos.x >= 0 && pos.x < grid->width && 
           pos.y >= 0 && pos.y < grid->height;
}

// DFS implementation
void dfs(VisitedSet* visited, Grid* grid, Point pos) {
    if (!isPointInSet(visited, pos)) {
        addPoint(visited, pos);
        
        Point neighbors[4] = {
            {pos.x + 1, pos.y},
            {pos.x - 1, pos.y},
            {pos.x, pos.y + 1},
            {pos.x, pos.y - 1}
        };
        
        for (int i = 0; i < 4; i++) {
            Point next = neighbors[i];
            if (isPosInGrid(grid, next) && 
                grid->data[next.y][next.x] == grid->data[pos.y][pos.x]) {
                dfs(visited, grid, next);
            }
        }
    }
}

Grid* readInput(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("Error opening file\n");
        exit(1);
    }

    Grid* grid = malloc(sizeof(Grid));
    grid->height = 0;
    grid->width = 0;

    char line[MAX_WIDTH];
    while (fgets(line, sizeof(line), file)) {
        int len = strlen(line);
        if (line[len-1] == '\n') {
            line[--len] = '\0';
        }
        if (grid->width == 0) {
            grid->width = len;
        }
        strcpy(grid->data[grid->height], line);
        grid->height++;
    }

    fclose(file);
    return grid;
}

// Calculate perimeter of a region (Part 1)
int calculatePerimeter(VisitedSet* region, Grid* grid) {
    int perimeter = 0;
    for (int i = 0; i < region->size; i++) {
        Point p = region->points[i];
        int sharedSides = 0;
        
        Point neighbors[4] = {
            {p.x + 1, p.y},
            {p.x - 1, p.y},
            {p.x, p.y + 1},
            {p.x, p.y - 1}
        };
        
        for (int j = 0; j < 4; j++) {
            if (isPointInSet(region, neighbors[j])) {
                sharedSides++;
            }
        }
        perimeter += 4 - sharedSides;
    }
    return perimeter;
}

// Count shared sides between points in a region (Part 2)
int countSharedSides(VisitedSet* region) {
    int count = 0;
    for (int i = 0; i < region->size; i++) {
        Point p = region->points[i];
        Point left = {p.x - 1, p.y};
        
        if (isPointInSet(region, left)) {
            Point up1 = {p.x, p.y - 1};
            Point up2 = {p.x - 1, p.y - 1};
            Point down1 = {p.x, p.y + 1};
            Point down2 = {p.x - 1, p.y + 1};
            
            if (!isPointInSet(region, up1) && !isPointInSet(region, up2)) {
                count++;
            }
            if (!isPointInSet(region, down1) && !isPointInSet(region, down2)) {
                count++;
            }
        }
        
        Point up = {p.x, p.y - 1};
        if (isPointInSet(region, up)) {
            Point left1 = {p.x - 1, p.y};
            Point left2 = {p.x - 1, p.y - 1};
            Point right1 = {p.x + 1, p.y};
            Point right2 = {p.x + 1, p.y - 1};
            
            if (!isPointInSet(region, left1) && !isPointInSet(region, left2)) {
                count++;
            }
            if (!isPointInSet(region, right1) && !isPointInSet(region, right2)) {
                count++;
            }
        }
    }
    return count;
}

int main() {
    Grid* grid = readInput("data.txt");
    VisitedSet* global_visited = createVisitedSet(1000);
    long long totalCost = 0;
    long long discountedCost = 0;

    for (int y = 0; y < grid->height; y++) {
        for (int x = 0; x < grid->width; x++) {
            Point current = {x, y};
            if (!isPointInSet(global_visited, current)) {
                VisitedSet* region = createVisitedSet(1000);
                dfs(region, grid, current);
                
                int area = region->size;
                int perimeter = calculatePerimeter(region, grid);
                int sharedSides = countSharedSides(region);
                
                totalCost += (long long)area * perimeter;
                discountedCost += (long long)area * (perimeter - sharedSides);

                for (int i = 0; i < region->size; i++) {
                    addPoint(global_visited, region->points[i]);
                }
                
                freeVisitedSet(region);
            }
        }
    }

    printf("Part 1: Total cost is %lld\n", totalCost);
    printf("Part 2: Discounted cost is %lld\n", discountedCost);

    freeVisitedSet(global_visited);
    free(grid);
    return 0;
}