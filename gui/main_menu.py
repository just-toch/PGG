# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MyPanel4
###########################################################################

class MyPanel4 ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 854,480 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

        gSizer2 = wx.GridSizer( 6, 1, 5, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"POVSTANCI GOVNA GAUNTLET"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        self.m_staticText3.SetFont( wx.Font( 20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Baloo" ) )

        gSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.StartButton = wx.Button( self, wx.ID_ANY, _(u"Старт"), wx.DefaultPosition, wx.Size( 200,50 ), 0 )
        gSizer2.Add( self.StartButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.StatsButton = wx.Button( self, wx.ID_ANY, _(u"Статистика игроков"), wx.DefaultPosition, wx.Size( 200,50 ), 0 )
        self.StatsButton.SetMinSize( wx.Size( 200,50 ) )

        gSizer2.Add( self.StatsButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

        bSizer12 = wx.BoxSizer( wx.VERTICAL )


        gSizer2.Add( bSizer12, 1, wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.VERTICAL )


        gSizer2.Add( bSizer13, 1, wx.EXPAND, 5 )

        self.ExitButton = wx.Button( self, wx.ID_ANY, _(u"Выход"), wx.DefaultPosition, wx.Size( 200,50 ), 0 )
        gSizer2.Add( self.ExitButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


        self.SetSizer( gSizer2 )
        self.Layout()

        # Connect Events
        self.StartButton.Bind( wx.EVT_BUTTON, self.Start )
        self.StatsButton.Bind( wx.EVT_BUTTON, self.Stats )
        self.ExitButton.Bind( wx.EVT_BUTTON, self.Exit )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def Start( self, event ):
        event.Skip()

    def Stats( self, event ):
        event.Skip()

    def Exit( self, event ):
        wx.Exit()


class MainApp(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, title="POVSTANCI GOVNA GAUNTLET", size=(854, 480))
        self.panel = MyPanel4(self.frame)
        self.frame.Centre()
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()