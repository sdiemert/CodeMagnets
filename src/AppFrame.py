__author__ = 'sdiemert'

import wx


class AppFrame(wx.Frame):
    def __init__(self, parent, title, controller=None):

        self.controller = controller

        wx.Frame.__init__(self, parent, title=title)

        self.display = wx.Panel(self, wx.ID_ANY)

        self.PhotoMaxSize = 500

        self.SetMaxSize(wx.Size(900, 800))

        wrapper = wx.BoxSizer(wx.VERTICAL)
        control = wx.BoxSizer(wx.HORIZONTAL)
        content = wx.BoxSizer(wx.HORIZONTAL)

        img = wx.EmptyImage(400, 400)
        self.image_1 = wx.StaticBitmap(self.display, wx.ID_ANY, wx.BitmapFromImage(img))
        self.output = wx.TextCtrl(self.display, wx.ID_ANY, size=(400, 400), style=wx.TE_MULTILINE)
        self.browse_button = wx.Button(self.display, wx.ID_ANY, label="Browser for File")
        self.analysis_button = wx.Button(self.display, wx.ID_ANY, label="Analyze Image")
        self.execute_button = wx.Button(self.display, wx.ID_ANY, label="Execute Code!")

        self.browse_button.Bind(wx.EVT_BUTTON, self.on_browse)
        self.analysis_button.Bind(wx.EVT_BUTTON, self.on_analysis)
        self.execute_button.Bind(wx.EVT_BUTTON, self.on_execute)

        self.output.Disable()

        content.Add(self.image_1, 0, wx.ALL, 5)
        content.Add(self.output, 0, wx.ALL, 5)

        control.Add(self.browse_button, 0, wx.ALL, 5)
        control.Add(self.analysis_button, 0, wx.ALL, 5)
        control.Add(self.execute_button, 0, wx.ALL, 5)

        wrapper.Add(control, 0, wx.ALL, 5)
        wrapper.Add(content, 0, wx.ALL, 5)

        self.display.SetSizer(wrapper)
        wrapper.Fit(self)

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
        self.display.Refresh()

    def on_analysis(self, event):
        print "Analysis!"
        self.controller.process()

    def on_execute(self, event):
        print "Execute!"
        pass

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
