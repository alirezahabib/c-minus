# import logging  # Just for logging, you can remove it

# logging.getLogger().setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.DEBUG)  # For more info
# Uncomment logging.* lines to see what's going on

from ctoken import *
from intercode_gen import Address

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
    # symbol table

    def __init__(self):
        # Here dictionary acts as an ordered set
        self.symbols = dict.fromkeys(keywords)
        self.st = self.get_st()
        # self.symbol_table = {"lexeme": [], "type": [], "size": [], "data_type": [], "scope": [],
        #                      "address": []}
        self.scope_stack = [0]
        self.symbol_table = {"lexeme": [], "type": [], "size": [], "data_type": [], "scope": [],
                             "address": []}
        for keyword in keywords:
            self.add_symbol_to_new_st(keyword, "keyword", 0, None, 1)

    def add_symbol(self, symbol):
        # Symbols is a dictionary, so no need to check if symbol is already in the table
        self.symbols[symbol] = None
        self.st = self.get_st()
        # self.add_symbol_st(symbol, "id", 0, None, self.scope_stack[-1])
    def get_top_symbols(self):
        return self.symbols.keys[-1]
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
        # self.address = Address()

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
            # dfjsl;
            # self.symbol_table.add_symbol_to_new_st(token_name, self.current_state.state_type,)
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









# import json
# from enum import Enum
# from typing import Set, Dict, Tuple, List, Union
#
# from anytree import Node, RenderTree
#
# from scanner import Scanner
#
#
# class ErrorType(Enum):
#     ILLEGAL_TOKEN = 1
#     TOKEN_DISCARDED = 2
#     STACK_CORRECTION = 3
#     MISSING_NON_TERMINAL = 4
#     UNEXPECTED_EOF = 5
#
#
# class Error:
#     """
#     A class used to represent an error in parser.
#     """
#
#     def __init__(self, error_type: ErrorType, subject: Union[str, Node], line_number: int):
#         """Inits Error.
#
#         :arg error_type: ErrorType: the type of the error
#         :arg subject: Union[str, Tuple[str, str]]: the subject of the error
#         :arg line_number: int: the line number of the error
#         """
#         if isinstance(subject, Node):
#             subject = subject.name
#
#         self._type: ErrorType = error_type
#         self._content: str = subject
#         self._line_number: int = line_number
#         self._content: str = ""
#         if self._type == ErrorType.ILLEGAL_TOKEN:
#             self._content = f"#{line_number} : syntax error , illegal {subject}"
#         elif self._type == ErrorType.TOKEN_DISCARDED:
#             self._content = f"#{line_number} : syntax error , discarded {subject} from input"
#         elif self._type == ErrorType.STACK_CORRECTION:
#             self._content = f"syntax error , discarded {subject} from stack"
#         elif self._type == ErrorType.MISSING_NON_TERMINAL:
#             self._content = f"#{line_number} : syntax error , missing {subject}"
#         elif self._type == ErrorType.UNEXPECTED_EOF:
#             self._content = f"#{line_number} : syntax error , Unexpected EOF"
#         else:
#             self._content = f"Unknown error type: {error_type}"
#
#     @property
#     def type(self) -> ErrorType:
#         """Return the title of the error"""
#         return self._type
#
#     @property
#     def line_number(self) -> int:
#         """Return the line number of the error"""
#         return self._line_number
#
#     @property
#     def content(self) -> str:
#         """Return the content of the error"""
#         return self._content
#
#
# class Parser:
#     """
#     A C-Minus compiler's parser.
#     """
#     # Actions
#     _accept: str = "accept"
#     _shift: str = "shift"
#     _reduce: str = "reduce"
#     _goto: str = "goto"
#
#     def __init__(self, scanner: Scanner):
#         """Inits Parser
#
#         :arg scanner: Scanner: the compiler's scanner"""
#         self._scanner: Scanner = scanner
#
#         self._parse_stack: List[Union[str, Node]] = ["0"]
#         self._syntax_errors: List[Error] = []
#
#         self._semantic_errors = []
#         self._semantic_stack = []
#         self._program_block = []
#         self._current_data_address = 500
#         self._break_stack = []
#
#         self._failure: bool = False
#
#         self._update_current_token()
#         self._read_table()
#
#     @staticmethod
#     def _get_rhs_count(production: List[str]) -> int:
#         """Return count of rhs of the production."""
#         if production[-1] == "epsilon":
#             return 0
#         else:
#             return len(production) - 2
#
#     def _read_table(self):
#         """Initializes terminals, non_terminals, first_sets, follow_sets, grammar and parse_table."""
#         with open("table.json", mode="r") as table_file:
#             table: dict = json.load(table_file)
#
#         # set of grammars terminals
#         self._terminals: Set[str] = set(table["terminals"])
#         # set of grammars non-terminals
#         self._non_terminals: Set[str] = set(table["non_terminals"])
#         # first and follow sets of non-terminals
#         self._first_sets: Dict[str, Set[str]] = dict(zip(table["first"].keys(), map(set, table["first"].values())))
#         self._follow_sets: Dict[str, Set[str]] = dict(zip(table["follow"].keys(), map(set, table["follow"].values())))
#         # grammar's productions
#         self._grammar: Dict[str, List[str]] = table["grammar"]
#         # SLR parse table
#         self._parse_table: Dict[str, Dict[str, Tuple[str, str]]] = dict(
#             zip(table["parse_table"].keys(), map(lambda row: dict(
#                 zip(row.keys(), map(lambda entry: tuple(entry.split("_")), row.values()))
#             ), table["parse_table"].values()))
#         )
#
#     def _update_current_token(self):
#         """Stores next token in _current_token and updates _current_input."""
#         self._current_token: Tuple[str, str] = self.scanner.get_next_token()
#         self._current_input: str = ""
#         if self._current_token[0] in {Scanner.KEYWORD, Scanner.SYMBOL, Scanner.EOF}:
#             self._current_input = self._current_token[1]
#         else:
#             self._current_input = self._current_token[0]
#
#     def _get_goto_non_terminals(self, state: str) -> List[str]:
#         """Return the non-terminals which the state has a goto with them."""
#         non_terminals_of_state = []
#         state_goto_and_actions = self._parse_table[state]
#         for non_terminal in self._non_terminals:
#             if state_goto_and_actions.get(non_terminal) is not None:
#                 non_terminals_of_state.append(non_terminal)
#         non_terminals_of_state.sort()
#         return non_terminals_of_state
#
#     def run(self):
#         """Parses the input. Return True if UNEXPECTED_EOF"""
#         self._semantic_stack.append(len(self._program_block))
#         self._program_block.append(None)
#         while True:
#             # get action from parse_table
#             last_state = self._parse_stack[-1]
#             try:
#                 action = self._parse_table[last_state].get(self._current_input)
#             except KeyError:
#                 # invalid state
#                 raise Exception(f"State \"{last_state}\" does not exist.")
#             if action is not None:
#                 # perform the action
#                 if action[0] == self._accept:
#                     # accept
#                     break
#                 elif action[0] == self._shift:
#                     # push current_token and shift_state into the stack
#                     shift_state = action[1]
#                     self._parse_stack.append(Node(f"({self._current_token[0]}, {self._current_token[1]})"))
#                     self._parse_stack.append(shift_state)
#
#                     # get next token
#                     self._update_current_token()
#                 elif action[0] == self._reduce:
#                     # pop rhs of the production from the stack and update parse tree
#                     production_number = action[1]
#                     self.generate_code(int(production_number))
#                     production = self._grammar[production_number]
#                     production_lhs = production[0]
#                     production_rhs_count = self._get_rhs_count(production)
#                     production_lhs_node: Node = Node(production_lhs)
#                     if production_rhs_count == 0:
#                         node = Node("epsilon")
#                         node.parent = production_lhs_node
#                     else:
#                         popped_nodes = []
#                         for _ in range(production_rhs_count):
#                             self._parse_stack.pop()
#                             popped_nodes.append(self._parse_stack.pop())
#                         for node in popped_nodes[::-1]:
#                             node.parent = production_lhs_node
#
#                     # push lhs of the production and goto_state into the stack
#                     last_state = self._parse_stack[-1]
#                     try:
#                         goto_state = self._parse_table[last_state][production_lhs][1]
#                     except KeyError:
#                         # problem in parse_table
#                         raise Exception(f"Goto[{last_state}, {production_lhs}] is empty.")
#                     self._parse_stack.append(production_lhs_node)
#                     self._parse_stack.append(goto_state)
#                 else:
#                     # problem in parse_table
#                     raise Exception(f"Unknown action: {action}.")
#             else:
#                 if self.handle_error():
#                     # failure if UNEXPECTED_EOF
#                     self._failure = True
#                     break
#
#     def handle_error(self) -> bool:
#         """Handles syntax errors. Return True if error is UNEXPECTED_EOF"""
#         # discard the first input
#         self._syntax_errors.append(Error(ErrorType.ILLEGAL_TOKEN, self._current_token[1], self._scanner.line_number))
#         self._update_current_token()
#
#         # pop from stack until state has non-empty goto cell
#         while True:
#             state = self._parse_stack[-1]
#             goto_and_actions_of_current_state = self._parse_table[state].values()
#             # break if the current state has a goto cell
#             if any(map(lambda table_cell: table_cell[0] == self._goto,
#                        goto_and_actions_of_current_state)):
#                 break
#             discarded_state, discarded_node = self._parse_stack.pop(), self._parse_stack.pop()
#             self._syntax_errors.append(Error(ErrorType.STACK_CORRECTION, discarded_node, self._scanner.line_number))
#
#         goto_keys = self._get_goto_non_terminals(state)
#         # discard input, while input not in any follow(non_terminal)
#         selected_non_terminal = None
#         while True:
#             for non_terminal in goto_keys:
#                 if self._current_input in self._follow_sets[non_terminal]:
#                     selected_non_terminal = non_terminal
#                     break
#             if selected_non_terminal is None:
#                 if self._current_input == Scanner.EOF_symbol:
#                     # input is EOF, halt parser
#                     self._syntax_errors.append(Error(ErrorType.UNEXPECTED_EOF, "", self._scanner.line_number))
#                     return True
#                 else:
#                     # discard input
#                     self._syntax_errors.append(
#                         Error(ErrorType.TOKEN_DISCARDED, self._current_token[1], self._scanner.line_number))
#                     self._update_current_token()
#             else:
#                 # input is in follow(non_terminal)
#                 break
#         self._parse_stack.append(Node(selected_non_terminal))
#         self._parse_stack.append(self._parse_table[state][selected_non_terminal][1])
#         self._syntax_errors.append(
#             Error(ErrorType.MISSING_NON_TERMINAL, selected_non_terminal, self._scanner.line_number))
#         return False
#
#     def generate_code(self, rule_number):
#         """Generates intermediate code based on the rule_number."""
#         if rule_number == 67:           # p_id_index
#             # push index of identifier into the semantic stack
#             lexeme = self._current_token[1]
#             index = self._scanner.get_symbol_index(lexeme)
#             self._semantic_stack.append(index)
#         elif rule_number == 70:         # p_id
#             # push address of identifier into the semantic stack
#             lexeme = self._current_token[1]
#             index = self._scanner.get_symbol_index(lexeme)
#             address = self._scanner.symbol_table["address"][index]
#             self._semantic_stack.append(address)
#         elif rule_number == 69:         # p_type
#             # push type into the semantic stack
#             data_type = self._current_token[1]
#             self._semantic_stack.append(data_type)
#         elif rule_number == 68:         # p_num
#             # push number into the semantic stack
#             number = int(self._current_token[1])
#             self._semantic_stack.append(number)
#         elif rule_number == 72:         # p_num_temp
#             # push #number into the semantic stack
#             number = int(self._current_token[1])
#             self._semantic_stack.append(f"#{number}")
#         elif rule_number in {6, 15, 16}:    # declare_var
#             # assign an address to the identifier, assign 0 to the variable in the program block
#             # and update identifier's row in the symbol table
#             data_type = self._semantic_stack[-2]
#             index = self._semantic_stack[-1]
#             self.pop_semantic_stack(2)
#
#             self._program_block.append(f"(ASSIGN, #0, {self._current_data_address},\t)")
#             self._scanner.update_symbol(index,
#                                         symbol_type="var",
#                                         size=0,
#                                         data_type=data_type,
#                                         scope=len(self._scanner.scope_stack),
#                                         address=self._current_data_address)
#             self._current_data_address += 4
#         elif rule_number == 7:              # declare_array
#             # assign an address to the identifier, assign 0 to the start of the array in the program block
#             # and update identifier's row in the symbol table
#             data_type = self._semantic_stack[-3]
#             index = self._semantic_stack[-2]
#             size = self._semantic_stack[-1]
#             self.pop_semantic_stack(3)
#
#             self._program_block.append(f"(ASSIGN, #0, {self._current_data_address},\t)")
#             self._scanner.update_symbol(index,
#                                         symbol_type="array",
#                                         size=size,
#                                         data_type=data_type,
#                                         scope=len(self._scanner.scope_stack),
#                                         address=self._current_data_address)
#             self._current_data_address += 4 * size
#         elif rule_number == 73:             # declare_func
#             # update identifier's row in the symbol table, initialize next scope
#             # and if function is "main" add a jump to the start of function
#             data_type = self._semantic_stack[-2]
#             index = self._semantic_stack[-1]
#             self.pop_semantic_stack(2)
#
#             self._scanner.update_symbol(index,
#                                         symbol_type="function",
#                                         size=0,
#                                         data_type=data_type,
#                                         scope=len(self._scanner.scope_stack),
#                                         address=len(self._program_block))
#             self._scanner.scope_stack.append(index + 1)
#             if self._scanner.symbol_table["lexeme"][index] == "main":
#                 line_number = self._semantic_stack[-1]
#                 self.pop_semantic_stack(1)
#                 self._program_block[line_number] = f"(JP, {len(self._program_block)},\t,\t)"
#         elif rule_number == 10:             # end_function
#             # deletes the current scope
#             scope_start = self._scanner.scope_stack.pop()
#             self._scanner.pop_scope(scope_start)
#         elif rule_number == 28:             # pop_exp
#             # remove last assignment output from the semantic stack
#             self.pop_semantic_stack(1)
#         elif rule_number == 74:             # save
#             # save an instruction in program block's current line
#             current_line_number = len(self._program_block)
#             self._semantic_stack.append(current_line_number)
#             self._program_block.append(None)
#         elif rule_number in {31, 80}:       # jpf
#             # add a JPF instruction in line number with a condition both stored in semantic stack to the current line
#             line_number = self._semantic_stack[-1]
#             condition = self._semantic_stack[-2]
#             self.pop_semantic_stack(2)
#
#             current_line_number = len(self._program_block)
#             self._program_block[line_number] = f"(JPF, {condition}, {current_line_number},\t)"
#         elif rule_number == 75:             # jpf_save
#             # add a JPF instruction in line number with a condition both stored in semantic stack to the next line
#             # and save an instruction in program block's current line
#             line_number = self._semantic_stack[-1]
#             condition = self._semantic_stack[-2]
#             self.pop_semantic_stack(2)
#
#             current_line_number = len(self._program_block)
#             self._program_block[line_number] = f"(JPF, {condition}, {current_line_number + 1},\t)"
#             self._semantic_stack.append(len(self._program_block))
#             self._program_block.append(None)
#         elif rule_number == 32:             # jp
#             # add a JP instruction in line number stored in semantic stack to the current line
#             line_number = self._semantic_stack[-1]
#             self.pop_semantic_stack(1)
#
#             current_line_number = len(self._program_block)
#             self._program_block[line_number] = f"(JP, {current_line_number},\t,\t)"
#         elif rule_number == 29:             # break_jp
#             # add an indirect jump to the top of the break stack
#             break_temp = self._break_stack[-1]
#             self._program_block.append(f"(JP, @{break_temp},\t,\t)")
#         elif rule_number == 76:             # save_break_temp
#             # save a temp in break stack
#             dest = self.get_temp()
#             self._break_stack.append(dest)
#         elif rule_number == 77:             # while_condition
#             # add a JPF in the current line with condition stored in semantic stack to top of the break stack
#             condition = self._semantic_stack[-1]
#             self.pop_semantic_stack(1)
#
#             break_temp = self._break_stack[-1]
#             self._program_block.append(f"(JPF, {condition}, @{break_temp},\t)")
#         elif rule_number == 33:             # while_end
#             # add a JP to the start of while and an ASSIGN for break temp at the start of while
#             line_number = self._semantic_stack[-1]
#             self.pop_semantic_stack(1)
#
#             break_temp = self._break_stack.pop()
#             self._program_block.append(f"(JP, {line_number + 1},\t,\t)")
#
#             current_line_number = len(self._program_block)
#             self._program_block[line_number] = f"(ASSIGN, #{current_line_number}, {break_temp}.\t)"
#         elif rule_number == 79:             # dummy_save
#             # save #1 and an instruction in the semantic stack
#             current_line_number = len(self._program_block)
#             self._semantic_stack.append("#1")
#             self._semantic_stack.append(current_line_number)
#             self._program_block.append(None)
#         elif rule_number == 78:             # case_condition
#             # add an EQ which compares switch variable and case number and store result temp in semantic stack
#             dest = self.get_temp()
#             number = int(self._current_token[1])
#             switch_variable = self._semantic_stack[-1]
#             self._program_block.append(f"(EQ, {switch_variable}, #{number}, {dest})")
#             self._semantic_stack.append(dest)
#         elif rule_number == 36:             # switch_end
#             # remove switch variable from semantic stack and add an ASSIGN for break temp at the start of switch
#             line_number = self._semantic_stack[-2]
#             self.pop_semantic_stack(2)
#
#             current_line_number = len(self._program_block)
#             break_temp = self._break_stack.pop()
#             self._program_block[line_number] = f"(ASSIGN, #{current_line_number}, {break_temp}.\t)"
#         elif rule_number == 42:             # assign
#             # add an assign instruction
#             source_var = self._semantic_stack[-1]
#             dest_var = self._semantic_stack[-2]
#             self.pop_semantic_stack(1)
#
#             self._program_block.append(f"(ASSIGN, {source_var}, {dest_var},\t)")
#         elif rule_number == 45:             # array_access
#             # calculate selected array element address and save result temp in semantic stack
#             array_index = self._semantic_stack[-1]
#             array_base_address = self._semantic_stack[-2]
#             self.pop_semantic_stack(2)
#
#             temp1 = self.get_temp()
#             temp2 = self.get_temp()
#             self._program_block.append(f"(MULT, #4, {array_index}, {temp1})")
#             self._program_block.append(f"(ADD, {temp1}, #{array_base_address}, {temp2})")
#             self._semantic_stack.append(f"@{temp2}")
#         elif rule_number == 71:             # p_op
#             # push operation to semantic stack
#             operation = self._current_input
#             self._semantic_stack.append(operation)
#         elif rule_number in {46, 50, 54}:       # op
#             # add operation instruction
#             operand_1 = self._semantic_stack[-3]
#             operation = self._semantic_stack[-2]
#             operand_2 = self._semantic_stack[-1]
#             self.pop_semantic_stack(3)
#             if operation == "==":
#                 assembly_operation = "EQ"
#             elif operation == "<":
#                 assembly_operation = "LT"
#             elif operation == "*":
#                 assembly_operation = "MULT"
#             elif operation == "/":
#                 assembly_operation = "DIV"
#             elif operation == "+":
#                 assembly_operation = "ADD"
#             elif operation == "-":
#                 assembly_operation = "SUB"
#             else:
#                 raise ValueError("Operation is invalid!")
#             dest = self.get_temp()
#             self._program_block.append(f"({assembly_operation}, {operand_1}, {operand_2}, {dest})")
#             self._semantic_stack.append(dest)
#         elif rule_number == 62:             # end_call
#             # add a PRINT instruction for output
#             value = self._semantic_stack[-1]
#             self.pop_semantic_stack(2)
#
#             self._program_block.append(f"(PRINT, {value},\t,\t)")
#             self._semantic_stack.append(None)
#         return
#
#     def pop_semantic_stack(self, count: int):
#         self._semantic_stack = self._semantic_stack[:len(self._semantic_stack) - count]
#
#     def get_temp(self) -> int:
#         temp = self._current_data_address
#         self._current_data_address += 4
#
#         return temp
#
#     def save_parse_tree(self):
#         """Writes parse tree in parse_tree.txt."""
#         # empty file if failure
#         if self._failure:
#             with open("parse_tree.txt", mode='w') as parse_tree_file:
#                 parse_tree_file.write("")
#                 return
#
#         root = self._parse_stack[1]
#         # add EOF node
#         node = Node("$")
#         node.parent = root
#
#         # write parse tree in the file
#         lines = []
#         for pre, fill, node in RenderTree(root):
#             lines.append(str(f"{pre}{node.name}\n"))
#         with open("parse_tree.txt", mode='w', encoding="utf-8") as parse_tree_file:
#             parse_tree_file.writelines(lines)
#
#     def save_syntax_errors(self):
#         """Writes syntax errors in syntax_errors.txt."""
#         with open("syntax_errors.txt", "w") as syntax_errors_file:
#             if len(self._syntax_errors) == 0:
#                 syntax_errors_file.write("There is no syntax error.")
#             else:
#                 for error in self._syntax_errors:
#                     syntax_errors_file.write(f"{error.content}\n")
#
#     def save_semantic_errors(self):
#         """Writes semantic errors in semantic_errors.txt"""
#         with open("semantic_errors.txt", "w") as semantic_errors_file:
#             if len(self._semantic_errors) == 0:
#                 semantic_errors_file.write("The input program is semantically correct.")
#
#     def save_program_block(self):
#         """Writes program block in output.txt"""
#         with open("output.txt", "w") as output_file:
#             for i in range(len(self._program_block)):
#                 output_file.write(f"{i}\t{self._program_block[i]}\n")
