# C- compiler (Phase 1 - Scanner)
# Compiler Design | Sharif University of Technology
# Soheil   Nazari  Mendejin    99102412
# Alireza  Habibzadeh          99109393


keywords = ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']
symbols = ['+', '-', '*', '/', '<', '==', '=', ':', ';', ',', '(', ')', '[', ']', '{', '}']
whitespaces = [' ', '\n', '\r', '\t', '\v', '\f']
digits = [chr(i) for i in range(48, 58)]
letters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
valid_chars = keywords + symbols + whitespaces + letters + digits
invalid_chars = [chr(i) for i in range(256) if chr(i) not in valid_chars]
all_chars_except_whitespace = [chr(i) for i in range(256) if chr(i) not in whitespaces]


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
    def __init__(self, file):
        self.line_number = 0
        self.file = file
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

    def close(self):
        self.file.close()

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
    def __init__(self, reader):
        self.symbol_table = SymbolTable()
        self.reader = reader
        self.start_state = State.states[0]
        self.tokens = []  # line_number, list of tokens
        self.lexical_errors = []  # line_number, list of errors

    def get_next_token(self) -> Token:
        current_state: State = self.start_state
        token_name = ''

        while True:
            c = self.reader.get_char()
            current_state = current_state.next_state(next_char=c)
            if current_state.is_star:
                self.reader.char_index -= 1

            if current_state.is_final:
                if token_name in keywords:
                    return Token(KEYWORD, token_name)
                return Token(current_state.state_type, token_name)

            token_name += c

    def __str__(self):
        s = ''
        for line_number, line_tokens in self.tokens:
            s += f'{str(line_number) + ".":<5}'
            for token in line_tokens:
                s += ' ' + str(token)
            s += '\n'
        return s

    def repr_lexical_errors(self):
        s = ''
        for line_number, line_lexical_errors in self.lexical_errors:
            s += f'{str(line_number) + ".":<5}'
            for error in line_lexical_errors:
                s += ' ' + str(error)
            s += '\n'
        return s


class State:
    states = dict()

    def __init__(self, state_id, state_type, is_final, is_star, error=''):
        self.id = state_id
        self.transitions = {}
        self.error = error
        self.state_type = state_type
        self.is_final = is_final
        self.is_star = is_star
        self.states[state_id] = self

    def add_transition(self, characters, destination):
        self.transitions.update(dict.fromkeys(characters, destination))
        return self

    def next_state(self, next_char):
        return self.transitions.get(next_char)  # returns None if char is not in transitions


# State and token types
NUM = 'NUM'
ID = 'ID'
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
COMMENT = 'COMMENT'
WHITESPACE = 'WHITESPACE'
START = 'START'
PANIC = 'PANIC'
EOF = 'EOF'

State(0, START, is_final=True, is_star=False)

State(10, NUM, is_final=False, is_star=False)
State(11, NUM, is_final=True, is_star=True)

State(20, ID, is_final=False, is_star=False)
State(21, ID, is_final=True, is_star=True)

State(30, WHITESPACE, is_final=False, is_star=False)
State(31, WHITESPACE, is_final=True, is_star=True)

State(90, PANIC, is_final=False, is_star=False)
State(91, PANIC, is_final=True, is_star=True, error='Invalid number')

State(100, EOF, is_final=True, is_star=False)

State.states[0] \
    .add_transition(digits, State.states[10]) \
    .add_transition(letters, State.states[20]) \
    .add_transition(whitespaces, State.states[30])
State.states[10] \
    .add_transition(digits, State.states[10]) \
    .add_transition(letters, State.states[90]) \
    .add_transition(whitespaces, State.states[11])
State.states[20] \
    .add_transition(digits + letters, State.states[20]) \
    .add_transition(whitespaces, State.states[21])
State.states[30] \
    .add_transition(whitespaces, State.states[30]) \
    .add_transition(all_chars_except_whitespace, State.states[31])


def main(file_name):
    with open(file_name, 'r') as input_file:
        scanner = Scanner(reader=Reader(input_file))
        while scanner.get_next_token().token_type != EOF:
            pass

    with open('tokens.txt', 'w') as output_file:
        output_file.write(str(scanner))
    with open('symbol_table.txt', 'w') as output_file:
        output_file.write(str(scanner.symbol_table))
    with open('lexical_errors.txt', 'w') as output_file:
        output_file.write(scanner.repr_lexical_errors())


if __name__ == '__main__':
    main('input.txt')
