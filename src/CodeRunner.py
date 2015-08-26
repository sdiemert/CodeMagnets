__author__ = 'sdiemert'

import subprocess

class CodeRunner:
    def __init__(self):
        pass

    def create_file(self, program):
        f = open('tmp.py', 'w')
        f.write(program)
        f.close()
        return "tmp.py"

    def execute(self, prog):
        print "Program is: " + prog
        path = self.create_file(prog)
        codeproc = subprocess.Popen(['python', path], stdout=subprocess.PIPE)
        x = codeproc.stdout.read()
        return x


if __name__ == "__main__":
    p = "print 'It works!'"
    c = CodeRunner()
    print c.execute(p)
