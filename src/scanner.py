# import logging  # Just for logging, you can remove it
import string
from enum import Enum
from typing import Dict, Tuple, List, Optional, Set

# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG)  # For more info
# Uncomment logging.* lines to see what's going on

from ctoken import *
from symbol_table import Symbol_Table
from symbol_table import Address


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
        address = Address.get_instance()
        # self.code_gen_st = Symbol_Table() #**
        self.code_gen_st = Symbol_Table.get_instance()
        self.symbol_table = {"lexeme": [], "type": [], "size": [], "data_type": [], "scope": [],
                             "address": []}
        for keyword in keywords:
            self.add_symbol_to_new_st(keyword, "keyword", 0, None, 1)
        self.st = self.get_st()
        # self.symbol_table = {"lexeme": [], "type": [], "size": [], "data_type": [], "scope": [],
        #                      "address": []}
        self.scope_stack = [0]



        # self

    def add_symbol(self, symbol):
        # Symbols is a dictionary, so no need to check if symbol is already in the table
        self.symbols[symbol] = None
        # self.table.append({'id': len(self.symbols), 'lexeme': symbol})
        # self.symbols[symbol] = None
        # self.st = self.get_st()
        # the_row = self.code_gen_st.lookup(symbol, 0, False)
        # if the_row is not None and the_row["scope"] == self.code_gen_st.current_scope:
        #     # this means that the variable is already declared,
        #     # and we want to redefine it
        #     del the_row["type"]

        self.code_gen_st.insert(symbol)
        # self.code_gen_st.modify_last_row(type="id",
        #                                  scope=self.code_gen_st.current_scope,
        #                                  kind=""
        #                                  )
        # if self.semantic_stack[-1] == "void":
        #     self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
        #                                                 error=self.error_void_type,
        #                                                 first_op=token)

        # self.code_gen_st.modify_last_row(kind=kind, type=self.semantic_stack[-1])
        # self.program_block_insert(
        #     operation=":=",
        #     first_op="#0",
        #     second_op=self.symbol_table.get_last_row()[address_key],
        # )
        # self.add_symbol_st(symbol, "id", 0, None, self.scope_stack[-1])

    def get_top_symbols(self):
        return self.symbols.keys[-1]

    def exists(self, symbol):
        if symbol in self.code_gen_st.table:
            return True
        return False

    def add_to_code_gen_st(self, symbol):
        self.code_gen_st.add_symbol(symbol)

    def get_top_symbol_table(self):
        return self.symbol_table["lexemes"][-1]

    # def add_symbol_st(self, lexeme, symbol_type, size, data_type, scope):
    #     """Adds a new row to the symbol table"""
    #     self.symbol_table["lexeme"].append(lexeme)
    #     self.symbol_table["type"].append(symbol_type)
    #     self.symbol_table["size"].append(size)
    #     self.symbol_table["data_type"].append(data_type)
    #     self.symbol_table["scope"].append(scope)

    def save_symbols(self):
        """Writes symbol table in symbol_table.txt."""
        with open("symbol_table.txt", mode="w") as symbol_table_file:
            for key, value in self.symbol_table.items():
                symbol_table_file.write(f"{value}.\t{key}\n")

    def add_symbol_to_new_st(self,
                             lexeme: str,
                             symbol_type: str = None,
                             size: int = 0,
                             data_type: str = None,
                             scope: int = None,
                             address: int = None):
        """Adds a new row to the symbol table"""
        self.symbol_table["lexeme"].append(lexeme)
        self.symbol_table["type"].append(symbol_type)
        self.symbol_table["size"].append(size)
        self.symbol_table["data_type"].append(data_type)
        self.symbol_table["scope"].append(scope)
        self.symbol_table["address"].append(address)

    # def _install_id(self, current_token: object) -> object:
    #     """Adds current id to symbol table if it is not."""
    #     token: str = current_token
    #     if token not in self.symbol_table["lexeme"]:
    #         self.add_symbol(token, None, 0, None, None)
    #     return token

    def update_symbol(self,
                      index: int,
                      symbol_type: str = None,
                      size: int = None,
                      data_type: str = None,
                      scope: int = None,
                      address: int = None):
        if symbol_type is not None:
            self.symbol_table["type"][index] = symbol_type
        if size is not None:
            self.symbol_table["size"][index] = size
        if data_type is not None:
            self.symbol_table["data_type"][index] = data_type
        if scope is not None:
            self.symbol_table["scope"][index] = scope
        if address is not None:
            self.symbol_table["address"][index] = address

    # Used to create symbol_table.txt file, use str(symbol_table) to get the string
    # Or use print(symbol_table) to print the table
    def __str__(self):
        s = ''
        for i, symbol in enumerate(self.symbols):
            s += f'{line_number_str(i + 1)}{symbol}\n'
        return s

    def get_st(self):
        # it must return index of symbols plus the keywords and values in the symbols
        toReturn = {}
        for i, symbol in enumerate(self.symbol_table):
            # toReturn.append(line_number_str(i + 1), symbol)
            toReturn[i + 1] = symbol
        return toReturn

    def get_row_by_id(self, id):
        # return self.table[id]
        return self.get_st()[id+1]

    def is_useless_row(self, id):
        if "type" not in self.get_row_by_id(id):
            return True

    def lookup(self, name, in_declare=False, end_ind=-1) -> dict:
        # print("inside lookup")
        # search in symbol table
        # search for it between the start_ind and end_ind of symbol table
        # if end_ind == -1 then it means to search till the end of symbol table

        row_answer = None
        nearest_scope = -1
        end = end_ind

        if end_ind == -1:
            end = len(self.symbols.keys)
            toCheck = ["void", "int"]
            if in_declare and self.symbol_table["data_type"][-1] not in toCheck:
            # if in_declare and self.is_useless_row(-1):
                end -= 1

        while len(self.scope_stack) >= -nearest_scope:
            # print("inside whileeeee")
            start = self.scope_stack[nearest_scope]

            for i in range(start, end):
                # row_i = self.table[i]
                # row_i = self.symbols.key[i]
                # "lexeme": [], "type": [], "size": [], "data_type": [], "scope": [],
                #                              "address"
                row_i = [self.symbol_table["lexeme"][i]
                         , self.symbol_table["type"]
                         , self.symbol_table["size"]
                         , self.symbol_table["data_type"]
                         , self.symbol_table["scope"]] #lexeme,sym_type,size,data_type,scope
                if self.symbol_table["data_type"][i] not in ["void", "int"]:
                    if nearest_scope != -1 and row_i[1] == "ID":
                        pass
                    elif row_i[0] == name:
                        toReturn = {"lexeme":row_i[0] , "type":row_i[1] , "size":row_i[2] , "data_type":row_i[3] , "scope":row_i[4]}
                        # return row_i
                        return toReturn

            nearest_scope -= 1
            end = start

        return row_answer

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
        self._is_terminal: bool = False
        self._is_lookahead: bool = False

    def add_transition(self, characters, destination):
        self.transitions.update(dict.fromkeys(characters, destination))
        return self

    def otherwise(self, destination):
        self.add_transition([chr(i) for i in range(256) if chr(i) not in self.transitions], destination)
        if None not in self.transitions:
            self.transitions[None] = destination

    def get_is_final(self):
        return self.is_final

    def get_is_star(self):
        return self.is_star

    # @property
    # def is_terminal(self) -> bool:
    #     """Determines if the state is terminal or not."""
    #     return self._is_terminal

    @property
    def is_lookahead(self) -> bool:
        """Determines if the state is lookahead or not."""
        return self._is_lookahead

    def next_state(self, next_char):
        return self.transitions.get(next_char)  # returns None if char is not in transitions


class ErrorType(Enum):
    NO_TRANSITION = 1
    INCOMPLETE_TOKEN = 2

class Error:
    """
    A class used to represent an error in scanner.
    """

    def __init__(self, title: str, content: str, line_number: int):
        """Inits Error.

        :arg title: str: the title of the error
        :arg content: str: the content of the error
        :arg line_number: int: the line number of the error
        """
        self._title: str = title
        self._content: str = content
        self._line_number: int = line_number

    @property
    def title(self) -> str:
        """Return the title of the error"""
        return self._title

    @property
    def content(self) -> str:
        """Return the content of the error"""
        return self._content

    @property
    def line_number(self) -> int:
        """Return the line number of the error"""
        return self._line_number



class Scanner:
    # token types
    NUM: str = "NUM"
    ID: str = "ID"
    KEYWORD: str = "KEYWORD"
    SYMBOL: str = "SYMBOL"
    COMMENT: str = "COMMENT"
    WHITESPACE: str = "WHITESPACE"
    EOF: str = "EOF"

    EOF_symbol: str = "$"

    _digits: Set[str] = set(string.digits)
    _letters: Set[str] = set(string.ascii_letters)
    _alphanumerics: Set[str] = _digits.union(_letters)
    def __init__(self, reader: Reader, start_state: State):
        self._alphanumerics = None
        self.symbol_table = SymbolTable()
        self.reader = reader
        self.start_state: State = start_state
        self.current_state: State = start_state
        self._token_buffer: List[str] = []
        self.tokens = {}  # line_number: list of tokens
        self.lexical_errors = {}  # line_number: list of errors
        self.scope_stack = [0]
        self.symbol_tablee: Dict[str, list] = {"lexeme": [], "type": [], "size": [], "data_type": [], "scope": [],
                                              "address": []}
        for keyword in ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']:
            # self.add_symbol(keyword, "keyword", 0, None, 1, None)
            self.symbol_tablee["lexeme"].append(keyword)
            self.symbol_tablee["type"].append("keyword")
            self.symbol_tablee["size"].append(0)
            self.symbol_tablee["data_type"].append(None)
            self.symbol_tablee["scope"].append(1)
            self.symbol_tablee["address"].append(None)
        self._is_file_ended: bool = False
        self._forward: int = 0
        self._current_char: Optional[str] = None
        # self._buffer_size = buffer_size
        self._buffer_size = 1024
        self._line_number: int = 1
        self._errors_dict: Dict[int, List[Error]] = {}

    @property
    def _current_token(self) -> Optional[str]:
        if self._token_buffer is not None:
            return ''.join(self._token_buffer)
        else:
            return None


    def update_symbol(self,
                      index: int,
                      symbol_type: str = None,
                      size: int = None,
                      data_type: str = None,
                      scope: int = None,
                      address: int = None):
        if symbol_type is not None:
            self.symbol_tablee["type"][index] = symbol_type
        if size is not None:
            self.symbol_tablee["size"][index] = size
        if data_type is not None:
            self.symbol_tablee["data_type"][index] = data_type
        if scope is not None:
            self.symbol_tablee["scope"][index] = scope
        if address is not None:
            self.symbol_tablee["address"][index] = address

    def get_symbol_index(self, lexeme: str) -> int:
        """Return index of the lexeme in the symbol table"""
        # return self.symbol_table["lexeme"].index(lexeme)
        current_scope_end = len(self.symbol_tablee["lexeme"])
        for current_scope_start in self.scope_stack[::-1]:
            if lexeme not in self.symbol_tablee["lexeme"][current_scope_start:current_scope_end]:
                current_scope_end = current_scope_start
                continue
            else:
                return self.symbol_tablee["lexeme"].index(lexeme, current_scope_start, current_scope_end)
        return -1

    def pop_scope(self, scope_start: int):
        for column in self.symbol_tablee.values():
            column.pop(len(column) - scope_start)

    def save_symbols(self):
        """Writes symbol table in symbol_table.txt."""
        with open("symbol_table.txt", mode="w") as symbol_table_file:
            for key, value in self.symbol_tablee.items():
                symbol_table_file.write(f"{value}.\t{key}\n")

    def _decrement_forward(self):
        """Move forward back."""
        if self._forward == 0:
            self._forward = 2 * self._buffer_size - 1
        else:
            self._forward -= 1

    @property
    def line_number(self) -> int:
        """Return current line number."""
        return self._line_number

    # def get_next_token(self) -> Tuple[str, str]:
    #     """Return next token of input_file."""
    #     if self._is_file_ended:
    #         return "EOF", "$"
    #
    #     self._token_buffer.clear()
    #     # self._current_state = self._states[0]
    #     self._current_state = self.start_state
    #     while True:
    #         # Check terminal
    #         if self._current_state.get_is_final():
    #             # Terminal state
    #             if self._current_state.get_is_star():
    #                 self._token_buffer.pop()
    #                 self._decrement_forward()
    #                 # update line number
    #                 if self._current_char == '\n':
    #                     self._line_number -= 1
    #             token = self._get_token_tuple()
    #             if token[0] in {self.WHITESPACE, self.COMMENT}:
    #                 self._token_buffer.clear()
    #                 # self._current_state = self._states[0]
    #                 self._current_state = self.start_state
    #             else:
    #                 return token

    def _get_token_tuple(self) -> Tuple[str, str]:
        """Return tuple with form (token_type, token_lexeme)"""
        if self._current_state.state_type == NUM:
            return self.NUM, self._current_token
        elif self._current_state.state_type == ID:
            token_type = self._get_token_type()
            return token_type, self._install_id()
        elif self._current_state.state_type == SYMBOL:
            return self.SYMBOL, self._current_token
        elif self._current_state.state_type == COMMENT :
            return self.COMMENT, self._current_token
        elif self._current_state.state_type == WHITESPACE:
            return self.WHITESPACE, self._current_token

    def _get_token_type(self) -> str:
        """Return \"KEYWORD\" if current token is a keyword else \"ID\"."""
        if self._current_token in ['break', 'else', 'if', 'int', 'repeat', 'return', 'until', 'void']:
            return self.KEYWORD
        return self.ID


    def _install_id(self):
        """Adds current id to symbol table if it is not."""
        token: str = self._current_token
        if token not in self.symbol_tablee["lexeme"]:
            self.add_symbol(token, None, 0, None, None)
        return token

    def _handle_error(self, error_type: ErrorType):
        """Adds occurred error to error dict."""
        error = None
        if error_type == ErrorType.NO_TRANSITION:
            if self._current_state.id == 1 and self._current_char in self._alphanumerics:
                error = Error("Invalid number", self._current_token, self._line_number)
            elif self._current_state.id == 17 and self._current_char == '/':
                error = Error("Unmatched comment", self._current_token, self._line_number)
            else:
                error = Error("Invalid input", self._current_token, self._line_number)
        elif error_type == ErrorType.INCOMPLETE_TOKEN:
            if self._current_state.id in {13, 14}:
                line_number: int = self._line_number - self._token_buffer.count('\n')
                error = Error("Unclosed comment", f"{''.join(self._token_buffer[:7])}...", line_number)

        if error is None:
            error = Error("Undefined Error!", self._current_token, self._line_number)

        if error.line_number in self._errors_dict:
            self._errors_dict[error.line_number].append(error)
        else:
            self._errors_dict[error.line_number] = [error]

    def add_symbol(self,
                   lexeme: str,
                   symbol_type: str = None,
                   size: int = 0,
                   data_type: str = None,
                   scope: int = None,
                   address: int = None):
        """Adds a new row to the symbol table"""
        self.symbol_tablee["lexeme"].append(lexeme)
        self.symbol_tablee["type"].append(symbol_type)
        self.symbol_tablee["size"].append(size)
        self.symbol_tablee["data_type"].append(data_type)
        self.symbol_tablee["scope"].append(scope)
        self.symbol_tablee["address"].append(address)

    def get_next_token(self):
        self.current_state = self.start_state
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
            # self.symbol_table.code_gen_st.modify_last_row()
            if token_name in keywords:
                self.symbol_table.add_symbol_to_new_st(token_name, self.current_state.state_type
                                                       , 1, token_name, self.symbol_table.scope_stack[-1])
                return Token(KEYWORD, token_name)
        elif self.current_state.state_type == PANIC:
            token_name = token_name[:7] + '...' if len(token_name) > 7 else token_name
        return Token(self.current_state.state_type, token_name)

    def get_tokens(self):
        token = Token(token_type=START)
        while token.type != EOF:
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

    # we want to implement a function that returns the index of the lexeme in the symbol table
    # if the lexeme is not in the symbol table, return -1
    # let's call it get_symbol_index
    def get_symbol_index(self, lexeme):
        st = self.symbol_table.get_st()  # {i:{lex:None}, ...}
        # we must search the keys of st which will be in the form of {lex : None}
        # then if lex== lexeme, return i
        for i in st.keys():
            if st[i][0] == lexeme:
                return i - 1
        return -1

    def pop_scope(self, scope_start: int):
        for column in self.symbol_table.symbol_table.values():
            column.pop(len(column) - scope_start)

    def get_symbol_index_st(self, lexeme: str) -> int:
        # symbol_table = self.symbol_table.symbol_table
        """Return index of the lexeme in the symbol table"""
        # return self.symbol_table["lexeme"].index(lexeme)
        current_scope_end = len(self.symbol_table.symbol_table["lexeme"])
        for current_scope_start in self.symbol_table.scope_stack[::-1]:
            if lexeme not in self.symbol_table.symbol_table["lexeme"][current_scope_start:current_scope_end]:
                current_scope_end = current_scope_start
                continue
            else:
                return self.symbol_table.symbol_table["lexeme"].index(lexeme, current_scope_start, current_scope_end)
        return -1


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
