import sys
from gui.cli import main_menu
import wx
from gui.main_menu import MainFrame

if __name__ == "__main__":
    if '--console' in sys.argv:
        main_menu()
    else:
        app = wx.App()
        frame = MainFrame()
        app.MainLoop()
