import sys
import re

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

class PrePro:
    @staticmethod
    def filter(source):
        clear_comments = re.sub(r'#.*', '', source)
        return clear_comments

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = self.selectNext()

    def selectNext(self):
        original_size = len(self.source)
        while self.position < original_size and self.source[self.position]==' ':
            self.position += 1
        if self.position == original_size:
            self.next = Token('EOE', '')
        elif self.source[self.position].isdigit():
            n = ''
            while self.position < original_size and self.source[self.position].isdigit():
                n = n + self.source[self.position]
                self.position += 1
            self.next = Token('INT', n)
        elif self.position < original_size and self.source[self.position] == '-':
            self.next = Token('SUB', '-')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == '+':
            self.next = Token('ADD', '+')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == '*':
            self.next = Token('MUL', '*')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == '/':
            self.next = Token('DIV', '/')
            self.position += 1
        else:
            raise Exception('Algo de estranho aconteceu, confira a entrada')
        return self.next   

class Parser:
    def __init__(self, source):
        self.tokenizer = Tokenizer(source)

    def parseTerm(self):
        result = 0
        if self.tokenizer.next.type == 'INT':
            result += int(self.tokenizer.next.value)
            self.tokenizer.selectNext()

            while self.tokenizer.next.type == 'MUL' or self.tokenizer.next.type == 'DIV':
                if self.tokenizer.next.type == 'MUL':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == 'INT':
                        result *= int(self.tokenizer.next.value)
                    else:
                        raise Exception('Algo de estranho aconteceu, confira a entrada')
                else:
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == 'INT':
                        result = result // int(self.tokenizer.next.value)
                    else:
                        raise Exception('Algo de estranho aconteceu, confira a entrada')
                self.tokenizer.selectNext()
        else:
            raise Exception('Algo de estranho aconteceu, confira a entrada')
        return result
    
    def parseExpression(self):
        result = self.parseTerm()
        while self.tokenizer.next.type == 'ADD' or self.tokenizer.next.type == 'SUB':
            if self.tokenizer.next.type == 'ADD':
                self.tokenizer.selectNext()
                result += self.parseTerm()
            else:
                self.tokenizer.selectNext()
                result -= self.parseTerm()
        return result
    
    
    @staticmethod
    def run(self):
        result = self.parseExpression()
        if self.tokenizer.next.type != 'EOE':
            raise Exception('Algo de estranho aconteceu, confira a entrada')
        return result
        

if __name__ == "__main__":
    code = sys.argv[1]
    print(Parser.run(Parser(PrePro.filter(code))))