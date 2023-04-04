# C- compiler (Phase 1 - Scanner)
# Compiler Design | Sharif University of Technology
# Soheil   Nazari  Mendejin    99102412
# Alireza  Habibzadeh          99109393


keywords = ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']
symbols = ['+', '-', '*', '/', '<', '==', '=', ':', ';', ',', '(', ')', '[', ']', '{', '}']
whitespaces = [' ', '\n', '\r', '\t', '\v', '\f']
alphabets = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
digits = [chr(i) for i in range(48, 58)]
# Token types
NUM = 'NUM'
ID = 'ID'
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
COMMENT = 'COMMENT'
WHITESPACE = 'WHITESPACE'
START = 'START'
ERROR = 'ERROR'
EOF = 'EOF'
valid_chars = keywords + symbols + whitespaces + alphabets + digits
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
        return f'({self.token_type}, {self.token_value})'


class Scanner:
    def __init__(self, file_name):
        self.symbol_table = SymbolTable()
        self.tokens = []
        self.char = ''
        self.reader = Reader(file_name)
        self.start_state = states[0]
        self.errors = []

    def get_token(self):
        return self.tokens.pop(0)

    def get_symbol_table(self):
        return self.symbol_table

    def get_next_token(self):
        self.text = ''
        while True:
            c = self.reader.get_char()
            if c is None:
                break
            self.text += c
            for pattern in patterns:
                if re.match(pattern[0], self.text):
                    if pattern[1] == 'ID' or pattern[1] == 'keyword':
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

    def goto_next_state(self):
        if self.char is None:
            return None
        if self.char in self.current_state.transitions:
            self.current_state = self.current_state.transitions[self.char]
            return self.current_state
        else:
            return None


class State:
    states = dict()

    def __init__(self, id, state_type, is_final, is_star, error=""):
        self.id = id
        self.transitions = {}
        self.error = error
        states[id] = self
        self.state_type = state_type
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

    def next(self, char):
        return self.transitions.get(char)  # returns None if char is not in transitions
