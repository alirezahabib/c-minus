# from intercode_gen import Address
from typing import Optional


class Address:
    instance: Optional["Address"] = None

    @staticmethod
    def get_instance():
        if Address.instance is None:
            Address.instance = Address()
        return Address.instance

    def __init__(self):
        # self.address = address
        # self.last_tmp = Address(500 - 4)
        # self.last_addr = Address(100 - 4)
        self.last_tmp = 500 - 4
        self.last_addr = 100 - 4
        self.all_addresses = []

    def set_indirect(self, address):
        address = "@" + str(address)
        return address

    def __str__(self, address):
        return str(address)

    def get_current_tmp_addr(self):
        return self.last_tmp

    def get_tmp_address(self):
        self.last_tmp += 4
        self.all_addresses.append(self.last_tmp)
        # return Address(self.last_tmp.address)
        return self.last_tmp

    def update_tmp_addr(self, size):
        self.last_tmp += size

    def get_address(self):
        self.last_addr += 1
        self.all_addresses.append(self.last_addr)
        # return Address(self.last_addr.address)
        return self.last_addr

    def get_temp(self):
        temp = self.last_tmp
        self.all_addresses.append(temp)
        self.last_tmp += 4

        return temp

    def get_tmp_address_by_size(self, entries_type, array_size):
        self.last_tmp += entries_type * array_size
        self.all_addresses.append(self.last_tmp)
        # return Address(self.last_tmp.address)
        return self.last_tmp
    def get_next_addr(self,addr):
        return self.all_addresses[self.all_addresses.index(addr)+1]

    def get_type(self, addr):
        next_addr = self.get_next_addr(addr)
        if next_addr - addr == 4:
            return "int"
        elif next_addr - addr == 1:
            return "void"


class Symbol_Table:
    instance : Optional["Symbol_Table"] = None

    @staticmethod
    def get_instance():
        if Symbol_Table.instance is None:
            Symbol_Table.instance = Symbol_Table()
        return Symbol_Table.instance

    def __init__(self) -> None:
        # row properties are id, lexeme, proc/func/var/param (kind), No. Arg/Cell (attributes), type, scope, address
        self.address_to_row = {}
        self.table = []
        self.current_scope = 0
        self.scope_stack = [0]
        self.insert("output")
        self.modify_last_row("func", "void")
        self.table[-1]['attributes'] = 1
        self.address = Address.get_instance()
        self.table.append({'id': 1, 'lexeme': 'init_lex', 'kind': "param", 'attributes': '-', 'type': "int",
                           'scope': 1, 'address': Address.get_instance().get_tmp_address()})  # ("int", 1)
        # self.scanner = scanner

    def insert(self, lexeme):
        dict = {'id': len(self.table), 'lexeme': lexeme}
        self.table.append(dict)
        # print(type(self.table[-1]))
        # print(self.table[-1])
        # self.table[-1]['added'] = "added?"
        # print(self.table[-1])

    def modify_last_row(self, kind, type):
        self.table[-1]['kind'] = kind
        self.table[-1]['type'] = type
        # self.table[-1]['address'] = self.address.get_tmp_address()  # (type, 1)
        self.table[-1]['address'] = Address.get_instance().get_tmp_address()
        self.table[-1]['scope'] = self.current_scope
        self.table[-1]['attributes'] = '-'
        self.address_to_row[self.table[-1]['address']] = len(self.table) - 1

    def modify_func_row(self, row_index, invocation_addr, return_addr, return_value):
        self.table[row_index]['invocation_address'] = invocation_addr
        self.table[row_index]['return_address'] = return_addr
        self.table[row_index]['return_value'] = return_value

    def modify_attributes_last_row(self, num_attributes):
        # self.table[-1]['attributes'] = num_attributes
        self.modify_attributes_by_index(-1, num_attributes)

    def modify_attributes_by_index(self, row_id, num_attributes, arr_func: bool = True):
        self.table[row_id]['attributes'] = num_attributes

    def modify_kind_last_row(self, kind):
        self.table[-1]['kind'] = kind

    def add_scope(self):
        self.current_scope += 1
        self.scope_stack.append(len(self.table))

    def get_len(self):
        return len(self.table)

    def end_scope(self):
        remove_ind = self.get_len()
        for i in range(self.scope_stack[-1], self.get_len()):
            if self.has_type(i) or self.table[i]['kind'] != "param":
                remove_ind = i
                break

        self.table = self.table[:remove_ind]

        self.current_scope -= 1
        self.scope_stack.pop()

    def declare_array(self, num_of_cells):
        self.table[-1]['attributes'] = num_of_cells

    def lookup(self, name, start_ind=0, is_declaring=False, end_ind=-1) -> dict:
        end_index = end_ind
        current_scope = -1
        toReturn = None

        if end_ind == -1:
            end_index = len(self.table)
            if is_declaring and self.has_type(-1):
                end_index -= 1

        while len(self.scope_stack) >= -current_scope:
            # print("inside while")
            # print(self.scope_stack, "this is scope stack")
            start = self.scope_stack[current_scope]

            for i in range(start, end_index):
                # print("inside for")
                row = self.table[i]
                # print("row_i before:", row_i)
                # print("lexeme ", row_i['lexeme'])
                # if not self.is_useless_row(i):
                # print("inside if at all")
                if current_scope != -1 and row['kind'] == "param":
                    print("inside wrong if")
                    pass
                elif row['lexeme'] == name:
                    print("inside right elif")
                    print("row_i ", row)
                    return row

            current_scope -= 1
            end_index = start

        return toReturn

    def remove_last_row(self):
        self.table.pop()

    def has_type(self, id):
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


class PB:
    instance : Optional['PB'] = None
    @staticmethod
    def get_instance():
        if PB.instance is None:
            PB.instance = PB()
        return PB.instance
    def __init__(self):
        self.block = []
        self.line = 0
        self.last_tmp = 500 - 4
        self.last_addr = 100 - 4
        self.all_addresses = []

    def get_len(self):
        return len(self.block)

    def get_line(self):
        return self.line

    def get_current_tmp_addr(self):
        return self.last_tmp

    def add_code(self, operation, op1, op2=None, op3=None):
        self.block.append([operation, op1, op2, op3])
        self.line += 1

    def add_to_index(self, index, operation, op1, op2=None, op3=None):
        self.block.insert(index, [operation, op1, op2, op3])
        self.line += 1

    def get_tmp_address(self):
        self.last_tmp += 4
        self.all_addresses.append(self.last_tmp)
        return self.last_tmp

    # def get_current_tmp_addr(self):
    #     return self.last_tmp

    def update_tmp_addr(self, size):
        self.last_tmp += size

    def get_address(self):
        self.last_addr += 1
        self.all_addresses.append(self.last_addr)
        return self.last_addr

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
        temp = self.last_tmp
        self.all_addresses.append(temp)
        self.last_tmp += 4

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
        self.last_tmp += entries_type * array_size
        self.all_addresses.append(self.last_tmp)
        return self.last_tmp

    def get_next_addr(self,addr):
        return self.all_addresses[self.all_addresses.index(addr)+1]

    def get_type(self, addr):
        next_addr = self.get_next_addr(addr)
        if next_addr - addr == 4:
            return "int"
        elif next_addr - addr == 1:
            return "void"