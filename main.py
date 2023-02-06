import sys
import re

def check_args(args):
    if '+' not in args and '-' not in args:
        raise Exception('Algo de estranho aconteceu, confira a entrada') 
    if args.replace(' ', '')[0] == '+' or args.replace(' ', '')[0] == '-':
        raise Exception('Algo de estranho aconteceu, confira a entrada') 
    else:
        return

def separa_string(sum_clear):
    split_numbers = re.split(r'[+-]', sum_clear)
    split_operations = []

    for i in range(len(sum_clear)):
        if sum_clear[i] in ['+', '-']:
            split_operations.append(sum_clear[i])

    return split_numbers, split_operations

def somador(sum):
    sum_clear = sum.replace(' ', '')
    split_numbers, split_operations = separa_string(sum_clear)
    
    sum_result = int(split_numbers[0])

    for i in range(len(split_operations)):
        if split_operations[i] == '+':
            sum_result += int(split_numbers[i+1])
        if split_operations[i] == '-':
            sum_result -= int(split_numbers[i+1])   

    print(sum_result)



if __name__ == "__main__":
    check_args(sys.argv[1])
    somador(sys.argv[1])
