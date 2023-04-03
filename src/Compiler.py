keywords = ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']
symbols = ['+', '-', '*', '/', '<', '==', '=', ':', ';', ',', '(', ')', '[', ']', '{', '}']
whitespace = [' ', '\n', '\r', '\t', '\v', '\f']
valid_chars = keywords + symbols + whitespace + [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [
    chr(i) for i in range(48, 58)]
invalid_chars = [chr(i) for i in range(256) if chr(i) not in valid_chars]
# Regular expression patterns for tokens
patterns = [
    (r'[a-zA-Z][a-zA-Z0-9]*', 'ID'),
    (r'\d+', 'NUM'),
    (r'break', 'keyword'),
    (r'else', 'keyword'),
    (r'if', 'keyword'),
    (r'int', 'keyword'),
    (r'repeat', 'keyword'),
    (r'return', 'keyword'),
    (r'until', 'keyword'),
    (r'void', 'keyword'),
    (r'=', 'symbol'),
    (r'==', 'symbol'),
    (r'<', 'symbol'),
    (r'\+', 'symbol'),
    (r'-', 'symbol'),
    (r'\*', 'symbol'),
    (r'/', 'symbol'),
    (r':', 'symbol'),
    (r';', 'symbol'),
    (r',', 'symbol'),
    (r'\(', 'symbol'),
    (r'\)', 'symbol'),
    (r'\[', 'symbol'),
    (r'\]', 'symbol'),
    (r'\{', 'symbol'),
    (r'\}', 'symbol'),
    (r'//.*', 'Comment'),
    (r'/\*.*\*/', 'Comment'),
    (r'\s+', 'White Space'),
    (r'.', 'Error')
]


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

    def scan(self):
        self.tokens = []
        self.text = ''
        while True:
            c = self.reader.get_char()
            if c is None:
                break
            self.text += c
            for pattern in patterns:
                if re.match(pattern[0], self.text):
                    if pattern[1] == 'ID':
                        self.symbol_table.add_symbol(self.text)
                    if pattern[1] == 'NUM':
                        if int(self.text) > 999999999:
                            self.tokens.append(Token('Error', 'Number too large'))
                            self.text = ''
                            break
                    if pattern[1] == 'Error':
                        self.tokens.append(Token('Error', 'Invalid character'))
                        self.text = ''
                        break
                    if pattern[1] != 'White Space' and pattern[1] != 'Comment':
                        self.tokens.append(Token(pattern[1], self.text))
                        self.text = ''
                        break
                    else:
                        self.text = ''
                        break



class State:
    def __init__(self, id, type, is_final, is_star, error=""):
        self.id = id
        self.transitions = {}
        self.error = error
        states[ID] = self
        self.type = type
        self.is_star = is_star
        self.is_final = is_final

    def add_transition(self, destination, characters):
        for character in characters:
            self.transitions[character] = destination

    def get_state_by_id(self, id):
        for state in self.transitions.values():
            if state.id == id:
                return state
        return None

    def get_error(self):
        return self.error
