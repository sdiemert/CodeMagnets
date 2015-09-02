__author__ = 'sdiemert'

import subprocess as sub
import threading

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout
        self.result = None

    def run(self):
        self.p = sub.Popen(self.cmd, stdout=sub.PIPE, stderr=sub.PIPE)
        self.result = self.p.communicate()
        self.p.wait()

    def Run(self):
        print "timeout is: "+str(self.timeout)
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.kill()
            self.join()
            return (None, "Timeout reached!\nDoes you program infinite loop?")
        else:
            return self.result

class CodeRunner:
    def __init__(self):
        self.runner = None

    def create_file(self, program):
        f = open('tmp.py', 'w')
        f.write(program)
        f.close()
        return "tmp.py"

    def execute(self, prog):
        print "Program is: " + prog

        path = self.create_file(prog)

        try:
            x,y = self.runner = RunCmd(["python", path], 5).Run()
        except Exception as e:
            print e
            x = None
            y = "Error!"

        return x,y


if __name__ == "__main__":
    p = "print 'It works!'"
    c = CodeRunner()
    print c.execute(p)
