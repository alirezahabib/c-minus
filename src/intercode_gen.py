'''

1
Introduction
In programming assignment II, you implemented a top-down parser for C-minus, using the transition
diagrams method. In this assignment you are to implement an intermediate code generator for
certain parts of C-minus. This assignment also includes an optional part, which is the implementation
of a simple semantic analyzer for C-minus (see section 6). Note that you may use codes from text
books, with a reference to the used book in your code. However, using codes from the internet
and/or other students in this course is strictly forbidden and will result in Fail grade in the course.
Besides, even if you did not implement the parser in the previous assignment, you may not use the
parsers from other students/groups. In such a case, you must implement the parser, too.
2
Intermediate Code Generator
Specification
In this assignment, you will implement the intermediate code generator with the following
characteristics:
• The code generator is called by the parser to perform a code generation task, which can be
modifying the semantic stack and/or generating a number of three address codes.
• Code generation is performed in the same pass as other compilation tasks (because the
compiler is supposed to be a one-pass compiler).
• The parser calls a function called 'code_gen' and sends an action symbol as an argument to
'code_gen' at appropriate times during parsing.
• The code generator (i.e., the 'code_gen' function) executes the appropriate semantic routine
associated with the received action symbol (based on the technique introduced in Lecture 8).
• Generated three-address codes are saved in an output text file called 'output.txt'.
3
Augmented C-minus Grammar
To implement your intermediate code generator, you should first add the required action symbols to
the grammar of C-minus that was included in section 3 of programming assignment II. For each action
symbol, you need to write an appropriate semantic routine in Python that performs the required code
generation tasks, such as modifying the semantic stack and/or generating a number of three address
codes. Note that you should not change the given grammar in any way other than adding the
required action symbols to the right-hand side of the production rules.
4
Intermediate Code Generation
The intermediate code generation is performed with the same method that was introduced in Lecture
8. In the first part of implementing intermediate code generation in this assignment, all constructs
supported by the given C-minus grammar are to be implemented except for: return statements and
function calls. Therefore, the sample/test 'input.txt' files for this part of the assignment will be a
simple C-minus program which does not contain any type of error. In implementing the required
sematic routines for the intermediate code generation, you should pay attention to the following
points:
• Every input program may include only a number of global variables and contain just a main
function with the signature 'void main (void)'.
• All local variables of the main function are declared at the beginning of the function. That is,
there will not be any declaration of variables inside other constructs such as while loops.
• In conditional statements such as 'if' and/or 'while', if the expression value is zero, it will be
regarded as a 'false' condition; otherwise, it will be regarded to be 'true'. Moreover, the result
of a 'relop' operation that is true, will be '1'. Alternatively, if the result of a 'relop' operation
is 'false', its value will be '0'.
• You should implicitly define a function called 'output' with the signature 'void output (int a);'
which prints its argument (an integer) as the main program's output.


5 Available Three address Codes
In this project, you can only use the following three address codes. Three address codes produced
by your compiler will be executed by an interpreter called 'Tester', which can only interpret the
following three address codes. Otherwise, the tester program fails to run your three address codes.
Please note that the single and most important factor in evaluating your solution to this assignment
is that the output of your intermediate code generator will be successfully interpreted by the
'Tester' program and produce the expected output value. The 'Tester' program and its help file are
released together with this description.
Three address
code
Explanation
1 (ADD, A1, A2, R) The contents of A1 and A2 are added. The result will be saved in R.
2 (MULT, A1, A2, R) The contents of A1 and A2 are multiplied. The result will be saved in R.
3 (SUB, A1, A2, R) The content of A2 is subtracted from A1. The result will be saved in R.
4 (EQ, A1, A2, R) The contents of A1 and A2 are compared. If they are equal, '1' (i.e., as a
true value) will be saved in R; otherwise, '0' (i.e., as a false value) will be
saved in R.
5 (LT, A1, A2, R) If the content of A1 is less than the content of A2, '1' will be saved in R;
otherwise, '0' will be saved in R.
6 (ASSIGN, A, R, ) The content of A is assigned to R.
7 (JPF, A, L, ) If content of A is 'false', the control will be transferred to L; otherwise,
next three address code will be executed.
8 (JP, L, , ) The control is transferred to L.
9 (PRINT, A, , ) The content of A will be printed to the standard output.
As it was explained in Lecture 8, in three address codes, you can use three addressing modes of direct
address (e.g., 100), indirect address (e.g., @100), and immediate value (e.g., #100). For simplicity, you
can suppose that all memory locations are allocated statically. In other words, we don't have a runtime
stack or heap. Also, assume that four bytes of memory are required to store an integer. Therefore, the
address of all data memory locations is divisible by four. The following figures show a sample C-minus
program and the three address codes produced for it. Note that each three address code is preceded
by a line number starting from zero. The tester program outputs a value of '15' by running the three
address codes in the given sample. For more information about the tester program and the formatting
of the three address codes, please read the provided help file very carefully. As it was mentioned
earlier, the grading of the code generation part of this assignment is solely based on whether or not
the produced three address code can be successfully run by the Tester program and produce the
expected value.
Note that the three address codes produced for an input program such as the given sample in Fig. 1 do
not need to be identical to the code given in Fig 2. There can be a virtually infinite number of correct
three-address codes for such programs. As long as the produced code can be executed by the Tester
program and prints the expected value(s), it is acceptable.

lineno code
1 void main( void ) {
2 int prod;
3 int i;
4 prod = 1;
5 i = 1;
6 repeat {
7 prod = i * prod;
8 i = i + 2;
9 } until ( 6 < i )
10 output (prod);
11 }
Fig. 1 C-minus input sample (saved in “input.txt”)

produced three address codes
0 (JP, 1, , )
1 (ASSIGN, #1, 100, )
2 (ASSIGN, #1, 104, )
3 (MULT, 104, 100, 500)
4 (ASSIGN, 500, 100, )
5 (ADD, 104, #2, 504)
6 (ASSIGN, 504, 104, )
7 (LT, #6, 104, 508)
8 (JPF, 508, 3, )
9 (PRINT, 100, , )
Fig. 2 'Output.txt' Sample

'''

from enum import Enum

'''
 where is it implemented?
'''
# import symbol_table as st

from src.parser import Parser
from src.scanner import Scanner
from scanner import KEYWORD, SYMBOL
from symbol_table import Address
from symbol_table import Symbol_Table

class OPERATIONS(Enum):
    ADD = "ADD"
    MULT = "MULT"
    SUB = "SUB"
    EQ = "EQ"
    LT = "LT"
    ASSIGN = "ASSIGN"
    JPF = "JPF"
    JP = "JP"
    PRINT = "PRINT"


class SS:
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            return -1

    def pop_mult(self, number):
        if len(self.stack) > number - 1:
            toReturn = []
            for i in range(number):
                toReturn.append(self.stack.pop())
            return toReturn
        else:
            return -1

    def pop_out(self):
        if len(self.stack) > 0:
            self.stack.pop()
        else:
            return -1

    def pop_out_mult(self, num):
        if len(self.stack) > num - 1:
            for i in range(num):
                self.stack.pop()
        else:
            return -1

    def get_index(self, index):
        if len(self.stack) > index:
            return self.stack[index]

    def top(self):
        if len(self.stack) != 0:
            return self.stack[-1]
        else:
            return -1

    def __str__(self):
        return str(self.stack)


# class Address:
#     def __init__(self, address):
#         self.address = address
#
#     def set_indirect(self):
#         self.address = "@" + str(self.address)
#         return self
#
#     def __str__(self):
#         return str(self.address)


# highly needs to be refactored
# class Symbol_Table:
#
#     def __init__(self, scanner : Scanner) -> None:
#         # row properties are id, lexeme, proc/func/var/param (kind), No. Arg/Cell (attributes), type, scope, address
#         self.address_to_row = {}
#         self.table = []
#         self.current_scope = 0
#         self.scope_stack = [0]
#         self.insert("output")
#         self.modify_last_row("func", "void")
#         self.table[-1]['attributes'] = 1
#         self.pb = PB()
#         self.table.append({'id': 1, 'lexeme': 'somethingwild', 'kind': "param", 'attributes': '-', 'type': "int",
#                            'scope': 1, 'address': self.pb.get_tmp_address()})  # ("int", 1)
#         self.scanner = scanner
#
#     def insert(self, lexeme):
#         self.table.append({'id': len(self.table), 'lexeme': lexeme})
#
#     def modify_last_row(self, kind, type):
#         # after declaration of a variable by scanner, code generator needs
#         # to complete the declaration by modifying the last row of symbol table
#         self.table[-1]['kind'] = kind
#         self.table[-1]['type'] = type
#         self.table[-1]['address'] = self.pb.get_tmp_address()  # (type, 1)
#         self.table[-1]['scope'] = self.current_scope
#         self.table[-1]['attributes'] = '-'
#         self.address_to_row[self.table[-1]['address']] = len(self.table) - 1
#
#     def modify_func_row_information(self, row_index, invocation_address, return_address, return_value):
#         # add a "invocation_address" field to the row,
#         # this is used when we declare a function and we want to invoke it. We should know where to jump to
#         self.table[row_index]['invocation_address'] = invocation_address
#         # add a "return_address" field to the row,
#         # anyone who calls the function should put its address (PC) in this address
#         self.table[row_index]['return_address'] = return_address
#         # return value is the address of a temp that is supposed to hold the return value of the function
#         self.table[row_index]['return_value'] = return_value
#
#     def modify_attributes_last_row(self, num_attributes):
#         # used for array declaration and function declaration
#         # if arr_func == True then it is an array
#         # else it is a function
#         # note: for now it is only used for array declaration
#         self.table[-1]['attributes'] = num_attributes
#
#     def modify_attributes_row(self, row_id, num_attributes, arr_func: bool = True):
#         # used for modifying function No. of args after counting them
#         # if arr_func == True then it is an array
#         # else it is a function
#         self.table[row_id]['attributes'] = num_attributes
#
#     def modify_kind_last_row(self, kind):
#         self.table[-1]['kind'] = kind
#
#     def add_scope(self):
#         self.current_scope += 1
#         self.scope_stack.append(len(self.table))
#
#     def end_scope(self):
#         # remove all rows of symbol table that are in the current scope
#         # and update the current scope
#         # remember function is first added and then the scope is added
#         # also param type of the function that the scope is created for,
#         # must not be removed
#         remove_from = len(self.table)
#         for i in range(self.scope_stack[-1], len(self.table)):
#             if self.is_useless_row(i) or self.table[i]['kind'] != "param":
#                 remove_from = i
#                 break
#
#         self.table = self.table[:remove_from]
#
#         self.current_scope -= 1
#         self.scope_stack.pop()
#
#     def declare_array(self, num_of_cells):
#         self.table[-1]['attributes'] = num_of_cells
#
#     def lookup(self, name, start_ind=0, in_declare=False, end_ind=-1) -> dict:
#         # search in symbol table
#         # search for it between the start_ind and end_ind of symbol table
#         # if end_ind == -1 then it means to search till the end of symbol table
#
#         row_answer = None
#         nearest_scope = -1
#         end = end_ind
#
#         if end_ind == -1:
#             end = len(self.table)
#             if in_declare and self.is_useless_row(-1):
#                 end -= 1
#
#         while len(self.scope_stack) >= -nearest_scope:
#             start = self.scope_stack[nearest_scope]
#
#             for i in range(start, end):
#                 row_i = self.table[i]
#                 if not self.is_useless_row(i):
#                     if nearest_scope != -1 and row_i['kind'] == "param":
#                         pass
#                     elif row_i['lexeme'] == name:
#                         return row_i
#
#             nearest_scope -= 1
#             end = start
#
#         return row_answer
#
#     def remove_last_row(self):
#         self.table.pop()
#
#     def is_useless_row(self, id):
#         if "type" not in self.get_row_by_id(id):
#             return True
#
#     def get_row_id_by_address(self, address) -> int:
#         return self.address_to_row[address]
#
#     def get_row_by_id(self, id) -> dict:
#         return self.table[id]
#
#     def get_id_last_row(self):
#         return len(self.table) - 1
#
#     def get_row_by_address(self, address) -> dict:
#         return self.get_row_by_id(self.get_row_id_by_address(address))
#
#     def get_last_row(self):
#         return self.get_row_by_id(-1)
#
#     def get_last_row_index(self):
#         return len(self.table) - 1
#
#
class PB:
    def __init__(self):
        self.block = []
        self.line = 0
        # self.address = address
        self.address = Address.get_instance()
        # self.last_tmp = Address(500 - 4)
        # self.last_addr = Address(100 - 4)
        # self.all_addresses = []

    def get_len(self):
        return len(self.block)

    def get_line(self):
        return self.line

    def get_current_tmp_addr(self):
        return self.address.last_tmp

    def add_code(self, operation, op1, op2=None, op3=None):
        self.block.append([operation, op1, op2, op3])
        self.line += 1

    def add_to_index(self, index, operation, op1, op2=None, op3=None):
        self.block.insert(index, [operation, op1, op2, op3])
        self.line += 1

    def get_tmp_address(self):
        self.address.last_tmp += 4
        self.address.all_addresses.append(self.address.last_tmp)
        return Address(self.address.last_tmp.address)

    # def get_current_tmp_addr(self):
    #     return self.last_tmp

    def update_tmp_addr(self, size):
        self.address.last_tmp += size

    def get_address(self):
        self.address.last_addr += 1
        self.address.all_addresses.append(self.address.last_addr)
        return Address(self.address.last_addr.address)

    # modify this shiiiiiiiiiiiiiiiiiiiiit
    def modify(self, index, op, first_op="", second_op="", third_op=""):
        if op == "==":
            opr = "EQ"
        elif op == '-':
            opr = "SUB"
        elif op == ":=":
            opr = "ASSIGN"
        elif op == "<":
            opr = "LT"
        elif op == '+':
            opr = "ADD"
        elif op == '*':
            opr = "MULT"

        # now we want to add the new code to the block (we removed index at the start)
        self.block[index] = [opr, first_op, second_op, third_op]

    def get_temp(self):
        temp = self.address.last_tmp
        self.address.all_addresses.append(temp)
        self.address.last_tmp += 4

        return temp

    def add_code_str(self, code):
        code_split = code.split(",")
        if code_split[3] == "\t":
            code_split[3] = None
        if code_split[2] == "\t":
            code_split[2] = None
        if len(code_split) == 4:
            self.add_code(code_split[0], code_split[1], code_split[2], code_split[3])
        elif len(code_split) == 3:
            self.add_code(code_split[0], code_split[1], code_split[2])
        elif len(code_split) == 2:
            self.add_code(code_split[0], code_split[1])
        # self.block.append([code])
        # self.line += 1

    def add_code_to_index_str(self, index, code):
        code_split = code.split(",")
        if code_split[3] == "\t":
            code_split[3] = None
        if code_split[2] == "\t":
            code_split[2] = None

        if len(code_split) == 4:
            self.add_to_index(index, code_split[0], code_split[1], code_split[2], code_split[3])
        elif len(code_split) == 3:
            self.add_to_index(index, code_split[0], code_split[1], code_split[2])
        elif len(code_split) == 2:
            self.add_to_index(index, code_split[0], code_split[1])

        # self.block.append([code])
        # self.line += 1

    def get_tmp_address_by_size(self, entries_type, array_size):
        self.address.last_tmp += entries_type * array_size
        self.address.all_addresses.append(self.address.last_tmp)
        return Address(self.address.last_tmp.address)

    def get_next_addr(self,addr):
        return self.address.all_addresses[self.address.all_addresses.index(addr)+1]

    def get_type(self, addr):
        next_addr = self.get_next_addr(addr)
        if next_addr - addr == 4:
            return "int"
        elif next_addr - addr == 1:
            return "void"


# to be refactored
class SemanticAnalyzer:
    def __init__(self):
        self.num_semantic_errors = 0
        self.all_errors = []

    def raise_semantic_error(self, line_no, error="error", first_op="", second_op="", third_op="", fourth_op=""):
        self.all_errors.append(error.format(line_no, first_op, second_op, third_op, fourth_op))
        self.num_semantic_errors += 1

    def pop_error(self):
        # if we declare a function of type void we must pop the error
        self.all_errors.pop()
        self.num_semantic_errors -= 1


# main class
class CodeGenerator:
    def __init__(self, scanner: Scanner, parser: Parser): #, address : Address):
        self.ss = SS()
        self.address = Address.get_instance()
        self.pb = PB()
        # self.st = st.SymbolTable()
        self.loop = []
        self.scanner = scanner
        self.parser = parser
        self.break_stack = []

        self.symbol_table = self.scanner.symbol_table
        self.code_gen_st = Symbol_Table.get_instance()
        self.curr_repeats = 0
        self.get_curr_input()
        # self.semantic_analyzer = SemanticAnalyzer()
        # # errors
        # self.error_scoping = "#{0}: Semantic Error! '{1}' is not defined.{2}{3}{4}"
        # self.error_void_type = "#{0}: Semantic Error! Illegal type of void for '{1}'.{2}{3}{4}"
        # self.error_type_missmatch = "#{0}: Semantic Error! Type mismatch in operands, Got {1} instead of {2}.{3}{4}"
        # self.error_break = "#{0}: Semantic Error! No 'repeat ... until' found for 'break'."
        # self.error_param_type_missmatch = "#{0}: Semantic Error! Mismatch in type of argument {1} of '{2}'. Expected '{3}' but got '{4}' instead."
        # self.error_num_args = "#{0}: Semantic Error! Mismatch in numbers of arguments of '{1}'.{2}{3}{4}"

        # ...

    '''
    this must be implemented in parser part so we get _current_token and current_input as used:
        def _update_current_token(self):
            """Stores next token in _current_token and updates _current_input."""
            self._current_token: Tuple[str, str] = self._scanner.get_next_token()
            self._current_input: str = ""
            if self._current_token[0] in {Scanner.KEYWORD, Scanner.SYMBOL, Scanner.EOF}:
                self._current_input = self._current_token[1]
            else:
                self._current_input = self._current_token[0]
    '''

    def get_curr_input(self):
        self._current_token = self.parser.get_next_token()
        print(self._current_token)
        print(self._current_token[0])
        print(self._current_token[1])
        print(self._current_token[0].type)
        # self._current_token = self.parsre.get_current_token()[0]
        toCheck = KEYWORD + SYMBOL + "$"
        if self._current_token == None:
            return
        if self._current_token[0].type in toCheck:
            self._current_input = self._current_token[1]
        else:
            self._current_input = self._current_token[0]

    def call_main(self):
        main_function_row = self.scanner.symbol_table.code_gen_st.lookup("main")
        # set up the return address register of main
        self.pb.add_code(
            ":=",
            "#" + str(self.pb.get_line() + 2),
            str(main_function_row["return_address"])
        )
        # now jump to the invocation address of main
        self.pb.add_code(
            "JP",
            str(main_function_row["invocation_address"])
        )

    def declare_id(self):
        # search in symbol table
        # if found in current scope raise error
        # if not found
        # add to symbol table
        # token will be the lexeme of the variable
        # the_row = self.scanner.symbol_table.lookup(token, self.scanner.symbol_table.start_scope, False)
        # if the_row is not None and the_row["scope"] == self.symbol_table.current_scope:
        #     # this means that the variable is already declared,
        #     # and we want to redefine it
        #     del the_row["type"]
        #
        # self.symbol_table.insert(token)
        # if self.ss.top() == "void":
        # to be implented
        # self.semantic_analyzer.raise_semantic_error(line_no=self.pb.get_line(),
        #                                             error=self.error_void_type,
        #                                             first_op=token)

        self.code_gen_st.modify_last_row(kind="var", type=self.ss.top())
        self.pb.add_code(
            ":=",
            "#0",
            self.code_gen_st.get_last_row()["address"],
        )
        self.ss.pop()

    # refactore this shiiiiiiiiiiiiiit
    def declare_entry_array(self):
        self.p_zero()
        self.dec_array()

    # refactore this shiiiiiiiiiiiiiiiiiiit
    def dec_array(self):
        # add to symbol table
        # self.symbol_table
        array_size = self.ss.pop()
        if str(array_size).startswith("#"):
            array_size = int(array_size[1:])
        self.code_gen_st.modify_attributes_last_row(num_attributes=array_size)
        array_row = self.code_gen_st.get_last_row()
        # array address is the address of pointer to array
        # we need to allocate memory for the array itself and then assign the address of the first entry to the pointer
        array_address = array_row["address"]
        entries_type = array_row["type"]
        array_start_address = self.pb.get_tmp_address_by_size(entries_type, array_size)
        self.pb.add_code(
            ":=",
            "#" + str(array_start_address),
            array_address
        )

    def label(self):
        # declare where to jump back after until in repeat-until
        self.ss.push(self.pb.get_line())

        self.curr_repeats += 1

    def until(self):
        # jump back to label if condition is true
        # also check if there were any break statements before
        self.curr_repeats -= 1
        temp_until_condition = self.ss.pop()  # the value that until should decide to jump based on it
        # check breaks
        # sdfasdfa
        while len(self.ss.stack) > 0 and self.ss.top() == "break":  # [-1] == "break":
            self.pb.modify(self.ss.stack[-2], "JP", self.pb.get_line() + 1)
            self.ss.pop_mult(2)
        # jump back
        self.pb.add_code("JPF", temp_until_condition,
                         self.ss.top())
        self.ss.pop()

    def push_eq(self):
        # in case of assignment, push = to stack
        # used for finding out if there is a nested assignment
        self.ss.push("=")

    def start_call(self):
        # start of function call
        # row_id = self.symbol_table.lookup(self.semantic_stack[-1])['id']
        function_row_id = self.code_gen_st.get_row_id_by_address(self.ss.top())
        self.ss.pop()
        num_parameters = self.code_gen_st.get_row_by_id(function_row_id)["attributes"]
        # add parameter types to stack in the form of tuple (type, is_array)
        for i in range(num_parameters, 0, -1):
            temp_address_param = self.code_gen_st.get_row_by_id(function_row_id + i)["address"]
            # type_param = self.get_operand_type(temp_address_param)
            self.ss.push(temp_address_param)

        # add the number of parameters to stack
        self.ss.push(num_parameters)
        # add a counter for arguments - at first it is equal to number of parameters
        self.ss.push(num_parameters)
        # add name of function to stack
        self.ss.push(self.code_gen_st.get_row_by_id(function_row_id)["lexeme"])

    def end_call(self):
        # end of function call
        self.no_more_arg_input = False
        name_func = self.ss.pop()
        counter_args = self.ss.pop()
        # num_parameters = self.ss.pop()
        # if counter_args != 0:
        #     self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
        #                                                 error=self.error_num_args,
        #                                                 first_op=name_func
        #                                                 )
        #     self.pop_last_n(counter_args)

        function_row = self.code_gen_st.lookup(name_func)
        index = function_row['id']
        # if index in self.FS:
        #     self.semantic_analyzer.raise_semantic_error(1)  # todo added to avoid recursive call

        # return if function_row does not have needed keys (may not happen!)
        if "invocation_address" not in function_row or "return_address" not in function_row:
            # print("error in function declaration")
            return
        # update the return address temp of function (we want the function to return here after invocation)
        return_address_temp = function_row["return_address"]
        self.pb.add_code(
            ":=",
            "#" + str(self.pb.get_line() + 2),
            return_address_temp
        )
        # # if the function is supposed to return a value, we need to push the address of return value to stack
        # if function_row[type_key] != "void":
        #     self.semantic_stack.append(function_row[return_value_key]
        # now that everything is set (including return address and arguments assignment), we can jump to the function
        self.pb.add_code(
            "JP",
            function_row["invocation_address"]
        )
        if function_row["type"] != "void":
            returnee_copy = self.pb.get_tmp_address(1, function_row["type"])
            self.pb.add_code(
                ":=",
                function_row["return_value"],
                returnee_copy
            )
            self.ss.push(returnee_copy)

    def print(self):
        self.pb.add_code("print", self.ss.top())
        self.ss.pop()

    def get_operand_type(self, operand):
        is_array = False
        if str(operand).startswith("#"):
            return "int", is_array
        elif str(operand).startswith("@"):
            operand = operand[1:]
        type = self.pb.get_type(int(operand))
        if type.endswith("-arr"):
            type = type[:-4]
            is_array = True

        return type, is_array

    def arg_input(self):
        # take input argument for function call
        if not self.no_more_arg_input:
            arg = self.ss.pop()
            type_arg = self.get_operand_type(arg)
            name_func = self.ss.pop()
            counter_args = self.ss.pop()
            counter_args -= 1
            # if counter_args == 0 and token != ")":
            #     self.no_more_arg_input = True
            #     self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
            #                                                 error=self.error_num_args,
            #                                                 first_op=name_func
            #                                                 )

            num_parameters = self.ss.pop()
            temp_param = self.ss.pop()
            self.pb.add_code(
                ":=",
                arg,
                temp_param
            )

            type_param = self.get_operand_type(temp_param)
            if type_arg != type_param:
                pass
                # self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
                #                                             error=self.error_param_type_missmatch,
                #                                             first_op=num_parameters - counter_args,
                #                                             second_op=name_func,
                #                                             third_op=self.get_type_name(type_param),
                #                                             fourth_op=self.get_type_name(type_arg)
                #                                             )
            else:
                if name_func == "output":
                    self.ss.push(arg)
                    self.print("nothing")

            self.ss.push(num_parameters)
            self.ss.push(counter_args)
            self.ss.push(name_func)

    # def dec_array(self):
    #     size, index, data_type = self.ss.pop_mult(3)
    #     self.ss.pop_out_mult(3)
    #
    #     self.pb.add_code("ASSIGN", 0, self.pb.get_current_tmp_addr())
    #     self.scanner.symbol_table.update_symbol(index,
    #                                 symbol_type="array",
    #                                 size=size,
    #                                 data_type=data_type,
    #                                 scope=len(self.scanner.symbol_table.scope_stack),
    #                                 address=self.pb.get_current_tmp_addr())
    #     self.pb.update_tmp_addr(4 * size)

    # def run_routine(self, routine_name, params):
    #     func_to_call = getattr(self, routine_name)
    #     if func_to_call is not None and callable(func_to_call):
    #         func_to_call(*params)
    #     else:
    #         raise Exception("Routine not found")

    # def code_gen(self, action_symbol, token, line_number):
    #     self.current_line = line_number
    #     if self.no_more_arg_input and action_symbol != "#end_call":
    #         return
    #
    #     action_symbol = action_symbol[1:]
    #     method = getattr(self, action_symbol, None)
    #     if method:
    #         method(token)

    # push type / get_id_type / p_input
    def p_type(self):
        # p_type
        # push type into the semantic stack
        data_type = self._current_token[1]
        self.ss.push(data_type)

    '''
    self._scanner must become the scanner used in Parser
    if it is change all repetitions of it to self.scanner
    '''

    def p_id_index(self):  # p_id_index
        # push index of identifier into the semantic stack
        lexeme = self._current_token[1]
        index = self.scanner.get_symbol_index(lexeme)
        self.ss.push(index)

    def p_id(self):  # p_id
        # push address of identifier into the semantic stack
        lexeme = self._current_token[1]
        index = self.scanner.get_symbol_index(lexeme)
        # st = self.scanner.symbol_table.get_st()
        # -1 how
        address = self.scanner.symbol_table.symbol_table["address"][index]
        self.ss.push(address)

    def dec_var(self):  # declare_var
        # assign an address to the identifier, assign 0 to the variable in the program block
        # and update identifier's row in the symbol table
        data_type = self.ss.get_index(-2)
        index = self.ss.get_index(-1)
        self.ss.pop_mult(2)

        # self.pb.add_code("ASSIGN", 0, self.pb.get_tmp_address())
        self.pb.add_code("ASSIGN", 0, self.pb.get_current_tmp_addr())
        '''
        this is what the update_symbol is supposed to do in Scanner class:
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

        '''
        self.scanner.symbol_table.update_symbol(index,
                                                symbol_type="var",
                                                size=0,
                                                data_type=data_type,
                                                scope=len(self.scanner.symbol_table.scope_stack),
                                                address=self.pb.get_current_tmp_addr())
        self.pb.update_tmp_addr(4)

    # def dec_array(self):  # declare_array
    # # assign an address to the identifier, assign 0 to the start of the array in the program block
    # # and update identifier's row in the symbol table
    # # data_type = self._semantic_stack[-3]
    # # index = self._semantic_stack[-2]
    # # size = self._semantic_stack[-1]
    # size, index, data_type = self.ss.pop_mult(3)
    # self.ss.pop_out_mult(3)
    #
    # self.pb.add_code("ASSIGN", 0, self.pb.get_current_tmp_addr())
    # '''
    # this is what the update_symbol is supposed to do in Scanner class:
    # def update_symbol(self,
    #                   index: int,
    #                   symbol_type: str = None,
    #                   size: int = None,
    #                   data_type: str = None,
    #                   scope: int = None,
    #                   address: int = None):
    #     if symbol_type is not None:
    #         self.symbol_table["type"][index] = symbol_type
    #     if size is not None:
    #         self.symbol_table["size"][index] = size
    #     if data_type is not None:
    #         self.symbol_table["data_type"][index] = data_type
    #     if scope is not None:
    #         self.symbol_table["scope"][index] = scope
    #     if address is not None:
    #         self.symbol_table["address"][index] = address
    #
    # '''
    # self.scanner.symbol_table.update_symbol(index,
    #                             symbol_type="array",
    #                             size=size,
    #                             data_type=data_type,
    #                             scope=len(self.scanner.symbol_table.scope_stack),
    #                             address=self.pb.get_current_tmp_addr())
    # self.pb.update_tmp_addr(4 * size)

    def dec_func(self):  # declare_func
        # update identifier's row in the symbol table, initialize next scope
        # and if function is "main" add a jump to the start of function
        # data_type = self._semantic_stack[-2]
        # index = self._semantic_stack[-1]
        index, data_type = self.ss.pop_mult(2)
        self.ss.pop_out_mult(2)
        # self.pop_semantic_stack(2)

        '''
        this is what the update_symbol is supposed to do in Scanner class:
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

        '''
        self.scanner.symbol_table.update_symbol(index,
                                                symbol_type="function",
                                                size=0,
                                                data_type=data_type,
                                                scope=len(self.scanner.symbol_table.scope_stack),
                                                address=self.pb.get_len())
        '''
        depends on how scope_stack is implemented in Scanner class
        '''
        # -1 to be implemented
        self.scanner.symbol_table.scope_stack.append(index + 1)
        if self.scanner.symbol_table.symbol_table["lexeme"][index] == "main":
            # line_number = self._semantic_stack[-1]
            # self.pop_semantic_stack(1)
            line_number = self.ss.pop()
            self.pb.add_to_index(line_number, "JP", self.pb.get_len())
            # self.pb.add_to_index(line_number, "JP", self.pb.get_line())

    def end_func(self):  # end_function
        # deletes the current scope
        '''
        depends on how scope_stack is implemented in Scanner class
        '''
        # to be implemented
        scope_start = self.scanner.symbol_table.scope_stack.pop()
        self.scanner.pop_scope(scope_start)

    # def p_type

    def break_jp(self):  # break_jp
        # add an indirect jump to the top of the break stack
        break_temp = self.break_stack[-1]
        self.pb.add_code_str(f"(JP, @{break_temp})")

    def save(self):  # save
        # save an instruction in program block's current line
        current_line_number = self.pb.get_len()
        self.ss.push(current_line_number)
        self.pb.add_code(None, None)

    def jpf_save(self):  # jpf_save
        # add a JPF instruction in line number with a condition both stored in semantic stack to the next line
        # and save an instruction in program block's current line
        # line_number = self._semantic_stack[-1]
        # condition = self._semantic_stack[-2]
        line_number, condition = self.ss.pop_mult(2)
        # self.pop_semantic_stack(2)

        current_line_number = self.pb.get_len()
        self.pb.add_code_to_index_str(line_number, f"(JPF, {condition}, {current_line_number + 1})")
        self.ss.push(self.pb.get_len())
        self.pb.add_code(None, None)

    def jp(self):  # jp
        # add a JP instruction in line number stored in semantic stack to the current line
        line_number = self.ss.pop()
        # self.pop_semantic_stack(1)

        current_line_number = self.pb.get_len()
        self.pb.add_code_to_index_str(line_number, f"(JP, {current_line_number},\t,\t)")

    def assign(self):  # assign
        # add an assign instruction
        # source_var = self._semantic_stack[-1]
        # dest_var = self._semantic_stack[-2]
        source_var, dest_var = self.ss.pop_mult(2)
        # self.pop_semantic_stack(1)

        self.pb.add_code_str(f"(ASSIGN, {source_var}, {dest_var},\t)")

    def array_access(self):  # array_access
        # calculate selected array element address and save result temp in semantic stack
        # array_index = self._semantic_stack[-1]
        # array_base_address = self._semantic_stack[-2]
        array_index, array_base_address = self.ss.pop_mult(2)
        # self.pop_semantic_stack(2)

        temp1 = self.pb.get_temp()
        temp2 = self.pb.get_temp()
        self.pb.add_code_str(f"(MULT, #4, {array_index}, {temp1})")
        self.pb.add_code_str(f"(ADD, {temp1}, #{array_base_address}, {temp2})")
        self.ss.push(f"@{temp2}")

    def push_op(self):  # p_op
        # push operation to semantic stack
        '''
        update_token must be implemented as explained above
        '''
        operation = self._current_input
        self.ss.push(operation)

    def op(self):  # op
        # add operation instruction
        # operand_1 = self._semantic_stack[-3]
        # operation = self._semantic_stack[-2]
        # operand_2 = self._semantic_stack[-1]
        operand_2, operation, operand_1 = self.ss.pop_mult(3)
        # self.pop_semantic_stack(3)
        if operation == "==":
            assembly_operation = "EQ"
        elif operation == "<":
            assembly_operation = "LT"
        elif operation == "*":
            assembly_operation = "MULT"
        elif operation == "/":
            assembly_operation = "DIV"
        elif operation == "+":
            assembly_operation = "ADD"
        elif operation == "-":
            assembly_operation = "SUB"
        else:
            raise ValueError("Operation is invalid!")
        dest = self.pb.get_temp()
        self.pb.add_code_str(f"({assembly_operation}, {operand_1}, {operand_2}, {dest})")
        self.ss.push(dest)

    def p_num(self):  # p_num
        # push number into the semantic stack
        number = int(self._current_token[1])
        self.ss.push(number)

    def p_num_tmp(self):  # p_num_temp
        # push #number into the semantic stack
        number = int(self._current_token[1])
        self.ss.push(f"#{number}")

    def save_break_tmp(self):  # save_break_temp
        # save a temp in break stack
        dest = self.pb.get_temp()
        self.break_stack.append(dest)

    def p_zero(self):
        self.ss.push("0")

    # def label(self):
    #     self.ss.push(self.pb.get_line())
    #
    # def start_loop(self):
    #
    # def repeat(self):
    #
    # def end_loop(self):

    # declare id
    # it may not be needed actually
    # def did(self, token):
    #     # search in symbol table
    #     # if found in current scope raise error
    #     # if not found
    #     # add to symbol table
    #     # token will be the lexeme of the variable
    #     the_row = self.scanner.symbol_table.lookup(token, self.start_scope, False)
    #     if the_row is not None and the_row[type_key] == "param":
    #         # this means that the variable is already declared and is the function parameter,
    #         # and we want to redefine it
    #         del the_row[type_key]
    #
    #     self.scanner.symbol_table.insert(token)
    #     if self.ss.top() == "void":
    #         self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
    #                                                     error=self.error_void_type,
    #                                                     first_op=token)
    #
    #     self.symbol_table.modify_last_row(kind=kind, type=self.semantic_stack[-1])
    #     self.pb.add_code(
    #         ":=",
    #         "#0",
    #         self.scanner.symbol_table.get_last_row()[address_key],
    #     )
    #     self.ss.pop()

    def mult(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("MUL", op1, op2, tmp)
        self.ss.push(tmp)

    # def add(self):
    #     op2 = self.ss.pop()
    #     op1 = self.ss.pop()
    #     tmp = self.pb.get_tmp_address()
    #     self.pb.add_code("ADD", op1, op2, tmp)
    #     self.ss.push(tmp)
    # ...

    # def sub(self):
    #     # op2 = self.ss.pop()
    #     # op1 = self.ss.pop()
    #     op2, op1 = self.ss.pop_mult(2)
    #     tmp = self.pb.get_tmp_address()
    #     self.pb.add_code("SUB", op1, op2, tmp)
    #     self.ss.push(tmp)
    #     # ...
    #
    # def mult(self):
    #     # op2 = self.ss.pop()
    #     # op1 = self.ss.pop()
    #     op2, op1 = self.ss.pop_mult(2)
    #     tmp = self.pb.get_tmp_address()
    #     self.pb.add_code("MUL", op1, op2, tmp)
    #     self.ss.push(tmp)
    #     # ...
    #
    # def equals(self):
    #     # op2 = self.ss.pop()
    #     # op1 = self.ss.pop()
    #     op2, op1 = self.ss.pop_mult(2)
    #     tmp = self.pb.get_tmp_address()
    #     self.pb.add_code("EQ", op1, op2, tmp)
    #     self.ss.push(tmp)
    #     # ...
    #
    # def less_than(self):
    #     # op2 = self.ss.pop()
    #     # op1 = self.ss.pop()
    #     op2, op1 = self.ss.pop_mult(2)
    #     tmp = self.pb.get_tmp_address()
    #     self.pb.add_code("LT", op1, op2, tmp)
    #     self.ss.push(tmp)
    #     # ...
    #
    # def assign(self):
    #     # op2 = self.ss.pop()
    #     # op1 = self.ss.pop()
    #     op2, op1 = self.ss.pop_mult(2)
    #     -1
    #     to
    #     be
    #     implemented
    #     if op1 == "=":
    #         op1 = self.ss.pop()
    #     if is_array:
    #         self.pb.add_code("ASSIGN", op1, op2 + index * 4)
    #     else:
    #         self.pb.add_code("ASSIGN", op1, op2)
    #
    #     self.ss.push("=")
    #     self.ss.push(op1)
    #
    #     # ...
    #
    # def jpf(self):
    #     # op2 = self.ss.pop()
    #     # op1 = self.ss.pop()
    #     addr = self.ss.pop_mult(2)
    #     op1 = self.ss.pop()
    #     # -1 to be implemented
    #     self.pb.add_to_index(addr, "JPF", op1, self.pb.get_line(), None)
    #
    #     # ...
    #
    # def jp(self):
    #     addr = self.ss.pop()
    #     # -1 to be implemented
    #     self.pb.add_to_index(addr, "JP", self.pb.get_line(), None, None)
    #     # ...
    #
    # def output(self):
    #     op1 = self.ss.pop()
    #     self.pb.add_code("PRINT", op1, None, None)
    #
    #     # ...
    #
    # def routine(self, name, params):
    #     sem_func = getattr(self, name)
    #     if sem_func is None or not callable(sem_func):
    #         -1
    #         to
    #         be
    #         implemented
    #         return -1
    #
    #     sem_func(*params)
    #     # ...
    #
    # def pid(self, name):
    #     self.ss.push(name)
    #
    # def pnum(self, value):
    #     self.ss.push(value)
    #
    # def save(self):
    #     self.ss.push(self.pb.get_line())
    #     self.pb.add_code(None, None)
    #
    # # def jpf(self):
    # #     addr = self.ss.pop()
    # #     self.pb.add_code[addr]("JPF", self.ss.pop(), self.pb.get_line(), None)
    #
    # def jpf_save(self):
    #     addr = self.ss.pop()
    #     # -1 to be implemented
    #     self.pb.add_to_index(addr, "JPF", self.ss.pop(), self.pb.get_line() + 1, None)
    #     self.pb.add_code(None, None)
    #     self.ss.push(self.pb.get_line())
    #
    # # -1 to be refactored
    # def loop(self):
    #     self.loop.append(self.pb.get_line() + 1)
    #     self.pb.add_code(None, None)
    #
    # def until(self):
    #     expr = self.ss.pop()
    #     addr = self.ss.pop()
    #     self.pb.add_code("JPF", expr, addr, None)
    #     addr = self.pb.get_line()
    #     for address in self.loop:
    #         self.pb.add_to_index(address, "JP", addr, None, None)
    #
    # def label(self):
    #     self.ss.append(self.pb.get_line())
    #
    # def j_main(self):
    #     addr = self.ss.pop()
    #     if addr == 1:
    #         self.pb.add_to_index(addr, "JP", self.pb.get_line(), None, None)
    #
    # def ptype(self):
    #     self.pb.add_code("INPUT", self.ss.pop(), None, None)
    #
    # # declare id
    # def did(self, token):
    #     # search in symbol table
    #     # if found in current scope raise error
    #     # if not found
    #     # add to symbol table
    #     # token will be the lexeme of the variable
    #     the_row = self.symbol_table.lookup(token, self.start_scope, False)
    #     if the_row is not None and the_row[type_key] == "param":
    #         # this means that the variable is already declared and is the function parameter,
    #         # and we want to redefine it
    #         del the_row[type_key]
    #
    #     self.symbol_table.insert(token)
    #     if self.semantic_stack[-1] == "void":
    #         self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
    #                                                     error=self.error_void_type,
    #                                                     first_op=token)
    #
    #     self.symbol_table.modify_last_row(kind=kind, type=self.semantic_stack[-1])
    #     self.program_block_insert(
    #         operation=":=",
    #         first_op="#0",
    #         second_op=self.symbol_table.get_last_row()[address_key],
    #     )
    #     self.semantic_stack.pop()
    #
    # # declare var
    # def darray(self):
    #     # add to symbol table
    #     self.symbol_table.modify_attributes_last_row(num_attributes=self.semantic_stack[-1])
    #     self.semantic_stack.pop()
    #
    # # start function scope
    # def sfunctions(self, token):
    #     # start of function declaration
    #     self.symbol_table.modify_kind_last_row("func")
    #     # add the row_id of function in symbol table to stack so
    #     # we can modify num attributes of this function later
    #     self.semantic_stack.append(self.symbol_table.get_id_last_row())
    #     if self.symbol_table.get_last_row()['type'] == "void":
    #         self.semantic_analyzer.pop_error()
    #     self.add_scope(token)
    #     # add the counter for parameters
    #     self.semantic_stack.append(0)
    #
    # # end function scope
    # def efunctions(self):
    #     # end of function declaration
    #     self.symbol_table.modify_attributes_row(row_id=self.semantic_stack[-2],
    #                                             num_attributes=self.semantic_stack[-1],
    #                                             arr_func=False)
    #     self.pop_last_n(2)
    #
    # # param input
    # def pinput(self):
    #     self.symbol_table.modify_kind_last_row("param")
    #     counter = self.semantic_stack.pop()
    #     counter += 1
    #     self.semantic_stack.append(counter)
    #
    # # declare array for function
    # def darray_func(self):
    #     # self.push_num("0")
    #     # self.declare_array(token)
    #
    #     self.symbol_table.modify_attributes_last_row(num_attributes=self.semantic_stack[-1])
    #     self.semantic_stack.pop()
    #
    # # declare var
    # # def dvar(self):
    #
    # # expression stmt jump break save
    # # def jp_break_save(self):
    #
    # # save if
    # # def save_if(self):
    #
    # # label repeat
    # def jp_repeat(self):
    #     # jump back to label if condition is true
    #     # also check if there were any break statements before
    #     self.num_open_repeats -= 1
    #     temp_until_condition = self.semantic_stack.pop()  # the value that until should decide to jump based on it
    #     # check breaks
    #     while len(self.semantic_stack) > 0 and self.semantic_stack[-1] == "break":
    #         self.program_block_modification(self.semantic_stack[-2], operation="JP", first_op=self.PC + 1)
    #         self.pop_last_n(2)
    #     # jump back
    #     self.program_block_insert(operation="JPF", first_op=temp_until_condition,
    #                               second_op=self.semantic_stack[-1])
    #     self.pop_last_n(1)
