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

from board.square_status import SquareStatus
from utils.gsheets import (load_game_from_cloud, create_player_worksheet, get_column)
from utils.game import new_game, open_squares, save_game, check_victory
from json import decoder

_ = gettext.gettext

# names = get_column('games', 1)
# descriptions = get_column('games', 2)

###########################################################################
## Class MainMenu
###########################################################################

class MainMenu ( wx.Panel ):

    def __init__(self, parent, frame_id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size(854, 480), style = wx.TAB_TRAVERSAL, name = wx.EmptyString):
        wx.Panel.__init__ (self, parent, id = frame_id, pos = pos, size = size, style = style, name = name)

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


        gSizer2.Add( wx.Size(0, 0), 1, wx.EXPAND, 5 )


        gSizer2.Add( wx.Size(0, 0), 1, wx.EXPAND, 5 )

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
    def Start(self, event):
        dialog = NameInput(self)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            player_name = dialog.get_player_name()
            print(f"Игрок: {player_name}")

            try:
                if create_player_worksheet(player_name):
                    player = new_game(player_name)
                else:
                    print('Такой игрок уже существует')
                    try:
                        player = load_game_from_cloud(player_name)
                    except (decoder.JSONDecodeError, TypeError):
                        print('Однако данных по нему нет или они повреждены, создаю нового пользователя')
                        player = new_game(player_name)
                game_frame = wx.Frame(None, title=f"Игра - {player_name}", size=wx.Size(854, 480))
                game_panel = Game(game_frame, player=player, game_field=player.field)
                game_frame.player = player
                game_frame.game_panel = game_panel
                game_frame.Centre()
                game_frame.Show()
                self.GetParent().Close()

            except Exception as e:
                print(f"Ошибка: {e}")
                wx.MessageBox(f"Ошибка создания игры: {e}", "Ошибка", wx.OK | wx.ICON_ERROR)

        dialog.Destroy()
        event.Skip()

    def Stats( self, event ):
        event.Skip()

    def Exit( self, event ):
        self.GetParent().Close()
        event.Skip()


###########################################################################
## Class NameInput
###########################################################################

class NameInput ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 459,176 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        gbSizer3 = wx.GridBagSizer( 0, 0 )
        gbSizer3.SetFlexibleDirection( wx.BOTH )
        gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m123 = wx.StaticText( self, wx.ID_ANY, _(u"Введите имя"), wx.Point( 3,0 ), wx.DefaultSize, 0 )
        self.m123.Wrap( -1 )

        gbSizer3.Add( self.m123, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 30 ), wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_textCtrl11 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer3.Add( self.m_textCtrl11, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 30 ), wx.ALL|wx.EXPAND, 15 )

        self.Ok = wx.Button( self, wx.ID_ANY, _(u"Принять"), wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer3.Add( self.Ok, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 30 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        gbSizer3.AddGrowableCol( 0 )
        gbSizer3.AddGrowableCol( 1 )
        gbSizer3.AddGrowableCol( 2 )

        self.SetSizer( gbSizer3 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Ok.Bind( wx.EVT_BUTTON, self.close_dialog )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def get_player_name(self):
        """Метод для получения введенного имени"""
        return self.m_textCtrl11.GetValue().strip()

    def close_dialog(self, event):
        """Обработчик кнопки Принять"""
        name = self.get_player_name()
        if not name:  # Если имя пустое
            wx.MessageBox("Пожалуйста, введите имя!", "Внимание", wx.OK | wx.ICON_WARNING)
            self.m_textCtrl11.SetFocus()
            return

        self.EndModal(wx.ID_OK)
        event.Skip()


class Game(wx.Panel):
    def __init__(self, parent, player=None, game_field=None, frame_id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.Size(854, 480),
                 style=wx.TAB_TRAVERSAL, name=wx.EmptyString):
        wx.Panel.__init__(self, parent, id=frame_id, pos=pos, size=size, style=style, name=name)
        self.player = player
        self.game_field = game_field or (player.field if player else [])
        self.selected_square = None
        self.selected_cell = None
        print("Создание игрового поля:")
        print(f"Размер поля: {len(self.game_field)}x{len(self.game_field[0]) if self.game_field else 0}")
        for row in range(5):
            for col in range(5):
                if row < len(self.game_field) and col < len(self.game_field[row]):
                    square = self.game_field[row][col]
                    print(f"Клетка ({row},{col}): name={square.name}, status={square.status}")
                else:
                    print(f"Клетка ({row},{col}): ОШИБКА - не существует")
        try:
            self.names = get_column('games', 1)
            self.descriptions = get_column('games', 2)
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.names = [f"Клетка {i + 1}" for i in range(25)]
            self.descriptions = [f"Описание {i + 1}" for i in range(25)]

        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))

        fgSizer1 = wx.FlexGridSizer(5, 3, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizer2 = wx.FlexGridSizer(5, 5, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.cells = []
        for row in range(5):
            for col in range(5):
                if row < len(self.game_field) and col < len(self.game_field[row]):
                    square = self.game_field[row][col]
                    cell = self.create_cell(row, col, square)
                else:
                    cell = self.create_empty_cell(row, col)

                fgSizer2.Add(cell, 0, wx.ALL | wx.EXPAND, 5)
                self.cells.append(cell)

        fgSizer1.Add(fgSizer2, 1, wx.EXPAND, 5)

        self.m_staticline3 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        fgSizer1.Add(self.m_staticline3, 0, wx.EXPAND | wx.ALL, 5)

        wSizer2 = wx.WrapSizer(wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS)

        self.name_text = wx.StaticText(self, wx.ID_ANY, _(u"Выберите клетку"), wx.DefaultPosition, wx.Size(390, 50), 0)
        self.name_text.Wrap(-1)
        self.name_text.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        wSizer2.Add(self.name_text, 0, wx.ALL, 5)

        self.description_text = wx.StaticText(self, wx.ID_ANY, _(u"Выберите клетку"), wx.DefaultPosition,
                                              wx.Size(390, 150), 0)
        self.description_text.Wrap(-1)
        self.description_text.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        wSizer2.Add(self.description_text, 0, wx.ALL, 5)

        self.open_button = wx.Button(self, wx.ID_ANY, _(u"Раскрыть клетку"), wx.DefaultPosition, wx.Size(180, 30), 0)
        self.open_button.Disable()
        wSizer2.Add(self.open_button, 0, wx.ALL, 5)

        self.clear_button = wx.Button(self, wx.ID_ANY, _(u"Зачистить клетку"), wx.DefaultPosition, wx.Size(180, 30), 0)
        self.clear_button.Disable()
        wSizer2.Add(self.clear_button, 0, wx.ALL, 5)

        player_info = self.get_player_info()
        self.player_info_text = wx.StaticText(self, wx.ID_ANY, player_info, wx.DefaultPosition, wx.Size(390, 100), 0)
        self.player_info_text.Wrap(-1)
        self.player_info_text.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        wSizer2.Add(self.player_info_text, 0, wx.ALL, 5)

        fgSizer3 = wx.FlexGridSizer(0, 2, 0, 235)
        fgSizer3.SetFlexibleDirection(wx.HORIZONTAL)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer3.SetMinSize(wx.Size(390, -1))
        self.m_button119 = wx.Button(self, wx.ID_ANY, _(u"Сохранить"), wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer3.Add(self.m_button119, 0, wx.ALL, 5)

        self.m_button120 = wx.Button(self, wx.ID_ANY, _(u"Выход"), wx.Point(-1, -1), wx.DefaultSize, 0)
        fgSizer3.Add(self.m_button120, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        wSizer2.Add(fgSizer3, 1, wx.EXPAND | wx.RIGHT, 5)

        fgSizer1.Add(wSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(fgSizer1)
        self.Layout()

        self.m_button119.Bind(wx.EVT_BUTTON, self.on_save)
        self.m_button120.Bind(wx.EVT_BUTTON, self.on_exit)
        self.open_button.Bind(wx.EVT_BUTTON, self.on_open_square)
        self.clear_button.Bind(wx.EVT_BUTTON, self.on_clear_square)

        self.check_victory()

    def create_cell(self, row, col, square):
        cell_text = self.get_cell_text(square)

        cell = wx.StaticText(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(75, 75),
                             wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE | wx.BORDER_SIMPLE)
        cell.Wrap(70)

        if square.status == SquareStatus.CLEARED:
            cell.SetLabel(cell_text)
            cell.SetBackgroundColour(wx.Colour(200, 255, 200))
            cell.SetForegroundColour(wx.BLACK)
            cell.Bind(wx.EVT_LEFT_DOWN, self.create_cell_handler(row, col))

        elif square.status == SquareStatus.CLOSED:
            cell.SetLabel('')
            cell.SetBackgroundColour(wx.Colour(150, 150, 150))
            cell.SetForegroundColour(wx.Colour(100, 100, 100))

        elif square.status == SquareStatus.OPENED:
            cell.SetLabel(cell_text)
            cell.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
            cell.SetForegroundColour(wx.BLACK)
            cell.Bind(wx.EVT_LEFT_DOWN, self.create_cell_handler(row, col))

        elif square.status == SquareStatus.AVAILABLE:
            cell.SetLabel('???')
            cell.SetBackgroundColour(wx.Colour(255, 255, 200))
            cell.SetForegroundColour(wx.BLACK)
            cell.Bind(wx.EVT_LEFT_DOWN, self.create_cell_handler(row, col))

        return cell

    def create_empty_cell(self, _row, _col):
        cell = wx.StaticText(self, wx.ID_ANY, "ERROR", wx.DefaultPosition, wx.Size(75, 75),
                             wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE | wx.BORDER_SIMPLE)
        cell.SetBackgroundColour(wx.Colour(255, 200, 200))
        cell.SetForegroundColour(wx.BLACK)
        return cell

    def get_cell_text(self, square):
        if hasattr(square, 'name'):
            try:
                name_index = int(square.name)
                if 0 <= name_index < len(self.names):
                    return str(self.names[name_index])
                else:
                    return f"Клетка {square.name}"
            except (ValueError, TypeError):
                return str(square.name)
        return f"R{square.row}C{square.column}"

    def create_cell_handler(self, row, col):
        def on_cell_click(event):
            self.on_square_click(row, col, event)
        return on_cell_click

    def on_cell_enter(self, event):
        cell = event.GetEventObject()
        cell.SetBackgroundColour(wx.Colour(200, 200, 255))  # Светло-синий
        cell.Refresh()
        event.Skip()

    def on_cell_leave(self, event):
        cell = event.GetEventObject()
        cell.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        cell.Refresh()
        event.Skip()

    def on_cell_enter_available(self, event):
        cell = event.GetEventObject()
        cell.SetBackgroundColour(wx.Colour(255, 255, 150))  # Ярко-желтый
        cell.Refresh()
        event.Skip()

    def on_cell_leave_available(self, event):
        cell = event.GetEventObject()
        cell.SetBackgroundColour(wx.Colour(255, 255, 200))  # Светло-желтый
        cell.Refresh()
        event.Skip()

    def on_square_click(self, row, col, event):
        if row < len(self.game_field) and col < len(self.game_field[row]):
            square = self.game_field[row][col]
            cell = event.GetEventObject()

            if self.selected_cell:
                self.reset_cell_color(self.selected_cell, self.selected_square)

            self.selected_square = square
            self.selected_cell = cell

            self.set_selected_cell_color(cell, square)

        if row < len(self.game_field) and col < len(self.game_field[row]):
            square = self.game_field[row][col]
            self.selected_square = square
            if square.status == SquareStatus.AVAILABLE:
                self.name_text.SetLabel("Закрытая клетка")
                self.description_text.SetLabel("Эта клетка доступна для открытия, но пока скрыта")
                cell = event.GetEventObject()
                cell.SetBackgroundColour(wx.Colour(255, 255, 150))  # Ярко-желтый
                cell.Refresh()
            else:
                try:
                    name_index = int(square.name)
                    if 0 <= name_index < len(self.descriptions):
                        name = self.names[name_index]
                        description = self.descriptions[name_index]
                        self.name_text.SetLabel(name)
                        self.description_text.SetLabel(description)
                    else:
                        self.name_text.SetLabel(f"Клетка {square.name}")
                        self.description_text.SetLabel(f"Описание для клетки {square.name}")
                except (ValueError, TypeError):
                    self.name_text.SetLabel(str(square.name))
                    self.description_text.SetLabel(f"Клетка: {square.name}")

            self.update_action_buttons(square)

    def reset_cell_color(self, cell, square):
        if square.status == SquareStatus.CLEARED:
            cell.SetBackgroundColour(wx.Colour(200, 255, 200))  # Светло-зеленый
        elif square.status == SquareStatus.CLOSED:
            cell.SetBackgroundColour(wx.Colour(150, 150, 150))  # Серый
        elif square.status == SquareStatus.OPENED:
            cell.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        elif square.status == SquareStatus.AVAILABLE:
            cell.SetBackgroundColour(wx.Colour(255, 255, 200))  # Светло-желтый
        cell.Refresh()

    def set_selected_cell_color(self, cell, square):
        if square.status == SquareStatus.CLEARED:
            cell.SetBackgroundColour(wx.Colour(100, 200, 100))  # Темно-зеленый
        elif square.status == SquareStatus.CLOSED:
            cell.SetBackgroundColour(wx.Colour(100, 100, 100))  # Темно-серый
        elif square.status == SquareStatus.OPENED:
            cell.SetBackgroundColour(wx.Colour(150, 150, 200))  # Темно-синий
        elif square.status == SquareStatus.AVAILABLE:
            cell.SetBackgroundColour(wx.Colour(200, 200, 100))  # Темно-желтый
        cell.Refresh()

    def update_action_buttons(self, square):
        self.open_button.Disable()
        self.clear_button.Disable()

        if square.status == SquareStatus.AVAILABLE:
            if self.player and self.player.tokens > 0:
                self.open_button.Enable()
                self.open_button.SetLabel("Раскрыть клетку")
            else:
                self.open_button.Disable()
                self.open_button.SetLabel("Нет токенов")

        elif square.status == SquareStatus.OPENED:
            self.clear_button.SetLabel("Зачистить клетку")
            self.clear_button.Enable()

    def on_open_square(self, _event):
        if self.selected_square and self.selected_square.status == SquareStatus.AVAILABLE:
            print(f"Открываем клетку: row={self.selected_square.row}, col={self.selected_square.column}")
            self.selected_square.status = SquareStatus.OPENED

            if self.player:
                print(f"Игрок: {self.player.name}, поле: {len(self.player.field)}x{len(self.player.field[0])}")
                open_squares(self.selected_square, self.player)
            else:
                print("Ошибка: player is None")
            self.refresh_cells()
            self.player.tokens -= 1
            self.update_player_info()

    def on_clear_square(self, _event):
        if self.selected_square and self.selected_square.status == SquareStatus.OPENED:
            self.selected_square.status = SquareStatus.CLEARED
            self.player.tokens += 3
            self.update_player_info()
            self.check_victory()
            self.refresh_cells()

    def refresh_cells(self):
        save_game(self.player)
        self.selected_square = None
        self.selected_cell = None

        fgSizer2 = self.GetSizer().GetItem(0).GetSizer()
        fgSizer2.Clear(True)

        self.cells = []

        for row in range(5):
            for col in range(5):
                if row < len(self.game_field) and col < len(self.game_field[row]):
                    square = self.game_field[row][col]
                    cell = self.create_cell(row, col, square)
                else:
                    cell = self.create_empty_cell(row, col)

                fgSizer2.Add(cell, 0, wx.ALL | wx.EXPAND, 5)
                self.cells.append(cell)

        self.Layout()
        self.Refresh()

    def get_player_info(self):
        if self.player:
            return f"Игрок: {self.player.name}\nТокены: {self.player.tokens}\nСтатус: Активен"
        return "Информация об игроке"

    def update_player_info(self):
        self.player_info_text.SetLabel(self.get_player_info())

    def check_victory(self):
        if self.player and check_victory(self.player):
            wx.MessageBox("Поздравляем! Вы победили!", "Победа!", wx.OK | wx.ICON_INFORMATION)

    def on_save(self, _event):
        if self.player:
            save_game(self.player)
            wx.MessageBox("Игра сохранена!", "Сохранение", wx.OK | wx.ICON_INFORMATION)

    def on_exit(self, _event):
        self.GetParent().Close()

    def __del__(self):
        pass


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="POVSTANCI GOVNA GAUNTLET", size=wx.Size(854, 480))
        self.current_panel = None
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)
        self.show_main_menu()
        self.Centre()
        self.Show()

    def show_main_menu(self):
        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = MainMenu(self)
        self.main_sizer.Clear()
        self.main_sizer.Add(self.current_panel, 1, wx.EXPAND)
        self.Layout()

    def show_game_panel(self, game_panel):
        if self.current_panel:
            self.current_panel.Destroy()
        self.current_panel = game_panel
        self.main_sizer.Clear()
        self.main_sizer.Add(self.current_panel, 1, wx.EXPAND)
        self.Layout()

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()