#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ROBOTS 500
#define MAX_LINE 100

typedef struct {
    int x, y;
    int vx, vy;
} Robot;

typedef struct {
    Robot* robots;
    int count;
} GameData;

int mod(int a, int n) {
    return ((a % n) + n) % n;
}

GameData readFile(const char* filename) {
    GameData data = {NULL, 0};
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("Error opening file: %s\n", filename);
        return data;
    }

    data.robots = malloc(MAX_ROBOTS * sizeof(Robot));
    if (!data.robots) {
        printf("Memory allocation failed\n");
        fclose(file);
        return data;
    }

    char line[MAX_LINE];
    while (fgets(line, sizeof(line), file) && data.count < MAX_ROBOTS) {
        if (strlen(line) > 1) {  // Skip empty lines
            Robot* robot = &data.robots[data.count];
            if (sscanf(line, "p=%d,%d v=%d,%d", 
                      &robot->x, &robot->y, &robot->vx, &robot->vy) == 4) {
                data.count++;
            }
        }
    }

    fclose(file);
    return data;
}

long long solutionOne(GameData data) {
    int width = 101;
    int height = 103;
    
    if (data.count == 12) {
        width = 11;
        height = 7;
    }

    int quads[4] = {0, 0, 0, 0};
    
    for (int i = 0; i < data.count; i++) {
        int x = mod(data.robots[i].x + 100 * (data.robots[i].vx + width), width);
        int y = mod(data.robots[i].y + 100 * (data.robots[i].vy + height), height);
        
        if (x == width / 2 || y == height / 2) {
            continue;
        }
        
        int quad_idx = (x > width / 2) + ((y > height / 2) * 2);
        quads[quad_idx]++;
    }
    
    return (long long)quads[0] * quads[1] * quads[2] * quads[3];
}

long long solutionTwo(GameData data) {
    int width = 101;
    int height = 103;
    int t = 0;
    int positions[MAX_ROBOTS][2];  
    
    while (1) {
        t++;
        int valid = 1;
        
        for (int i = 0; i < data.count; i++) {
            positions[i][0] = mod(data.robots[i].x + t * (data.robots[i].vx + width), width);
            positions[i][1] = mod(data.robots[i].y + t * (data.robots[i].vy + height), height);
            
            for (int j = 0; j < i; j++) {
                if (positions[i][0] == positions[j][0] && 
                    positions[i][1] == positions[j][1]) {
                    valid = 0;
                    break;
                }
            }
            if (!valid) break;
        }
        
        if (valid) {
            return t;
        }
    }
}

int main(int argc, char* argv[]) {
    char* filename = "data.txt";

    GameData data = readFile(filename);
    if (!data.robots) {
        return 1;
    }

    long long result1 = solutionOne(data);
    printf("Part 1: %lld\n", result1);

    long long result2 = solutionTwo(data);
    printf("Part 2: %lld\n", result2);

    free(data.robots);
    return 0;
}