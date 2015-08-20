__author__ = 'sdiemert'

class Expr:

    def __init__(self, e):
        self.value = e

    def get_code(self):
        try:
            x = " ".join(self.value).lower()
            return x

        except:
            print "failed on "+self.value

class Statement:
    def __init__(self, expr):
        self.expr = Expr(expr)
        self.sub_statements = []

    def add_sub_statement(self, s):
        self.sub_statements.append(s)

    def get_code(self):
        return self.expr.get_code()

class Declaration(Statement):

    def __init__(self, var, expr):
        Statement.__init__(self, expr)
        self.var = var

    def get_code(self):
        return self.var.lower()+" = "+self.expr.get_code()+"\n"

class Loop(Statement):

    def __init__(self, expr):
        Statement.__init__(self, expr)

    def get_code(self):
        s = "while "+self.expr.get_code()+":\n"
        for i in self.sub_statements:
            s += "\t"+i.get_code()+"\n"
        return s

class Print(Statement):

    def __init__(self, expr):
        Statement.__init__(self, expr)

    def get_code(self):
        return "print "+self.expr.get_code()

class Assignment(Statement):

    def __init__(self, target, expr):
        Statement.__init__(self, expr)
        self.target = target

    def get_code(self):
        return self.target.lower()+" = "+self.expr.get_code()+"\n"

class If(Statement):

    def __init__(self, expr):
        Statement.__init__(self, expr)

    def get_code(self):
        s = "if "+self.expr.get_code()+":"

        for i in self.sub_statements:
            s += "\t"+i.get_code()+"\n"
        return s

class EndBlock(Statement):

    def __init__(self, v):
        Statement.__init__(self, v)
        self.value = v
