__author__ = 'sdiemert'

from statements.Statements import *

class CodeGenerator:
    def __init__(self):
        pass

    def get_code(self, lines):
        print "CodeGenerator.get_code()"
        print lines

        x = []

        prog = []

        for l in lines:
            if l:
                x.append(l)

        # make sure the program has a start and stop.

        if x[0] != "START":
            x[0] = "START"

        if x[len(x) - 1] != "STOP":
            x[len(x) - 1] = "STOP"

        depth = []

        for l in x:

            s = self.get_statement(l, depth=len(depth))

            if not s:
                continue

            statement_type = s.__class__.__name__

            print statement_type, len(depth)

            if len(depth) == 0:
                prog.append(s)
            else:
                if statement_type != "EndBlock":
                    depth[len(depth) - 1].add_sub_statement(s)

            if statement_type == "Loop":
                depth.append(s)
            elif statement_type == "If":
                depth.append(s)
            elif statement_type == "EndBlock":
                depth.pop()

        return self.get_code_string(prog)

    def get_code_string(self, prog):

        s = ""

        for st in prog:
            try:
                x = st.get_code()
                s += str(x)
            except:
                print "failed on: " + str(st)

        s = s.replace("plus", "+")
        s = s.replace("minus", "-")
        s = s.replace("lt", "<")
        s = s.replace("gt", ">")
        s = s.replace("mod", "%")
        s = s.replace("eequals", "==")
        s = s.replace("equals", "=")
        s = s.replace("zero", "0")
        s = s.replace("one", "1")
        s = s.replace("two", "2")
        s = s.replace("ten", "10")

        return s

    def get_statement(self, statement, depth=0):

        s = statement.split(" ")

        # check the first word of the statement

        if s[0] == "VAR" and s[2] == "EQUALS":
            return Declaration(s[1], s[3], depth=depth)

        elif s[0] == "LOOP":
            if len(s) > 2:
                return Loop(s[1:], depth=depth)

        elif s[0] == "PRINT":
            if len(s) > 1:
                return Print(s[1:], depth=depth)

        elif (s[0] == "X" or s[0] == "Y") and s[1] == "EQUALS":
            return Assignment(s[0], s[2:], depth=depth)

        elif s[0] == "IF":
            return If(s[1:], depth=depth)

        elif s[0] == "ENDLOOP" or s[0] == "ENDIF":
            return EndBlock(s[0])


if __name__ == "__main__":
    s = "START\nVAR X EQUALS 0\nLOOP X LT 10\nIF X MOD 2 LT 0\nPRINT X\nENDIF\nX EQUALS X PLUS 1\nENDLOOP\nSTOP"
    print s
    c = CodeGenerator()
    print c.get_code(s.split("\n"))
