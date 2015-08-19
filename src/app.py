__author__ = 'sdiemert'

import wx

from AppFrame import AppFrame
from Controller import Controller

app = wx.App(False)

frame = AppFrame(None, "Code Magnets")

control = Controller()

frame.set_controller(control)
control.set_view(frame)

app.MainLoop()
