import sys
import re

def check_args(args):
    if ('+' not in args and '-' not in args) or (args.replace(' ', '')[0] == '+' or args.replace(' ', '')[0] == '-'): 
        raise Exception('Algo de estranho aconteceu, confira a entrada') 
    else:
        return

def separa_string(sum_clear):
    split_numbers = re.split(r'[+-]', sum_clear)
    split_operations = re.findall(r'[+-]', sum_clear)
    return split_numbers, split_operations

def somador(split_numbers, split_operations):
    sum_result = int(split_numbers[0])

    for i in range(len(split_operations)):
        if split_operations[i] == '+':
            sum_result += int(split_numbers[i+1])
        if split_operations[i] == '-':
            sum_result -= int(split_numbers[i+1])   

    return sum_result


if __name__ == "__main__":
    check_args(sys.argv[1])

    sum_clear = sys.argv[1].replace(' ', '')
    split_numbers, split_operations = separa_string(sum_clear)

    result = somador(split_numbers, split_operations)

    print(result)