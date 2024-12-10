import regex as re

def extract_str_data(file_path : str):
    with open(file_path, 'r') as file:
        return file.read()
    
def extract_dict_data(file_path : str) -> dict:
    file_content = extract_str_data(file_path)
    result = {
        'left': [],
        'right': []
    }
    for line in file_content.split('\n'):
        line_splited = re.split(r'\s+', line)
        result['left'].append(int(line_splited[0].strip()))
        result['right'].append(int(line_splited[1].strip()))

    return result


# part 1 - solution
def solution_one(file_path : str) -> int : 
    data = extract_dict_data(file_path)
    left = data['left']
    right = data['right']
    result = 0

    min_left = -1
    min_right = -1

    for _ in range(len(left)):
        min_left = min(left)
        min_right = min(right)
        result += abs(min_left - min_right)       
        left.remove(min_left)
        right.remove(min_right)

    return result

# part 2 - solution
def solution_two(file_path : str) -> int : 
    data = extract_dict_data(file_path)
    left = data['left']
    right = data['right']
    result = 0
    already_done = {} # list of DoneNumber
    temp_repetition = 0

    for number in left:
        try : 
            result += int(already_done[str(number)].repetition) * number
        except KeyError:
            temp_repetition = right.count(number)
            result += int(temp_repetition) * number
            already_done[str(number)] = DoneNumber(number, temp_repetition)

    return result



class DoneNumber:
    def __init__(self, number : int, repetition : int):
        self.number = number
        self.repetition = repetition