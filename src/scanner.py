keywords = ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']


class SymbolTable:
    def __init__(self):
        # Here dictionary acts as an ordered set
        self.symbols = dict.fromkeys(keywords)

    def add_symbol(self, symbol):
        # Symbols is a dictionary, so no need to check if symbol is already in the table
        self.symbols[symbol] = None

    # Used to create symbol_table.txt file, use str(symbol_table) to get the string
    # Or use print(symbol_table) to print the table
    def __str__(self):
        s = ''
        for i, symbol in enumerate(self.symbols):
            s += f'{str(i + 1) + ".":<5} {symbol}\n'
        return s


class Reader:
    def __init__(self, file_name):
        self.line_number = 0
        self.file_name = file_name
        self.file = open(file_name, 'r')
        self.line = self.readline()
        self.char_index = 0

    def get_char(self):
        if self.char_index == len(self.line):
            self.line = self.readline()
            self.char_index = 0
            if not self.line:
                return None
        c = self.line[self.char_index]
        self.char_index += 1
        return c

    def get_line_number(self):
        return self.line_number

    def close(self):
        self.file.close()

    def open(self):
        self.file = open(self.file_name, 'r')

    def readline(self):
        line = self.file.readline()
        if line:
            self.line_number += 1
        return line


class Token:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.token_value = token_value

    def __str__(self):
        return f'{self.token_type} {self.token_value}'

    def get_type(self):
        return self.token_type

    def get_value(self):
        return self.token_value

    def set_type(self, token_type):
        self.token_type = token_type

    def set_value(self, token_value):
        self.token_value = token_value


class Scanner:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.tokens = []
        self.text = ''
        self.reader = None

    def set_reader(self, reader):
        self.reader = reader

    def get_token(self):
        return self.tokens.pop(0)

    def get_symbol_table(self):
        return self.symbol_table




