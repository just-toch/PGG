import sys
from gui.cli import main_menu
import wx
from gui.main_menu import MainFrame
from utils import GoogleSheets

if __name__ == "__main__":
    google_sheets = GoogleSheets()
    if '--console' in sys.argv:
        main_menu(google_sheets)
    else:
        app = wx.App()
        frame = MainFrame(google_sheets)
        app.MainLoop()
