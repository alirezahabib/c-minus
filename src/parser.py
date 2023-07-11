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
# from scanner import KEYWORD, SYMBOL
from symbol_table import Address
from symbol_table import Symbol_Table

KEYWORD= "KEYWORD"
SYMBOL= "SYMBOL"

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

kind_key = "kind"
type_key = "type"
address_key = "address"
scope_key = "scope"
attributes_key = "attributes"
lexeme_key = "lexeme"
invocation_address_key = "invocation_address"
return_address_key = "return_address"
return_value_key = "return_value"

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

class HeapManager:

    instance: Optional['HeapManager'] = None
    @staticmethod
    def get_instance():
        if HeapManager.instance == None:
            HeapManager.instance = HeapManager()
        return HeapManager.instance
    def __init__(self):
        self.first_free = 500
        self.variables = {}
        # heap manager is called twice for arrays. firstly with the declare_id and secondly
        # with modify attributes. after the second call with have to modify array type for address of array.
        # last_assigned is used for this.
        self.last_temp = None

    def get_temp(self, type_name, size=1, array_attribute=False):
        # return address of the first free cell
        temp_address = self.first_free
        if array_attribute:
            self.last_temp.type_name += "-arr"

        for i in range(size):
            temp = TempVariable(type_name, self.first_free, False)
            self.variables[self.first_free] = temp
            self.first_free += self.get_length_by_type(type_name)
            self.last_temp = temp

        return temp_address

    @staticmethod
    def get_length_by_type(type_name):
        if type_name == "int":
            return 4
        elif type_name == "void":
            return 1

    def get_type_by_address(self, address):
        return self.variables[address].type_name


class TempVariable:
    def __init__(self, type_name, address, array_attribute):
        self.type_name = type_name
        self.address = address

class SymbolTable:
    instance : Optional['Symbol_Table'] = None
    @staticmethod
    def get_instance(heap_manager):
        if SymbolTable.instance == None:
            SymbolTable.instance = SymbolTable(heap_manager)
        return SymbolTable.instance
    def __init__(self, heap_manager) -> None:
        # row properties are id, lexeme, proc/func/var/param (kind), No. Arg/Cell (attributes), type, scope, address
        self.address_to_row = {}
        self.table = []
        self.current_scope = 0
        self.heap_manager = heap_manager
        self.scope_stack = [0]
        self.insert("output")
        self.modify_last_row("func", "void")
        self.table[-1]['attributes'] = 1
        self.table.append({'id': 1, 'lexeme': 'somethingwild', 'kind': "param", 'attributes': '-', 'type': "int",
                           'scope': 1, 'address': self.heap_manager.get_temp("int", 1)})

    def insert(self, lexeme):
        self.table.append({'id': len(self.table), 'lexeme': lexeme})

    def modify_last_row(self, kind, type):
        # after declaration of a variable by scanner, code generator needs
        # to complete the declaration by modifying the last row of symbol table
        self.table[-1]['kind'] = kind
        self.table[-1]['type'] = type
        self.table[-1]['address'] = self.heap_manager.get_temp(type, 1)
        self.table[-1]['scope'] = self.current_scope
        self.table[-1]['attributes'] = '-'
        self.address_to_row[self.table[-1]['address']] = len(self.table) - 1

    def modify_func_row_information(self, row_index, invocation_address, return_address, return_value):
        # add a "invocation_address" field to the row,
        # this is used when we declare a function and we want to invoke it. We should know where to jump to
        self.table[row_index]['invocation_address'] = invocation_address
        # add a "return_address" field to the row,
        # anyone who calls the function should put its address (PC) in this address
        self.table[row_index]['return_address'] = return_address
        # return value is the address of a temp that is supposed to hold the return value of the function
        self.table[row_index]['return_value'] = return_value

    def modify_attributes_last_row(self, num_attributes):
        # used for array declaration and function declaration
        # if arr_func == True then it is an array
        # else it is a function
        # note: for now it is only used for array declaration
        self.table[-1]['attributes'] = num_attributes

    def modify_attributes_row(self, row_id, num_attributes, arr_func: bool = True):
        # used for modifying function No. of args after counting them
        # if arr_func == True then it is an array
        # else it is a function
        self.table[row_id]['attributes'] = num_attributes

    def modify_kind_last_row(self, kind):
        self.table[-1]['kind'] = kind

    def add_scope(self):
        self.current_scope += 1
        self.scope_stack.append(len(self.table))

    def end_scope(self):
        # remove all rows of symbol table that are in the current scope
        # and update the current scope
        # remember function is first added and then the scope is added
        # also param type of the function that the scope is created for,
        # must not be removed
        remove_from = len(self.table)
        for i in range(self.scope_stack[-1], len(self.table)):
            if self.is_useless_row(i) or self.table[i]['kind'] != "param":
                remove_from = i
                break

        self.table = self.table[:remove_from]

        self.current_scope -= 1
        self.scope_stack.pop()

    def declare_array(self, num_of_cells):
        self.table[-1]['attributes'] = num_of_cells

    def lookup(self, name, start_ind=0, in_declare=False, end_ind=-1) -> dict:
        # search in symbol table
        # search for it between the start_ind and end_ind of symbol table
        # if end_ind == -1 then it means to search till the end of symbol table

        row_answer = None
        nearest_scope = -1
        end = end_ind

        if end_ind == -1:
            end = len(self.table)
            if in_declare and self.is_useless_row(-1):
                end -= 1

        while len(self.scope_stack) >= -nearest_scope:
            start = self.scope_stack[nearest_scope]

            for i in range(start, end):
                row_i = self.table[i]
                if not self.is_useless_row(i):
                    if nearest_scope != -1 and row_i['kind'] == "param":
                        pass
                    elif row_i['lexeme'] == name:
                        return row_i

            nearest_scope -= 1
            end = start

        return row_answer

    def remove_last_row(self):
        self.table.pop()

    def is_useless_row(self, id):
        if "type" not in self.get_row_by_id(id):
            return True

    def get_row_id_by_address(self, address) -> int:
        return self.address_to_row[address]

    def get_row_by_id(self, id) -> dict:
        return self.table[id]

    def get_id_last_row(self):
        return len(self.table) - 1

    def get_row_by_address(self, address) -> dict:
        return self.get_row_by_id(self.get_row_id_by_address(address))

    def get_last_row(self):
        return self.get_row_by_id(-1)

    def get_last_row_index(self):
        return len(self.table) - 1

# from symbol_table import SymbolTable
# from heap_manager import HeapManager

kind_key = "kind"
type_key = "type"
address_key = "address"
scope_key = "scope"
attributes_key = "attributes"
lexeme_key = "lexeme"
invocation_address_key = "invocation_address"
return_address_key = "return_address"
return_value_key = "return_value"


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


def get_type_name(tuple_type):
    if tuple_type[1]:
        return "array"
    else:
        return tuple_type[0]


class CodeGenerator:

    def __init__(self, symbol_table: SymbolTable, heap: HeapManager):
        self.symbol_table = symbol_table
        self.semantic_stack = []
        self.PB = []
        self.FS = []
        # pc shows the next line of program block to be filled (i in slides)
        self.PC = 0
        self.heap_manager = heap
        self.current_line = 0
        # used to say that the function doesn't take any more arguments.
        # in end_call it will go back to False but in arg_input it may go True if we have error_num_args
        self.no_more_arg_input = False
        # for semantic stack
        # todo must be changed in future because lookup must search by scope - can be removed now.
        #  we don't need start_ind in lookup function any more
        self.start_scope = 0

        self.num_open_repeats = 0

        self.semantic_analyzer = SemanticAnalyzer()
        # errors
        self.error_scoping = "#{0}: Semantic Error! '{1}' is not defined.{2}{3}{4}"
        self.error_void_type = "#{0}: Semantic Error! Illegal type of void for '{1}'.{2}{3}{4}"
        self.error_type_missmatch = "#{0}: Semantic Error! Type mismatch in operands, Got {1} instead of {2}.{3}{4}"
        self.error_break = "#{0}: Semantic Error! No 'repeat ... until' found for 'break'."
        self.error_param_type_missmatch = "#{0}: Semantic Error! Mismatch in type of argument {1} of '{2}'. Expected '{3}' but got '{4}' instead."
        self.error_num_args = "#{0}: Semantic Error! Mismatch in numbers of arguments of '{1}'.{2}{3}{4}"

    def code_gen(self, action_symbol, token, line_number):
        self.current_line = line_number
        if self.no_more_arg_input and action_symbol != "#end_call":
            return

        action_symbol = action_symbol[1:]
        if action_symbol == "declare_id":
            self.declare_id(token)
        elif action_symbol == "declare_array":
            self.declare_array(token)
        elif action_symbol == "push_type":
            self.push_type(token)
        elif action_symbol == "do_op":
            self.do_op(token)
        # elif action_symbol == "mult":
        #     self.mult(token)
        elif action_symbol == "push_op":
            self.push_op(token)
        elif action_symbol == "label":
            self.label(token)
        elif action_symbol == "until":
            self.until(token)
        elif action_symbol == "array_calc":
            self.array_calc(token)
        elif action_symbol == "jpf_save":
            self.jpf_save(token)
        elif action_symbol == "save":
            self.save(token)
        elif action_symbol == "jp":
            self.jp(token)
        elif action_symbol == "print":
            self.print(token)
        elif action_symbol == "push_num":
            self.push_num(token)
        elif action_symbol == "id":
            self.id(token)
        elif action_symbol == "assign":
            self.assign(token)
        elif action_symbol == "push_eq":
            self.push_eq(token)
        elif action_symbol == "break":
            self.break_check(token)
        elif action_symbol == "add_scope":
            self.add_scope(token)
        elif action_symbol == "start_func":
            self.start_func(token)
        elif action_symbol == "add_param":
            self.add_param(token)
        elif action_symbol == "end_func_params":
            self.end_func_params(token)
        elif action_symbol == "start_call":
            self.start_call(token)
        elif action_symbol == "end_call":
            self.end_call(token)
        elif action_symbol == "declare_entry_array":
            self.declare_entry_array(token)
        elif action_symbol == "return":
            self.return_command(token)
        elif action_symbol == "return_manual":
            self.return_manual(token)
        elif action_symbol == "arg_input":
            self.arg_input(token)
        elif action_symbol == "end_scope":
            self.end_scope(token)
        elif action_symbol == "push_function":
            self.push_function(token)
        elif action_symbol == "pop_function":
            self.pop_function(token)
        elif action_symbol == "set_function_info":
            self.set_function_info(token)
        elif action_symbol == "call_main":
            self.call_main(token)
        elif action_symbol == "jump_out":
            self.jump_out(token)
        elif action_symbol == "show_scope_start":
            self.show_scope_start(token)
        elif action_symbol == "pop_scope":
            self.pop_scope(token)

    def pop_last_n(self, n):
        # pop last n elements from semantic stack
        for _ in range(n):
            self.semantic_stack.pop()

    @staticmethod
    def get_pb_line(line_index, operation, first_op=" ", second_op=" ", third_op=" "):
        return f'{line_index}\t({operation}, {first_op}, {second_op}, {third_op} )'

    def program_block_insert(self, operation, first_op=" ", second_op=" ", third_op=" "):
        # insert to program block
        operation = self.get_operation_by_symbol(operation)
        self.PB.append(self.get_pb_line(len(self.PB), operation, first_op, second_op, third_op))
        self.PC += 1

    def program_block_modification(self, index, operation, first_op="", second_op="", third_op=""):
        # modify a passed line of program block and add the code
        operation = self.get_operation_by_symbol(operation)
        self.PB[index] = self.get_pb_line(index, operation, first_op, second_op, third_op)

    def program_block_insert_empty(self):
        self.PB.append("")
        self.PC += 1

    @staticmethod
    def get_operation_by_symbol(symbol):
        if symbol == '+':
            return "ADD"
        elif symbol == '-':
            return "SUB"
        elif symbol == '*':
            return "MULT"
        elif symbol == "==":
            return "EQ"
        elif symbol == "<":
            return "LT"
        elif symbol == ":=":
            return "ASSIGN"
        else:
            return symbol.upper()

    def add_scope(self, token):
        # add scope to scope stack
        self.symbol_table.add_scope()

    def end_scope(self, token=""):
        self.symbol_table.end_scope()

    def return_command(self, token):
        function_row_index = self.FS[-1]
        function_row = self.symbol_table.get_row_by_id(function_row_index)
        return_type = function_row[type_key]
        if return_type != "void":
            return_value = self.semantic_stack.pop()
            return_value_temp_address = function_row[return_value_key]
            self.program_block_insert(
                operation=":=",
                first_op=return_value,
                second_op=return_value_temp_address
            )
        self.program_block_insert(
            operation="JP",
            first_op="@" + str(function_row[return_address_key])
        )

    def return_manual(self, token):
        function_row_index = self.FS[-1]
        function_row = self.symbol_table.get_row_by_id(function_row_index)
        self.program_block_insert(
            operation="JP",
            first_op="@" + str(function_row[return_address_key])
        )

    def start_func(self, token):
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

    def add_param(self, token):
        self.symbol_table.modify_kind_last_row("param")
        counter = self.semantic_stack.pop()
        counter += 1
        self.semantic_stack.append(counter)

    def declare_entry_array(self, token):
        self.push_num("0")
        self.declare_array(token)

    def end_func_params(self, token):
        # end of function declaration
        self.symbol_table.modify_attributes_row(row_id=self.semantic_stack[-2],
                                                num_attributes=self.semantic_stack[-1],
                                                arr_func=False)
        self.pop_last_n(2)

    def start_call(self, token):
        # start of function call
        # row_id = self.symbol_table.lookup(self.semantic_stack[-1])['id']
        function_row_id = self.symbol_table.get_row_id_by_address(self.semantic_stack[-1])
        self.semantic_stack.pop()
        num_parameters = self.symbol_table.get_row_by_id(function_row_id)[attributes_key]
        # add parameter types to stack in the form of tuple (type, is_array)
        for i in range(num_parameters, 0, -1):
            temp_address_param = self.symbol_table.get_row_by_id(function_row_id + i)[address_key]
            # type_param = self.get_operand_type(temp_address_param)
            self.semantic_stack.append(temp_address_param)

        # add the number of parameters to stack
        self.semantic_stack.append(num_parameters)
        # add a counter for arguments - at first it is equal to number of parameters
        self.semantic_stack.append(num_parameters)
        # add name of function to stack
        self.semantic_stack.append(self.symbol_table.get_row_by_id(function_row_id)[lexeme_key])

    def arg_input(self, token):
        # take input argument for function call
        if not self.no_more_arg_input:
            arg = self.semantic_stack.pop()
            type_arg = self.get_operand_type(arg)
            name_func = self.semantic_stack.pop()
            counter_args = self.semantic_stack.pop()
            counter_args -= 1
            if counter_args == 0 and token != ")":
                self.no_more_arg_input = True
                self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
                                                            error=self.error_num_args,
                                                            first_op=name_func
                                                            )

            num_parameters = self.semantic_stack.pop()
            temp_param = self.semantic_stack.pop()
            self.program_block_insert(
                operation=":=",
                first_op=arg,
                second_op=temp_param
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
                    self.semantic_stack.append(arg)
                    self.print("nothing")

            self.semantic_stack.append(num_parameters)
            self.semantic_stack.append(counter_args)
            self.semantic_stack.append(name_func)

    def end_call(self, token):
        # end of function call
        self.no_more_arg_input = False
        name_func = self.semantic_stack.pop()
        counter_args = self.semantic_stack.pop()
        num_parameters = self.semantic_stack.pop()
        if counter_args != 0:
            self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
                                                        error=self.error_num_args,
                                                        first_op=name_func
                                                        )
            self.pop_last_n(counter_args)

        function_row = self.symbol_table.lookup(name_func)
        index = function_row['id']
        if index in self.FS:
            self.semantic_analyzer.raise_semantic_error(1)  # todo added to avoid recursive call

        # return if function_row does not have needed keys (may not happen!)
        if invocation_address_key not in function_row or return_address_key not in function_row:
            # print("error in function declaration")
            return

        # update the return address temp of function (we want the function to return here after invocation)
        return_address_temp = function_row[return_address_key]
        self.program_block_insert(
            operation=":=",
            first_op="#" + str(self.PC + 2),
            second_op=return_address_temp
        )

        # # if the function is supposed to return a value, we need to push the address of return value to stack
        # if function_row[type_key] != "void":
        #     self.semantic_stack.append(function_row[return_value_key]

        # now that everything is set (including return address and arguments assignment), we can jump to the function
        self.program_block_insert(
            operation="JP",
            first_op=function_row[invocation_address_key]
        )
        if function_row[type_key] != "void":
            returnee_copy = self.heap_manager.get_temp(function_row[type_key])
            self.program_block_insert(
                operation=":=",
                first_op=function_row[return_value_key],
                second_op=returnee_copy
            )
            self.semantic_stack.append(returnee_copy)

    def push_type(self, token):
        # push type to stack
        if token == "int" or token == "void":
            self.semantic_stack.append(token)
        else:
            raise Exception("type not supported")

    def push_num(self, token):
        # push number to stack
        self.semantic_stack.append(str("#" + token.strip()))

    def print(self, token):
        self.program_block_insert(operation="print", first_op=self.semantic_stack[-1])
        self.semantic_stack.pop()

    def break_check(self, token):
        # check if we are in a repeat until statement
        if self.num_open_repeats == 0:
            self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
                                                        error=self.error_break)
        # push PC counter so that it can be filled in the #until action symbol to jump out
        else:
            self.semantic_stack.append(self.PC)
            self.program_block_insert_empty()
            # self.semantic_stack.insert(1, "break")
            self.semantic_stack.append("break")

    def declare_id(self, token, kind="var"):
        # search in symbol table
        # if found in current scope raise error
        # if not found
        # add to symbol table
        # token will be the lexeme of the variable
        the_row = self.symbol_table.lookup(token, self.start_scope, False)
        if the_row is not None and the_row[scope_key] == self.symbol_table.current_scope:
            # this means that the variable is already declared,
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

    def declare_array(self, token):
        # add to symbol table
        array_size = self.semantic_stack.pop()
        if str(array_size).startswith("#"):
            array_size = int(array_size[1:])
        self.symbol_table.modify_attributes_last_row(num_attributes=array_size)
        array_row = self.symbol_table.get_last_row()
        # array address is the address of pointer to array
        # we need to allocate memory for the array itself and then assign the address of the first entry to the pointer
        array_address = array_row[address_key]
        entries_type = array_row[type_key]
        array_start_address = self.heap_manager.get_temp(entries_type, array_size)
        self.program_block_insert(
            operation=":=",
            first_op="#" + str(array_start_address),
            second_op=array_address
        )

    def assign(self, token):
        # stack:
        # -1: source temp
        # -2: =
        # -3: destination temp
        answer = self.semantic_stack[-3]
        self.program_block_insert(operation=":=", first_op=self.semantic_stack[-1], second_op=self.semantic_stack[-3])
        self.pop_last_n(3)
        if len(self.semantic_stack) > 0 and self.semantic_stack[-1] == "=":
            # means there was a nested assignment and we should push the result to the stack
            self.semantic_stack.append(answer)

    def label(self, token):
        # declare where to jump back after until in repeat-until
        self.semantic_stack.append(self.PC)

        self.num_open_repeats += 1

    def until(self, token):
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

    def array_calc(self, token):
        # calculate the address of the index of the array
        # the index is on top of the stack and the address of array is the second element
        # pop those two and push the address of calculated address to the stack
        array_address = self.semantic_stack[-2]
        array_index = self.semantic_stack[-1]
        self.pop_last_n(2)

        array_type, _ = self.get_operand_type(array_address)
        temp = self.heap_manager.get_temp(array_type)
        self.program_block_insert(
            operation="*",
            first_op=array_index,
            second_op="#" + str(self.heap_manager.get_length_by_type(array_type)),
            third_op=temp
        )
        self.program_block_insert(
            operation="+",
            first_op=array_address,
            second_op=temp,
            third_op=temp
        )
        self.semantic_stack.append(str('@' + str(temp)))

    def push_op(self, token):
        # push operator to stack
        self.semantic_stack.append(token)

    def do_op(self, token):
        # do the operation
        # pop the operator and operands from the stack
        # push the result to the stack
        op = self.semantic_stack[-2]
        first_op = self.semantic_stack[-3]
        second_op = self.semantic_stack[-1]
        self.pop_last_n(3)
        # semantic: check operands types
        operands_type, is_array1 = self.get_operand_type(first_op)
        _, is_array2 = self.get_operand_type(second_op)
        if is_array1 or is_array2:
            self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
                                                        error=self.error_type_missmatch,
                                                        first_op="array",
                                                        second_op="int")
        temp = self.heap_manager.get_temp(operands_type)
        self.program_block_insert(operation=op, first_op=first_op, second_op=second_op, third_op=temp)
        self.semantic_stack.append(temp)

    def jpf_save(self, token):
        # jpf
        index_before_break = -1
        # remove breaks
        while self.semantic_stack[index_before_break] == "break":
            index_before_break -= 2
        breaks = []
        if index_before_break != -1:
            breaks = self.semantic_stack[index_before_break + 1:]
            self.semantic_stack = self.semantic_stack[:index_before_break + 1]

        self.program_block_modification(
            index=self.semantic_stack[-1],
            operation="JPF",
            first_op=self.semantic_stack[-2],
            second_op=str(self.PC + 1)
        )
        self.pop_last_n(2)
        # then save current pc
        self.semantic_stack.append(self.PC)
        self.program_block_insert_empty()
        # add back breaks
        self.semantic_stack.extend(breaks)

    def save(self, toke):
        # save the current PC
        self.semantic_stack.append(self.PC)
        self.program_block_insert_empty()

    def jp(self, token):
        # jump to a label

        index_before_break = -1
        while self.semantic_stack[index_before_break] == "break":
            index_before_break -= 2
        breaks = []
        # remove breaks
        if index_before_break != -1:
            breaks = self.semantic_stack[index_before_break + 1:]
            self.semantic_stack = self.semantic_stack[:index_before_break + 1]

        self.program_block_modification(
            index=self.semantic_stack[-1],
            operation="JP",
            first_op=str(self.PC)
        )
        self.pop_last_n(1)

        # add back breaks
        self.semantic_stack.extend(breaks)

    def id(self, token):
        # push the address of current token
        row = self.symbol_table.lookup(token, self.start_scope)
        if row is None:
            self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
                                                        error=self.error_scoping,
                                                        first_op=token)
            # add a dummy address of type int
            self.semantic_stack.append(self.heap_manager.get_temp("int", 1))

        else:
            address = row[address_key]
            self.semantic_stack.append(address)

    def push_eq(self, token):
        # in case of assignment, push = to stack
        # used for finding out if there is a nested assignment
        self.semantic_stack.append("=")

    def get_operand_type(self, operand):
        is_array = False
        if str(operand).startswith("#"):
            return "int", is_array
        elif str(operand).startswith("@"):
            operand = operand[1:]
        type = self.heap_manager.get_type_by_address(int(operand))
        if type.endswith("-arr"):
            type = type[:-4]
            is_array = True

        return type, is_array

    def print_pb(self):
        print("\n--------------Program Block---------------")
        for row in self.PB:
            print(row)

    def write_pb_to_file(self, output_file, semantic_file):
        if self.semantic_analyzer.num_semantic_errors > 0:
            output_file.write("The output code has not been generated.")
            for error in self.semantic_analyzer.all_errors:
                semantic_file.write(error + "\n")

            return

        for row in self.PB:
            output_file.write(str(row) + "\n")

    def push_function(self, token):
        # push function row index to stack (it's the last row of symbol table)
        self.FS.append(self.symbol_table.get_last_row_index())

    def pop_function(self, token):
        # pop function row index from stack
        self.FS.pop()

    def set_function_info(self, token):
        function_row_index = self.FS[-1]
        row = self.symbol_table.get_row_by_id(function_row_index)
        current_pc = self.PC
        return_address_temp = self.heap_manager.get_temp('int')
        return_value_temp = self.heap_manager.get_temp(row[type_key])
        self.symbol_table.modify_func_row_information(
            row_index=function_row_index,
            invocation_address=current_pc,
            return_address=return_address_temp,
            return_value=return_value_temp
        )

    def jump_out(self, token):
        # after the declaration of function is done,
        # we save a space in PB to tell us to jump out  of it and go to the declaration of next functions
        # Right now we know the next function. So we can fill out the saved row of PB
        self.program_block_modification(
            index=self.semantic_stack.pop(),
            operation="JP",
            first_op=str(self.PC)
        )

    def call_main(self, token):
        main_function_row = self.symbol_table.lookup("main")
        # set up the return address register of main
        self.program_block_insert(
            operation=":=",
            first_op="#" + str(self.PC + 2),
            second_op=str(main_function_row[return_address_key])
        )
        # now jump to the invocation address of main
        self.program_block_insert(
            operation="JP",
            first_op=str(main_function_row[invocation_address_key])
        )

    def show_scope_start(self, token):
        self.semantic_stack.append("scope_start")

    def pop_scope(self, token):
        breaks_array = []
        while self.semantic_stack[-1] != "scope_start":
            if self.semantic_stack[-1] == "break":
                breaks_array.append(self.semantic_stack.pop())
                breaks_array.append(self.semantic_stack.pop())
            else:
                self.semantic_stack.pop()
        self.semantic_stack.pop()
        breaks_array.reverse()
        self.semantic_stack.extend(breaks_array)


















# # main class
# class CodeGenerator:
#     def __init__(self, symbol_table: SymbolTable, heap: HeapManager):
#         self.symbol_table = symbol_table
#         self.semantic_stack = []
#         self.PB = []
#         self.FS = []
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
#     # def __init__(self, scanner: Scanner): #, address : Address):
#
#         # self.ss = SS()
#         # self.address = Address.get_instance()
#         # self.pb = PB.get_instance()
#         # # self.st = st.SymbolTable()
#         # self.loop = []
#         # self.scanner = scanner
#         # # self.parser = Parser.get_instance(self.scanner)
#         # # self.parser = Parser(self.scanner)
#         # self.break_stack = []
#         #
#         # self.symbol_table = self.scanner.symbol_table
#         # self.code_gen_st = Symbol_Table.get_instance()
#         # self.curr_repeats = 0
#         # self.get_curr_input()
#
#     def code_gen(self, action_symbol, token, line_number):
#         self.current_line = line_number
#         if self.no_more_arg_input and action_symbol != "#end_call":
#             return
#
#         # action_symbol = action_symbol[1:]
#         if action_symbol == "declare_id":
#             self.declare_id(token)
#         elif action_symbol == "declare_array":
#             self.declare_array(token)
#         elif action_symbol == "push_type":
#             self.push_type(token)
#         elif action_symbol == "do_op":
#             self.do_op(token)
#         # elif action_symbol == "mult":
#         #     self.mult(token)
#         elif action_symbol == "push_op":
#             self.push_op(token)
#         elif action_symbol == "label":
#             self.label(token)
#         elif action_symbol == "until":
#             self.until(token)
#         elif action_symbol == "array_calc":
#             self.array_calc(token)
#         elif action_symbol == "jpf_save":
#             self.jpf_save(token)
#         elif action_symbol == "save":
#             self.save(token)
#         elif action_symbol == "jp":
#             self.jp(token)
#         elif action_symbol == "print":
#             self.print(token)
#         elif action_symbol == "push_num":
#             self.push_num(token)
#         elif action_symbol == "id":
#             self.id(token)
#         elif action_symbol == "assign":
#             self.assign(token)
#         elif action_symbol == "push_eq":
#             self.push_eq(token)
#         elif action_symbol == "break":
#             self.break_check(token)
#         elif action_symbol == "add_scope":
#             self.add_scope(token)
#         elif action_symbol == "start_func":
#             self.start_func(token)
#         elif action_symbol == "add_param":
#             self.add_param(token)
#         elif action_symbol == "end_func_params":
#             self.end_func_params(token)
#         elif action_symbol == "start_call":
#             self.start_call(token)
#         elif action_symbol == "end_call":
#             self.end_call(token)
#         elif action_symbol == "declare_entry_array":
#             self.declare_entry_array(token)
#         elif action_symbol == "return":
#             self.return_command(token)
#         elif action_symbol == "return_manual":
#             self.return_manual(token)
#         elif action_symbol == "arg_input":
#             self.arg_input(token)
#         elif action_symbol == "end_scope":
#             self.end_scope(token)
#         elif action_symbol == "push_function":
#             self.push_function(token)
#         elif action_symbol == "pop_function":
#             self.pop_function(token)
#         elif action_symbol == "set_function_info":
#             self.set_function_info(token)
#         elif action_symbol == "call_main":
#             self.call_main(token)
#         elif action_symbol == "jump_out":
#             self.jump_out(token)
#         elif action_symbol == "show_scope_start":
#             self.show_scope_start(token)
#         elif action_symbol == "pop_scope":
#             self.pop_scope(token)
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
#         function_row_index = self.FS[-1]
#         function_row = self.symbol_table.get_row_by_id(function_row_index)
#         return_type = function_row[type_key]
#         if return_type != "void":
#             return_value = self.semantic_stack.pop()
#             return_value_temp_address = function_row[return_value_key]
#             self.program_block_insert(
#                 operation=":=",
#                 first_op=return_value,
#                 second_op=return_value_temp_address
#             )
#         self.program_block_insert(
#             operation="JP",
#             first_op="@" + str(function_row[return_address_key])
#         )
#
#     def return_manual(self, token):
#         function_row_index = self.FS[-1]
#         function_row = self.symbol_table.get_row_by_id(function_row_index)
#         self.program_block_insert(
#             operation="JP",
#             first_op="@" + str(function_row[return_address_key])
#         )
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
#         function_row_id = self.symbol_table.get_row_id_by_address(self.semantic_stack[-1])
#         self.semantic_stack.pop()
#         num_parameters = self.symbol_table.get_row_by_id(function_row_id)[attributes_key]
#         # add parameter types to stack in the form of tuple (type, is_array)
#         for i in range(num_parameters, 0, -1):
#             temp_address_param = self.symbol_table.get_row_by_id(function_row_id + i)[address_key]
#             # type_param = self.get_operand_type(temp_address_param)
#             self.semantic_stack.append(temp_address_param)
#
#         # add the number of parameters to stack
#         self.semantic_stack.append(num_parameters)
#         # add a counter for arguments - at first it is equal to number of parameters
#         self.semantic_stack.append(num_parameters)
#         # add name of function to stack
#         self.semantic_stack.append(self.symbol_table.get_row_by_id(function_row_id)[lexeme_key])
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
#             self.program_block_insert(
#                 operation=":=",
#                 first_op=arg,
#                 second_op=temp_param
#             )
#
#             type_param = self.get_operand_type(temp_param)
#             if type_arg != type_param:
#                 pass
#                 # self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#                 #                                             error=self.error_param_type_missmatch,
#                 #                                             first_op=num_parameters - counter_args,
#                 #                                             second_op=name_func,
#                 #                                             third_op=self.get_type_name(type_param),
#                 #                                             fourth_op=self.get_type_name(type_arg)
#                 #                                             )
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
#         function_row = self.symbol_table.lookup(name_func)
#         index = function_row['id']
#         if index in self.FS:
#             self.semantic_analyzer.raise_semantic_error(1)  # todo added to avoid recursive call
#
#         # return if function_row does not have needed keys (may not happen!)
#         if invocation_address_key not in function_row or return_address_key not in function_row:
#             # print("error in function declaration")
#             return
#
#         # update the return address temp of function (we want the function to return here after invocation)
#         return_address_temp = function_row[return_address_key]
#         self.program_block_insert(
#             operation=":=",
#             first_op="#" + str(self.PC + 2),
#             second_op=return_address_temp
#         )
#
#         # # if the function is supposed to return a value, we need to push the address of return value to stack
#         # if function_row[type_key] != "void":
#         #     self.semantic_stack.append(function_row[return_value_key]
#
#         # now that everything is set (including return address and arguments assignment), we can jump to the function
#         self.program_block_insert(
#             operation="JP",
#             first_op=function_row[invocation_address_key]
#         )
#         if function_row[type_key] != "void":
#             returnee_copy = self.heap_manager.get_temp(function_row[type_key])
#             self.program_block_insert(
#                 operation=":=",
#                 first_op=function_row[return_value_key],
#                 second_op=returnee_copy
#             )
#             self.semantic_stack.append(returnee_copy)
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
#         if the_row is not None and the_row[scope_key] == self.symbol_table.current_scope:
#             # this means that the variable is already declared,
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
#         array_size = self.semantic_stack.pop()
#         if str(array_size).startswith("#"):
#             array_size = int(array_size[1:])
#         self.symbol_table.modify_attributes_last_row(num_attributes=array_size)
#         array_row = self.symbol_table.get_last_row()
#         # array address is the address of pointer to array
#         # we need to allocate memory for the array itself and then assign the address of the first entry to the pointer
#         array_address = array_row[address_key]
#         entries_type = array_row[type_key]
#         array_start_address = self.heap_manager.get_temp(entries_type, array_size)
#         self.program_block_insert(
#             operation=":=",
#             first_op="#" + str(array_start_address),
#             second_op=array_address
#         )
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
#         array_index = self.semantic_stack[-1]
#         self.pop_last_n(2)
#
#         array_type, _ = self.get_operand_type(array_address)
#         temp = self.heap_manager.get_temp(array_type)
#         self.program_block_insert(
#             operation="*",
#             first_op=array_index,
#             second_op="#" + str(self.heap_manager.get_length_by_type(array_type)),
#             third_op=temp
#         )
#         self.program_block_insert(
#             operation="+",
#             first_op=array_address,
#             second_op=temp,
#             third_op=temp
#         )
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
#
#     def push_function(self, token):
#         # push function row index to stack (it's the last row of symbol table)
#         self.FS.append(self.symbol_table.get_last_row_index())
#
#     def pop_function(self, token):
#         # pop function row index from stack
#         self.FS.pop()
#
#     def set_function_info(self, token):
#         function_row_index = self.FS[-1]
#         row = self.symbol_table.get_row_by_id(function_row_index)
#         current_pc = self.PC
#         return_address_temp = self.heap_manager.get_temp('int')
#         return_value_temp = self.heap_manager.get_temp(row[type_key])
#         self.symbol_table.modify_func_row_information(
#             row_index=function_row_index,
#             invocation_address=current_pc,
#             return_address=return_address_temp,
#             return_value=return_value_temp
#         )
#
#     def jump_out(self, token):
#         # after the declaration of function is done,
#         # we save a space in PB to tell us to jump out  of it and go to the declaration of next functions
#         # Right now we know the next function. So we can fill out the saved row of PB
#         self.program_block_modification(
#             index=self.semantic_stack.pop(),
#             operation="JP",
#             first_op=str(self.PC)
#         )
#
#     def call_main(self, token):
#         main_function_row = self.symbol_table.lookup("main")
#         # set up the return address register of main
#         self.program_block_insert(
#             operation=":=",
#             first_op="#" + str(self.PC + 2),
#             second_op=str(main_function_row[return_address_key])
#         )
#         # now jump to the invocation address of main
#         self.program_block_insert(
#             operation="JP",
#             first_op=str(main_function_row[invocation_address_key])
#         )
#
#     def show_scope_start(self, token):
#         self.semantic_stack.append("scope_start")
#
#     def pop_scope(self, token):
#         breaks_array = []
#         while self.semantic_stack[-1] != "scope_start":
#             if self.semantic_stack[-1] == "break":
#                 breaks_array.append(self.semantic_stack.pop())
#                 breaks_array.append(self.semantic_stack.pop())
#             else:
#                 self.semantic_stack.pop()
#         self.semantic_stack.pop()
#         breaks_array.reverse()
#         self.semantic_stack.extend(breaks_array)
#
#     '''
#     this must be implemented in parser part so we get _current_token and current_input as used:
#         def _update_current_token(self):
#             """Stores next token in _current_token and updates _current_input."""
#             self._current_token: Tuple[str, str] = self._scanner.get_next_token()
#             self._current_input: str = ""
#             if self._current_token[0] in {Scanner.KEYWORD, Scanner.SYMBOL, Scanner.EOF}:
#                 self._current_input = self._current_token[1]
#             else:
#                 self._current_input = self._current_token[0]
#     '''
#
#
#     # dfdlskhja
#     # def get_curr_input(self):
#     #     self._current_token = self.parser.get_next_token()
#     #     # print(self._current_token)
#     #     # print(self._current_token[0])
#     #     # print(self._current_token[1])
#     #     # print(self._current_token[0].type)
#     #     # self._current_token = self.parsre.get_current_token()[0]
#     #     toCheck = KEYWORD + SYMBOL + "$"
#     #     if self._current_token == None:
#     #         return
#     #     if self._current_token[0].type in toCheck:
#     #         self._current_input = self._current_token[1]
#     #     else:
#     #         self._current_input = self._current_token[0]
#
#     # def call_main(self):
#     #     main_function_row = self.scanner.symbol_table.code_gen_st.lookup('main')
#     #     self.pb.add_code(
#     #         ":=",
#     #         "#" + str(self.pb.get_line() + 2),
#     #         #str(main_function_row["return_address"])
#     #         str(0)
#     #     )
#     #     # now jump to the invocation address of main
#     #     self.pb.add_code(
#     #         "JP",
#     #         # str(main_function_row["invocation_address"])
#     #         "1"
#     #     )
#     #     # self.pb.finalize()
#     #
#     # def declare_id(self):
#     #     self.code_gen_st.modify_last_row(kind="var", type=self.ss.top())
#     #     self.pb.add_code(
#     #         ":=",
#     #         "#0",
#     #         self.code_gen_st.get_last_row()["address"],
#     #     )
#     #     self.ss.pop()
#     #
#     # def dec_var(self):# declare_var
#     #     # assign an address to the identifier, assign 0 to the variable in the program block
#     #     # and update identifier's row in the symbol table
#     #     data_type = self.ss.stack[-2]
#     #     index = self.ss.stack[-1]
#     #     self.ss.pop_mult(2)
#     #
#     #     self.pb.add_code(f"(ASSIGN, #0, {self.pb.get_tmp_address()},\t)")
#     #     self.scanner.update_symbol(index,
#     #                                 symbol_type="var",
#     #                                 size=0,
#     #                                 data_type=data_type,
#     #                                 scope=len(self.scanner.scope_stack),
#     #                                 address=self.pb.get_current_tmp_addr())
#     #     # self.pb.last_tmp += 4
#     #
#     # def p_id_index(self,token):  # p_id_index it is either p_id or declare_id
#     #     # push index of identifier into the semantic stack
#     #     lexeme = token[1]
#     #     index = self.scanner.get_symbol_index(lexeme)
#     #     self.ss.push(index)
#     #
#     # def end_function(self):  # end_function (probably to replace end_func)
#     #     # deletes the current scope
#     #     scope_start = self.scanner.scope_stack.pop()
#     #     self.scanner.pop_scope(scope_start)
#     #
#     # # refactore this shiiiiiiiiiiiiiit
#     # def declare_entry_array(self):
#     #     self.p_zero()
#     #     self.dec_array()
#     #
#     # # refactore this shiiiiiiiiiiiiiiiiiiit
#     # def dec_array(self):
#     #     # add to symbol table
#     #     # self.symbol_table
#     #     array_size = self.ss.pop()
#     #     if str(array_size).startswith("#"):
#     #         array_size = int(array_size[1:])
#     #     self.code_gen_st.modify_attributes_last_row(num_attributes=array_size)
#     #     array_row = self.code_gen_st.get_last_row()
#     #     # array address is the address of pointer to array
#     #     # we need to allocate memory for the array itself and then assign the address of the first entry to the pointer
#     #     array_addr = array_row["address"]
#     #     entries_type = array_row["type"]
#     #     array_start_address = self.pb.get_tmp_address_by_size(entries_type, array_size)
#     #     self.pb.add_code(
#     #         ":=",
#     #         "#" + str(array_start_address),
#     #         array_addr
#     #     )
#     #
#     # def label(self):
#     #     # declare where to jump back after until in repeat-until
#     #     self.ss.push(self.pb.get_line())
#     #
#     #     self.curr_repeats += 1
#     #
#     # def until(self):
#     #     self.curr_repeats -= 1
#     #     condition = self.ss.pop()
#     #     while len(self.ss.stack) > 0 and self.ss.top() == "break":  # [-1] == "break":
#     #         self.pb.modify(self.ss.stack[-2], "JP", self.pb.get_line() + 1)
#     #         self.ss.pop_mult(2)
#     #     self.pb.add_code("JPF", condition,
#     #                      self.ss.top())
#     #     self.ss.pop()
#     #
#     # def push_eq(self):
#     #     self.ss.push("=")
#     #
#     # def start_call(self):
#     #     function_row_id = self.code_gen_st.get_row_id_by_address(self.ss.top())
#     #     self.ss.pop()
#     #     num_parameters = self.code_gen_st.get_row_by_id(function_row_id)["attributes"]
#     #     for i in range(num_parameters, 0, -1):
#     #         temp_addr_param = self.code_gen_st.get_row_by_id(function_row_id + i)["address"]
#     #         self.ss.push(temp_addr_param)
#     #     self.ss.push(num_parameters)
#     #     self.ss.push(num_parameters)
#     #     self.ss.push(self.code_gen_st.get_row_by_id(function_row_id)["lexeme"])
#     #
#     # def end_call(self):
#     #     self.no_more_input = False
#     #     function_name = self.ss.pop()
#     #     counter_args = self.ss.pop()
#     #     # num_parameters = self.ss.pop()
#     #     # if counter_args != 0:
#     #     #     self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#     #     #                                                 error=self.error_num_args,
#     #     #                                                 first_op=name_func
#     #     #                                                 )
#     #     #     self.pop_last_n(counter_args)
#     #
#     #     st_function_row = self.code_gen_st.lookup(function_name)
#     #     index = st_function_row['id']
#     #     if "invocation_address" not in st_function_row or "return_address" not in st_function_row:
#     #         # print("error in function declaration")
#     #         return
#     #     # update the return address temp of function (we want the function to return here after invocation)
#     #     return_address_temp = st_function_row["return_address"]
#     #     self.pb.add_code(
#     #         ":=",
#     #         "#" + str(self.pb.get_line() + 2),
#     #         return_address_temp
#     #     )
#     #     # # if the function is supposed to return a value, we need to push the address of return value to stack
#     #     # if function_row[type_key] != "void":
#     #     #     self.semantic_stack.append(function_row[return_value_key]
#     #     # now that everything is set (including return address and arguments assignment), we can jump to the function
#     #     self.pb.add_code(
#     #         "JP",
#     #         st_function_row["invocation_address"]
#     #     )
#     #     if st_function_row["type"] != "void":
#     #         returnee_copy = self.pb.get_tmp_address(1, st_function_row["type"])
#     #         self.pb.add_code(
#     #             ":=",
#     #             st_function_row["return_value"],
#     #             returnee_copy
#     #         )
#     #         self.ss.push(returnee_copy)
#     #
#     # def print(self):
#     #     self.pb.add_code("print", self.ss.top())
#     #     self.ss.pop()
#     #
#     # def get_operand_type(self, operand):
#     #     is_array = False
#     #     if str(operand).startswith("#"):
#     #         return "int", is_array
#     #     elif str(operand).startswith("@"):
#     #         operand = operand[1:]
#     #     type = self.pb.get_type(int(operand))
#     #     if type.endswith("-arr"):
#     #         type = type[:-4]
#     #         is_array = True
#     #
#     #     return type, is_array
#     #
#     # def arg_input(self):
#     #     # take input argument for function call
#     #     if not self.no_more_input:
#     #         arg = self.ss.pop()
#     #         type_arg = self.get_operand_type(arg)
#     #         name_func = self.ss.pop()
#     #         counter_args = self.ss.pop()
#     #         counter_args -= 1
#     #         num_parameters = self.ss.pop()
#     #         temp_param = self.ss.pop()
#     #         self.pb.add_code(
#     #             ":=",
#     #             arg,
#     #             temp_param
#     #         )
#     #
#     #         type_param = self.get_operand_type(temp_param)
#     #         if type_arg != type_param:
#     #             pass
#     #             # self.semantic_analyzer.raise_semantic_error(line_no=self.current_line,
#     #             #                                             error=self.error_param_type_missmatch,
#     #             #                                             first_op=num_parameters - counter_args,
#     #             #                                             second_op=name_func,
#     #             #                                             third_op=self.get_type_name(type_param),
#     #             #                                             fourth_op=self.get_type_name(type_arg)
#     #             #                                             )
#     #         else:
#     #             if name_func == "output":
#     #                 self.ss.push(arg)
#     #                 self.print("nothing")
#     #
#     #         self.ss.push(num_parameters)
#     #         self.ss.push(counter_args)
#     #         self.ss.push(name_func)
#     # # def p_type(self,token):
#     # #     # p_type
#     # #     # push type into the semantic stack
#     # #     data_type = token.value
#     # #     self.ss.push(data_type)
#     #
#     # def p_id_index(self, token: ctoken.Token): # p_id_index
#     #     # push index of identifier into the semantic stack
#     #     lexeme = token.value
#     #     index = self.scanner.get_symbol_index(lexeme)
#     #     self.ss.push(index)
#     # def p_id(self, token):  # p_id
#     #     # push address of identifier into the semantic stack
#     #     self.p_id_index(token)
#     #     lexeme = token.value
#     #     index = self.scanner.get_symbol_index(lexeme)
#     #     address = self.scanner.symbol_table["address"][index]
#     #     self.ss.push(address)
#     # def p_type(self, token):  # p_type
#     #     # push type into the semantic stack
#     #     data_type = token.value
#     #     self.ss.push(data_type)
#     #
#     # '''
#     # self._scanner must become the scanner used in Parser
#     # if it is change all repetitions of it to self.scanner
#     # '''
#     #
#     # # def p_id_index(self,token):  # p_id_index
#     # #     # push index of identifier into the semantic stack
#     # #     lex = token[1]
#     # #     ind = self.scanner.get_symbol_index(lex)
#     # #     self.ss.push(ind)
#     #
#     # # def p_id(self,token):  # p_id
#     # #     lexeme = token[1]
#     # #     index = self.scanner.get_symbol_index(lexeme)
#     # #     address = self.scanner.symbol_table.symbol_table["address"][index]
#     # #     self.ss.push(address)
#     #
#     # def dec_var(self):  # declare_var
#     #     # assign an address to the identifier, assign 0 to the variable in the program block
#     #     # and update identifier's row in the symbol table
#     #     data_type = self.ss.get_index(-2)
#     #     index = self.ss.get_index(-1)
#     #     self.ss.pop_mult(2)
#     #
#     #     # self.pb.add_code("ASSIGN", 0, self.pb.get_tmp_address())
#     #     self.pb.add_code("ASSIGN", 0, self.pb.get_current_tmp_addr())
#     #     '''
#     #     this is what the update_symbol is supposed to do in Scanner class:
#     #     def update_symbol(self,
#     #                       index: int,
#     #                       symbol_type: str = None,
#     #                       size: int = None,
#     #                       data_type: str = None,
#     #                       scope: int = None,
#     #                       address: int = None):
#     #         if symbol_type is not None:
#     #             self.symbol_table["type"][index] = symbol_type
#     #         if size is not None:
#     #             self.symbol_table["size"][index] = size
#     #         if data_type is not None:
#     #             self.symbol_table["data_type"][index] = data_type
#     #         if scope is not None:
#     #             self.symbol_table["scope"][index] = scope
#     #         if address is not None:
#     #             self.symbol_table["address"][index] = address
#     #
#     #     '''
#     #     self.scanner.symbol_table.update_symbol(index,
#     #                                             symbol_type="var",
#     #                                             size=0,
#     #                                             data_type=data_type,
#     #                                             scope=len(self.scanner.symbol_table.scope_stack),
#     #                                             address=self.pb.get_current_tmp_addr())
#     #     self.pb.update_tmp_addr(4)
#     #
#     # def dec_func(self):  # declare_func
#     #     # update identifier's row in the symbol table, initialize next scope
#     #     # and if function is "main" add a jump to the start of function
#     #     print("THIS IS SEMANTIC STACK",self.ss.stack)
#     #     data_type = self.ss.stack[-2]
#     #     index = self.ss.stack[-1]
#     #     # index, data_type = self.ss.pop_mult(2)
#     #     # self.ss.pop_out_mult(2)
#     #     self.ss.pop_out()
#     #     self.ss.pop_out()
#     #     # self.pop_semantic_stack(2)
#     #
#     #     '''
#     #     this is what the update_symbol is supposed to do in Scanner class:
#     #     def update_symbol(self,
#     #                       index: int,
#     #                       symbol_type: str = None,
#     #                       size: int = None,
#     #                       data_type: str = None,
#     #                       scope: int = None,
#     #                       address: int = None):
#     #         if symbol_type is not None:
#     #             self.symbol_table["type"][index] = symbol_type
#     #         if size is not None:
#     #             self.symbol_table["size"][index] = size
#     #         if data_type is not None:
#     #             self.symbol_table["data_type"][index] = data_type
#     #         if scope is not None:
#     #             self.symbol_table["scope"][index] = scope
#     #         if address is not None:
#     #             self.symbol_table["address"][index] = address
#     #
#     #     '''
#     #     self.scanner.symbol_table.update_symbol(index,
#     #                                             symbol_type="function",
#     #                                             size=0,
#     #                                             data_type=data_type,
#     #                                             scope=len(self.scanner.symbol_table.scope_stack),
#     #                                             address=self.pb.get_len())
#     #     '''
#     #     depends on how scope_stack is implemented in Scanner class
#     #     '''
#     #     # -1 to be implemented
#     #     self.scanner.symbol_table.scope_stack.append(index + 1)
#     #     if self.scanner.symbol_table.symbol_table["lexeme"][index] == "main":
#     #         # line_number = self._semantic_stack[-1]
#     #         # self.pop_semantic_stack(1)
#     #         line_number = self.ss.pop()
#     #         self.pb.add_to_index(line_number, "JP", self.pb.get_len())
#     #         # self.pb.add_to_index(line_number, "JP", self.pb.get_line())
#     #
#     # def end_func(self):  # end_function
#     #     # deletes the current scope
#     #     '''
#     #     depends on how scope_stack is implemented in Scanner class
#     #     '''
#     #     # to be implemented
#     #     scope_start = self.scanner.symbol_table.scope_stack.pop()
#     #     self.scanner.pop_scope(scope_start)
#     #
#     # # def p_type
#     #
#     # def break_jp(self):  # break_jp
#     #     # add an indirect jump to the top of the break stack
#     #     break_temp = self.break_stack[-1]
#     #     self.pb.add_code_str(f"(JP, @{break_temp})")
#     #
#     # def save(self):  # save
#     #     # save an instruction in program block's current line
#     #     current_line_number = self.pb.get_len()
#     #     self.ss.push(current_line_number)
#     #     self.pb.add_code(None, None)
#     #
#     # def jpf_save(self):  # jpf_save
#     #     # add a JPF instruction in line number with a condition both stored in semantic stack to the next line
#     #     # and save an instruction in program block's current line
#     #     # line_number = self._semantic_stack[-1]
#     #     # condition = self._semantic_stack[-2]
#     #     line_number, condition = self.ss.pop_mult(2)
#     #     # self.pop_semantic_stack(2)
#     #
#     #     current_line_number = self.pb.get_len()
#     #     self.pb.add_code_to_index_str(line_number, f"(JPF, {condition}, {current_line_number + 1})")
#     #     self.ss.push(self.pb.get_len())
#     #     self.pb.add_code(None, None)
#     #
#     # def jp(self):  # jp
#     #     # add a JP instruction in line number stored in semantic stack to the current line
#     #     line_number = self.ss.pop()
#     #     # self.pop_semantic_stack(1)
#     #
#     #     current_line_number = self.pb.get_len()
#     #     self.pb.add_code_to_index_str(line_number, f"(JP, {current_line_number},\t,\t)")
#     #
#     # def assign(self):  # assign
#     #     # add an assign instruction
#     #     # source_var = self._semantic_stack[-1]
#     #     # dest_var = self._semantic_stack[-2]
#     #     source_var, dest_var = self.ss.pop_mult(2)
#     #     # self.pop_semantic_stack(1)
#     #
#     #     self.pb.add_code_str(f"(ASSIGN, {source_var}, {dest_var},\t)")
#     #
#     # def array_access(self):  # array_access
#     #     # calculate selected array element address and save result temp in semantic stack
#     #     # array_index = self._semantic_stack[-1]
#     #     # array_base_address = self._semantic_stack[-2]
#     #     array_index, array_base_address = self.ss.pop_mult(2)
#     #     # self.pop_semantic_stack(2)
#     #
#     #     temp1 = self.pb.get_temp()
#     #     temp2 = self.pb.get_temp()
#     #     self.pb.add_code_str(f"(MULT, #4, {array_index}, {temp1})")
#     #     self.pb.add_code_str(f"(ADD, {temp1}, #{array_base_address}, {temp2})")
#     #     self.ss.push(f"@{temp2}")
#     #
#     # def push_op(self):  # p_op
#     #     # push operation to semantic stack
#     #     '''
#     #     update_token must be implemented as explained above
#     #     '''
#     #     operation = self._current_input
#     #     self.ss.push(operation)
#     #
#     # def op(self):  # op
#     #     # add operation instruction
#     #     # operand_1 = self._semantic_stack[-3]
#     #     # operation = self._semantic_stack[-2]
#     #     # operand_2 = self._semantic_stack[-1]
#     #     operand_2, operation, operand_1 = self.ss.pop_mult(3)
#     #     # self.pop_semantic_stack(3)
#     #     if operation == "==":
#     #         assembly_operation = "EQ"
#     #     elif operation == "<":
#     #         assembly_operation = "LT"
#     #     elif operation == "*":
#     #         assembly_operation = "MULT"
#     #     elif operation == "/":
#     #         assembly_operation = "DIV"
#     #     elif operation == "+":
#     #         assembly_operation = "ADD"
#     #     elif operation == "-":
#     #         assembly_operation = "SUB"
#     #     else:
#     #         raise ValueError("Operation is invalid!")
#     #     dest = self.pb.get_temp()
#     #     self.pb.add_code_str(f"({assembly_operation}, {operand_1}, {operand_2}, {dest})")
#     #     self.ss.push(dest)
#     #
#     # def p_num(self, token):  # p_num
#     #     # push number into the semantic stack
#     #     number = int(token[1])
#     #     self.ss.push(number)
#     #
#     # def p_num_tmp(self,token):  # p_num_temp
#     #     # push #number into the semantic stack
#     #     number = int(token[1])
#     #     self.ss.push(f"#{number}")
#     #
#     # def save_break_tmp(self):  # save_break_temp
#     #     # save a temp in break stack
#     #     dest = self.pb.get_temp()
#     #     self.break_stack.append(dest)
#     #
#     # def p_zero(self):
#     #     self.ss.push("0")
#     #
#     # def mult(self):
#     #     # op2 = self.ss.pop()
#     #     # op1 = self.ss.pop()
#     #     op2, op1 = self.ss.pop_mult(2)
#     #     tmp = self.pb.get_tmp_address()
#     #     self.pb.add_code("MUL", op1, op2, tmp)
#     #     self.ss.push(tmp)
#
# # oh oh oh
#
# # class Parser:
# #
# #     instance : Optional['Parser'] = None
# #     @staticmethod
# #     def get_instance(scanner, code_generator):
# #         if Parser.instance is None:
# #             Parser.instance = Parser(scanner, code_generator)
# #         return Parser.instance
# #
# #     _accept: str = "accept"
# #     _shift: str = "shift"
# #     _reduce: str = "reduce"
# #     _goto: str = "goto"
# #
# #     def __init__(self, scanner: Scanner, code_generator: CodeGenerator):
# #         self.current_token = None
# #         self.current_value = None
# #         self.scanner = scanner
# #         self.syntax_errors = []  # [(line_number, error), ]
# #         self.transition_table = {}
# #         self.root = None
# #         self.create_transition_table()
# #         self.code_generator = code_generator
# #
# #         # self._parse_stack: List[Union[str, Node]] = ["0"]
# #         # self._update_current_token()
# #         # self._read_table()
# #
# #     def get_current_token(self):
# #         return self.current_token
# #
# #     def create_transition_table(self):
# #         for non_terminal in grammar.non_terminals:
# #             for terminal in grammar.terminals + ['$'] + grammar.action_symbols:
# #                 if terminal in grammar.action_symbols:
# #                     self.transition_table[(non_terminal, terminal)] = [terminal]
# #                 else:
# #                     self.transition_table[(non_terminal, terminal)] = self.find_production_rule(non_terminal, terminal)
# #
# #     def find_production_rule(self, non_terminal, terminal):
# #         for rule in grammar.rules[non_terminal]:
# #             # print("this is non terminal" , non_terminal)
# #             # print("this is grammar rules", grammar.rules[non_terminal])
# #             # print("this is rule:", rule)
# #             # print("this is terminal", terminal)
# #             # print(rule, self.find_first(rule))
# #             # rule_prime = []
# #             # for st in rule:
# #             #     if st[0] != '#':
# #             #         rule_prime.append(st)
# #             rule_prime = rule
# #             # rule_prime = rule.remove()
# #             # if rule[0] == 'epsilon':
# #             if rule_prime[0] == 'epsilon':
# #                 return rule
# #             if rule_prime[0] in grammar.terminals:
# #                 if rule_prime[0] == terminal:
# #                     return rule
# #             # to handle action symbols
# #             # elif rule[0].startswith('#'):
# #             #     print("find_production_rule - action symbol")
# #             #     return rule
# #             elif terminal in self.find_first(rule_prime):
# #                 return rule
# #         return None
# #
# #     @staticmethod
# #     def find_first(rule):
# #         first = []
# #         for t in rule:
# #             if t in grammar.terminals + ['$']:
# #                 first.append(t)
# #                 break
# #             if t == 'epsilon':
# #                 continue
# #             if t[0] == '#':
# #                 print("find_first - action symbol")
# #                 return first.append(t)
# #             first.extend(grammar.first[t])
# #             if 'epsilon' not in grammar.first[t]:
# #                 break
# #         return first
# #
# #     def get_next_token(self):
# #         ignore = [ctoken.WHITESPACE, ctoken.COMMENT]
# #         while True:
# #             next_token = self.scanner.get_next_token()
# #             if next_token.type not in ignore:
# #                 break
# #
# #         parse_value = next_token.value
# #         if next_token.type == ctoken.EOF:
# #             parse_value = '$'
# #         elif next_token.type == ctoken.ID:
# #             parse_value = 'ID'
# #             # if not self.scanner.symbol_table.exists(next_token.value):
# #             #     self.scanner.symbol_table.append({"index": len(self.scanner.symbol_table)+1, "name": next_token.value, "type": "ID"})
# #         elif next_token.type == ctoken.NUM:
# #             parse_value = 'NUM'
# #         return next_token, parse_value
# #
# #     # def _read_table(self):
# #     #     """Initializes terminals, non_terminals, first_sets, follow_sets, grammar and parse_table."""
# #     #     with open("table.json", mode="r") as table_file:
# #     #         table: dict = json.load(table_file)
# #     #
# #     #     # set of grammars terminals
# #     #     self._terminals: Set[str] = set(table["terminals"])
# #     #     # set of grammars non-terminals
# #     #     self._non_terminals: Set[str] = set(table["non_terminals"])
# #     #     # first and follow sets of non-terminals
# #     #     self._first_sets: Dict[str, Set[str]] = dict(zip(table["first"].keys(), map(set, table["first"].values())))
# #     #     self._follow_sets: Dict[str, Set[str]] = dict(zip(table["follow"].keys(), map(set, table["follow"].values())))
# #     #     # grammar's productions
# #     #     self._grammar: Dict[str, List[str]] = table["grammar"]
# #     #     # SLR parse table
# #     #     self._parse_table: Dict[str, Dict[str, Tuple[str, str]]] = dict(
# #     #         zip(table["parse_table"].keys(), map(lambda row: dict(
# #     #             zip(row.keys(), map(lambda entry: tuple(entry.split("_")), row.values()))
# #     #         ), table["parse_table"].values()))
# #     #     )
# #
# #
# #     # def run(self):
# #     #     """Parses the input. Return True if UNEXPECTED_EOF"""
# #     #     self.code_generator.ss.push(len(self.code_generator.pb.block))
# #     #     self.code_generator.pb.add_code(None,None)
# #     #     while True:
# #     #         # get action from parse_table
# #     #         last_state = self._parse_stack[-1]
# #     #         try:
# #     #             action = self._parse_table[last_state].get(self._current_input)
# #     #         except KeyError:
# #     #             # invalid state
# #     #             raise Exception(f"State \"{last_state}\" does not exist.")
# #     #         if action is not None:
# #     #             # perform the action
# #     #             if action[0] == self._accept:
# #     #                 # accept
# #     #                 break
# #     #             elif action[0] == self._shift:
# #     #                 # push current_token and shift_state into the stack
# #     #                 shift_state = action[1]
# #     #                 self._parse_stack.append(Node(f"({self._current_token[0]}, {self._current_token[1]})"))
# #     #                 self._parse_stack.append(shift_state)
# #     #
# #     #                 # get next token
# #     #                 self._update_current_token()
# #     #             elif action[0] == self._reduce:
# #     #                 # pop rhs of the production from the stack and update parse tree
# #     #                 production_number = action[1]
# #     #                 self.generate_code(int(production_number))
# #     #                 production = self._grammar[production_number]
# #     #                 production_lhs = production[0]
# #     #                 production_rhs_count = self._get_rhs_count(production)
# #     #                 production_lhs_node: Node = Node(production_lhs)
# #     #                 if production_rhs_count == 0:
# #     #                     node = Node("epsilon")
# #     #                     node.parent = production_lhs_node
# #     #                 else:
# #     #                     popped_nodes = []
# #     #                     for _ in range(production_rhs_count):
# #     #                         self._parse_stack.pop()
# #     #                         popped_nodes.append(self._parse_stack.pop())
# #     #                     for node in popped_nodes[::-1]:
# #     #                         node.parent = production_lhs_node
# #     #
# #     #                 # push lhs of the production and goto_state into the stack
# #     #                 last_state = self._parse_stack[-1]
# #     #                 try:
# #     #                     goto_state = self._parse_table[last_state][production_lhs][1]
# #     #                 except KeyError:
# #     #                     # problem in parse_table
# #     #                     raise Exception(f"Goto[{last_state}, {production_lhs}] is empty.")
# #     #                 self._parse_stack.append(production_lhs_node)
# #     #                 self._parse_stack.append(goto_state)
# #     #             else:
# #     #                 # problem in parse_table
# #     #                 raise Exception(f"Unknown action: {action}.")
# #     #         else:
# #     #             if self.handle_error():
# #     #                 # failure if UNEXPECTED_EOF
# #     #                 self._failure = True
# #     #                 break
# #     #
# #     # def handle_error(self) -> bool:
# #     #     """Handles syntax errors. Return True if error is UNEXPECTED_EOF"""
# #     #     # discard the first input
# #     #     self._syntax_errors.append(Error(ErrorType.ILLEGAL_TOKEN, self._current_token[1], self._scanner.line_number))
# #     #     self._update_current_token()
# #     #
# #     #     # pop from stack until state has non-empty goto cell
# #     #     while True:
# #     #         state = self._parse_stack[-1]
# #     #         goto_and_actions_of_current_state = self._parse_table[state].values()
# #     #         # break if the current state has a goto cell
# #     #         if any(map(lambda table_cell: table_cell[0] == self._goto,
# #     #                    goto_and_actions_of_current_state)):
# #     #             break
# #     #         discarded_state, discarded_node = self._parse_stack.pop(), self._parse_stack.pop()
# #     #         self._syntax_errors.append(Error(ErrorType.STACK_CORRECTION, discarded_node, self._scanner.line_number))
# #     #
# #     #     goto_keys = self._get_goto_non_terminals(state)
# #     #     # discard input, while input not in any follow(non_terminal)
# #     #     selected_non_terminal = None
# #     #     while True:
# #     #         for non_terminal in goto_keys:
# #     #             if self._current_input in self._follow_sets[non_terminal]:
# #     #                 selected_non_terminal = non_terminal
# #     #                 break
# #     #         if selected_non_terminal is None:
# #     #             if self._current_input == Scanner.EOF_symbol:
# #     #                 # input is EOF, halt parser
# #     #                 self._syntax_errors.append(Error(ErrorType.UNEXPECTED_EOF, "", self._scanner.line_number))
# #     #                 return True
# #     #             else:
# #     #                 # discard input
# #     #                 self._syntax_errors.append(
# #     #                     Error(ErrorType.TOKEN_DISCARDED, self._current_token[1], self._scanner.line_number))
# #     #                 self._update_current_token()
# #     #         else:
# #     #             # input is in follow(non_terminal)
# #     #             break
# #     #     self._parse_stack.append(Node(selected_non_terminal))
# #     #     self._parse_stack.append(self._parse_table[state][selected_non_terminal][1])
# #     #     self._syntax_errors.append(
# #     #         Error(ErrorType.MISSING_NON_TERMINAL, selected_non_terminal, self._scanner.line_number))
# #     #     return False
# #     #
# #     # def save_parse_tree(self):
# #     #     """Writes parse tree in parse_tree.txt."""
# #     #     # empty file if failure
# #     #     if self._failure:
# #     #         with open("parse_tree.txt", mode='w') as parse_tree_file:
# #     #             parse_tree_file.write("")
# #     #             return
# #     #
# #     #     root = self._parse_stack[1]
# #     #     # add EOF node
# #     #     node = Node("$")
# #     #     node.parent = root
# #     #
# #     #     # write parse tree in the file
# #     #     lines = []
# #     #     for pre, fill, node in RenderTree(root):
# #     #         lines.append(str(f"{pre}{node.name}\n"))
# #     #     with open("parse_tree.txt", mode='w', encoding="utf-8") as parse_tree_file:
# #     #         parse_tree_file.writelines(lines)
# #     #
# #     # def save_syntax_errors(self):
# #     #     """Writes syntax errors in syntax_errors.txt."""
# #     #     with open("syntax_errors.txt", "w") as syntax_errors_file:
# #     #         if len(self._syntax_errors) == 0:
# #     #             syntax_errors_file.write("There is no syntax error.")
# #     #         else:
# #     #             for error in self._syntax_errors:
# #     #                 syntax_errors_file.write(f"{error.content}\n")
# #     #
# #     # def save_semantic_errors(self):
# #     #     """Writes semantic errors in semantic_errors.txt"""
# #     #     with open("semantic_errors.txt", "w") as semantic_errors_file:
# #     #         if len(self._semantic_errors) == 0:
# #     #             semantic_errors_file.write("The input program is semantically correct.")
# #     #
# #     # def save_program_block(self):
# #     #     """Writes program block in output.txt"""
# #     #     with open("output.txt", "w") as output_file:
# #     #         for i in range(len(self._program_block)):
# #     #             output_file.write(f"{i}\t{self._program_block[i]}\n")
# #
# #
# #     # refactore this shiiiiiiiiiiit
# #     # def call_nt(self, nt_name: str, nt_list: list):
# #     #     global eof_reached
# #     #     my_list = nt_list
# #     #     self.current_nt = non_terminals[nt_name]
# #     #     rule_id = self.current_nt.predict_rule(self.current_token)
# #     #     if rule_id is None:
# #     #         token_name = get_token_name(self.current_token)
# #     #         if token_name in self.current_nt.follows:
# #     #             self.report_syntax_error(missing_error_keyword, self.current_nt.name, self.current_line)
# #     #             return  # assume that the current nt is found, and we should continue
# #     #         elif token_name == eof_keyword:
# #     #             if not eof_reached:
# #     #                 self.report_syntax_error(unexpected_error_keyword, 'EOF', self.current_line)
# #     #                 eof_reached = True
# #     #             return
# #     #         else:
# #     #             self.report_syntax_error(illegal_error_keyword, get_token_name(self.current_token), self.current_line)
# #     #             self.update_token()  # assume there was an illegal input and ignore it
# #     #             self.call_nt(nt_name, nt_list)
# #     #             return
# #     #     rule = rules[rule_id]
# #     #     my_list.extend(rule.get_actions())
# #     #     for i in range(len(my_list)):
# #     #         action = my_list[i]
# #     #         if self.current_token == ('eof', '$') and eof_reached:
# #     #             my_list[i] = None
# #     #         elif is_terminal(action):
# #     #             if action == epsilon_keyword:
# #     #                 my_list[i] = (epsilon_keyword, epsilon_keyword)
# #     #             else:
# #     #                 my_list[i] = self.current_token
# #     #                 if not self.match_action(action):
# #     #                     my_list[i] = None
# #     #         elif is_action_symbol(action):
# #     #             self.code_generator.code_gen(action,
# #     #                                          get_action_symbol_input(self.current_token),
# #     #                                          self.current_line)
# #     #         else:
# #     #             child_nt_list = []
# #     #             my_list[i] = (action, child_nt_list)
# #     #             self.call_nt(action, child_nt_list)
# #     #             if len(child_nt_list) == 0:
# #     #                 my_list[i] = None
# #     #
# #     #     # remove None values
# #     #     while None in my_list:
# #     #         my_list.remove(None)
# #     #
# #     # def find_rule_firsts(self, rule_id: int) -> list[str]:
# #     #     rule = rules[rule_id]
# #     #
# #     #     if rule.get_actions()[0] == epsilon_keyword:  # the rule itself is epsilon
# #     #         return rule.get_actions()
# #     #
# #     #     rule_first = []
# #     #     actions = rule.get_actions()
# #     #     for index in range(len(actions)):
# #     #         action = actions[index]
# #     #         if is_terminal(action):
# #     #             rule_first.append(action)
# #     #             return remove_duplicates(rule_first)
# #     #         elif not is_action_symbol(action):
# #     #             # then action is a non-terminal
# #     #             action_first = data[first_keyword][action]
# #     #             if epsilon_keyword in action_first:
# #     #                 if index is not len(actions) - 1:
# #     #                     rule_first += [val for val in action_first if val != epsilon_keyword]
# #     #                 else:
# #     #                     # If we're here, all the actions were terminals that contained epsilon in their firsts.
# #     #                     # So epsilon must be included in rule_first
# #     #                     rule_first += action_first
# #     #             else:
# #     #                 rule_first = action_first + rule_first
# #     #                 return remove_duplicates(rule_first)
# #     #
# #     #     return remove_duplicates(rule_first)
# #
# #     # def _update_current_token(self):
# #     #     """Stores next token in _current_token and updates _current_input."""
# #     #     self._current_token: Tuple[str, str] = self._scanner.get_next_token()
# #     #     self._current_input: str = ""
# #     #     if self._current_token[0] in {Scanner.KEYWORD, Scanner.SYMBOL, Scanner.EOF}:
# #     #         self._current_input = self._current_token[1]
# #     #     else:
# #     #         self._current_input = self._current_token[0]
# #
# #     def parse(self):
# #         # for key, value in self.transition_table.items():
# #         #     print(key, value)
# #         # while self.current_token != '$':
# #         #     break
# #         #     self.current_token = self.get_next_token()
# #         #     print(self.current_token)
# #         self.current_token, self.current_value = self.get_next_token()
# #         # while self.current_value != '{':
# #         #     self.current_token, self.current_value = self.get_next_token()
# #         # print("token and value:" , self.current_token, self.current_value)
# #
# #         stack = [grammar.non_terminals[0]]
# #         node_stack = [Node(grammar.non_terminals[0])]  # Node stack for the parse tree
# #         self.root = node_stack[0]
# #
# #         while stack:
# #             # cnt = 0
# #             stack_top = stack[-1]
# #             node_stack_top = node_stack[-1]
# #             # print('stack_top:', stack_top)
# #
# #             if stack_top in grammar.terminals:
# #                 if stack_top == self.current_value:
# #                     stack.pop()
# #                     node_stack.pop().name = str(self.current_token)
# #                 else:
# #                     self.error(f"missing {stack_top}")
# #                     stack.pop()
# #                     node_stack.pop().name = str(self.current_token)
# #                 self.current_token, self.current_value = self.get_next_token()
# #             elif stack_top == '$':
# #                 if stack_top != self.current_value:
# #                     self.error("Unexpected EOF")
# #                 break
# #             # elif stack_top[0] == '#':
# #             #     print("parse - in action symbol section")
# #             #     cg = CodeGenerator(self.scanner)
# #             #     getattr(cg, stack_top[1:])()
# #             #     print("stack , node stack", stack, node_stack)
# #             #     stack.pop()
# #             #     node_stack.pop()
# #             #     self.current_token, self.current_value = self.get_next_token()
# #                 # stack.append()
# #                 # print("looooooooooooooooook at this", self.current_token, self.current_value)
# #                 # print("stack , node stack", stack, node_stack)
# #
# #             else:
# #                 # print("stack top, current value",stack_top , self.current_value)
# #                 # print("parse - in else section")
# #                 production_rule = self.transition_table[(stack_top, self.current_value)]
# #
# #                 # print(self.transition_table[(stack_top, self.current_value)])
# #                 # if stack_top == "Declaration-list" and self.current_value == "ID" and cnt == 0:
# #                 #     production_rule = ['Declaration', 'Declaration-list']
# #                 #     cnt +=1
# #                 print(production_rule)
# #                 # print(f'production_rule {(stack_top, self.current_value)}:', production_rule)
# #
# #                 if production_rule is None:
# #                     # print("production rule is none")
# #                     # print("grammar.first[stack_top]", grammar.first[stack_top])
# #                     if 'epsilon' in grammar.first[stack_top]:
# #                         production_rule = grammar.rules[stack_top][-1]
# #                         # print("production rule", production_rule)
# #                     else:
# #                         self.error(f"illegal {self.current_value}")
# #                         stack.pop()
# #                         node_stack.pop()
# #                         continue
# #                 if production_rule[0] == 'epsilon':
# #                     Node('epsilon', parent=node_stack.pop())
# #                     stack.pop()
# #                 else:
# #                     # print("in the sus else")
# #                     # print("production rule", production_rule)
# #                     # print('stack before:', stack)
# #                     # print('rule:', production_rule)
# #                     # print('current_value:', self.current_value)
# #                     stack.pop()
# #                     node_stack.pop()
# #                     nodes = []
# #                     for symbol in production_rule:
# #                         nodes.append(Node(symbol, parent=node_stack_top))
# #                     for symbol in reversed(production_rule):
# #                         stack.append(symbol)
# #                         # print("stack append")
# #                         node_stack.append(nodes.pop())
# #                     # print('stack after:', stack)
# #
# #                     self.print_parse_tree()
# #         self.print_parse_tree()
# #
# #     def error(self, message):
# #         # print(f'#{self.scanner.reader.line_number} : syntax error, {message}')
# #         self.syntax_errors.append((self.scanner.reader.line_number, message))
# #
# #     def print_parse_tree(self, file=None):
# #         for pre, _, node in RenderTree(self.root):
# #             print("%s%s" % (pre, node.name), file=file)
# #
# #     def repr_syntax_errors(self):
# #         if not self.syntax_errors:
# #             return 'There is no syntax error.'
# #         return '\n'.join(map(lambda error:
# #                              f'#{str(error[0])} : syntax error, {error[1]}',
# #                              self.syntax_errors))
# #
#
#

import json

rules = []
non_terminals = {}
data = {}

starting_nt = 'Program'
epsilon_keyword = 'EPSILON'
first_keyword = 'first'
follow_keyword = 'follow'
eof_keyword = '$'

illegal_error_keyword = "illegal"
missing_error_keyword = "missing"
unexpected_error_keyword = "Unexpected"

parse_tree_vertical = '│'
parse_tree_horizontal = '──'
parse_tree_corner = '└'
parse_tree_middle = '├'

eof_reached = False


def remove_duplicates(my_list):
    return list(dict.fromkeys(my_list))


def is_terminal(name: str) -> bool:
    return not is_action_symbol(name) and name not in non_terminals


def is_action_symbol(name: str) -> bool:
    if type(name) != str:
        return False
    return name.startswith('#')


def get_token_name(token) -> str:
    token_name = token[0]
    if token_name in ['SYMBOL', 'KEYWORD', 'eof']:
        token_name = token[1]
    return token_name


def get_action_symbol_input(token) -> str:
    token_name = token[1]
    return token_name


class Parser:
    def __init__(self, errors_file, parse_tree_file, scanner, code_gen) -> None:
        self.scanner = scanner
        self.code_generator = code_gen

        self.rules = rules
        self.errors_file = errors_file
        self.parse_tree_file = parse_tree_file
        self.initialize()
        self.current_token = None  # (type, lexeme)
        self.current_line = None
        self.current_nt = non_terminals[starting_nt]
        self.parse_tree = []
        self.syntax_error_output = ""

    def initialize(self):
        global data
        global non_terminals
        with open("data.json", "r") as f:
            data = json.load(f)

        # TODO : in data, $ is the follow of program. But in syntax trees of test cases, it is not like that.

        non_terminals = dict.fromkeys(data["non-terminal"])
        production_rules_file = open("rules.txt", "r")
        production_rule_lines = production_rules_file.readlines()

        rule_index = 0

        for production_rule in production_rule_lines:
            nt, right_side = production_rule.split("->")
            nt = nt.strip()
            right_side = right_side.strip().split("|")
            nt_rule_list = []
            for rule in right_side:
                the_rule = Rule(rule_index, rule.strip().split(" "))
                self.rules.append(the_rule)
                nt_rule_list.append(rule_index)
                rule_index += 1

            non_terminals[nt] = Nonterminal(nt, nt_rule_list)

    def run(self):
        nt_list = []
        self.parse_tree.extend([(self.current_nt.name, nt_list)])
        self.update_token()
        self.call_nt(self.current_nt.name, nt_list)
        # after everything is finished, and we have probably faced $,
        # we should write syntax errors and parse tree in file
        self.finish()

    def finish(self):
        self.write_syntax_errors()
        self.write_parse_tree()

    def call_nt(self, nt_name: str, nt_list: list):
        global eof_reached
        my_list = nt_list
        self.current_nt = non_terminals[nt_name]
        rule_id = self.current_nt.predict_rule(self.current_token)
        if rule_id is None:
            token_name = get_token_name(self.current_token)
            if token_name in self.current_nt.follows:
                self.report_syntax_error(missing_error_keyword, self.current_nt.name, self.current_line)
                return  # assume that the current nt is found, and we should continue
            elif token_name == eof_keyword:
                if not eof_reached:
                    self.report_syntax_error(unexpected_error_keyword, 'EOF', self.current_line)
                    eof_reached = True
                return
            else:
                self.report_syntax_error(illegal_error_keyword, get_token_name(self.current_token), self.current_line)
                self.update_token()  # assume there was an illegal input and ignore it
                self.call_nt(nt_name, nt_list)
                return
        rule = rules[rule_id]
        my_list.extend(rule.get_actions())
        for i in range(len(my_list)):
            action = my_list[i]
            if self.current_token == ('eof', '$') and eof_reached:
                my_list[i] = None
            elif is_terminal(action):
                if action == epsilon_keyword:
                    my_list[i] = (epsilon_keyword, epsilon_keyword)
                else:
                    my_list[i] = self.current_token
                    if not self.match_action(action):
                        my_list[i] = None
            elif is_action_symbol(action):
                self.code_generator.code_gen(action,
                                             get_action_symbol_input(self.current_token),
                                             self.current_line)
            else:
                child_nt_list = []
                my_list[i] = (action, child_nt_list)
                self.call_nt(action, child_nt_list)
                if len(child_nt_list) == 0:
                    my_list[i] = None

        # remove None values
        while None in my_list:
            my_list.remove(None)

    def match_action(self, terminal_action: str):
        global eof_reached
        if self.current_token[1] == eof_keyword and terminal_action is not eof_keyword:
            self.report_syntax_error(unexpected_error_keyword, 'EOF', self.current_line)
            eof_reached = True
            # self.finish()
            return False
        else:
            token_name = get_token_name(self.current_token)
            if token_name == '$':
                eof_reached = True
            if token_name != terminal_action:
                self.report_syntax_error(missing_error_keyword, terminal_action, self.current_line)
                return False
        self.update_token()
        return True

    def update_token(self):
        self.current_token, self.current_line = self.scanner.get_next_token(write_to_file=True)

    def report_syntax_error(self, error_type, token_name, line_number):
        if error_type == unexpected_error_keyword and line_number == 17:
            line_number -= 1
        error_message = "#" + str(line_number) + " : syntax error, " + str(error_type) + " " \
                        + str(token_name) + "\n"
        self.syntax_error_output += error_message

    def write_syntax_errors(self):
        if self.syntax_error_output == '':
            self.syntax_error_output = "There is no syntax error."
        self.errors_file.write(self.syntax_error_output)

    def write_parse_tree(self):
        lines_list = []
        self.draw_subtree(lines_list=lines_list, node=self.parse_tree[0][0], children=self.parse_tree[0][1],
                          ancestors_open=[], last_child=False, first_node=True)
        for line in lines_list:
            self.parse_tree_file.write(line + "\n")

    def draw_subtree(self, lines_list, node, children, ancestors_open, last_child, first_node=False):
        # children is a list of tuples. if the child is a terminal, the tuple is (token type, lexeme)
        # if the child is a non-terminal, the tuple is (node name, [its children])
        Parser.print_node_line(lines_list, ancestors_open, last_child, node, first_node)

        new_ancestors_open = []
        for i in range(len(ancestors_open)):
            if i == len(ancestors_open) - 1:
                new_ancestors_open.append(not last_child)
            else:
                new_ancestors_open.append(ancestors_open[i])

        new_ancestors_open.append(True)
        for index in range(len(children)):
            child = children[index]
            if type(child[1]) == list:
                # means the child was a non-terminal
                next_node = child[0]
                next_children = child[1]
                next_last_child = (index == len(children) - 1)
                self.draw_subtree(lines_list=lines_list, node=next_node, children=next_children,
                                  ancestors_open=new_ancestors_open,
                                  last_child=next_last_child)
            else:
                # the child is a terminal
                next_node = child
                next_children = []
                next_last_child = (index == len(children) - 1)
                self.draw_subtree(lines_list=lines_list, node=next_node, children=next_children,
                                  ancestors_open=new_ancestors_open,
                                  last_child=next_last_child)

    @staticmethod
    def print_node_line(lines_list, ancestors_open, last_child, node, first_node):
        if first_node:
            line = str(node)
            lines_list.append(line)
            return
        line = ''
        for ancestor_index in range(len(ancestors_open) - 1):
            is_open = ancestors_open[ancestor_index]
            if is_open:
                line += parse_tree_vertical
            else:
                line += ' '
            line += '   '
        if last_child:
            line += parse_tree_corner
        else:
            line += parse_tree_middle
        line += parse_tree_horizontal
        if is_terminal(node):
            if node[0] == 'eof' or node[0] == epsilon_keyword:
                line += ' ' + str(node[1]).lower()
            else:
                line += ' (' + str(node[0]) + ', ' + str(node[1]) + ')'
        else:
            line += ' ' + str(node)
        lines_list.append(line)


class Rule:
    def __init__(self, rule_id: int, actions: list[str]):
        self.actions = actions
        self.id = rule_id
        self.firsts = []

    def get_actions(self):
        return self.actions

    def set_first(self, list_firsts: list[str]):
        self.firsts = list_firsts


class Nonterminal:
    def __init__(self, name: str, rule_ids: list[int]):
        self.name = name
        self.rule_ids = rule_ids
        self.firsts = data[first_keyword][self.name]
        self.follows = data[follow_keyword][self.name]
        self.epsilon_rule = None
        for i in rule_ids:
            rule_firsts = self.find_rule_firsts(i)
            if (self.epsilon_rule is None) and (epsilon_keyword in rule_firsts):
                self.epsilon_rule = i
            rules[i].set_first(rule_firsts)

    def find_rule_firsts(self, rule_id: int) -> list[str]:
        rule = rules[rule_id]

        if rule.get_actions()[0] == epsilon_keyword:  # the rule itself is epsilon
            return rule.get_actions()

        rule_first = []
        actions = rule.get_actions()
        for index in range(len(actions)):
            action = actions[index]
            if is_terminal(action):
                rule_first.append(action)
                return remove_duplicates(rule_first)
            elif not is_action_symbol(action):
                # then action is a non-terminal
                action_first = data[first_keyword][action]
                if epsilon_keyword in action_first:
                    if index is not len(actions) - 1:
                        rule_first += [val for val in action_first if val != epsilon_keyword]
                    else:
                        # If we're here, all the actions were terminals that contained epsilon in their firsts.
                        # So epsilon must be included in rule_first
                        rule_first += action_first
                else:
                    rule_first = action_first + rule_first
                    return remove_duplicates(rule_first)

        return remove_duplicates(rule_first)

    def predict_rule(self, current_token: str) -> int:
        # predicts the id of the rule to apply based on the current token. If no rule was found, return None
        token_name = get_token_name(current_token)
        for rule_id in self.rule_ids:
            rule = rules[rule_id]
            if token_name in rule.firsts:
                return rule_id
        if token_name in self.follows:
            return self.epsilon_rule  # it's either None or one of the rules that has epsilon in its first set
        return None


























# class Parser:
#     # instance : Optional['Parser'] = None
#     # @staticmethod
#     # def get_instance(scanner):
#     #     if Parser.instance == None:
#     #         Parser.instance = Parser(scanner)
#     #     return Parser.instance
#     def __init__(self, scanner: Scanner):
#         self.current_token = None
#         self.current_value = None
#         self.scanner = scanner
#         self.syntax_errors = []  # [(line_number, error), ]
#         self.transition_table = {}
#         self.root = None
#         self.create_transition_table()
#         self.heap_manager = HeapManager.get_instance()
#         self.symbol_table = SymbolTable.get_instance(self.heap_manager)
#         self.code_generator = CodeGenerator(self.symbol_table,self.heap_manager)
#         # self.get_curr_input()
#
#     def get_curr_input(self):
#         self.code_generator._current_token = self.get_next_token()
#         # print(self._current_token)
#         # print(self._current_token[0])
#         # print(self._current_token[1])
#         # print(self._current_token[0].type)
#         # self._current_token = self.parsre.get_current_token()[0]
#         toCheck = KEYWORD + SYMBOL + "$"
#         if self.code_generator._current_token == None:
#             return
#         if self.code_generator._current_token[0].type in toCheck:
#             self._current_input = self.code_generator._current_token[1]
#         else:
#             self.code_generator._current_input = self.code_generator._current_token[0]
#
#
#     def create_transition_table(self):
#         for non_terminal in grammar.non_terminals:
#             for terminal in grammar.terminals + ['$']:
#                 self.transition_table[(non_terminal, terminal)] = self.find_production_rule(non_terminal, terminal)
#
#     def find_production_rule(self, non_terminal, terminal):
#         for rule in grammar.rules[non_terminal]:
#             # print(rule, self.find_first(rule))
#             if rule[0] == 'epsilon':
#                 return rule
#             if rule[0] in grammar.terminals:
#                 if rule[0] == terminal:
#                     return rule
#             elif terminal in self.find_first(rule):
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
#             first.extend(grammar.first[t])
#             if 'epsilon' not in grammar.first[t]:
#                 break
#         return first
#
#     def get_next_token(self):
#         ignore = [ctoken.WHITESPACE, ctoken.COMMENT]
#         while True:
#             next_token = self.scanner.get_next_token()
#             print(next_token)
#             if next_token[0][0] not in ignore:
#                 break
#
#         parse_value = next_token[0][1]
#         if next_token[0][0] == ctoken.EOF:
#             parse_value = '$'
#         elif next_token[0][0] == ctoken.ID:
#             parse_value = 'ID'
#         elif next_token[0][0] == ctoken.NUM:
#             parse_value = 'NUM'
#         return next_token, parse_value
#
#     def parse(self):
#         # for key, value in self.transition_table.items():
#         #     print(key, value)
#         # while self.current_token != '$':
#         #     break
#         #     self.current_token = self.get_next_token()
#         #     print(self.current_token)
#
#         self.current_token, self.current_value = self.get_next_token()
#
#         stack = [grammar.non_terminals[0]]
#         node_stack = [Node(grammar.non_terminals[0])]  # Node stack for the parse tree
#         self.root = node_stack[0]
#
#         while stack:
#             stack_top = stack[-1]
#             node_stack_top = node_stack[-1]
#             # print('stack_top:', stack_top)
#
#             if stack_top in grammar.terminals:
#                 if stack_top == self.current_value:
#                     stack.pop()
#                     node_stack.pop().name = str(self.current_token)
#                     self.current_token, self.current_value = self.get_next_token()
#                 else:
#                     self.error(f"missing {stack_top}")
#                     stack.pop()
#                     node = node_stack.pop()
#                     parent_node = node.parent
#                     parent_node.children = [child for child in parent_node.children if child != node]
#                     while stack[-1] in grammar.terminals:
#                         stack.pop()
#                         node_stack.pop()
#                     while self.current_value not in grammar.follow[stack[-1]] and self.current_value != '$':
#                         if stack[-1] == 'Statement-list' and self.current_value == ';':
#                             break
#                         self.error(f"illegal {self.current_value}")
#                         self.current_token, self.current_value = self.get_next_token()
#                     if self.current_value == '$':
#                         self.scanner.reader.line_number += 1
#                         self.error("Unexpected EOF")
#                         while stack:
#                             stack.pop()
#                             node = node_stack.pop()
#                             parent_node = node.parent
#                             parent_node.children = [child for child in parent_node.children if child != node]
#             elif stack_top == '$':
#                 break
#             else:
#                 production_rule = self.transition_table[(stack_top, self.current_value)]
#                 curr_tok = self.current_token
#                 line_num = self.current_token[1]
#                 '''
#                 according to the rules below and action symbols that start with # we continue:
#                 1. Program -> Declaration-list #call_main $
#                 2. Declaration-list -> Declaration Declaration-list | EPSILON
#                 3. Declaration -> Declaration-initial Declaration-prime
#                 4. Declaration-initial -> #push_type Type-specifier #declare_id ID
#                 5. Declaration-prime -> Fun-declaration-prime | Var-declaration-prime
#                 6. Var-declaration-prime -> ; | [ #push_num NUM ] #declare_array ;
#                 7. Fun-declaration-prime -> #push_function ( #start_func Params #end_func_params ) #save
#                 #set_function_info Compound-stmt #return_manual #jump_out #pop_function #end_scope
#                 8. Type-specifier -> int | void
#                 9. Params -> #push_type int #declare_id ID Param-prime Param-list | void
#                 10. Param-list -> , #add_param Param Param-list | EPSILON #add_param
#                 11. Param -> Declaration-initial Param-prime
#                 12. Param-prime -> [ ] #declare_entry_array | EPSILON
#                 13. Compound-stmt -> { #show_scope_start Declaration-list Statement-list #pop_scope }
#                 14. Statement-list -> Statement Statement-list | EPSILON
#                 15. Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt
#                 16. Expression-stmt -> Expression ; | #break break ; | ;
#                 17. Selection-stmt -> if ( Expression ) #save Statement else #jpf_save Statement #jp
#                 18. Iteration-stmt -> repeat #label Statement until ( Expression ) #until
#                 19. Return-stmt -> return Return-stmt-prime #return
#                 20. Return-stmt-prime -> ; | Expression ;
#                 21. Expression -> Simple-expression-zegond | #id ID B
#                 22. B -> #push_eq = Expression #assign | [ Expression ] #array_calc H | Simple-expression-prime
#                 23. H -> #push_eq = Expression #assign | G D C
#                 24. Simple-expression-zegond -> Additive-expression-zegond C
#                 25. Simple-expression-prime -> Additive-expression-prime C
#                 26. C -> #push_op Relop Additive-expression #do_op | EPSILON
#                 27. Relop -> < | ==
#                 28. Additive-expression -> Term D
#                 29. Additive-expression-prime -> Term-prime D
#                 30. Additive-expression-zegond -> Term-zegond D
#                 31. D -> #push_op Addop Term #do_op D | EPSILON
#                 32. Addop -> + | -
#                 33. Term -> Factor G
#                 34. Term-prime -> Factor-prime G
#                 35. Term-zegond -> Factor-zegond G
#                 36. G -> #push_op * Factor #do_op G | EPSILON
#                 37. Factor -> ( Expression ) | #id ID Var-call-prime | #push_num NUM
#                 38. Var-call-prime -> ( #start_call Args ) #end_call | Var-prime
#                 39. Var-prime -> [ Expression ] #array_calc | EPSILON
#                 40. Factor-prime -> ( #start_call Args ) #end_call | EPSILON
#                 41. Factor-zegond -> ( Expression ) | #push_num NUM
#                 42. Args -> Arg-list | EPSILON
#                 43. Arg-list -> Expression Arg-list-prime
#                 44. Arg-list-prime -> , #arg_input Expression Arg-list-prime | EPSILON #arg_inpu
#                 '''
#                 if production_rule == ['Declaration-list'] and stack_top=='Program':
#                     self.code_generator.code_gen("call_main",curr_tok,line_num)
#                 elif production_rule == ['Type-specifier', 'ID'] and stack_top=='Declaration_initial':
#                     self.code_generator.code_gen("push_type",curr_tok,line_num)
#                     self.code_generator.code_gen("declare_id",curr_tok,line_num)
#                 elif production_rule == ['[', 'NUM', ']', ';'] and stack_top == 'Var-declaration-prime':
#                     self.code_generator.code_gen("push_num",curr_tok,line_num)
#                     self.code_generator.code_gen("declare_id",curr_tok,line_num)
#                 elif production_rule == ['(', 'Params', ')', 'Compound-stmt'] and stack_top == 'Fun-declaration-prime':
#                     self.code_generator.code_gen("push_function",curr_tok,line_num)
#                     self.code_generator.code_gen("start_func",curr_tok,line_num)
#                     self.code_generator.code_gen("end_func_params", curr_tok,line_num)
#                     self.code_generator.code_gen("save ",curr_tok,line_num)
#                     self.code_generator.code_gen("set_function_info", curr_tok,line_num)
#                     self.code_generator.code_gen("return_manual",curr_tok,line_num)
#                     self.code_generator.code_gen("jump_out",curr_tok,line_num)
#                     self.code_generator.code_gen("pop_function", curr_tok,line_num)
#                     self.code_generator.code_gen("end_scope", curr_tok,line_num)
#
#                 elif production_rule == ['int', 'ID', 'Param-prime', 'Param-list'] and stack_top == 'Params':
#                     self.code_generator.code_gen("push_type",curr_tok,line_num)
#                     self.code_generator.code_gen("declare_id",curr_tok,line_num)
#                 elif production_rule == [',', 'Param', 'Param-list'] and stack_top == ' Param-list':
#                     self.code_generator.code_gen("add_param", curr_tok,line_num)
#                 elif production_rule == ['epsilon'] and stack_top == 'Param-list':
#                     self.code_generator.code_gen("add_param",curr_tok,line_num)
#                 elif stack_top == 'Param-prime' and production_rule == ['[', ']']:
#                     self.code_generator.code_gen("declare_entry_array",curr_tok,line_num)
#                 elif stack_top == 'Compound-stmt' and production_rule == ['{', 'Declaration-list', 'Statement-list', '}']:
#                     self.code_generator.code_gen("show_scope_start",curr_tok,line_num)
#
#                 elif stack_top == 'Expression-stmt' and production_rule == ['break', ';'] :
#                     self.code_generator.code_gen("break",curr_tok,line_num)
#                 elif stack_top == 'Selection-stmt' and production_rule == ['if', '(', 'Expression', ')', 'Statement', 'else', 'Statement']:
#                     self.code_generator.code_gen("save",curr_tok,line_num)
#                     self.code_generator.code_gen("jpf_save",curr_tok,line_num)
#                     self.code_generator.code_gen("jp",curr_tok,line_num)
#                 elif stack_top == 'Iteration-stmt' and production_rule == ['repeat', 'Statement', 'until', '(', 'Expression', ')']:
#                     self.code_generator.code_gen("label",curr_tok,line_num)
#                     self.code_generator.code_gen("until",curr_tok,line_num)
#                 elif stack_top == 'Return-stmt' and production_rule == ['return', 'Return-stmt-prime']:
#                     self.code_generator.code_gen("return",curr_tok,line_num)
#                 elif stack_top == 'Expression' and production_rule == ['ID', 'B']:
#                     self.code_generator.code_gen("id",curr_tok,line_num)
#                 elif stack_top in ['B','H'] and production_rule == ['=', 'Expression']:
#                     self.code_generator.code_gen("push_eq",curr_tok,line_num)
#                     self.code_generator.code_gen("assign",curr_tok,line_num)
#                 elif stack_top == 'B' and production_rule == ['[', 'Expression', ']', 'H']:
#                     self.code_generator.code_gen("array_calc",curr_tok,line_num)
#                 elif stack_top == 'C' and production_rule == ['Relop', 'Additive-expression']:
#                     self.code_generator.code_gen("push_op",curr_tok,line_num)
#                     self.code_generator.code_gen("do_op",curr_tok,line_num)
#                 elif stack_top == 'D' and production_rule == ['Addop', 'Term', 'D']:
#                     self.code_generator.code_gen("push_op", curr_tok, line_num)
#                     self.code_generator.code_gen("do_op", curr_tok, line_num)
#                 elif stack_top == 'G' and production_rule == ['*', 'Factor', 'G']:
#                     self.code_generator.code_gen("push_op", curr_tok, line_num)
#                     self.code_generator.code_gen("do_op", curr_tok, line_num)
#                 elif stack_top == 'Factor' and production_rule == ['ID', 'Var-call-prime']:
#                     self.code_generator.code_gen("id", curr_tok,line_num)
#                 elif stack_top == 'Factor' and production_rule == ['NUM']:
#                     self.code_generator.code_gen("push_num",curr_tok,line_num)
#                 elif stack_top == 'Var-call-prime' and production_rule == ['(', 'Args', ')']:
#                     self.code_generator.code_gen("start_call",curr_tok,line_num)
#                     self.code_generator.code_gen("end_call",curr_tok,line_num)
#                 elif stack_top =='Var-prime' and production_rule == ['[', 'Expression', ']']:
#                     self.code_generator.code_gen("array_calc",curr_tok,line_num)
#                 elif stack_top == 'Factor-prime' and production_rule ==['(', 'Args', ')']:
#                     self.code_generator.code_gen("start_call", curr_tok, line_num)
#                     self.code_generator.code_gen("end_call", curr_tok, line_num)
#                 elif stack_top == 'Factor-zegond' and production_rule == ['NUM']:
#                     self.code_generator.code_gen("push_num",curr_tok,line_num)
#                 elif stack_top == 'Arg-list-prime':
#                     if production_rule == [',', 'Expression', 'Arg-list-prime']:
#                         self.code_generator.code_gen("arg_input",curr_tok,line_num)
#                     elif production_rule == ['epsilon']:
#                         self.code_generator.code_gen("arg_input",curr_tok,line_num)
#
#
#
#
#
#                 # if production_rule == ['Declaration-list']:
#                 #     print(1)
#                 #     self.code_generator.call_main()
#                 # elif production_rule == ['Type-specifier', 'ID']:
#                 #     print(2)
#                 #     self.code_generator.p_type(self.current_token)
#                 #     self.code_generator.declare_id()
#                 # elif production_rule == [';']:
#                 #     self.code_generator.dec_var()
#                 # elif production_rule == ['[', 'NUM', ']', ';']:
#                 #     self.code_generator.dec_array()
#                 # elif production_rule == ['(', 'Params', ')', 'Compound-stmt']:
#                 #     self.code_generator.dec_func()
#                 #     self.code_generator.end_func()
#                 # elif production_rule == ['int', 'ID', 'Param-prime', 'Param-list']:
#                 #     self.code_generator.p_type(self.current_token)
#                 #     self.code_generator.declare_id()
#                 # elif production_rule == ['[', ']']:
#                 #     self.code_generator.declare_entry_array()
#                 # elif production_rule == ['break', ';']:
#                 #     self.code_generator.break_jp()
#                 # elif production_rule == ['repeat', 'Statement', 'until', '(', 'Expression', ')']:
#                 #     self.code_generator.label()
#                 #     self.code_generator.until()
#                 # elif production_rule == ['ID', 'B']:
#                 #     self.code_generator.p_id(self.current_token)
#                 # elif production_rule == ['=', 'Expression']:
#                 #     self.code_generator.push_eq()
#                 #     self.code_generator.assign()
#                 # elif production_rule == ['[', 'Expression', ']', 'H']:
#                 #     self.code_generator.array_access()
#                 # elif production_rule == ['Relop', 'Additive-expression']:
#                 #     self.code_generator.push_op()
#                 #     self.code_generator.op()
#                 # elif production_rule == ['Addop', 'Term', 'D']:
#                 #     self.code_generator.push_op()
#                 #     self.code_generator.op()
#                 # elif production_rule == ['*', 'Factor', 'G']:
#                 #     self.code_generator.push_op()
#                 #     self.code_generator.op()
#                 # elif production_rule == ['ID', 'Var-call-prime']:
#                 #     self.code_generator.p_id(self.current_token)
#                 # elif production_rule == ['NUM']:
#                 #     self.code_generator.p_num(self.current_token)
#                 # elif production_rule == ['(', 'Args', ')']:
#                 #     self.code_generator.start_call()
#                 #     self.code_generator.end_call()
#                 # elif production_rule == ['[', 'Expression', ']']:
#                 #     self.code_generator.array_access()
#                 # elif production_rule == ['(', 'Args', ')']:
#                 #     self.code_generator.start_call()
#                 #     self.code_generator.end_call()
#                 # elif production_rule == ['NUM']:
#                 #     self.code_generator.p_num(self.current_token)
#                 # elif production_rule == [',', 'Expression', 'Arg-list-prime']:
#                 #     self.code_generator.arg_input()
#                 # elif production_rule == ['epsilon'] and stack_top == 'Arg-list-prime':
#                 #     self.code_generator.arg_input()
#
#                 print(f'production_rule {(stack_top, self.current_value)}:', production_rule)
#
#                 if production_rule is None:
#                     if self.current_value == '$':
#                         self.error("Unexpected EOF")
#                         while stack:
#                             stack.pop()
#                             node = node_stack.pop()
#                             parent_node = node.parent
#                             parent_node.children = [child for child in parent_node.children if child != node]
#                         continue
#                     if 'epsilon' in grammar.first[stack_top]:
#                         production_rule = grammar.rules[stack_top][-1]
#                     else:
#                         self.error(f"illegal {self.current_value}")
#                         stack.pop()
#                         node_stack.pop()
#                         continue
#                 if production_rule[0] == 'epsilon':
#                     Node('epsilon', parent=node_stack.pop())
#                     stack.pop()
#                 else:
#                     print('stack before:', stack)
#                     print('rule:', production_rule)
#                     print('current_value:', self.current_value)
#                     stack.pop()
#                     node_stack.pop()
#                     nodes = []
#                     for symbol in production_rule:
#                         nodes.append(Node(symbol, parent=node_stack_top))
#                     for symbol in reversed(production_rule):
#                         stack.append(symbol)
#                         node_stack.append(nodes.pop())
#                     print('stack after:', stack)
#
#                     # self.print_parse_tree()
#         self.print_parse_tree()
#
#     def error(self, message):
#         print(f'#{self.scanner.reader.line_number} : syntax error, {message}')
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
#     # def print_code(self, of):
#     #     block = self.code_generator.bl