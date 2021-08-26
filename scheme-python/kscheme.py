import sys
import os
from enum import Enum


class Type(Enum):
    NIL = 0
    INT = 1
    REAL = -2
    SYM = -1
    PAIR = 2
    BUILTIN = 3
    CLOSURE = 4


class ErrorType(Enum):
    UNEXPECTED_TOKEN = "Unexpected Token"
    ID_INVALID_TOKEN = "invaild type"
    NO_INPUT_FILE = "No Input File"
    ERROR_OK = "No Error"
    ERROR_SYNTAX = "Syntax Error"
    ERROR_ARGS = "Error Args"


class Error(Exception):
    pass


def Err(token, type):
    raise Error("{0} : {1}".format(str(type), str(token)))


class Token(object):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return (
            self.__class__.__name__ + "(" + str(self.value) + ")" + "." + str(self.type)
        )

    def __repr__(self):
        return self.__str__()


class Input:
    def __init__(self):
        self.text = ""

    def _input(self):
        self.text = input(">> ")
        if self.text == "exit":
            exit()
        return self.text


class Keyword(Enum):
    LPAREN = 4
    RPAREN = 5
    DEFINE = 6
    LAMBDA = 7
    PLUS_OP = 8
    SUB_OP = 9
    DIV_OP = 10
    MUL_OP = 11
    DEF = 12
    EQ_OP = 13
    LESS_OP = 14
    IF = 15
    QUOTE = 16


class Data:
    def __init__(self, type=Type.NIL, value=0):
        self.type = type
        self.value = value

    def car(self):
        return self.value[0]

    def cdr(self):
        return self.value[1]

    def __str__(self):
        if self.type == Type.NIL:
            return "NIL"
        elif self.type == Type.PAIR:
            try:
                if self.cdr() == int(self.cdr()):
                    return "(" + str(self.car()) + " . " + str(self.cdr()) + ")"
            except:
                retStr = "("
                retStr += str(self.car())
                atom = self.cdr()
                while atom.type != Type.NIL:
                    if atom.type == Type.PAIR:
                        retStr += " . "
                        retStr += str(atom.car())
                        atom = atom.cdr()
                    else:
                        retStr += " . "
                        retStr += str(atom)
                        break
                retStr += ")"
                return str(retStr)
        else:
            return str(self.value)

    def __repr__(self):
        return self.__str__()


class Nil:
    pass


class Symbol:
    def __init__(self, value, type):
        self.value = str(value.value)
        self.type = str(value.type)


class Pair:
    def __init__(self, root=None, LV=None, RV=None):
        self.root = root
        self.LV = LV
        self.RV = RV


def isNil(d):
    return d.type == Type.NIL


def nilp():
    return Data(Type.NIL)


def cons(d1, d2):
    return Data(Type.PAIR, [d1, d2])


def mkint(n):
    return Data(Type.INT, n)


def mksym(s):
    return Data(Type.SYM, s)


class Lexer:
    def __init__(self, text):
        self.pos = 0
        self.text = text if len(text) != 0 else Err(Type.NIL, ErrorType.NO_INPUT_FILE)
        self.currentToken = self.text[self.pos]

    def eat(self, tokenType):
        if self.currentToken == tokenType:
            return True
        return False

    def jmp(self):
        if self.pos == len(self.text) - 1:
            self.currentToken = None
            return False
        else:
            self.pos += 1
            self.currentToken = self.text[self.pos]
            return True

    def lex(self):
        lexR = []
        # print("===== === LEX === =====")
        while True:
            if self.pos == len(self.text) or self.currentToken == None:
                break

            if self.currentToken.isspace():
                try:
                    while self.currentToken.isspace():
                        self.jmp()
                except:
                    break

            elif self.currentToken == ".":
                self.jmp()

            elif self.currentToken == "(":
                if not self.eat("("):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("(", Keyword.LPAREN))
                self.jmp()
                if self.currentToken == ")":
                    lexR.append(Token(")", Keyword.RPAREN))
                    self.jmp()

            elif self.currentToken == ")":
                if not self.eat(")"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token(")", Keyword.RPAREN))
                self.jmp()

            elif self.currentToken == ";":
                flag = 3
                while flag:
                    self.jmp()
                    if self.currentToken == ".":
                        flag = flag - 1
                        pass
                    else:
                        break
                break

            elif self.currentToken.isalpha():
                id = ""
                while self.currentToken.isalpha() and self.currentToken is not None:
                    if self.currentToken.isalpha():
                        id += self.currentToken
                        if self.jmp():
                            pass
                        else:
                            break
                if id == "람다":
                    lexR.append(Token("LAM", Keyword.LAMBDA))
                elif id == "정의":
                    lexR.append(Token("DEF", Keyword.DEF))
                elif id == "Nil":
                    lexR.append(Token("NIL", Type.NIL))
                else:
                    lexR.append(Token(id, Type.SYM))

            elif self.currentToken.isdigit():
                num = ""
                realFlag = False
                while self.currentToken.isdigit() or self.currentToken == ".":
                    if self.currentToken == ".":
                        realFlag = True
                        num += self.currentToken
                        if self.jmp():
                            pass
                        else:
                            break
                    else:
                        num += self.currentToken
                        if self.jmp():
                            pass
                        else:
                            break
                if realFlag:
                    lexR.append(Token(num, Type.REAL))
                else:
                    lexR.append(Token(num, Type.INT))

            elif self.currentToken == "+":
                if not self.eat("+"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("+", Keyword.PLUS_OP))
                self.jmp()

            elif self.currentToken == "-":
                if not self.eat("-"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("-", Keyword.SUB_OP))
                self.jmp()

            elif self.currentToken == "*":
                if not self.eat("*"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("*", Keyword.MUL_OP))
                self.jmp()

            elif self.currentToken == "/":
                if not self.eat("/"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("/", Keyword.DIV_OP))
                self.jmp()

            elif self.currentToken == "=":
                if not self.eat("="):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("=", Keyword.EQ_OP))
                self.jmp()

            elif self.currentToken == "<":
                if not self.eat("<"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("<", Keyword.LESS_OP))
                self.jmp()

        # print(lexR)
        # print("===== === OUT === =====")
        return lexR


def iCons(d_list):
    if len(d_list) != 1:
        return cons(d_list[0], iCons(d_list[1:]))
    else:
        return cons(d_list[0], nilp())


def Parser(tokenlist):
    if len(tokenlist) == 0:
        return Err(Nil(), ErrorType.NO_INPUT_FILE)

    LA = tokenlist.pop(0)
    if LA.type == Keyword.LPAREN:
        if tokenlist[0].type == Keyword.RPAREN:
            return nilp()
        L = []
        while tokenlist[0].type != Keyword.RPAREN:
            L.append(Parser(tokenlist))
        tokenlist.pop(0)
        LR = iCons(L)
        return LR
    elif LA.type == Keyword.RPAREN:
        return Err(LA, ErrorType.UNEXPECTED_TOKEN)
    elif LA.value == "0":
        return Data(Type.INT, int(LA.value))
    else:
        try:
            if int(LA.value):
                return Data(Type.INT, int(LA.value))
        except:
            return Data(Type.SYM, LA.value)


class Bindings:
    def __init__(self, parent):
        self.parent = parent
        self.symbols = dict()

    def add_symbol(self, symbol, value):
        if symbol.type == Type.SYM:
            self.symbols[symbol.value.upper()] = value

    def __str__(self):
        if isNil(self.parent):
            return f"ENV class : root"
        else:
            return f"ENV class : {str(self.parent)}"

    def __repr__(self):
        return self.__str__()


def env_create(parent):
    new_bindings = Bindings(parent)
    return new_bindings


def env_get(env, symbol):
    parent = env.parent

    if symbol.value.upper() in env.symbols:
        return env.symbols[symbol.value.upper()]

    if type(parent) is Bindings:
        pass
    elif isNil(parent):
        return nilp()

    return env_get(parent, symbol)


def env_set(env, symbol, value):
    env.add_symbol(symbol, value)
    return ErrorType.ERROR_OK, nilp()


def listp(expr):
    while not isNil(expr):
        if expr.type != Type.PAIR:
            return False
        expr = expr.cdr()
    return True


def eval_expr(expr, env):
    if expr.type == Type.SYM:
        return ErrorType.ERROR_OK, env_get(env, expr)
    elif expr.type != Type.PAIR:
        return ErrorType.ERROR_OK, expr

    if not listp(expr):
        return ErrorType.ERROR_SYNTAX, nilp()

    op = expr.car()
    args = expr.cdr()

    if op.type == Type.SYM:
        if op.value.upper() == "쿼트":
            if isNil(args) or not isNil(args.cdr()):
                return ErrorType.ERROR_ARGS, nilp()
            return ErrorType.ERROR_OK, args.car()
        elif op.value.upper() == "DEF":
            if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
                return ErrorType.ERROR_ARGS, nilp()
            sym = args.car()
            if sym.type != Type.SYM:
                return ErrorType.ID_INVALID_TOKEN, nilp()

            err, val = eval_expr(args.cdr().car(), env)

            env_set(env, sym, val)
            return ErrorType.ERROR_OK, sym
        elif op.value.upper() == "LAM":
            if isNil(args) or isNil(args.cdr()):
                return ErrorType.ID_INVALID_TOKEN, nilp()
            return mk_closure(env, args.car(), args.cdr())
        elif op.value.upper() == "만약":
            if (
                isNil(args)
                or isNil(args.cdr())
                or isNil(args.cdr().cdr())
                or not isNil(args.cdr().cdr().cdr())
            ):
                return ErrorType.ERROR_ARGS, nilp()
            err, result = eval_expr(args.car(), env)
            if err != ErrorType.ERROR_OK:
                return err, nilp()
            val = args.cdr().cdr().car() if isNil(result) else args.cdr().car()
            return eval_expr(val, env)

    err, op = eval_expr(op, env)
    if err != ErrorType.ERROR_OK:
        return err, nilp()
    args = copy_list(args)
    p = args
    while not isNil(p):
        err, p.value[0] = eval_expr(p.car(), env)

        p = p.cdr()

    return apply(op, args)

    return ErrorType.ERROR_SYNTAX, nilp()


def make_builtin(fn):
    a = Data()
    a.type = Type.BUILTIN
    a.value = fn
    return a


def mk_closure(env, params, body):
    if not listp(params) or not listp(body):
        return ErrorType.ID_INVALID_TOKEN, nilp()

    p = params

    while not isNil(p):
        if p.car().type != Type.SYM:
            return ErrorType.ID_INVALID_TOKEN, nilp()
        p = p.cdr()

    result = cons(env, cons(params, body))
    result.type = Type.CLOSURE

    return ErrorType.ERROR_OK, result


def copy_list(lst):
    if isNil(lst):
        return nilp()

    a = cons(lst.car(), nilp())
    p = a
    lst = lst.cdr()

    while not isNil(lst):
        p.value[1] = cons(lst.car(), nilp())
        p = p.cdr()
        lst = lst.cdr()

    return a


def apply(fn, args):
    if fn.type == Type.BUILTIN:
        return fn.value(args)
    elif fn.type != Type.CLOSURE:
        return ErrorType.ID_INVALID_TOKEN, nilp()

    env = env_create(fn.car())
    params = fn.cdr().car()
    body = fn.cdr().cdr()

    while not isNil(params):
        if isNil(args):
            return ErrorType.ERROR_ARGS, nilp()
        env_set(env, params.car(), args.car())
        params = params.cdr()
        args = args.cdr()

    if not isNil(args):
        return ErrorType.ERROR_ARGS, nilp()

    while not isNil(body):
        err, result = eval_expr(body.car(), env)
        if err != ErrorType.ERROR_OK:
            return err, nilp()
        body = body.cdr()

    return ErrorType.ERROR_OK, result


def builtin_car(args):
    return ErrorType.ERROR_OK, args.car()


def builtin_cdr(args):
    return ErrorType.ERROR_OK, args.cdr()


def builtin_cons(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return ErrorType.ERROR_ARGS, nilp()
    return ErrorType.ERROR_OK, cons(args.car(), args.cdr())


def builtin_plus(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        var = (args.car().value) + (args.cdr().car().value)
        return ErrorType.ERROR_OK, mkint(var)
    return ErrorType.ERROR_ARGS, nilp()


def builtin_minus(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        var = (args.car().value) - (args.cdr().car().value)
        return ErrorType.ERROR_OK, mkint(var)
    return ErrorType.ERROR_ARGS, nilp()


def builtin_multi(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        var = (args.car().value) * (args.cdr().car().value)
        return ErrorType.ERROR_OK, mkint(var)
    return ErrorType.ERROR_ARGS, nilp()


def builtin_divide(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        if args.cdr().car().value != 0:
            var = (args.car().value) / (args.cdr().car().value)
            return ErrorType.ERROR_OK, mkint(var)
        else:
            return ErrorType.UNEXPECTED_TOKEN, nilp()
    return ErrorType.ERROR_ARGS, nilp()


def builtin_numeq(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):

        if args.car().value == args.cdr().car().value:
            return ErrorType.ERROR_OK, mksym("T")
        else:
            return ErrorType.ERROR_OK, nilp()
    return ErrorType.ERROR_ARGS, nilp()


def builtin_less(args):
    if (args.car().type == Type.INT) and (args.cdr().car().type == Type.INT):
        if args.car().value < args.cdr().car().value:
            return ErrorType.ERROR_OK, mksym("T")
    return ErrorType.ERROR_ARGS, nilp()


if __name__ == "__main__":
    env = env_create(nilp())

    env_set(env, mksym("머리"), make_builtin(builtin_car))
    env_set(env, mksym("꼬리"), make_builtin(builtin_cdr))
    env_set(env, mksym("쌍쌍"), make_builtin(builtin_cons))
    env_set(env, mksym("+"), make_builtin(builtin_plus))
    env_set(env, mksym("-"), make_builtin(builtin_minus))
    env_set(env, mksym("*"), make_builtin(builtin_multi))
    env_set(env, mksym("/"), make_builtin(builtin_divide))
    env_set(env, mksym("="), make_builtin(builtin_numeq))
    env_set(env, mksym("<"), make_builtin(builtin_less))
    env_set(env, mksym("T"), mksym("T"))
    env_set(env, mksym("nil"), nilp())

    print(
        "|-----------------------------------------------------------------------|\n|    o   \ o /  _ o         __|    \ /     |__        o _  \ o /   o    |\n|   /|\    |     /\   ___\o   \o    |    o/    o/__   /\     |    /|\   |\n|   / \   / \   | \  /)  |    ( \  /o\  / )    |  (\  / |   / \   / \   |\n|-----------------------------------------------------------------------|\n"
    )
    print("한글 스킴 인터프리터에 오신 것을 환영합니다.\n종료를 원할 시 ':종료'를 입력해주세요.")

    if len(sys.argv) == 2:  # 파일 입력 시
        if os.path.isfile(sys.argv[1]):
            f = open(sys.argv[1], "r", encoding="utf-8")
            line = f.readline()
            while True:
                try:
                    if not line:
                        break
                    parsedlist = Parser(Lexer(line).lex())
                    err, result = eval_expr(parsedlist, env)

                    if err != ErrorType.ERROR_OK:
                        print(err)
                    else:
                        print(">> {result}".format(result=result))
                    line = f.readline()
                except Error:
                    line = f.readline()
                except IndexError:
                    tmp = f.readline()
                    if tmp == "":
                        break
                    line += tmp
            f.close()
        else:
            print('No file "{file}" found.'.format(file=sys.argv[1]))

    elif len(sys.argv) == 1:  # 인터프리터 실행 시
        line = input(">> ")
        while line != ":종료":
            try:
                parsedlist = Parser(Lexer(line).lex())
                
                err, result = eval_expr(parsedlist, env)

                if err != ErrorType.ERROR_OK:
                    print(err)
                else:
                    print(result)
                
                line = input(">> ")
            print(eval_expr(parsedlist, env))
            except Error:
                line = input(">> ")
            except IndexError:
                tmp = input("... ")
                if tmp == "" or tmp == ":종료":
                    break
                line += tmp

    else:
        print(
            "Usage for Interpreter: kscheme.exe\nUsage for File:        ksheme.exe [scm file]"
        )
