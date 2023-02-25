import sys

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

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
        else:
            raise Exception('Algo de estranho aconteceu, confira a entrada')
        return self.next   

class Parser:
    def __init__(self, source):
        self.tokenizer = Tokenizer(source)

    @staticmethod
    def parseExpression(self):
        result = 0
        if self.tokenizer.next.type == 'INT':
            result += int(self.tokenizer.next.value)
            self.tokenizer.selectNext()

            while self.tokenizer.next.type == 'ADD' or self.tokenizer.next.type == 'SUB':
                if self.tokenizer.next.type == 'ADD':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == 'INT':
                        result += int(self.tokenizer.next.value)
                    else:
                        raise Exception('Algo de estranho aconteceu, confira a entrada')
                else:
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == 'INT':
                        result -= int(self.tokenizer.next.value)
                    else:
                        raise Exception('Algo de estranho aconteceu, confira a entrada')
                self.tokenizer.selectNext()
        return result
    
    @staticmethod
    def run(self):
        result = self.parseExpression(self)
        if self.tokenizer.next.type != 'EOE':
            raise Exception('Algo de estranho aconteceu, confira a entrada')
        return result
        

if __name__ == "__main__":
    code = sys.argv[1]
    print(Parser.run(Parser(code)))