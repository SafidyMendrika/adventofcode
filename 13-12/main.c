#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 256
#define MAX_FILE_SIZE 4096
#define PART2_OFFSET 10000000000000LL

typedef struct {
    long long x;
    long long y;
} Point;

typedef struct {
    Point buttonA;
    Point buttonB;
    Point prize;
} GameConfig;

typedef struct {
    GameConfig* games;
    int count;
} GameData;

GameData readFile(const char* filename) {
    GameData data = {NULL, 0};
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("Error opening file: %s\n", filename);
        return data;
    }

    char line[MAX_LINE_LENGTH];
    int lineCount = 0;
    while (fgets(line, sizeof(line), file)) {
        if (strlen(line) > 1) { 
            lineCount++;
        }
    }
    data.count = lineCount / 3;
    data.games = malloc(sizeof(GameConfig) * data.count);

    rewind(file);

    for (int i = 0; i < data.count; i++) {
        fgets(line, sizeof(line), file);
        sscanf(line, "Button A: X+%lld, Y+%lld", 
               &data.games[i].buttonA.x, 
               &data.games[i].buttonA.y);

        fgets(line, sizeof(line), file);
        sscanf(line, "Button B: X+%lld, Y+%lld", 
               &data.games[i].buttonB.x, 
               &data.games[i].buttonB.y);

        fgets(line, sizeof(line), file);
        sscanf(line, "Prize: X=%lld, Y=%lld", 
               &data.games[i].prize.x, 
               &data.games[i].prize.y);

        fgets(line, sizeof(line), file);
    }

    fclose(file);
    return data;
}

long long playClawMachine(Point prize, Point buttonA, Point buttonB) {
    long long D = buttonA.x * buttonB.y - buttonA.y * buttonB.x;
    if (D == 0) return -1; 

    long long D_a = prize.x * buttonB.y - prize.y * buttonB.x;
    long long D_b = buttonA.x * prize.y - buttonA.y * prize.x;

    if (D_a % D != 0 || D_b % D != 0) return -1;

    long long countA = D_a / D;
    long long countB = D_b / D;

    if (countA < 0 || countB < 0) return -1;

    return countA * 3 + countB;
}

long long solutionOne(GameData data) {
    long long totalTokens = 0;
    
    for (int i = 0; i < data.count; i++) {
        long long cost = playClawMachine(
            data.games[i].prize,
            data.games[i].buttonA,
            data.games[i].buttonB
        );
        if (cost >= 0) {
            totalTokens += cost;
        }
    }
    
    return totalTokens;
}

long long solutionTwo(GameData data) {
    long long totalTokens = 0;
    
    for (int i = 0; i < data.count; i++) {
        GameConfig game = data.games[i];
        game.prize.x += PART2_OFFSET;
        game.prize.y += PART2_OFFSET;
        
        long long cost = playClawMachine(
            game.prize,
            game.buttonA,
            game.buttonB
        );
        if (cost >= 0) {
            totalTokens += cost;
        }
    }
    
    return totalTokens;
}

int main(int argc, char* argv[]) {
    char* filename = "data.txt";

    GameData data = readFile(filename);
    if (!data.games) {
        return 1;
    }

    long long result1 = solutionOne(data);
    printf("Part 1: %lld\n", result1);

    long long result2 = solutionTwo(data);
    printf("Part 2: %lld\n", result2);

    free(data.games);
    return 0;
}