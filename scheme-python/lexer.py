from enum import Enum

class Error(Enum):
    Error_OK = 0
    Error_Syntax = 1

class Type(Enum):
    EOF = 0
    OP = 1
    CP = 2
    DEF = 3
    LAM = 4
    ID = 5
    PLUS_SYM = 6
    MINUS_SYM = 7
    G_SYM = 8
    L_SYM = 9
    IF = 10

class Token:
    def __init__(self, type=0, value=0):
        self.type = type
        self.value = value
    def __str__(self):
        if (self.type == Type.ID):
            return f"Token [{self.type}, Value: {self.value}]"
        else:
            return f"Token [{self.type}]"

def Lexer(lists):   # Input: Input List / Return: Token List
    lexList = []

    for i in range(len(lists)):
        for j in range(len(lists[i])):
            LA = lists[i][j]
            if(LA == '('):
                lexList.append(Token(Type.OP))
            elif(LA == ')'):
                lexList.append(Token(Type.CP))
            elif(LA == 'define'):
                lexList.append(Token(Type.DEF))
            elif(LA == 'lambda'):
                lexList.append(Token(Type.LAM))
            elif(LA == 'if'):
                lexList.append(Token(Type.IF))
            elif(LA == '+'):
                lexList.append(Token(Type.PLUS_SYM))
            elif(LA == '-'):
                lexList.append(Token(Type.MINUS_SYM))
            elif(LA == '>'):
                lexList.append(Token(Type.G_SYM))
            elif(LA == '<'):
                lexList.append(Token(Type.L_SYM))
            else:
                lexList.append(Token(Type.ID, value=LA))

    return lexList
    

if __name__ == "__main__":
    inputList = []

    while True:
        line = input()
        if line:
            inputList.append(line.replace('(', ' ( ').replace(')', ' ) ').split())
        else:
            break

    results = Lexer(inputList)
    print("========Lexing Result========")
    for result in results:
        print(result)
