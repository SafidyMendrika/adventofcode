#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int comboOperand(int value, int A, int B, int C) {
    switch (value) {
        case 0:
        case 1:
        case 2:
        case 3:
            return value;
        case 4:
            return A;
        case 5:
            return B;
        case 6:
            return C;
        default:
            return 0;
    }
}

int* runProgram(int registers[3], int* program, int program_length, int* output_length) {
    int A = registers[0];
    int B = registers[1];
    int C = registers[2];
    int pointer = 0;
    int capacity = 10;
    int* outputs = malloc(capacity * sizeof(int));
    *output_length = 0;

    while (pointer < program_length) {
        int opcode = program[pointer];
        int operand = program[pointer + 1];
        int combo_value;

        switch (opcode) {
            case 0: 
                combo_value = comboOperand(operand, A, B, C);
                A /= (1 << combo_value);
                break;
            case 1:
                B ^= operand;
                break;
            case 2: 
                combo_value = comboOperand(operand, A, B, C);
                B = combo_value % 8;
                break;
            case 3: 
                if (A != 0) {
                    pointer = operand;
                    continue;
                }
                break;
            case 4:
                B ^= C;
                break;
            case 5: 
                combo_value = comboOperand(operand, A, B, C);
                if (*output_length >= capacity) {
                    capacity *= 2;
                    outputs = realloc(outputs, capacity * sizeof(int));
                }
                outputs[*output_length] = combo_value % 8;
                (*output_length)++;
                break;
            case 6: 
                combo_value = comboOperand(operand, A, B, C);
                B = A / (1 << combo_value);
                break;
            case 7: 
                combo_value = comboOperand(operand, A, B, C);
                C = A / (1 << combo_value);
                break;
        }
        pointer += 2;
    }

    return outputs;
}

int* parseProgram(char* str, int* length) {
    char* token = strtok(str, ",");
    int capacity = 10;
    int* program = malloc(capacity * sizeof(int));
    *length = 0;

    while (token != NULL) {
        if (*length >= capacity) {
            capacity *= 2;
            program = realloc(program, capacity * sizeof(int));
        }
        program[*length] = atoi(token);
        (*length)++;
        token = strtok(NULL, ",");
    }

    return program;
}

char* solutionOne(int registers[3], int* program, int program_length) {
    int output_length;
    int* result = runProgram(registers, program, program_length, &output_length);
    
    int buffer_size = 1;  
    for (int i = 0; i < output_length; i++) {
        buffer_size += (result[i] == 0) ? 1 : snprintf(NULL, 0, "%d", result[i]);
        if (i < output_length - 1) buffer_size++; 
    }
    
    char* output = malloc(buffer_size);
    output[0] = '\0';
    
    for (int i = 0; i < output_length; i++) {
        char temp[12];
        sprintf(temp, "%d", result[i]);
        strcat(output, temp);
        if (i < output_length - 1) strcat(output, ",");
    }
    
    free(result);
    return output;
}


int main() {
    FILE* file = fopen("data.txt", "r");
    if (file == NULL) {
        printf("Error opening file\n");
        return 1;
    }

    char line[1024];
    int registers[3];
    int* program = NULL;
    int program_length = 0;
    int line_count = 0;

    while (fgets(line, sizeof(line), file)) {
        line[strcspn(line, "\n")] = 0;
        
        if (line_count < 3) {
            char* value = strchr(line, ':');
            if (value != NULL) {
                registers[line_count] = atoi(value + 2);
            }
        } else if (line_count == 4) {
            char* value = strchr(line, ':');
            if (value != NULL) {
                program = parseProgram(value + 2, &program_length);
            }
        }
        line_count++;
    }
    fclose(file);

    char* part1_result = solutionOne(registers, program, program_length);
    printf("Part 1 result: %s\n", part1_result);
    free(part1_result);

    free(program);
    return 0;
}