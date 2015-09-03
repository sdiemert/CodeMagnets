__author__ = 'sdiemert'

from ImageProcessor import CodeMagnetsImageProcessor
from CodeGenerator import CodeGenerator
from CodeRunner import CodeRunner

class Controller:

    def __init__(self, view=None, path=None):
        self.view = view
        self.image_path = path

        self.processor = CodeMagnetsImageProcessor()
        self.processor.train(readFromFile=True, path="data.csv")
        self.code_generator = CodeGenerator()
        self.code_runner = CodeRunner()

    def set_view(self, v):
        self.view = v

    def set_image_path(self, path):
        self.image_path = path
        print "Controller.image_path set to: "+self.image_path

    def process(self):

        if not self._process_precondition():
            return None

        r = self.processor.process(self.image_path)

        print r

        self._send_output(r)

    def generate(self):
        x = self.do_code_generation()
        print "done generate()"
        return x

    def execute(self, code):
        print "Controller.execute(): "+code
        x = self.do_execute(code)
        print "done execute()"
        return x

    def _process_precondition(self):
        if not self.image_path:
            return False
        elif not self.processor:
            return False
        else:
            return True

    def _send_output(self, data):
        if self.view:
            self.view.show_code(data)

    def do_code_generation(self):
        return self.code_generator.get_code(self.view.get_output_text())

    def do_execute(self, c):
        return self.code_runner.execute(c)
