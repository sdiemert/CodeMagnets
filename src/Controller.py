__author__ = 'sdiemert'

from ImageProcessor import CodeMagnetsImageProcessor
from CodeGenerator import CodeGenerator

class Controller:

    def __init__(self, view=None, path=None):
        self.view = view
        self.image_path = path

        self.processor = CodeMagnetsImageProcessor()
        self.processor.train(readFromFile=True, path="data.csv")
        self.code_generator = CodeGenerator()

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

    def execute(self):
        x = self.do_code_generation()
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
