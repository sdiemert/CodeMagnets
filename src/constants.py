START = 0
X = 1
VAR = 2
EQUALS = 3
PLUS = 4
ZERO = 5
Y = 6
EEQUALS = 7
LT = 8
MINUS = 9
MOD = 10
MULT = 11
NEQUALS = 12
IF = 13
LOOP = 14
TWO = 15
TEN = 16
ENDLOOP = 17
STOP = 18
PRINT = 19
ONE = 20


def getConstantFromString(s):
    s = s.lower() 

    if s == 'start':
        return START
    elif s == 'x':
        return X 
    elif s == 'var':
        return VAR
    elif s == 'equals':
        return EQUALS
    elif s == 'plus':
        return PLUS
    elif s == '0' or s == 'zero':
        return ZERO
    elif s == '10' or s == 'ten':
        return TEN
    elif s == '2' or s == 'two':
        return TWO
    elif s == '1' or s == 'one':
        return ONE
    elif s == 'y':
        return Y
    elif s == 'eequals':
        return EEQUALS
    elif s == 'lt':
        return LT
    elif s == 'minus':
        return MINUS
    elif s == 'mod':
        return MOD
    elif s == 'mult':
        return MULT
    elif s == 'nequals':
        return NEQUALS
    elif s == 'if':
        return IF
    elif s == 'loop':
        return LOOP
    elif s == 'endloop':
        return ENDLOOP
    elif s == 'stop':
        return STOP
    elif s == 'print':
        return PRINT
    else:
        return None

def getStringFromNumber(n):
    s = int(n)

    if s == START:
        return "START"
    elif s == X:
        return "X" 
    elif s == VAR:
        return "VAR"
    elif s == EQUALS:
        return "EQUALS" 
    elif s == PLUS:
        return "PLUS"
    elif s == ZERO :
        return "0"
    elif s == TEN :
        return "10"
    elif s == TWO :
        return "2"
    elif s == ONE :
        return "1"
    elif s == Y:
        return "Y" 
    elif s == EEQUALS:
        return "EEQUALS"
    elif s == LT:
        return "LT"
    elif s == MINUS:
        return 'MINUS'
    elif s == MOD:
        return 'MOD'
    elif s == MULT:
        return 'MULT'
    elif s == NEQUALS:
        return 'NEQUALS'
    elif s == IF:
        return 'IF' 
    elif s == ENDLOOP:
        return 'ENDLOOP' 
    elif s == LOOP:
        return 'LOOP' 
    elif s == STOP:
        return 'STOP' 
    elif s == PRINT:
        return 'PRINT' 
    else:
        return None
