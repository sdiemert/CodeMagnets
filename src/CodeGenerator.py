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

            s = self.get_statement(l)

            if not s:
                continue

            statement_type = s.__class__.__name__

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
                print "failed on: "+str(st)

        s = s.replace("plus", "+")
        s = s.replace("lt", "<")
        s = s.replace("gt", ">")

        return s

    def get_statement(self, statement):

        s = statement.split(" ")

        # check the first word of the statement

        if s[0] == "VAR" and s[2] == "EQUALS":
            return Declaration(s[1], s[3])

        elif s[0] == "LOOP":
            if len(s) > 2:
                return Loop(s[1:])

        elif s[0] == "PRINT":
            if len(s) > 1:
                return Print(s[1:])

        elif (s[0] == "X" or s[0] == "Y") and s[1] == "EQUALS":
            return Assignment(s[0], s[2:])

        elif s[0] == "IF":
            return If(s[2:])

        elif s[0] == "ENDLOOP" or s[0] == "ENDIF":
            return EndBlock(s[0])
