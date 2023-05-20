from token import *

import logging  # Just for logging, you can remove it

logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG)  # For more info
# Uncomment logging.* lines to see what's going on

keywords = ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']
single_symbols = ['+', '-', '<', ':', ';', ',', '(', ')', '[', ']', '{', '}']
slash_symbol = ['/']
star_symbol = ['*']
equal_symbol = ['=']
whitespaces = [' ', '\n', '\r', '\t', '\v', '\f']
digits = [chr(i) for i in range(48, 58)]
letters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
legal_chars = single_symbols + slash_symbol + star_symbol + equal_symbol + whitespaces + digits + letters + [None]
illegal_chars = [chr(i) for i in range(256) if chr(i) not in legal_chars]


def line_number_str(line_number):
    # return f'{line_number}.\t' + '\b' * (len(str(line_number)) - 1)
    return f"{str(line_number) + '.':<7} "


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
            s += f'{line_number_str(i + 1)}{symbol}\n'
        return s


class Reader:
    def __init__(self, file):
        self.line_number = 0
        self.file = file
        self.line = self.readline()
        self.char_index = 0

    def get_char(self):
        if self.char_index >= len(self.line):
            self.line = self.readline()
            self.char_index = 0
        if not self.line:
            return None
        c = self.line[self.char_index]
        self.char_index += 1
        return c

    def readline(self):
        line = self.file.readline()
        if line:
            self.line_number += 1
        return line


class State:
    states = {}

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

    def otherwise(self, destination):
        self.add_transition([chr(i) for i in range(256) if chr(i) not in self.transitions], destination)
        if None not in self.transitions:
            self.transitions[None] = destination

    def next_state(self, next_char):
        return self.transitions.get(next_char)  # returns None if char is not in transitions


class Scanner:
    def __init__(self, reader: Reader, start_state: State):
        self.symbol_table = SymbolTable()
        self.reader = reader
        self.start_state: State = start_state
        self.current_state: State = start_state
        self.tokens = {}  # line_number: list of tokens
        self.lexical_errors = {}  # line_number: list of errors

    def get_next_token(self) -> Token:
        token_name = ''
        while not self.current_state.is_final:
            c = self.reader.get_char()
            # logging.debug(f'current_state: {self.current_state.id}, next_char: {c}')
            self.current_state = self.current_state.next_state(next_char=c)
            if self.current_state.is_star:
                self.reader.char_index -= 1
            else:
                token_name += c

        if self.current_state.state_type == ID:
            self.symbol_table.add_symbol(token_name)
            if token_name in keywords:
                return Token(KEYWORD, token_name)
        elif self.current_state.state_type == PANIC:
            token_name = token_name[:7] + '...' if len(token_name) > 7 else token_name
        return Token(self.current_state.state_type, token_name)

    def get_tokens(self):
        token = Token(token_type=START)
        while token.type != EOF:
            self.current_state = self.start_state
            line_number = self.reader.line_number
            token = self.get_next_token()

            if token.type == PANIC:
                self.lexical_errors.setdefault(line_number, []) \
                    .append(Token(token.value, self.current_state.error))
            self.tokens.setdefault(line_number, []).append(token)
            # logging.info(token)

    def __str__(self):
        hidden_tokens = [COMMENT, WHITESPACE, START, PANIC, EOF]

        s = ''
        for line_number in self.tokens:
            line_tokens = ''
            for token in self.tokens[line_number]:
                if token.type not in hidden_tokens:
                    line_tokens += str(token) + ' '
            if line_tokens:
                s += line_number_str(line_number) + line_tokens + '\n'
        return s

    def repr_lexical_errors(self):
        if not self.lexical_errors:
            return 'There is no lexical error.'
        # line_number_str str(token1) str(token2)... (\n)
        return '\n'.join(map(lambda line_number:
                             line_number_str(line_number) + ' '.join(map(str, self.lexical_errors[line_number])),
                             self.lexical_errors))


State(0, START, is_final=False, is_star=False)

State(10, NUM, is_final=False, is_star=False)
State(11, NUM, is_final=True, is_star=True)

State(20, ID, is_final=False, is_star=False)
State(21, ID, is_final=True, is_star=True)

State(30, WHITESPACE, is_final=False, is_star=False)
State(31, WHITESPACE, is_final=True, is_star=True)

State(40, SYMBOL, is_final=True, is_star=False)  # Always-single symbols
State(41, SYMBOL, is_final=False, is_star=False)  # Equal symbol reached
State(42, SYMBOL, is_final=True, is_star=False)  # Double equal finished
State(43, SYMBOL, is_final=True, is_star=True)  # Reached other characters after single/double-symbol

State(50, COMMENT, is_final=False, is_star=False)  # '/' reached
State(51, COMMENT, is_final=False, is_star=False)  # '*' reached after '/' (comment)
State(52, COMMENT, is_final=False, is_star=False)  # '*' reached inside comment
State(53, COMMENT, is_final=True, is_star=False)  # '/' reached after '*' (comment finished)
State(54, COMMENT, is_final=False, is_star=False)  # '*' reached outside comment

State(90, PANIC, is_final=True, is_star=False, error='Invalid number')
State(92, PANIC, is_final=True, is_star=True, error='Unclosed comment')
State(93, PANIC, is_final=True, is_star=False, error='Invalid input')
State(94, PANIC, is_final=True, is_star=True, error='Invalid input')

State(95, PANIC, is_final=True, is_star=False, error='Unmatched comment')

State(100, EOF, is_final=True, is_star=True)

State.states[0] \
    .add_transition(digits, State.states[10]) \
    .add_transition(letters, State.states[20]) \
    .add_transition(whitespaces, State.states[30]) \
    .add_transition([None], State.states[100]) \
    .add_transition(single_symbols, State.states[40]) \
    .add_transition(equal_symbol, State.states[41]) \
    .add_transition(slash_symbol, State.states[50]) \
    .add_transition(star_symbol, State.states[54]) \
    .add_transition(illegal_chars, State.states[93]) \
    .otherwise(State.states[93])

State.states[10] \
    .add_transition(digits, State.states[10]) \
    .add_transition(letters, State.states[90]) \
    .otherwise(State.states[11])

State.states[20] \
    .add_transition(digits + letters, State.states[20]) \
    .add_transition(illegal_chars, State.states[93]) \
    .otherwise(State.states[21])

State.states[30] \
    .add_transition(whitespaces, State.states[30]) \
    .otherwise(State.states[31])

State.states[41] \
    .add_transition(equal_symbol, State.states[42]) \
    .add_transition(illegal_chars, State.states[93]) \
    .otherwise(State.states[43])

State.states[50] \
    .add_transition(legal_chars, State.states[94]) \
    .add_transition(star_symbol, State.states[51]) \
    .otherwise(State.states[93])

State.states[51] \
    .add_transition(star_symbol, State.states[51]) \
    .add_transition([None], State.states[92]) \
    .add_transition(star_symbol, State.states[52]) \
    .otherwise(State.states[51])

State.states[52] \
    .add_transition(slash_symbol, State.states[53]) \
    .add_transition([None], State.states[92]) \
    .otherwise(State.states[51])

State.states[54] \
    .add_transition(slash_symbol, State.states[95]) \
    .add_transition(illegal_chars, State.states[93]) \
    .otherwise(State.states[43])
