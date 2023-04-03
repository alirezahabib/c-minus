keywords = ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']


class SymbolTable:
    def __init__(self):
        self.symbols = dict.fromkeys(keywords)

    def add_symbol(self, symbol):
        self.symbols[symbol] = None

    def __str__(self):
        s = ''
        for i, symbol in enumerate(self.symbols):
            s += f'{str(i + 1) + ".":<5} {symbol}\n'
        return s


