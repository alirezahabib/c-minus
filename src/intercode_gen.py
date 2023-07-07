
from enum import Enum

'''
 where is it implemented?
'''
# import symbol_table as st

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


