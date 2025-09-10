class Player:

    def __init__(self, name, field, tokens):
        self.name = name
        self.field = field
        self.tokens = tokens

    def save(self):
        return {
            'name': self.name,
            'tokens': self.tokens,
            'field': [[square.save() if hasattr(square, 'save') else square for square in row] for row in self.field]

        }