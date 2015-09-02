import constants as c

GREEN = 0
PINK = 1
YELLOW = 2
ORANGE = 3
WHITE = 4
BLUE = 5
PURPLE = 6

def getColorFromNumber(i):
    if i == GREEN:
        return "GREEN"
    elif i == PINK:
        return "PINK"
    elif i == YELLOW:
        return "YELLOW"
    elif i == ORANGE:
        return "ORANGE"
    elif i == WHITE:
        return "WHITE"
    elif i == BLUE:
        return "BLUE"
    elif i == PURPLE:
        return "PURPLE"

def getColorFromId(i):

    if i == c.START:
        return GREEN

    elif i == c.X:
        return ORANGE

    elif i == c.VAR:
        return YELLOW

    elif i == c.EQUALS:
        return BLUE

    elif i == c.PLUS:
        return BLUE 

    elif i == c.ZERO:
        return WHITE 

    elif i == c.ONE:
        return WHITE 

    elif i == c.TWO:
        return WHITE 

    elif i == c.TEN:
        return WHITE 

    elif i == c.EEQUALS:
        return PURPLE 

    elif i == c.LT:
        return PURPLE 

    elif i == c.LOOP:
        return YELLOW 

    elif i == c.ENDLOOP:
        return YELLOW 

    elif i == c.PRINT:
        return YELLOW 

    elif i == c.STOP:
        return PINK

    elif i == c.ENDIF:
        return YELLOW

    elif i == c.MOD:
        return BLUE

    else:
        return None
