import json
from typing import Optional, List, Union, Set, Dict, Tuple

from anytree import Node, RenderTree

import grammar
import ctoken
from scanner import Scanner
# import intercode_gen
# from intercode_gen import CodeGenerator


# oh oh
from enum import Enum

'''
 where is it implemented?
'''
# import symbol_table as st

# from parser import Parser
# from scanner import Scanner
from scanner import KEYWORD, SYMBOL
from symbol_table import Address
from symbol_table import Symbol_Table

# it is not used actually
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
    instance : Optional['PB'] = None
    @staticmethod
    def get_instance():
        if PB.instance == None:
            PB.instance = PB()
        return PB.instance
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
        return self.address.last_tmp

    # def get_current_tmp_addr(self):
    #     return self.last_tmp

    def update_tmp_addr(self, size):
        self.address.last_tmp += size

    def get_address(self):
        self.address.last_addr += 1
        self.address.all_addresses.append(self.address.last_addr)
        return self.address.last_addr

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
        return self.address.last_tmp

    def get_next_addr(self,addr):
        return self.address.all_addresses[self.address.all_addresses.index(addr)+1]

    def get_type(self, addr):
        next_addr = self.get_next_addr(addr)
        if next_addr - addr == 4:
            return "int"
        elif next_addr - addr == 1:
            return "void"

    def finalize(self):
        for j in range(len(self.block)):
            row = self.block[j]
            print(row)
            for k in range(len(row)):
                if row(k) == None:
                    row[k] = "\t"
            if row(0) == '+' or row(0) == '-' or row(0) == '*' or row(0) == '<' or row(0) == '==' or row(0) == ':=':
                    row[0] = self.modify(j,row[0],row[1],row[2],row[3])

        for l in range(len(self.block)):
            self.block[l] = f"{self.block[l][0], self.block[l][1], self.block[l][2], self.block[l][3]}"

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
    def __init__(self, scanner: Scanner): #, address : Address):
        self.ss = SS()
        self.address = Address.get_instance()
        self.pb = PB.get_instance()
        # self.st = st.SymbolTable()
        self.loop = []
        self.scanner = scanner
        # self.parser = Parser.get_instance(self.scanner)
        # self.parser = Parser(self.scanner)
        self.break_stack = []

        self.symbol_table = self.scanner.symbol_table
        self.code_gen_st = Symbol_Table.get_instance()
        self.curr_repeats = 0
        # self.get_curr_input()

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


    # dfdlskhja
    # def get_curr_input(self):
    #     self._current_token = self.parser.get_next_token()
    #     # print(self._current_token)
    #     # print(self._current_token[0])
    #     # print(self._current_token[1])
    #     # print(self._current_token[0].type)
    #     # self._current_token = self.parsre.get_current_token()[0]
    #     toCheck = KEYWORD + SYMBOL + "$"
    #     if self._current_token == None:
    #         return
    #     if self._current_token[0].type in toCheck:
    #         self._current_input = self._current_token[1]
    #     else:
    #         self._current_input = self._current_token[0]

    def call_main(self):
        main_function_row = self.scanner.symbol_table.code_gen_st.lookup('main')
        self.pb.add_code(
            ":=",
            "#" + str(self.pb.get_line() + 2),
            #str(main_function_row["return_address"])
            str(0)
        )
        # now jump to the invocation address of main
        self.pb.add_code(
            "JP",
            # str(main_function_row["invocation_address"])
            "1"
        )
        # self.pb.finalize()

    def declare_id(self):
        self.code_gen_st.modify_last_row(kind="var", type=self.ss.top())
        self.pb.add_code(
            ":=",
            "#0",
            self.code_gen_st.get_last_row()["address"],
        )
        self.ss.pop()

    def dec_var(self):# declare_var
        # assign an address to the identifier, assign 0 to the variable in the program block
        # and update identifier's row in the symbol table
        data_type = self.ss.stack[-2]
        index = self.ss.stack[-1]
        self.ss.pop_mult(2)

        self.pb.add_code(f"(ASSIGN, #0, {self.pb.get_tmp_address()},\t)")
        self.scanner.update_symbol(index,
                                    symbol_type="var",
                                    size=0,
                                    data_type=data_type,
                                    scope=len(self.scanner.scope_stack),
                                    address=self.pb.get_current_tmp_addr())
        # self.pb.last_tmp += 4

    def p_id_index(self,token):  # p_id_index it is either p_id or declare_id
        # push index of identifier into the semantic stack
        lexeme = token[1]
        index = self.scanner.get_symbol_index(lexeme)
        self.ss.push(index)

    def end_function(self):  # end_function (probably to replace end_func)
        # deletes the current scope
        scope_start = self.scanner.scope_stack.pop()
        self.scanner.pop_scope(scope_start)

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
        array_addr = array_row["address"]
        entries_type = array_row["type"]
        array_start_address = self.pb.get_tmp_address_by_size(entries_type, array_size)
        self.pb.add_code(
            ":=",
            "#" + str(array_start_address),
            array_addr
        )

    def label(self):
        # declare where to jump back after until in repeat-until
        self.ss.push(self.pb.get_line())

        self.curr_repeats += 1

    def until(self):
        self.curr_repeats -= 1
        condition = self.ss.pop()
        while len(self.ss.stack) > 0 and self.ss.top() == "break":  # [-1] == "break":
            self.pb.modify(self.ss.stack[-2], "JP", self.pb.get_line() + 1)
            self.ss.pop_mult(2)
        self.pb.add_code("JPF", condition,
                         self.ss.top())
        self.ss.pop()

    def push_eq(self):
        self.ss.push("=")

    def start_call(self):
        function_row_id = self.code_gen_st.get_row_id_by_address(self.ss.top())
        self.ss.pop()
        num_parameters = self.code_gen_st.get_row_by_id(function_row_id)["attributes"]
        for i in range(num_parameters, 0, -1):
            temp_addr_param = self.code_gen_st.get_row_by_id(function_row_id + i)["address"]
            self.ss.push(temp_addr_param)
        self.ss.push(num_parameters)
        self.ss.push(num_parameters)
        self.ss.push(self.code_gen_st.get_row_by_id(function_row_id)["lexeme"])

    def end_call(self):
        self.no_more_input = False
        function_name = self.ss.pop()
        counter_args = self.ss.pop()
        # num_parameters = self.ss.pop()
        # if counter_args != 0:
        #     self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
        #                                                 error=self.error_num_args,
        #                                                 first_op=name_func
        #                                                 )
        #     self.pop_last_n(counter_args)

        st_function_row = self.code_gen_st.lookup(function_name)
        index = st_function_row['id']
        if "invocation_address" not in st_function_row or "return_address" not in st_function_row:
            # print("error in function declaration")
            return
        # update the return address temp of function (we want the function to return here after invocation)
        return_address_temp = st_function_row["return_address"]
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
            st_function_row["invocation_address"]
        )
        if st_function_row["type"] != "void":
            returnee_copy = self.pb.get_tmp_address(1, st_function_row["type"])
            self.pb.add_code(
                ":=",
                st_function_row["return_value"],
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
        if not self.no_more_input:
            arg = self.ss.pop()
            type_arg = self.get_operand_type(arg)
            name_func = self.ss.pop()
            counter_args = self.ss.pop()
            counter_args -= 1
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
    # def p_type(self,token):
    #     # p_type
    #     # push type into the semantic stack
    #     data_type = token.value
    #     self.ss.push(data_type)

    def p_id_index(self, token: ctoken.Token): # p_id_index
        # push index of identifier into the semantic stack
        lexeme = token.value
        index = self.scanner.get_symbol_index(lexeme)
        self.ss.push(index)
    def p_id(self, token):  # p_id
        # push address of identifier into the semantic stack
        self.p_id_index(token)
        lexeme = token.value
        index = self.scanner.get_symbol_index(lexeme)
        address = self.scanner.symbol_table["address"][index]
        self.ss.push(address)
    def p_type(self, token):  # p_type
        # push type into the semantic stack
        data_type = token.value
        self.ss.push(data_type)

    '''
    self._scanner must become the scanner used in Parser
    if it is change all repetitions of it to self.scanner
    '''

    # def p_id_index(self,token):  # p_id_index
    #     # push index of identifier into the semantic stack
    #     lex = token[1]
    #     ind = self.scanner.get_symbol_index(lex)
    #     self.ss.push(ind)

    # def p_id(self,token):  # p_id
    #     lexeme = token[1]
    #     index = self.scanner.get_symbol_index(lexeme)
    #     address = self.scanner.symbol_table.symbol_table["address"][index]
    #     self.ss.push(address)

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

    def dec_func(self):  # declare_func
        # update identifier's row in the symbol table, initialize next scope
        # and if function is "main" add a jump to the start of function
        print("THIS IS SEMANTIC STACK",self.ss.stack)
        data_type = self.ss.stack[-2]
        index = self.ss.stack[-1]
        # index, data_type = self.ss.pop_mult(2)
        # self.ss.pop_out_mult(2)
        self.ss.pop_out()
        self.ss.pop_out()
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

    def p_num(self, token):  # p_num
        # push number into the semantic stack
        number = int(token[1])
        self.ss.push(number)

    def p_num_tmp(self,token):  # p_num_temp
        # push #number into the semantic stack
        number = int(token[1])
        self.ss.push(f"#{number}")

    def save_break_tmp(self):  # save_break_temp
        # save a temp in break stack
        dest = self.pb.get_temp()
        self.break_stack.append(dest)

    def p_zero(self):
        self.ss.push("0")

    def mult(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("MUL", op1, op2, tmp)
        self.ss.push(tmp)

# oh oh oh

# class Parser:
#
#     instance : Optional['Parser'] = None
#     @staticmethod
#     def get_instance(scanner, code_generator):
#         if Parser.instance is None:
#             Parser.instance = Parser(scanner, code_generator)
#         return Parser.instance
#
#     _accept: str = "accept"
#     _shift: str = "shift"
#     _reduce: str = "reduce"
#     _goto: str = "goto"
#
#     def __init__(self, scanner: Scanner, code_generator: CodeGenerator):
#         self.current_token = None
#         self.current_value = None
#         self.scanner = scanner
#         self.syntax_errors = []  # [(line_number, error), ]
#         self.transition_table = {}
#         self.root = None
#         self.create_transition_table()
#         self.code_generator = code_generator
#
#         # self._parse_stack: List[Union[str, Node]] = ["0"]
#         # self._update_current_token()
#         # self._read_table()
#
#     def get_current_token(self):
#         return self.current_token
#
#     def create_transition_table(self):
#         for non_terminal in grammar.non_terminals:
#             for terminal in grammar.terminals + ['$'] + grammar.action_symbols:
#                 if terminal in grammar.action_symbols:
#                     self.transition_table[(non_terminal, terminal)] = [terminal]
#                 else:
#                     self.transition_table[(non_terminal, terminal)] = self.find_production_rule(non_terminal, terminal)
#
#     def find_production_rule(self, non_terminal, terminal):
#         for rule in grammar.rules[non_terminal]:
#             # print("this is non terminal" , non_terminal)
#             # print("this is grammar rules", grammar.rules[non_terminal])
#             # print("this is rule:", rule)
#             # print("this is terminal", terminal)
#             # print(rule, self.find_first(rule))
#             # rule_prime = []
#             # for st in rule:
#             #     if st[0] != '#':
#             #         rule_prime.append(st)
#             rule_prime = rule
#             # rule_prime = rule.remove()
#             # if rule[0] == 'epsilon':
#             if rule_prime[0] == 'epsilon':
#                 return rule
#             if rule_prime[0] in grammar.terminals:
#                 if rule_prime[0] == terminal:
#                     return rule
#             # to handle action symbols
#             # elif rule[0].startswith('#'):
#             #     print("find_production_rule - action symbol")
#             #     return rule
#             elif terminal in self.find_first(rule_prime):
#                 return rule
#         return None
#
#     @staticmethod
#     def find_first(rule):
#         first = []
#         for t in rule:
#             if t in grammar.terminals + ['$']:
#                 first.append(t)
#                 break
#             if t == 'epsilon':
#                 continue
#             if t[0] == '#':
#                 print("find_first - action symbol")
#                 return first.append(t)
#             first.extend(grammar.first[t])
#             if 'epsilon' not in grammar.first[t]:
#                 break
#         return first
#
#     def get_next_token(self):
#         ignore = [ctoken.WHITESPACE, ctoken.COMMENT]
#         while True:
#             next_token = self.scanner.get_next_token()
#             if next_token.type not in ignore:
#                 break
#
#         parse_value = next_token.value
#         if next_token.type == ctoken.EOF:
#             parse_value = '$'
#         elif next_token.type == ctoken.ID:
#             parse_value = 'ID'
#             # if not self.scanner.symbol_table.exists(next_token.value):
#             #     self.scanner.symbol_table.append({"index": len(self.scanner.symbol_table)+1, "name": next_token.value, "type": "ID"})
#         elif next_token.type == ctoken.NUM:
#             parse_value = 'NUM'
#         return next_token, parse_value
#
#     # def _read_table(self):
#     #     """Initializes terminals, non_terminals, first_sets, follow_sets, grammar and parse_table."""
#     #     with open("table.json", mode="r") as table_file:
#     #         table: dict = json.load(table_file)
#     #
#     #     # set of grammars terminals
#     #     self._terminals: Set[str] = set(table["terminals"])
#     #     # set of grammars non-terminals
#     #     self._non_terminals: Set[str] = set(table["non_terminals"])
#     #     # first and follow sets of non-terminals
#     #     self._first_sets: Dict[str, Set[str]] = dict(zip(table["first"].keys(), map(set, table["first"].values())))
#     #     self._follow_sets: Dict[str, Set[str]] = dict(zip(table["follow"].keys(), map(set, table["follow"].values())))
#     #     # grammar's productions
#     #     self._grammar: Dict[str, List[str]] = table["grammar"]
#     #     # SLR parse table
#     #     self._parse_table: Dict[str, Dict[str, Tuple[str, str]]] = dict(
#     #         zip(table["parse_table"].keys(), map(lambda row: dict(
#     #             zip(row.keys(), map(lambda entry: tuple(entry.split("_")), row.values()))
#     #         ), table["parse_table"].values()))
#     #     )
#
#
#     # def run(self):
#     #     """Parses the input. Return True if UNEXPECTED_EOF"""
#     #     self.code_generator.ss.push(len(self.code_generator.pb.block))
#     #     self.code_generator.pb.add_code(None,None)
#     #     while True:
#     #         # get action from parse_table
#     #         last_state = self._parse_stack[-1]
#     #         try:
#     #             action = self._parse_table[last_state].get(self._current_input)
#     #         except KeyError:
#     #             # invalid state
#     #             raise Exception(f"State \"{last_state}\" does not exist.")
#     #         if action is not None:
#     #             # perform the action
#     #             if action[0] == self._accept:
#     #                 # accept
#     #                 break
#     #             elif action[0] == self._shift:
#     #                 # push current_token and shift_state into the stack
#     #                 shift_state = action[1]
#     #                 self._parse_stack.append(Node(f"({self._current_token[0]}, {self._current_token[1]})"))
#     #                 self._parse_stack.append(shift_state)
#     #
#     #                 # get next token
#     #                 self._update_current_token()
#     #             elif action[0] == self._reduce:
#     #                 # pop rhs of the production from the stack and update parse tree
#     #                 production_number = action[1]
#     #                 self.generate_code(int(production_number))
#     #                 production = self._grammar[production_number]
#     #                 production_lhs = production[0]
#     #                 production_rhs_count = self._get_rhs_count(production)
#     #                 production_lhs_node: Node = Node(production_lhs)
#     #                 if production_rhs_count == 0:
#     #                     node = Node("epsilon")
#     #                     node.parent = production_lhs_node
#     #                 else:
#     #                     popped_nodes = []
#     #                     for _ in range(production_rhs_count):
#     #                         self._parse_stack.pop()
#     #                         popped_nodes.append(self._parse_stack.pop())
#     #                     for node in popped_nodes[::-1]:
#     #                         node.parent = production_lhs_node
#     #
#     #                 # push lhs of the production and goto_state into the stack
#     #                 last_state = self._parse_stack[-1]
#     #                 try:
#     #                     goto_state = self._parse_table[last_state][production_lhs][1]
#     #                 except KeyError:
#     #                     # problem in parse_table
#     #                     raise Exception(f"Goto[{last_state}, {production_lhs}] is empty.")
#     #                 self._parse_stack.append(production_lhs_node)
#     #                 self._parse_stack.append(goto_state)
#     #             else:
#     #                 # problem in parse_table
#     #                 raise Exception(f"Unknown action: {action}.")
#     #         else:
#     #             if self.handle_error():
#     #                 # failure if UNEXPECTED_EOF
#     #                 self._failure = True
#     #                 break
#     #
#     # def handle_error(self) -> bool:
#     #     """Handles syntax errors. Return True if error is UNEXPECTED_EOF"""
#     #     # discard the first input
#     #     self._syntax_errors.append(Error(ErrorType.ILLEGAL_TOKEN, self._current_token[1], self._scanner.line_number))
#     #     self._update_current_token()
#     #
#     #     # pop from stack until state has non-empty goto cell
#     #     while True:
#     #         state = self._parse_stack[-1]
#     #         goto_and_actions_of_current_state = self._parse_table[state].values()
#     #         # break if the current state has a goto cell
#     #         if any(map(lambda table_cell: table_cell[0] == self._goto,
#     #                    goto_and_actions_of_current_state)):
#     #             break
#     #         discarded_state, discarded_node = self._parse_stack.pop(), self._parse_stack.pop()
#     #         self._syntax_errors.append(Error(ErrorType.STACK_CORRECTION, discarded_node, self._scanner.line_number))
#     #
#     #     goto_keys = self._get_goto_non_terminals(state)
#     #     # discard input, while input not in any follow(non_terminal)
#     #     selected_non_terminal = None
#     #     while True:
#     #         for non_terminal in goto_keys:
#     #             if self._current_input in self._follow_sets[non_terminal]:
#     #                 selected_non_terminal = non_terminal
#     #                 break
#     #         if selected_non_terminal is None:
#     #             if self._current_input == Scanner.EOF_symbol:
#     #                 # input is EOF, halt parser
#     #                 self._syntax_errors.append(Error(ErrorType.UNEXPECTED_EOF, "", self._scanner.line_number))
#     #                 return True
#     #             else:
#     #                 # discard input
#     #                 self._syntax_errors.append(
#     #                     Error(ErrorType.TOKEN_DISCARDED, self._current_token[1], self._scanner.line_number))
#     #                 self._update_current_token()
#     #         else:
#     #             # input is in follow(non_terminal)
#     #             break
#     #     self._parse_stack.append(Node(selected_non_terminal))
#     #     self._parse_stack.append(self._parse_table[state][selected_non_terminal][1])
#     #     self._syntax_errors.append(
#     #         Error(ErrorType.MISSING_NON_TERMINAL, selected_non_terminal, self._scanner.line_number))
#     #     return False
#     #
#     # def save_parse_tree(self):
#     #     """Writes parse tree in parse_tree.txt."""
#     #     # empty file if failure
#     #     if self._failure:
#     #         with open("parse_tree.txt", mode='w') as parse_tree_file:
#     #             parse_tree_file.write("")
#     #             return
#     #
#     #     root = self._parse_stack[1]
#     #     # add EOF node
#     #     node = Node("$")
#     #     node.parent = root
#     #
#     #     # write parse tree in the file
#     #     lines = []
#     #     for pre, fill, node in RenderTree(root):
#     #         lines.append(str(f"{pre}{node.name}\n"))
#     #     with open("parse_tree.txt", mode='w', encoding="utf-8") as parse_tree_file:
#     #         parse_tree_file.writelines(lines)
#     #
#     # def save_syntax_errors(self):
#     #     """Writes syntax errors in syntax_errors.txt."""
#     #     with open("syntax_errors.txt", "w") as syntax_errors_file:
#     #         if len(self._syntax_errors) == 0:
#     #             syntax_errors_file.write("There is no syntax error.")
#     #         else:
#     #             for error in self._syntax_errors:
#     #                 syntax_errors_file.write(f"{error.content}\n")
#     #
#     # def save_semantic_errors(self):
#     #     """Writes semantic errors in semantic_errors.txt"""
#     #     with open("semantic_errors.txt", "w") as semantic_errors_file:
#     #         if len(self._semantic_errors) == 0:
#     #             semantic_errors_file.write("The input program is semantically correct.")
#     #
#     # def save_program_block(self):
#     #     """Writes program block in output.txt"""
#     #     with open("output.txt", "w") as output_file:
#     #         for i in range(len(self._program_block)):
#     #             output_file.write(f"{i}\t{self._program_block[i]}\n")
#
#
#     # refactore this shiiiiiiiiiiit
#     # def call_nt(self, nt_name: str, nt_list: list):
#     #     global eof_reached
#     #     my_list = nt_list
#     #     self.current_nt = non_terminals[nt_name]
#     #     rule_id = self.current_nt.predict_rule(self.current_token)
#     #     if rule_id is None:
#     #         token_name = get_token_name(self.current_token)
#     #         if token_name in self.current_nt.follows:
#     #             self.report_syntax_error(missing_error_keyword, self.current_nt.name, self.current_line)
#     #             return  # assume that the current nt is found, and we should continue
#     #         elif token_name == eof_keyword:
#     #             if not eof_reached:
#     #                 self.report_syntax_error(unexpected_error_keyword, 'EOF', self.current_line)
#     #                 eof_reached = True
#     #             return
#     #         else:
#     #             self.report_syntax_error(illegal_error_keyword, get_token_name(self.current_token), self.current_line)
#     #             self.update_token()  # assume there was an illegal input and ignore it
#     #             self.call_nt(nt_name, nt_list)
#     #             return
#     #     rule = rules[rule_id]
#     #     my_list.extend(rule.get_actions())
#     #     for i in range(len(my_list)):
#     #         action = my_list[i]
#     #         if self.current_token == ('eof', '$') and eof_reached:
#     #             my_list[i] = None
#     #         elif is_terminal(action):
#     #             if action == epsilon_keyword:
#     #                 my_list[i] = (epsilon_keyword, epsilon_keyword)
#     #             else:
#     #                 my_list[i] = self.current_token
#     #                 if not self.match_action(action):
#     #                     my_list[i] = None
#     #         elif is_action_symbol(action):
#     #             self.code_generator.code_gen(action,
#     #                                          get_action_symbol_input(self.current_token),
#     #                                          self.current_line)
#     #         else:
#     #             child_nt_list = []
#     #             my_list[i] = (action, child_nt_list)
#     #             self.call_nt(action, child_nt_list)
#     #             if len(child_nt_list) == 0:
#     #                 my_list[i] = None
#     #
#     #     # remove None values
#     #     while None in my_list:
#     #         my_list.remove(None)
#     #
#     # def find_rule_firsts(self, rule_id: int) -> list[str]:
#     #     rule = rules[rule_id]
#     #
#     #     if rule.get_actions()[0] == epsilon_keyword:  # the rule itself is epsilon
#     #         return rule.get_actions()
#     #
#     #     rule_first = []
#     #     actions = rule.get_actions()
#     #     for index in range(len(actions)):
#     #         action = actions[index]
#     #         if is_terminal(action):
#     #             rule_first.append(action)
#     #             return remove_duplicates(rule_first)
#     #         elif not is_action_symbol(action):
#     #             # then action is a non-terminal
#     #             action_first = data[first_keyword][action]
#     #             if epsilon_keyword in action_first:
#     #                 if index is not len(actions) - 1:
#     #                     rule_first += [val for val in action_first if val != epsilon_keyword]
#     #                 else:
#     #                     # If we're here, all the actions were terminals that contained epsilon in their firsts.
#     #                     # So epsilon must be included in rule_first
#     #                     rule_first += action_first
#     #             else:
#     #                 rule_first = action_first + rule_first
#     #                 return remove_duplicates(rule_first)
#     #
#     #     return remove_duplicates(rule_first)
#
#     # def _update_current_token(self):
#     #     """Stores next token in _current_token and updates _current_input."""
#     #     self._current_token: Tuple[str, str] = self._scanner.get_next_token()
#     #     self._current_input: str = ""
#     #     if self._current_token[0] in {Scanner.KEYWORD, Scanner.SYMBOL, Scanner.EOF}:
#     #         self._current_input = self._current_token[1]
#     #     else:
#     #         self._current_input = self._current_token[0]
#
#     def parse(self):
#         # for key, value in self.transition_table.items():
#         #     print(key, value)
#         # while self.current_token != '$':
#         #     break
#         #     self.current_token = self.get_next_token()
#         #     print(self.current_token)
#         self.current_token, self.current_value = self.get_next_token()
#         # while self.current_value != '{':
#         #     self.current_token, self.current_value = self.get_next_token()
#         # print("token and value:" , self.current_token, self.current_value)
#
#         stack = [grammar.non_terminals[0]]
#         node_stack = [Node(grammar.non_terminals[0])]  # Node stack for the parse tree
#         self.root = node_stack[0]
#
#         while stack:
#             # cnt = 0
#             stack_top = stack[-1]
#             node_stack_top = node_stack[-1]
#             # print('stack_top:', stack_top)
#
#             if stack_top in grammar.terminals:
#                 if stack_top == self.current_value:
#                     stack.pop()
#                     node_stack.pop().name = str(self.current_token)
#                 else:
#                     self.error(f"missing {stack_top}")
#                     stack.pop()
#                     node_stack.pop().name = str(self.current_token)
#                 self.current_token, self.current_value = self.get_next_token()
#             elif stack_top == '$':
#                 if stack_top != self.current_value:
#                     self.error("Unexpected EOF")
#                 break
#             # elif stack_top[0] == '#':
#             #     print("parse - in action symbol section")
#             #     cg = CodeGenerator(self.scanner)
#             #     getattr(cg, stack_top[1:])()
#             #     print("stack , node stack", stack, node_stack)
#             #     stack.pop()
#             #     node_stack.pop()
#             #     self.current_token, self.current_value = self.get_next_token()
#                 # stack.append()
#                 # print("looooooooooooooooook at this", self.current_token, self.current_value)
#                 # print("stack , node stack", stack, node_stack)
#
#             else:
#                 # print("stack top, current value",stack_top , self.current_value)
#                 # print("parse - in else section")
#                 production_rule = self.transition_table[(stack_top, self.current_value)]
#
#                 # print(self.transition_table[(stack_top, self.current_value)])
#                 # if stack_top == "Declaration-list" and self.current_value == "ID" and cnt == 0:
#                 #     production_rule = ['Declaration', 'Declaration-list']
#                 #     cnt +=1
#                 print(production_rule)
#                 # print(f'production_rule {(stack_top, self.current_value)}:', production_rule)
#
#                 if production_rule is None:
#                     # print("production rule is none")
#                     # print("grammar.first[stack_top]", grammar.first[stack_top])
#                     if 'epsilon' in grammar.first[stack_top]:
#                         production_rule = grammar.rules[stack_top][-1]
#                         # print("production rule", production_rule)
#                     else:
#                         self.error(f"illegal {self.current_value}")
#                         stack.pop()
#                         node_stack.pop()
#                         continue
#                 if production_rule[0] == 'epsilon':
#                     Node('epsilon', parent=node_stack.pop())
#                     stack.pop()
#                 else:
#                     # print("in the sus else")
#                     # print("production rule", production_rule)
#                     # print('stack before:', stack)
#                     # print('rule:', production_rule)
#                     # print('current_value:', self.current_value)
#                     stack.pop()
#                     node_stack.pop()
#                     nodes = []
#                     for symbol in production_rule:
#                         nodes.append(Node(symbol, parent=node_stack_top))
#                     for symbol in reversed(production_rule):
#                         stack.append(symbol)
#                         # print("stack append")
#                         node_stack.append(nodes.pop())
#                     # print('stack after:', stack)
#
#                     self.print_parse_tree()
#         self.print_parse_tree()
#
#     def error(self, message):
#         # print(f'#{self.scanner.reader.line_number} : syntax error, {message}')
#         self.syntax_errors.append((self.scanner.reader.line_number, message))
#
#     def print_parse_tree(self, file=None):
#         for pre, _, node in RenderTree(self.root):
#             print("%s%s" % (pre, node.name), file=file)
#
#     def repr_syntax_errors(self):
#         if not self.syntax_errors:
#             return 'There is no syntax error.'
#         return '\n'.join(map(lambda error:
#                              f'#{str(error[0])} : syntax error, {error[1]}',
#                              self.syntax_errors))
#
#
#
#




class Parser:
    # instance : Optional['Parser'] = None
    # @staticmethod
    # def get_instance(scanner):
    #     if Parser.instance == None:
    #         Parser.instance = Parser(scanner)
    #     return Parser.instance
    def __init__(self, scanner: Scanner):
        self.current_token = None
        self.current_value = None
        self.scanner = scanner
        self.syntax_errors = []  # [(line_number, error), ]
        self.transition_table = {}
        self.root = None
        self.create_transition_table()
        self.code_generator = CodeGenerator(self.scanner)
        # self.get_curr_input()

    def get_curr_input(self):
        self.code_generator._current_token = self.get_next_token()
        # print(self._current_token)
        # print(self._current_token[0])
        # print(self._current_token[1])
        # print(self._current_token[0].type)
        # self._current_token = self.parsre.get_current_token()[0]
        toCheck = KEYWORD + SYMBOL + "$"
        if self.code_generator._current_token == None:
            return
        if self.code_generator._current_token[0].type in toCheck:
            self._current_input = self.code_generator._current_token[1]
        else:
            self.code_generator._current_input = self.code_generator._current_token[0]


    def create_transition_table(self):
        for non_terminal in grammar.non_terminals:
            for terminal in grammar.terminals + ['$']:
                self.transition_table[(non_terminal, terminal)] = self.find_production_rule(non_terminal, terminal)

    def find_production_rule(self, non_terminal, terminal):
        for rule in grammar.rules[non_terminal]:
            # print(rule, self.find_first(rule))
            if rule[0] == 'epsilon':
                return rule
            if rule[0] in grammar.terminals:
                if rule[0] == terminal:
                    return rule
            elif terminal in self.find_first(rule):
                return rule
        return None

    @staticmethod
    def find_first(rule):
        first = []
        for t in rule:
            if t in grammar.terminals + ['$']:
                first.append(t)
                break
            if t == 'epsilon':
                continue
            first.extend(grammar.first[t])
            if 'epsilon' not in grammar.first[t]:
                break
        return first

    def get_next_token(self):
        ignore = [ctoken.WHITESPACE, ctoken.COMMENT]
        while True:
            next_token = self.scanner.get_next_token()
            if next_token.type not in ignore:
                break

        parse_value = next_token.value
        if next_token.type == ctoken.EOF:
            parse_value = '$'
        elif next_token.type == ctoken.ID:
            parse_value = 'ID'
        elif next_token.type == ctoken.NUM:
            parse_value = 'NUM'
        return next_token, parse_value

    def parse(self):
        # for key, value in self.transition_table.items():
        #     print(key, value)
        # while self.current_token != '$':
        #     break
        #     self.current_token = self.get_next_token()
        #     print(self.current_token)

        self.current_token, self.current_value = self.get_next_token()

        stack = [grammar.non_terminals[0]]
        node_stack = [Node(grammar.non_terminals[0])]  # Node stack for the parse tree
        self.root = node_stack[0]

        while stack:
            stack_top = stack[-1]
            node_stack_top = node_stack[-1]
            # print('stack_top:', stack_top)

            if stack_top in grammar.terminals:
                if stack_top == self.current_value:
                    stack.pop()
                    node_stack.pop().name = str(self.current_token)
                    self.current_token, self.current_value = self.get_next_token()
                else:
                    self.error(f"missing {stack_top}")
                    stack.pop()
                    node = node_stack.pop()
                    parent_node = node.parent
                    parent_node.children = [child for child in parent_node.children if child != node]
                    while stack[-1] in grammar.terminals:
                        stack.pop()
                        node_stack.pop()
                    while self.current_value not in grammar.follow[stack[-1]] and self.current_value != '$':
                        if stack[-1] == 'Statement-list' and self.current_value == ';':
                            break
                        self.error(f"illegal {self.current_value}")
                        self.current_token, self.current_value = self.get_next_token()
                    if self.current_value == '$':
                        self.scanner.reader.line_number += 1
                        self.error("Unexpected EOF")
                        while stack:
                            stack.pop()
                            node = node_stack.pop()
                            parent_node = node.parent
                            parent_node.children = [child for child in parent_node.children if child != node]
            elif stack_top == '$':
                break
            else:
                production_rule = self.transition_table[(stack_top, self.current_value)]
                if production_rule == ['Declaration-list']:
                    print(1)
                    self.code_generator.call_main()
                elif production_rule == ['Type-specifier', 'ID']:
                    print(2)
                    self.code_generator.p_type(self.current_token)
                    self.code_generator.declare_id()
                elif production_rule == [';']:
                    self.code_generator.dec_var()
                elif production_rule == ['[', 'NUM', ']', ';']:
                    self.code_generator.dec_array()
                elif production_rule == ['(', 'Params', ')', 'Compound-stmt']:
                    self.code_generator.dec_func()
                    self.code_generator.end_func()
                elif production_rule == ['int', 'ID', 'Param-prime', 'Param-list']:
                    self.code_generator.p_type(self.current_token)
                    self.code_generator.declare_id()
                elif production_rule == ['[', ']']:
                    self.code_generator.declare_entry_array()
                elif production_rule == ['break', ';']:
                    self.code_generator.break_jp()
                elif production_rule == ['repeat', 'Statement', 'until', '(', 'Expression', ')']:
                    self.code_generator.label()
                    self.code_generator.until()
                elif production_rule == ['ID', 'B']:
                    self.code_generator.p_id(self.current_token)
                elif production_rule == ['=', 'Expression']:
                    self.code_generator.push_eq()
                    self.code_generator.assign()
                elif production_rule == ['[', 'Expression', ']', 'H']:
                    self.code_generator.array_access()
                elif production_rule == ['Relop', 'Additive-expression']:
                    self.code_generator.push_op()
                    self.code_generator.op()
                elif production_rule == ['Addop', 'Term', 'D']:
                    self.code_generator.push_op()
                    self.code_generator.op()
                elif production_rule == ['*', 'Factor', 'G']:
                    self.code_generator.push_op()
                    self.code_generator.op()
                elif production_rule == ['ID', 'Var-call-prime']:
                    self.code_generator.p_id(self.current_token)
                elif production_rule == ['NUM']:
                    self.code_generator.p_num(self.current_token)
                elif production_rule == ['(', 'Args', ')']:
                    self.code_generator.start_call()
                    self.code_generator.end_call()
                elif production_rule == ['[', 'Expression', ']']:
                    self.code_generator.array_access()
                elif production_rule == ['(', 'Args', ')']:
                    self.code_generator.start_call()
                    self.code_generator.end_call()
                elif production_rule == ['NUM']:
                    self.code_generator.p_num(self.current_token)
                elif production_rule == [',', 'Expression', 'Arg-list-prime']:
                    self.code_generator.arg_input()
                elif production_rule == ['epsilon'] and stack_top == 'Arg-list-prime':
                    self.code_generator.arg_input()

                print(f'production_rule {(stack_top, self.current_value)}:', production_rule)

                if production_rule is None:
                    if self.current_value == '$':
                        self.error("Unexpected EOF")
                        while stack:
                            stack.pop()
                            node = node_stack.pop()
                            parent_node = node.parent
                            parent_node.children = [child for child in parent_node.children if child != node]
                        continue
                    if 'epsilon' in grammar.first[stack_top]:
                        production_rule = grammar.rules[stack_top][-1]
                    else:
                        self.error(f"illegal {self.current_value}")
                        stack.pop()
                        node_stack.pop()
                        continue
                if production_rule[0] == 'epsilon':
                    Node('epsilon', parent=node_stack.pop())
                    stack.pop()
                else:
                    print('stack before:', stack)
                    print('rule:', production_rule)
                    print('current_value:', self.current_value)
                    stack.pop()
                    node_stack.pop()
                    nodes = []
                    for symbol in production_rule:
                        nodes.append(Node(symbol, parent=node_stack_top))
                    for symbol in reversed(production_rule):
                        stack.append(symbol)
                        node_stack.append(nodes.pop())
                    print('stack after:', stack)

                    # self.print_parse_tree()
        self.print_parse_tree()

    def error(self, message):
        print(f'#{self.scanner.reader.line_number} : syntax error, {message}')
        self.syntax_errors.append((self.scanner.reader.line_number, message))

    def print_parse_tree(self, file=None):
        for pre, _, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name), file=file)

    def repr_syntax_errors(self):
        if not self.syntax_errors:
            return 'There is no syntax error.'
        return '\n'.join(map(lambda error:
                             f'#{str(error[0])} : syntax error, {error[1]}',
                             self.syntax_errors))