__author__ = 'sdiemert'

import wx

from CodeMagnets import AppFrame
from CodeMagnets import Controller

app = wx.App(False)

frame = AppFrame(None, "Code Magnets")

control = Controller()

frame.set_controller(control)
control.set_view(frame)

app.MainLoop()
