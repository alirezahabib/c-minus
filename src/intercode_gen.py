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

# where is it implemented?
import symbol_table as st

from src.parser import Parser
from src.scanner import Scanner


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


-1
to
be
refactored
probably


class Address:
    def __init__(self, address):
        self.address = address

    def set_indirect(self):
        self.address = "@" + str(self.address)
        return self

    def __str__(self):
        return str(self.address)


class PB:
    def __init__(self):
        self.block = []
        self.line = 0
        self.last_tmp = Address(500 - 4)
        self.last_addr = Address(100 - 4)

    def get_len(self):
        return (self.block)

    def get_line(self):
        return self.line

    def add_code(self, operation, op1, op2=None, op3=None):
        self.block.append([operation, op1, op2, op3])
        self.line += 1

    def add_to_index(self, index, operation, op1, op2=None, op3=None):
        self.block.insert(index, [operation, op1, op2, op3])
        self.line += 1

    def get_line(self):
        return self.line

    def get_tmp_address(self):
        self.last_tmp += 4
        return Address(self.last_tmp.address)

    def get_current_tmp_addr(self):
        return self.last_tmp

    def update_tmp_addr(self, size):
        self.last_tmp += size

    def get_address(self):
        self.last_addr += 4
        return Address(self.last_addr.address)
    def get_temp(self):
        temp = self.last_tmp
        self.last_tmp += 4

        return temp


# main class
class CodeGenerator:
    def __init__(self, scanner: Scanner, parser: Parser):
        self.ss = SS()
        self.pb = PB()
        self.st = st.SymbolTable()
        self.loop = []
        self.scanner = scanner
        self.parser = parser
        self.break_stack = []
        # ...

    def add(self):
        op2 = self.ss.pop()
        op1 = self.ss.pop()
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("ADD", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def sub(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("SUB", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def mult(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("MUL", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def equals(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("EQ", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def less_than(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("LT", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def assign(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        -1
        to
        be
        implemented
        if op1 == "=":
            op1 = self.ss.pop()
        if is_array:
            self.pb.add_code("ASSIGN", op1, op2 + index * 4)
        else:
            self.pb.add_code("ASSIGN", op1, op2)

        self.ss.push("=")
        self.ss.push(op1)

        # ...

    def jpf(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        addr = self.ss.pop_mult(2)
        op1 = self.ss.pop()
        # -1 to be implemented
        self.pb.add_to_index(addr, "JPF", op1, self.pb.get_line(), None)

        # ...

    def jp(self):
        addr = self.ss.pop()
        # -1 to be implemented
        self.pb.add_to_index(addr, "JP", self.pb.get_line(), None, None)
        # ...

    def output(self):
        op1 = self.ss.pop()
        self.pb.add_code("PRINT", op1, None, None)

        # ...

    def routine(self, name, params):
        sem_func = getattr(self, name)
        if sem_func is None or not callable(sem_func):
            -1
            to
            be
            implemented
            return -1

        sem_func(*params)
        # ...

    def pid(self, name):
        self.ss.push(name)

    def pnum(self, value):
        self.ss.push(value)

    def save(self):
        self.ss.push(self.pb.get_line())
        self.pb.add_code(None, None)

    # def jpf(self):
    #     addr = self.ss.pop()
    #     self.pb.add_code[addr]("JPF", self.ss.pop(), self.pb.get_line(), None)

    def jpf_save(self):
        addr = self.ss.pop()
        # -1 to be implemented
        self.pb.add_to_index(addr, "JPF", self.ss.pop(), self.pb.get_line() + 1, None)
        self.pb.add_code(None, None)
        self.ss.push(self.pb.get_line())

    # -1 to be refactored
    def loop(self):
        self.loop.append(self.pb.get_line() + 1)
        self.pb.add_code(None, None)

    def until(self):
        expr = self.ss.pop()
        addr = self.ss.pop()
        self.pb.add_code("JPF", expr, addr, None)
        addr = self.pb.get_line()
        for address in self.loop:
            self.pb.add_to_index(address, "JP", addr, None, None)

    def label(self):
        self.ss.append(self.pb.get_line())

    def j_main(self):
        addr = self.ss.pop()
        if addr == 1:
            self.pb.add_to_index(addr, "JP", self.pb.get_line(), None, None)

    def ptype(self):
        self.pb.add_code("INPUT", self.ss.pop(), None, None)

    # declare id
    def did(self, token):
        # search in symbol table
        # if found in current scope raise error
        # if not found
        # add to symbol table
        # token will be the lexeme of the variable
        the_row = self.symbol_table.lookup(token, self.start_scope, False)
        if the_row is not None and the_row[type_key] == "param":
            # this means that the variable is already declared and is the function parameter,
            # and we want to redefine it
            del the_row[type_key]

        self.symbol_table.insert(token)
        if self.semantic_stack[-1] == "void":
            self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
                                                        error=self.error_void_type,
                                                        first_op=token)

        self.symbol_table.modify_last_row(kind=kind, type=self.semantic_stack[-1])
        self.program_block_insert(
            operation=":=",
            first_op="#0",
            second_op=self.symbol_table.get_last_row()[address_key],
        )
        self.semantic_stack.pop()

    # declare var
    def darray(self):
        # add to symbol table
        self.symbol_table.modify_attributes_last_row(num_attributes=self.semantic_stack[-1])
        self.semantic_stack.pop()

    # start function scope
    def sfunctions(self, token):
        # start of function declaration
        self.symbol_table.modify_kind_last_row("func")
        # add the row_id of function in symbol table to stack so
        # we can modify num attributes of this function later
        self.semantic_stack.append(self.symbol_table.get_id_last_row())
        if self.symbol_table.get_last_row()['type'] == "void":
            self.semantic_analyzer.pop_error()
        self.add_scope(token)
        # add the counter for parameters
        self.semantic_stack.append(0)

    # end function scope
    def efunctions(self):
        # end of function declaration
        self.symbol_table.modify_attributes_row(row_id=self.semantic_stack[-2],
                                                num_attributes=self.semantic_stack[-1],
                                                arr_func=False)
        self.pop_last_n(2)

    # param input
    def pinput(self):
        self.symbol_table.modify_kind_last_row("param")
        counter = self.semantic_stack.pop()
        counter += 1
        self.semantic_stack.append(counter)

    # declare array for function
    def darray_func(self):
        # self.push_num("0")
        # self.declare_array(token)

        self.symbol_table.modify_attributes_last_row(num_attributes=self.semantic_stack[-1])
        self.semantic_stack.pop()

    # declare var
    # def dvar(self):

    # expression stmt jump break save
    # def jp_break_save(self):

    # save if
    # def save_if(self):

    # label repeat
    def jp_repeat(self):
        # jump back to label if condition is true
        # also check if there were any break statements before
        self.num_open_repeats -= 1
        temp_until_condition = self.semantic_stack.pop()  # the value that until should decide to jump based on it
        # check breaks
        while len(self.semantic_stack) > 0 and self.semantic_stack[-1] == "break":
            self.program_block_modification(self.semantic_stack[-2], operation="JP", first_op=self.PC + 1)
            self.pop_last_n(2)
        # jump back
        self.program_block_insert(operation="JPF", first_op=temp_until_condition,
                                  second_op=self.semantic_stack[-1])
        self.pop_last_n(1)

    # assign
    # def assign(self):
    #
    # # array address
    # def array_address(self):

    # assign array

    '''
    we want to add appropriate action symbol to the grammar below and then define a semantic routine in the shape of
    a function for each action symbol. the grammar is as follows:
    1. Program -> Declaration-list
    2. Declaration-list -> Declaration Declaration-list | EPSILON 
    3. Declaration -> Declaration-initial Declaration-prime
    4. Declaration-initial -> Type-specifier ID
    5. Declaration-prime -> Fun-declaration-prime | Var-declaration-prime
    6. Var-declaration-prime -> ; | [ NUM ] ;
    7. Fun-declaration-prime -> ( Params ) Compound-stmt
    8. Type-specifier -> int | void
    9. Params -> int ID Param-prime Param-list | void
    10. Param-list -> , Param Param-list | EPSILON
    11. Param -> Declaration-initial Param-prime
    12. Param-prime -> [ ] | EPSILON
    13. Compound-stmt -> { Declaration-list Statement-list }
    14. Statement-list -> Statement Statement-list | EPSILON
    15. Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt
    16. Expression-stmt -> Expression ; | break ; | ;
    17. Selection-stmt -> if ( Expression ) Statement else Statement
    18. Iteration-stmt -> repeat Statement until ( Expression )
    19. Return-stmt -> return Return-stmt-prime
    20. Return-stmt-prime -> ; | Expression ;
    21. Expression -> Simple-expression-zegond | ID B
    22. B -> = Expression | [ Expression ] H | Simple-expression-prime
    23. H -> = Expression | G D C
    24. Simple-expression-zegond -> Additive-expression-zegond C
    25. Simple-expression-prime -> Additive-expression-prime C
    26. C -> Relop Additive-expression | EPSILON
    27. Relop -> < | ==
    28. Additive-expression -> Term D
    29. Additive-expression-prime -> Term-prime D
    30. Additive-expression-zegond -> Term-zegond D
    31. D -> Addop Term D | EPSILON
    32. Addop -> + | -
    33. Term -> Factor G
    34. Term-prime -> Factor-prime G
    35. Term-zegond -> Factor-zegond G
    36. G -> * Factor G | EPSILON
    37. Factor -> ( Expression ) | ID Var-call-prime | NUM
    38. Var-call-prime -> ( Args ) | Var-prime
    39. Var-prime -> [ Expression ] | EPSILON
    40. Factor-prime -> ( Args ) | EPSILON
    41. Factor-zegond -> ( Expression ) | NUM
    42. Args -> Arg-list | EPSILON
    43. Arg-list -> Expression Arg-list-prime
    44. Arg-list-prime -> , Expression Arg-list-prime | EPSILON
    '''

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
        index = self._scanner.get_symbol_index(lexeme)
        self.ss.push(index)

    def p_id(self):  # p_id
        # push address of identifier into the semantic stack
        lexeme = self._current_token[1]
        index = self._scanner.get_symbol_index(lexeme)
        address = self._scanner.symbol_table["address"][index]
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
        self._scanner.update_symbol(index,
                                    symbol_type="var",
                                    size=0,
                                    data_type=data_type,
                                    scope=len(self._scanner.scope_stack),
                                    address=self._current_data_address)
        self.pb.update_tmp_addr(4)

    def dec_array(self):  # declare_array
        # assign an address to the identifier, assign 0 to the start of the array in the program block
        # and update identifier's row in the symbol table
        # data_type = self._semantic_stack[-3]
        # index = self._semantic_stack[-2]
        # size = self._semantic_stack[-1]
        size, index, data_type = self.ss.pop_mult(3)
        self.ss.pop_out_mult(3)

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
        self._scanner.update_symbol(index,
                                    symbol_type="array",
                                    size=size,
                                    data_type=data_type,
                                    scope=len(self._scanner.scope_stack),
                                    address=self._current_data_address)
        self.pb.update_tmp_addr(4 * size)

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
        self._scanner.update_symbol(index,
                                    symbol_type="function",
                                    size=0,
                                    data_type=data_type,
                                    scope=len(self._scanner.scope_stack),
                                    address=len(self._program_block))
        '''
        depends on how scope_stack is implemented in Scanner class
        '''
        self._scanner.scope_stack.append(index + 1)
        if self._scanner.symbol_table["lexeme"][index] == "main":
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
        scope_start = self._scanner.scope_stack.pop()
        self._scanner.pop_scope(scope_start)

    # def p_type

    def break_jp(self):  # break_jp
        # add an indirect jump to the top of the break stack
        break_temp = self.break_stack[-1]
        self.pb.add_code(f"(JP, @{break_temp})")

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
        self.pb.add_to_index(line_number, f"(JPF, {condition}, {current_line_number + 1})")
        self.ss.push(self.pb.get_len())
        self.pb.add_code(None, None)

    def jp(self):  # jp
        # add a JP instruction in line number stored in semantic stack to the current line
        line_number = self.ss.pop()
        # self.pop_semantic_stack(1)

        current_line_number = self.pb.get_len()
        self.pb.add_to_index(line_number, f"(JP, {current_line_number},\t,\t)")

    def assign(self):  # assign
        # add an assign instruction
        # source_var = self._semantic_stack[-1]
        # dest_var = self._semantic_stack[-2]
        source_var, dest_var = self.ss.pop_mult(2)
        # self.pop_semantic_stack(1)

        self.pb.add_code(f"(ASSIGN, {source_var}, {dest_var},\t)")

    def array_access(self):  # array_access
        # calculate selected array element address and save result temp in semantic stack
        # array_index = self._semantic_stack[-1]
        # array_base_address = self._semantic_stack[-2]
        array_index, array_base_address = self.ss.pop_mult(2)
        # self.pop_semantic_stack(2)

        temp1 = self.pb.get_temp()
        temp2 = self.pb.get_temp()
        self.pb.add_code(f"(MULT, #4, {array_index}, {temp1})")
        self.pb.add_code(f"(ADD, {temp1}, #{array_base_address}, {temp2})")
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
        self.pb.add_code(f"({assembly_operation}, {operand_1}, {operand_2}, {dest})")
        self.ss.push(dest)

    def p_num(self):  # p_num
        # push number into the semantic stack
        number = int(self._current_token[1])
        self.ss.push(number)

    def p_num_tmp(self):  # p_num_temp
        # push #number into the semantic stack
        number = int(self._current_token[1])
        self.ss.push(f"#{number}")

    # push type / get_id_type / p_input
    def p_type(self):  # p_type
        # push type into the semantic stack
        data_type = self._current_token[1]
        self.ss.push(data_type)

    def break_jp(self):  # break_jp
        # add an indirect jump to the top of the break stack
        break_temp = self.break_stack[-1]
        self.pb.add_code(f"(JP, @{break_temp},\t,\t)")

    def save_break_tmp(self):  # save_break_temp
        # save a temp in break stack
        dest = self.pb.get_temp()
        self.break_stack.append(dest)

    def label(self):
        self.ss.append(self.pb.get_line())

    def start_loop(self):

    def repeat(self):

    def end_loop(self):

    # declare id
    # it may not be needed actually
    def did(self, token):
        # search in symbol table
        # if found in current scope raise error
        # if not found
        # add to symbol table
        # token will be the lexeme of the variable
        the_row = self.symbol_table.lookup(token, self.start_scope, False)
        if the_row is not None and the_row[type_key] == "param":
            # this means that the variable is already declared and is the function parameter,
            # and we want to redefine it
            del the_row[type_key]

        self.symbol_table.insert(token)
        if self.semantic_stack[-1] == "void":
            self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
                                                        error=self.error_void_type,
                                                        first_op=token)

        self.symbol_table.modify_last_row(kind=kind, type=self.semantic_stack[-1])
        self.program_block_insert(
            operation=":=",
            first_op="#0",
            second_op=self.symbol_table.get_last_row()[address_key],
        )
        self.semantic_stack.pop()

    def mult(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("MUL", op1, op2, tmp)
        self.ss.push(tmp)

# class CodeGenerator:
#
#     def __init__(self, symbol_table: SymbolTable, heap: HeapManager):
#         self.symbol_table = symbol_table
#         self.semantic_stack = []
#         self.PB = []
#         # pc shows the next line of program block to be filled (i in slides)
#         self.PC = 0
#         self.heap_manager = heap
#         self.current_line = 0
#         # used to say that the function doesn't take any more arguments.
#         # in end_call it will go back to False but in arg_input it may go True if we have error_num_args
#         self.no_more_arg_input = False
#         # for semantic stack
#         # todo must be changed in future because lookup must search by scope - can be removed now.
#         #  we don't need start_ind in lookup function any more
#         self.start_scope = 0
#
#         self.num_open_repeats = 0
#
#         self.semantic_analyzer = SemanticAnalyzer()
#         # errors
#         self.error_scoping = "#{0}: Semantic Error! '{1}' is not defined.{2}{3}{4}"
#         self.error_void_type = "#{0}: Semantic Error! Illegal type of void for '{1}'.{2}{3}{4}"
#         self.error_type_missmatch = "#{0}: Semantic Error! Type mismatch in operands, Got {1} instead of {2}.{3}{4}"
#         self.error_break = "#{0}: Semantic Error! No 'repeat ... until' found for 'break'."
#         self.error_param_type_missmatch = "#{0}: Semantic Error! Mismatch in type of argument {1} of '{2}'. Expected '{3}' but got '{4}' instead."
#         self.error_num_args = "#{0}: Semantic Error! Mismatch in numbers of arguments of '{1}'.{2}{3}{4}"
#
#     def code_gen(self, action_symbol, token, line_number):
#         self.current_line = line_number
#         if self.no_more_arg_input and action_symbol != "#end_call":
#             return
#
#         action_symbol = action_symbol[1:]
#         method = getattr(self, action_symbol, None)
#         if method:
#             method(token)
#
#
#     def pop_last_n(self, n):
#         # pop last n elements from semantic stack
#         for _ in range(n):
#             self.semantic_stack.pop()
#
#     @staticmethod
#     def get_pb_line(line_index, operation, first_op=" ", second_op=" ", third_op=" "):
#         return f'{line_index}\t({operation}, {first_op}, {second_op}, {third_op} )'
#
#     def program_block_insert(self, operation, first_op=" ", second_op=" ", third_op=" "):
#         # insert to program block
#         operation = self.get_operation_by_symbol(operation)
#         self.PB.append(self.get_pb_line(len(self.PB), operation, first_op, second_op, third_op))
#         self.PC += 1
#
#     def program_block_modification(self, index, operation, first_op="", second_op="", third_op=""):
#         # modify a passed line of program block and add the code
#         operation = self.get_operation_by_symbol(operation)
#         self.PB[index] = self.get_pb_line(index, operation, first_op, second_op, third_op)
#
#     def program_block_insert_empty(self):
#         self.PB.append("")
#         self.PC += 1
#
#     @staticmethod
#     def get_operation_by_symbol(symbol):
#         if symbol == '+':
#             return "ADD"
#         elif symbol == '-':
#             return "SUB"
#         elif symbol == '*':
#             return "MULT"
#         elif symbol == "==":
#             return "EQ"
#         elif symbol == "<":
#             return "LT"
#         elif symbol == ":=":
#             return "ASSIGN"
#         else:
#             return symbol.upper()
#
#     def add_scope(self, token):
#         # add scope to scope stack
#         self.symbol_table.add_scope()
#
#     def end_scope(self, token=""):
#         self.symbol_table.end_scope()
#
#     def return_command(self, token):
#         self.semantic_stack.pop()
#
#     def no_return(self, token):
#         self.semantic_stack.append(0)
#
#     def start_func(self, token):
#         # start of function declaration
#         self.symbol_table.modify_kind_last_row("func")
#         # add the row_id of function in symbol table to stack so
#         # we can modify num attributes of this function later
#         self.semantic_stack.append(self.symbol_table.get_id_last_row())
#         if self.symbol_table.get_last_row()['type'] == "void":
#             self.semantic_analyzer.pop_error()
#         self.add_scope(token)
#         # add the counter for parameters
#         self.semantic_stack.append(0)
#
#     def add_param(self, token):
#         self.symbol_table.modify_kind_last_row("param")
#         counter = self.semantic_stack.pop()
#         counter += 1
#         self.semantic_stack.append(counter)
#
#     def declare_entry_array(self, token):
#         self.push_num("0")
#         self.declare_array(token)
#
#     def end_func_params(self, token):
#         # end of function declaration
#         self.symbol_table.modify_attributes_row(row_id=self.semantic_stack[-2],
#                                                 num_attributes=self.semantic_stack[-1],
#                                                 arr_func=False)
#         self.pop_last_n(2)
#
#     def start_call(self, token):
#         # start of function call
#         # row_id = self.symbol_table.lookup(self.semantic_stack[-1])['id']
#         row_id = self.symbol_table.get_row_id_by_address(self.semantic_stack[-1])
#         self.semantic_stack.pop()
#         num_parameters = self.symbol_table.get_row_by_id(row_id)[attributes_key]
#         # add parameter types to stack in the form of tuple (type, is_array)
#         for i in range(num_parameters, 0, -1):
#             temp_address_param = self.symbol_table.get_row_by_id(row_id + i)['address']
#             # type_param = self.get_operand_type(temp_address_param)
#             self.semantic_stack.append(temp_address_param)
#
#         # add the number of parameters to stack
#         self.semantic_stack.append(num_parameters)
#         # add a counter for arguments - at first it is equal to number of parameters
#         self.semantic_stack.append(num_parameters)
#         # add name of function to stack
#         self.semantic_stack.append(self.symbol_table.get_row_by_id(row_id)['lexeme'])
#
#     def arg_input(self, token):
#         # take input argument for function call
#         if not self.no_more_arg_input:
#             arg = self.semantic_stack.pop()
#             type_arg = self.get_operand_type(arg)
#             name_func = self.semantic_stack.pop()
#             counter_args = self.semantic_stack.pop()
#             counter_args -= 1
#             if counter_args == 0 and token != ")":
#                 self.no_more_arg_input = True
#                 self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#                                                             error=self.error_num_args,
#                                                             first_op=name_func
#                                                             )
#
#             num_parameters = self.semantic_stack.pop()
#             temp_param = self.semantic_stack.pop()
#             type_param = self.get_operand_type(temp_param)
#             if type_arg != type_param:
#                 self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#                                                             error=self.error_param_type_missmatch,
#                                                             first_op=num_parameters - counter_args,
#                                                             second_op=name_func,
#                                                             third_op=self.get_type_name(type_param),
#                                                             fourth_op=self.get_type_name(type_arg)
#                                                             )
#             else:
#                 if name_func == "output":
#                     self.semantic_stack.append(arg)
#                     self.print("nothing")
#
#             self.semantic_stack.append(num_parameters)
#             self.semantic_stack.append(counter_args)
#             self.semantic_stack.append(name_func)
#
#     def end_call(self, token):
#         # end of function call
#         self.no_more_arg_input = False
#         name_func = self.semantic_stack.pop()
#         counter_args = self.semantic_stack.pop()
#         num_parameters = self.semantic_stack.pop()
#         if counter_args != 0:
#             self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#                                                         error=self.error_num_args,
#                                                         first_op=name_func
#                                                         )
#             self.pop_last_n(counter_args)
#
#         # todo: this must be replaced later. In the current way we find out if we want the output of function and
#         # push a dummy number
#         if token in ["=", "+", "*", "-", "==", "<", ")"] or (
#                 len(self.semantic_stack) > 0 and self.semantic_stack[-1] in ["=", "+", "*", "-", "==", "<"]):
#             self.push_num("20")
#
#     def get_type_name(self, tuple_type):
#         if tuple_type[1]:
#             return "array"
#         else:
#             return tuple_type[0]
#
#     def push_type(self, token):
#         # push type to stack
#         if token == "int" or token == "void":
#             self.semantic_stack.append(token)
#         else:
#             raise Exception("type not supported")
#
#     def push_num(self, token):
#         # push number to stack
#         self.semantic_stack.append(str("#" + token.strip()))
#
#     def print(self, token):
#         self.program_block_insert(operation="print", first_op=self.semantic_stack[-1])
#         self.semantic_stack.pop()
#
#     def break_check(self, token):
#         # check if we are in a repeat until statement
#         if self.num_open_repeats == 0:
#             self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#                                                         error=self.error_break)
#         # push PC counter so that it can be filled in the #until action symbol to jump out
#         else:
#             self.semantic_stack.append(self.PC)
#             self.program_block_insert_empty()
#             # self.semantic_stack.insert(1, "break")
#             self.semantic_stack.append("break")
#
#     def declare_id(self, token, kind="var"):
#         # search in symbol table
#         # if found in current scope raise error
#         # if not found
#         # add to symbol table
#         # token will be the lexeme of the variable
#         the_row = self.symbol_table.lookup(token, self.start_scope, False)
#         if the_row is not None and the_row[type_key] == "param":
#             # this means that the variable is already declared and is the function parameter,
#             # and we want to redefine it
#             del the_row[type_key]
#
#         self.symbol_table.insert(token)
#         if self.semantic_stack[-1] == "void":
#             self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#                                                         error=self.error_void_type,
#                                                         first_op=token)
#
#         self.symbol_table.modify_last_row(kind=kind, type=self.semantic_stack[-1])
#         self.program_block_insert(
#             operation=":=",
#             first_op="#0",
#             second_op=self.symbol_table.get_last_row()[address_key],
#         )
#         self.semantic_stack.pop()
#
#     def declare_array(self, token):
#         # add to symbol table
#         self.symbol_table.modify_attributes_last_row(num_attributes=self.semantic_stack[-1])
#         self.semantic_stack.pop()
#
#     def assign(self, token):
#         # stack:
#         # -1: source temp
#         # -2: =
#         # -3: destination temp
#         answer = self.semantic_stack[-3]
#         self.program_block_insert(operation=":=", first_op=self.semantic_stack[-1], second_op=self.semantic_stack[-3])
#         self.pop_last_n(3)
#         if len(self.semantic_stack) > 0 and self.semantic_stack[-1] == "=":
#             # means there was a nested assignment and we should push the result to the stack
#             self.semantic_stack.append(answer)
#
#     def label(self, token):
#         # declare where to jump back after until in repeat-until
#         self.semantic_stack.append(self.PC)
#
#         self.num_open_repeats += 1
#
#     def until(self, token):
#         # jump back to label if condition is true
#         # also check if there were any break statements before
#         self.num_open_repeats -= 1
#         temp_until_condition = self.semantic_stack.pop()  # the value that until should decide to jump based on it
#         # check breaks
#         while len(self.semantic_stack) > 0 and self.semantic_stack[-1] == "break":
#             self.program_block_modification(self.semantic_stack[-2], operation="JP", first_op=self.PC + 1)
#             self.pop_last_n(2)
#         # jump back
#         self.program_block_insert(operation="JPF", first_op=temp_until_condition,
#                                   second_op=self.semantic_stack[-1])
#         self.pop_last_n(1)
#
#     def array_calc(self, token):
#         # calculate the address of the index of the array
#         # the index is on top of the stack and the address of array is the second element
#         # pop those two and push the address of calculated address to the stack
#         array_address = self.semantic_stack[-2]
#         array_type, _ = self.get_operand_type(array_address)
#         temp = self.heap_manager.get_temp(array_type)
#         self.program_block_insert(
#             operation="*",
#             first_op=self.semantic_stack[-1],
#             second_op="#" + str(self.heap_manager.get_length_by_type(array_type)),
#             third_op=temp
#         )
#         self.program_block_insert(
#             operation="+",
#             first_op=str('#' + str(array_address)),
#             second_op=temp,
#             third_op=temp
#         )
#         self.pop_last_n(2)
#         self.semantic_stack.append(str('@' + str(temp)))
#
#     def push_op(self, token):
#         # push operator to stack
#         self.semantic_stack.append(token)
#
#     def do_op(self, token):
#         # do the operation
#         # pop the operator and operands from the stack
#         # push the result to the stack
#         op = self.semantic_stack[-2]
#         first_op = self.semantic_stack[-3]
#         second_op = self.semantic_stack[-1]
#         self.pop_last_n(3)
#         # semantic: check operands types
#         operands_type, is_array1 = self.get_operand_type(first_op)
#         _, is_array2 = self.get_operand_type(second_op)
#         if is_array1 or is_array2:
#             self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#                                                         error=self.error_type_missmatch,
#                                                         first_op="array",
#                                                         second_op="int")
#         temp = self.heap_manager.get_temp(operands_type)
#         self.program_block_insert(operation=op, first_op=first_op, second_op=second_op, third_op=temp)
#         self.semantic_stack.append(temp)
#
#     def jpf_save(self, token):
#         # jpf
#         index_before_break = -1
#         # remove breaks
#         while self.semantic_stack[index_before_break] == "break":
#             index_before_break -= 2
#         breaks = []
#         if index_before_break != -1:
#             breaks = self.semantic_stack[index_before_break + 1:]
#             self.semantic_stack = self.semantic_stack[:index_before_break + 1]
#
#         self.program_block_modification(
#             index=self.semantic_stack[-1],
#             operation="JPF",
#             first_op=self.semantic_stack[-2],
#             second_op=str(self.PC + 1)
#         )
#         self.pop_last_n(2)
#         # then save current pc
#         self.semantic_stack.append(self.PC)
#         self.program_block_insert_empty()
#         # add back breaks
#         self.semantic_stack.extend(breaks)
#
#     def save(self, toke):
#         # save the current PC
#         self.semantic_stack.append(self.PC)
#         self.program_block_insert_empty()
#
#     def jp(self, token):
#         # jump to a label
#
#         index_before_break = -1
#         while self.semantic_stack[index_before_break] == "break":
#             index_before_break -= 2
#         breaks = []
#         # remove breaks
#         if index_before_break != -1:
#             breaks = self.semantic_stack[index_before_break + 1:]
#             self.semantic_stack = self.semantic_stack[:index_before_break + 1]
#
#         self.program_block_modification(
#             index=self.semantic_stack[-1],
#             operation="JP",
#             first_op=str(self.PC)
#         )
#         self.pop_last_n(1)
#
#         # add back breaks
#         self.semantic_stack.extend(breaks)
#
#     def id(self, token):
#         # push the address of current token
#         # todo semantic: check if variable is declared in our scope
#         # todo how should we handle scope?
#         if token == "a":
#             pass
#         row = self.symbol_table.lookup(token, self.start_scope)
#         if row is None:
#             self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#                                                         error=self.error_scoping,
#                                                         first_op=token)
#             # add a dummy address of type int
#             self.semantic_stack.append(self.heap_manager.get_temp("int", 1))
#
#         else:
#             address = row[address_key]
#             self.semantic_stack.append(address)
#
#     def push_eq(self, token):
#         # in case of assignment, push = to stack
#         # used for finding out if there is a nested assignment
#         self.semantic_stack.append("=")
#
#     def get_operand_type(self, operand):
#         is_array = False
#         if str(operand).startswith("#"):
#             return "int", is_array
#         elif str(operand).startswith("@"):
#             operand = operand[1:]
#         type = self.heap_manager.get_type_by_address(int(operand))
#         if type.endswith("-arr"):
#             type = type[:-4]
#             is_array = True
#
#         return type, is_array
#
#     def print_pb(self):
#         print("\n--------------Program Block---------------")
#         for row in self.PB:
#             print(row)
#
#     def write_pb_to_file(self, output_file, semantic_file):
#         if self.semantic_analyzer.num_semantic_errors > 0:
#             output_file.write("The output code has not been generated.")
#             for error in self.semantic_analyzer.all_errors:
#                 semantic_file.write(error + "\n")
#
#             return
#
#         for row in self.PB:
#             output_file.write(str(row) + "\n")
