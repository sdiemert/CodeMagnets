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
    def __init__(self, expr, depth=0):
        self.expr = Expr(expr)
        self.sub_statements = []
        self.depth = depth

    def add_sub_statement(self, s):
        self.sub_statements.append(s)

    def get_code(self):
        return self.get_tab()+self.expr.get_code()

    def get_tab(self):
        return '\t'*self.depth

class Declaration(Statement):

    def __init__(self, var, expr, depth=0):
        Statement.__init__(self, expr, depth)
        self.var = var

    def get_code(self):
        return self.get_tab()+self.var.lower()+" = "+self.expr.get_code()+"\n"

class Loop(Statement):

    def __init__(self, expr, depth=0):
        Statement.__init__(self, expr, depth)

    def get_code(self):
        s = self.get_tab()+"while "+self.expr.get_code()+":\n"
        for i in self.sub_statements:
            s += i.get_code()+"\n"
        return s

class Print(Statement):

    def __init__(self, expr, depth=0):
        Statement.__init__(self, expr, depth)

    def get_code(self):
        return self.get_tab()+"print "+self.expr.get_code()

class Assignment(Statement):

    def __init__(self, target, expr, depth=0):
        Statement.__init__(self, expr, depth)
        self.target = target

    def get_code(self):
        return self.get_tab()+self.target.lower()+" = "+self.expr.get_code()+"\n"

class If(Statement):

    def __init__(self, expr, depth=0):
        Statement.__init__(self, expr, depth)

    def get_code(self):
        s = self.get_tab()+"if "+self.expr.get_code()+":\n"

        for i in self.sub_statements:
            s += i.get_code()+"\n"
        return s

class EndBlock(Statement):

    def __init__(self, v):
        Statement.__init__(self, v)
        self.value = v
