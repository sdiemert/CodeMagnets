__author__ = 'sdiemert'

import wx

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)


class AppFrame(wx.Frame):
    def __init__(self, parent, title, controller=None):

        self.controller = controller

        wx.Frame.__init__(self, parent, title=title)

        self.display = wx.Panel(self, wx.ID_ANY)

        self.PhotoMaxSize = 500

        self.SetMaxSize(wx.Size(1000, 800))

        wrapper = wx.BoxSizer(wx.VERTICAL)
        control = wx.BoxSizer(wx.HORIZONTAL)
        content = wx.BoxSizer(wx.HORIZONTAL)

        output_wrapper = wx.BoxSizer(wx.VERTICAL)
        run_wrapper = wx.BoxSizer(wx.VERTICAL)
        stdout_wrapper = wx.BoxSizer(wx.VERTICAL)
        image_wrapper = wx.BoxSizer(wx.VERTICAL)

        img = wx.EmptyImage(400, 400)

        self.image_1 = wx.StaticBitmap(self.display, wx.ID_ANY, wx.BitmapFromImage(img))

        self.output = wx.TextCtrl(self.display, wx.ID_ANY, size=(300, 198), style=wx.TE_MULTILINE)
        self.code_output = wx.TextCtrl(self.display, wx.ID_ANY, size=(300, 198), style=wx.TE_MULTILINE)
        self.result_output = wx.TextCtrl(self.display, wx.ID_ANY, size=(300, 198), style=wx.TE_MULTILINE)
        self.error_output = wx.TextCtrl(self.display, wx.ID_ANY, size=(300, 198), style=wx.TE_MULTILINE)

        # Allow for stdout to display in the UI
        # self.stdout_output = wx.TextCtrl(self.display, wx.ID_ANY, size=(900, 198), style=wx.TE_MULTILINE)
        # self.redir=RedirectText(self.stdout_output)
        # sys.stdout=self.redir
        # self.stdout_output.Disable()

        self.browse_button = wx.Button(self.display, wx.ID_ANY, label="Browse for Image")
        self.analysis_button = wx.Button(self.display, wx.ID_ANY, label="Analyze Image")
        self.generate_button = wx.Button(self.display, wx.ID_ANY, label="Generate Code")
        self.execute_button = wx.Button(self.display, wx.ID_ANY, label="Execute!")
        self.cancel_button = wx.Button(self.display, wx.ID_ANY, label="Cancel")

        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse)
        self.analysis_button.Bind(wx.EVT_BUTTON, self.on_analysis)
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate)
        self.execute_button.Bind(wx.EVT_BUTTON, self.on_execute)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.output.Disable()
        self.code_output.Disable()
        self.result_output.Disable()
        self.error_output.Disable()

        # stdout_wrapper.Add(self.stdout_output)

        output_wrapper.Add(self.output)
        output_wrapper.Add(self.code_output)

        run_wrapper.Add(self.result_output)
        run_wrapper.Add(self.error_output)

        image_wrapper.Add(self.image_1, 0, wx.ALL, 5)

        content.Add(image_wrapper, 0, wx.ALL, 5)
        content.Add(output_wrapper, 0, wx.ALL, 5)
        content.Add(run_wrapper, 0, wx.ALL, 5)

        control.Add(self.browse_button, 0, wx.ALL, 5)
        control.Add(self.analysis_button, 0, wx.ALL, 5)
        control.Add(self.generate_button, 0, wx.ALL, 5)
        control.Add(self.execute_button, 0, wx.ALL, 5)
        control.Add(self.cancel_button, 0, wx.ALL, 5)

        wrapper.Add(control, 0, wx.ALL, 5)
        wrapper.Add(content, 0, wx.ALL, 5)
        wrapper.Add(stdout_wrapper, 0, wx.ALL, 5)

        self.display.SetSizer(wrapper)
        wrapper.Fit(self)

        self.analysis_button.Disable()
        self.generate_button.Disable()
        self.execute_button.Disable()

        self.CreateStatusBar()

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_ABOUT, '&About', "Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, 'E&xit', "Exit this program")
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")

        self.SetMenuBar(menubar)
        self.Show(True)

    def on_browse(self, event):
        """
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file",
                               wildcard=wildcard,
                               style=wx.OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            self.on_view(dialog.GetPath())
        dialog.Destroy()

        self.analysis_button.Enable()
        self.generate_button.Disable()
        self.execute_button.Disable()
        self.code_output.Disable()
        self.result_output.Disable()
        self.code_output.Clear()
        self.result_output.Clear()
        self.output.Clear()
        self.output.Disable()

    def on_view(self, filepath):
        print "Browse!"
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)

        self.image_1.SetBitmap(wx.BitmapFromImage(img))
        self.set_image_path(filepath)
        self.analysis_button.Enable()
        self.execute_button.Disable()
        self.generate_button.Disable()
        self.display.Refresh()

    def on_analysis(self, event):
        print "Analysis!"
        self.analysis_button.Disable()
        self.code_output.Clear()
        self.controller.process()
        self.output.Enable()
        self.generate_button.Enable()

    def on_generate(self, event):
        print "Generate!"
        self.code_output.SetValue(self.controller.generate())
        self.execute_button.Enable()
        self.code_output.Enable()

    def on_execute(self, event):
        print "Execute!"
        self.result_output.Clear()
        self.error_output.Clear()
        result = self.controller.execute(self.code_output.GetValue())

        print result

        if result[1]:
            self.result_output.SetValue("There was an error!\nSee the error printout below.")
            self.error_output.SetValue(result[1])
        else:
            self.result_output.SetValue(result[0])
            self.error_output.SetValue("No Errors...")

        self.result_output.Enable()
        self.error_output.Enable()

    def on_cancel(self, event):
        print "Cancel!"
        self.output.Clear()
        self.code_output.Clear()
        self.result_output.Clear()
        self.error_output.Clear()

        self.image_1.SetBitmap(wx.BitmapFromImage(wx.EmptyImage(400, 400)))
        self.display.Refresh()

        self.execute_button.Disable()
        self.generate_button.Disable()
        self.analysis_button.Enable()

        self.result_output.Disable()
        self.error_output.Disable()
        self.code_output.Disable()
        self.output.Disable()

    def set_controller(self, c):
        self.controller = c

    def set_image_path(self, p):

        if self.controller:
            self.controller.set_image_path(p)

    def println(self, m):
        self.output.AppendText(m+"\n")

    def show_code(self, code):
        for l in code:
            self.println(" ".join(l))

    def get_output_text(self):
        x = self.output.GetValue()
        return x.split("\n")
