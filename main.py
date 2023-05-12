import sys

reserved_words = ['println', 'while', 'if', 'end', 'readline', 'else', 'Int', 'String']

global symboltable
global asmFile 

class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

#class WriteFile:
#    def __init__(self, file_name):
#        self.file_name = file_name
#
#    def write(self, source):
#        with open(self.file_name, 'w') as f:
#            f.write(source)

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
    i = 0
    
    def __init__(self, value):
        self.value = value
        self.children = []
        self.i = Node.newId()

    @staticmethod
    def newId():
        Node.i += 1
        return Node.i

    def Evaluate():
        pass 

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):
        x = self.children[0].Evaluate()[1]

        if self.value == '-':
            asmFile.write("  NEG EBX\n")

        if self.value == '!':
            asmFile.write("  NOT EBX\n")
       

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):

        esq_op = self.children[0].Evaluate()
        asmFile.write("  PUSH EBX\n")
        dir_op = self.children[1].Evaluate()
        asmFile.write("  POP EAX\n")

        if self.value == '+':
            asmFile.write("  ADD EAX, EBX\n")
            asmFile.write("  MOV EBX, EAX\n")
             
        elif self.value == '-':
            asmFile.write("  SUB EAX, EBX\n")
            asmFile.write("  MOV EBX, EAX\n")
             
        elif self.value == '*':
            asmFile.write("  IMUL EAX, EBX\n")
            asmFile.write("  MOV EBX, EAX\n")
             
        elif self.value == '/':
            asmFile.write("  IDIV EAX, EBX\n")
            asmFile.write("  MOV EBX, EAX\n")
             
        elif self.value == '==':
            asmFile.write("  CMP EAX, EBX\n")
            asmFile.write("  CALL binop_je\n")
                         
        elif self.value == '<':
            asmFile.write("  CMP EAX, EBX\n")
            asmFile.write("  CALL binop_jl\n")
             
        elif self.value == '>':
            asmFile.write("  CMP EAX, EBX\n")
            asmFile.write("  CALL binop_jg\n")
             
        elif self.value == '&&':
            asmFile.write("  AND EAX, EBX\n")
            asmFile.write("  MOV EBX, EAX\n")

        elif self.value == '||':
            asmFile.write("  OR EAX, EBX\n")
            asmFile.write("  MOV EBX, EAX\n")
        
class IntVal(Node):
    def __init__(self, value):
        self.value = value
        self.i = Node.newId()

    def Evaluate(self):
        asmFile.write(f"  MOV EBX, {self.value}\n")

class StrVal(Node):
    def __init__(self, value):
        self.value = value
        self.i = Node.newId()

    def Evaluate(self):
        return 

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):
        key = self.children[0].value
        if self.children[1] == 0 or self.children[1] == '' :
            y = self.children[1]
        else:
            y = self.children[1].Evaluate()
        symboltable.create(key, self.value, y)
        asmFile.write("  PUSH DWORD 0\n")


class NoOp(Node):
    def __init__(self):
        self.value = 'NOOP'
        self.i = Node.newId()

    def Evaluate(self):
        return 
    
class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):
        self.children[0].Evaluate()
        asmFile.write("  PUSH EBX\n")
        asmFile.write("  CALL print\n")
        asmFile.write("  POP EBX\n")
    
class Assign(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):
        x, y = self.children[0].value, self.children[1].Evaluate()
        value = symboltable.get(x)
        asmFile.write(f"  MOV [{value}], EBX\n")


class Identifier(Node):
    def __init__(self, value):
        self.value = value
        self.i = Node.newId()

    def Evaluate(self):
        value = symboltable.get(self.value)
        asmFile.write(f"  MOV EBX, [{value}]\n")
    
class Block(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class While(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):
        asmFile.write(f"  Loop{self.i}:\n")
        self.children[0].Evaluate()
        asmFile.write("  CMP EBX, False\n")
        asmFile.write(f"  JE exit{self.i}\n")
        self.children[1].Evaluate()
        asmFile.write(f"  JMP Loop{self.i}\n")
        asmFile.write(f"  exit{self.i}:\n")
        

class If(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.newId()

    def Evaluate(self):
        self.children[0].Evaluate()
        asmFile.write("  CMP EBX, True\n")
        asmFile.write(f"  JE IF{self.i}\n")
        if len(self.children) > 2:
            self.children[2].Evaluate()
            asmFile.write(f"  JMP ENDIF{self.i}\n")
        else:
            asmFile.write(f"  JMP ENDIF{self.i}\n")

        asmFile.write(f"  IF{self.i}:\n")
        self.children[1].Evaluate()
        asmFile.write(f"  ENDIF{self.i}:\n")


class Readline(Node):
    def __init__(self):
        pass

    def Evaluate(self):
        return 


class SymbolTable:
    def __init__(self):
        self.table = {}
        self.id = -4

    def set(self, key, value):
        if key not in self.table:
            raise Exception('Variable does not exist')
        else:
            if self.table[key][0] == value[0]:
                self.table[key][1] = value
            else:
                raise Exception('Type mismatch')

    def get(self, key):
        return self.table[key][1]
    
    def get_type(self, key):
        return self.table[key][0]
    
    def create(self, key, _type, value):
        if key in self.table:
            raise Exception('Variable already exists')
        else:
            self.table[key] = [_type, f"EBP{self.id}"]
        self.id -= 4        

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
        elif self.position < original_size and self.source[self.position] == '"':
            string = ''
            self.position += 1
            while self.position < original_size and self.source[self.position] != '"':
                string += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token('STRING', string)
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
                if n == 'Int' or n == 'String':
                    self.next = Token('TYPE', n)
                else:
                    self.next = Token('RESERVED', n)
            else:
                self.next = Token('IDENTIFIER', n)
        elif self.position < original_size and self.source[self.position] == '\n':
            self.next = Token('NEW_LINE', '\n')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == '=':
            if self.position + 1 < original_size and self.source[self.position+1] == '=':
                self.next = Token('EQUAL', '==')
                self.position += 2
            else:
                self.next = Token('ASSIGN', '=')
                self.position += 1
        elif self.position < original_size and self.source[self.position] == '>':
            self.next = Token('GREATER', '>')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == '<':
            self.next = Token('LESS', '<')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == '!':
            self.next = Token('DIFFERENT', '!')
            self.position += 1
        elif self.position < original_size and self.source[self.position] == '&':
            if self.position + 1 < original_size and self.source[self.position+1] == '&':
                self.next = Token('AND', '&&')
                self.position += 2
            else:
                raise Exception('Algo de estranho aconteceu, confira a entrada')
        elif self.position < original_size and self.source[self.position] == '|':
            if self.position + 1 < original_size and self.source[self.position+1] == '|':
                self.next = Token('OR', '||')
                self.position += 2
            else:
                raise Exception('Algo de estranho aconteceu, confira a entrada')
        elif self.position < original_size and self.source[self.position] == ':':
            if self.position + 1 < original_size and self.source[self.position+1] == ':':
                self.next = Token('DC', '::')
                self.position += 2
            else:
                raise Exception('Algo de estranho aconteceu, confira a entrada')
        elif self.position < original_size and self.source[self.position] == '.':
            self.next = Token('CONCAT', '.')
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
                return Assign('ASSIGN', [Identifier(identifier), self.parseRelExpr()])
            elif self.tokenizer.next.type == 'DC':
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == 'TYPE':
                    _type = self.tokenizer.next.value
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == 'ASSIGN':
                        self.tokenizer.selectNext()
                        return VarDec(_type, [Identifier(identifier), self.parseRelExpr()])
                    else:
                        self.tokenizer.selectNext()
                        if _type == 'Int':    
                            y = 0
                        elif _type == 'String':
                            y = ''
                        return VarDec(_type, [Identifier(identifier), y])
            else:
                raise Exception('Algo de estranho aconteceu, confira a entrada')
            
        elif self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'println':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'O_PAR':
                self.tokenizer.selectNext()
                to_print = self.parseRelExpr()
                if self.tokenizer.next.type == 'C_PAR':
                    self.tokenizer.selectNext()
                    return Print('PRINT', [to_print]) 
                else:
                    raise Exception('Algo de estranho aconteceu, confira a entrada')
        elif self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'while':
            self.tokenizer.selectNext()
            condition = self.parseRelExpr()   
            if self.tokenizer.next.type == 'NEW_LINE':
                self.tokenizer.selectNext()
                body = Block('BLOCK', [])
                while self.tokenizer.next.value != 'end':
                    body.children.append(self.parseStatement())
                if self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'end':
                    self.tokenizer.selectNext()
                    return While('WHILE', [condition, body])
        elif self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'if':
            self.tokenizer.selectNext()
            condition = self.parseRelExpr()
            if self.tokenizer.next.type == 'NEW_LINE':
                self.tokenizer.selectNext()
                body = Block('BLOCK', [])
                newline = False
                control = True
                while control:
                    if self.tokenizer.next.type == 'NEW_LINE':
                        newline = True
                        self.tokenizer.selectNext()
                    if newline and (self.tokenizer.next.value == 'end' or self.tokenizer.next.value == 'else'):
                            control = False
                    if control:
                        body.children.append(self.parseStatement())
                
                if self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'else':
                    self.tokenizer.selectNext()
                    if self.tokenizer.next.type == 'NEW_LINE':
                        self.tokenizer.selectNext()
                        else_body = Block('BLOCK', [])
                        while self.tokenizer.next.value != 'end':
                            else_body.children.append(self.parseStatement())
                        if self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'end':
                            self.tokenizer.selectNext()
                            return If('IF', [condition, body, else_body])
                        else:
                            raise Exception('Algo de estranho aconteceu, confira a entrada')
                elif self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'end':
                    self.tokenizer.selectNext()
                    return If('IF', [condition, body])
                else:
                    raise Exception('Algo de estranho aconteceu, confira a entrada')
        else:
            raise Exception('Algo de estranho aconteceu, confira a entrada')

    def parseFactor(self):
        if self.tokenizer.next.type == 'INT':
            result = int(self.tokenizer.next.value)
            self.tokenizer.selectNext()
            return IntVal(result)
        elif self.tokenizer.next.type == 'STRING':
            result = self.tokenizer.next.value
            self.tokenizer.selectNext()
            return StrVal(result)
        elif self.tokenizer.next.type == 'ADD':
            self.tokenizer.selectNext()
            result = self.parseFactor()
            return UnOp('+', [result])
        elif self.tokenizer.next.type == 'SUB':
            self.tokenizer.selectNext()
            result = self.parseFactor()
            return UnOp('-', [result])
        elif self.tokenizer.next.type == 'DIFFERENT':
            self.tokenizer.selectNext()
            result = self.parseFactor()
            return UnOp('!', [result])
        elif self.tokenizer.next.type == 'O_PAR':
            self.tokenizer.selectNext()
            result = self.parseRelExpr()
            if self.tokenizer.next.type == 'C_PAR':
                self.tokenizer.selectNext()
                return result
            else:
                raise Exception('Algo de estranho aconteceu, confira a entrada')
        elif self.tokenizer.next.type == 'RESERVED' and self.tokenizer.next.value == 'readline':
            self.tokenizer.selectNext()
            if self.tokenizer.next.type == 'O_PAR':
                self.tokenizer.selectNext()
                if self.tokenizer.next.type == 'C_PAR':
                    self.tokenizer.selectNext()
                    return Readline()
                else:
                    raise Exception('Algo de estranho aconteceu, confira a entrada')
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
        while self.tokenizer.next.type == 'MUL' or self.tokenizer.next.type == 'DIV' or self.tokenizer.next.type == 'AND':
            if self.tokenizer.next.type == 'MUL':
                self.tokenizer.selectNext()
                result = BinOp('*', [result, self.parseFactor()])
            elif self.tokenizer.next.type == 'DIV':
                self.tokenizer.selectNext()
                result = BinOp('/', [result, self.parseFactor()])
            elif self.tokenizer.next.type == 'AND':
                self.tokenizer.selectNext()
                result = BinOp('&&', [result, self.parseFactor()])
        return result
    
    def parseExpression(self):
        result = self.parseTerm()
        while self.tokenizer.next.type == 'ADD' or self.tokenizer.next.type == 'SUB' or self.tokenizer.next.type == 'OR' or self.tokenizer.next.type == 'CONCAT':
            if self.tokenizer.next.type == 'ADD':
                self.tokenizer.selectNext()
                result = BinOp('+', [result, self.parseTerm()])
            elif self.tokenizer.next.type == 'SUB':
                self.tokenizer.selectNext()
                result = BinOp('-', [result, self.parseTerm()])
            elif self.tokenizer.next.type == 'OR':
                self.tokenizer.selectNext()
                result = BinOp('||', [result, self.parseTerm()])
            elif self.tokenizer.next.type == 'CONCAT':
                self.tokenizer.selectNext()
                result = BinOp('.', [result, self.parseTerm()])
        return result
    
    def parseRelExpr(self):
        result = self.parseExpression()
        while self.tokenizer.next.type == 'EQUAL' or self.tokenizer.next.type == 'GREATER' or self.tokenizer.next.type == 'LESS':
            if self.tokenizer.next.type == 'EQUAL':
                self.tokenizer.selectNext()
                result = BinOp('==', [result, self.parseExpression()])
            elif self.tokenizer.next.type == 'GREATER':
                self.tokenizer.selectNext()
                result = BinOp('>', [result, self.parseExpression()])
            elif self.tokenizer.next.type == 'LESS':
                self.tokenizer.selectNext()
                result = BinOp('<', [result, self.parseExpression()])
        return result

    @staticmethod
    def run(self):
        result = self.parseBlock()
        if self.tokenizer.next.type != 'EOE':
            raise Exception('Algo de estranho aconteceu, confira a entrada')
        return result.Evaluate()
        

symboltable = SymbolTable()


if __name__ == "__main__":
    filename = sys.argv[1]
    asmFile = open(filename.split('.')[0]+'.asm', 'w')

    with open(filename, 'r') as f:
        code = f.read()

    with open('cabecalho.asm', 'r') as f:
        asmFile.write(f.read())
    
    Parser.run(Parser(PrePro.filter(code)))

    with open('rodape.asm', 'r') as f:
        asmFile.write(f.read())
    
    asmFile.close()