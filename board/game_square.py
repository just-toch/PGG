from .square_status import SquareStatus


class GameSquare:

    def __init__(self, column, row, name, description):
        self.column = column
        self.row = row
        self.name = name
        self.description = description
        self.status = SquareStatus.CLOSED
        self.mark = 'x'

    def coordinates(self):
        return f'{self.row}{self.column}'

    def data(self):
        return f'{self.name}\n{self.description}'

    def change_to_available(self):
        if self.status == SquareStatus.CLOSED:
            self.status = SquareStatus.AVAILABLE
            self.mark = 'a'

    def change_to_opened(self):
        if self.status == SquareStatus.AVAILABLE:
            self.status = SquareStatus.OPENED
            self.mark = 'o'

    def change_to_cleared(self):
        if self.status == SquareStatus.OPENED:
            self.status = SquareStatus.CLEARED
            self.mark = '!!'

    def save(self):
        return {
            'row': self.row,
            'column': self.column,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'mark': self.mark
        }