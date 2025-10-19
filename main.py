from gui.cli import main_menu
import wx
from gui.main_menu import MainFrame

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()


# if __name__ == "__main__":
#     main_menu()
