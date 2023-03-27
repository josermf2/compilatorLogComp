import sys

reserved_words = ['println']

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

class PrePro:
    @staticmethod
    def filter(source):
        if '#' not in source:
            return source
        lines = source.split('\n')
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j] == '#':
                    lines[i] = lines[i][:j]
                    break
        return '\n'.join(lines)

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def Evaluate():
        pass 

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        if self.value == '-':
            return - self.children[0].Evaluate()
        return self.children[0].Evaluate()

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        if self.value == '+':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == '-':
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == '*':
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == '/':
            return self.children[0].Evaluate() // self.children[1].Evaluate()
        

class IntVal(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self):
        return self.value


class NoOp(Node):
    def __init__(self):
        self.value = 'NOOP'

    def Evaluate(self):
        return 
    
class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        print(self.children[0].Evaluate())
    
class Assign(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        x, y = self.children[0].value, self.children[1].Evaluate()
        symboltable.set(x, y)

class Identifier(Node):
    def __init__(self, value):
        self.value = value

    def Evaluate(self):
        return symboltable.get(self.value)
    
class Block(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class SymbolTable:
    def __init__(self):
        self.table = {}

    def set(self, key, value):
        self.table[key] = value

    def get(self, key):
        return self.table[key]

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
        elif self.position < original_size and self.source[self.position] == '(':
            self.next = Token('O_PAR', '(')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == ')':
            self.next = Token('C_PAR', ')')
            self.position += 1
        elif self.position < original_size and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
            n = ''
            while self.position < original_size and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                n = n + self.source[self.position]
                self.position += 1
            if n in reserved_words:
                self.next = Token('RESERVED', n)
            else:
                self.next = Token('IDENTIFIER', n)
        elif self.position < original_size and self.source[self.position] == '\n':
            self.next = Token('NEW_LINE', '\n')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == '=':
            self.next = Token('ASSIGN', '=')
            self.position += 1
        else:
            raise Exception('Algo de estranho aconteceu, confira a entrada')
        return self.next   
 
class Parser:
    def __init__(self, source):
        self.tokenizer = Tokenizer(source)

    def parseBlock(self):
        result = []
        while self.tokenizer.next.type != 'EOE':
            result.append(self.parseStatement())
        return Block('BLOCK', result)  
    
    def parseStatement(self):
        if self.tokenizer.next.type == 'NEW_LINE':
            self.tokenizer.selectNext()
            return NoOp()
        elif self.tokenizer.next.type == 'IDENTIFIER':
            identifier = self.tokenizer.next.value
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'ASSIGN':
                self.tokenizer.selectNext()
                return Assign('ASSIGN', [Identifier(identifier), self.parseExpression()])
            else:
                raise Exception('Algo de estranho aconteceu, confira a entrada')
        elif self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'println':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'O_PAR':
                self.tokenizer.selectNext()
                to_print = self.parseExpression()
                if self.tokenizer.next.type == 'C_PAR':
                    self.tokenizer.selectNext()
                    return Print('PRINT', [to_print]) 
                else:
                    raise Exception('Algo de estranho aconteceu, confira a entrada')
        else:
            raise Exception('Algo de estranho aconteceu, confira a entrada')

    def parseFactor(self):
        if self.tokenizer.next.type == 'INT':
            result = int(self.tokenizer.next.value)
            self.tokenizer.selectNext()
            return IntVal(result)
        elif self.tokenizer.next.type == 'ADD':
            self.tokenizer.selectNext()
            result = self.parseFactor()
            return UnOp('+', [result])
        elif self.tokenizer.next.type == 'SUB':
            self.tokenizer.selectNext()
            result = self.parseFactor()
            return UnOp('-', [result])
        elif self.tokenizer.next.type == 'O_PAR':
            self.tokenizer.selectNext()
            result = self.parseExpression()
            if self.tokenizer.next.type == 'C_PAR':
                self.tokenizer.selectNext()
                return result
            else:
                raise Exception('Algo de estranho aconteceu, confira a entrada')
        elif self.tokenizer.next.type == 'IDENTIFIER':
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return Identifier(result)
        else:
            raise Exception('Algo de estranho aconteceu, confira a entrada')

    def parseTerm(self):
        result = self.parseFactor()
        while self.tokenizer.next.type == 'MUL' or self.tokenizer.next.type == 'DIV':
            if self.tokenizer.next.type == 'MUL':
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == 'O_PAR':
                    result = BinOp('*', [result, self.parseFactor()])
                    continue
                elif self.tokenizer.next.type == 'INT':
                    result = BinOp('*', [result, IntVal(int(self.tokenizer.next.value))])
                else:
                    raise Exception('Algo de estranho aconteceu, confira a entrada')
            else:
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == 'O_PAR':
                    result = BinOp('/', [result, self.parseFactor()])
                    continue
                elif self.tokenizer.next.type == 'INT':
                    result = BinOp('/', [result, IntVal(int(self.tokenizer.next.value))])
                else:
                    raise Exception('Algo de estranho aconteceu, confira a entrada')
        
            self.tokenizer.selectNext()
        return result
    
    def parseExpression(self):
        result = self.parseTerm()
        while self.tokenizer.next.type == 'ADD' or self.tokenizer.next.type == 'SUB':
            if self.tokenizer.next.type == 'ADD':
                self.tokenizer.selectNext()
                result = BinOp('+', [result, self.parseTerm()])
            else:
                self.tokenizer.selectNext()
                result = BinOp('-', [result, self.parseTerm()])
        return result
    
    
    @staticmethod
    def run(self):
        result = self.parseBlock()
        if self.tokenizer.next.type != 'EOE':
            raise Exception('Algo de estranho aconteceu, confira a entrada')
        return result.Evaluate()
        
global symboltable
symboltable = SymbolTable()

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        code = f.read()
    Parser.run(Parser(PrePro.filter(code)))