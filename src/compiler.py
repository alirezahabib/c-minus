"""
C- compiler (Phase 2 - Parser)
Compiler Design | Sharif University of Technology
Abolfazl Eshagh    9910105
Alireza  Habibzadeh          99109393
"""

from parser import Parser
from scanner import Scanner, State
from parser import HeapManager, SymbolTable
heap_manager=HeapManager()
symbol_table=SymbolTable(heap_manager)

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
from parser import HeapManager, SymbolTable
# from intercode_gen import CodeGenerator
from parser import CodeGenerator
list_needed_files = ["intermediate_code", "input", "semantic_errors"]
def create_file_by_mode(name, mode, encoding='utf-8'):
    name_pure = name.split(".")[0]
    if name_pure in list_needed_files:
        return open(name, mode, encoding=encoding)
    return DummyFile()


class DummyFile:
    def __init__(self):
        pass

    def write(self, text):
        pass

    def close(self):
        pass

in_file = create_file_by_mode("input.txt", "r")
out_file = create_file_by_mode("tokens.txt", "w+")
lex_file = create_file_by_mode("lexical_errors.txt", "w+")
sym_file = create_file_by_mode("symbol_table.txt", "w+")
parser_errors_file = create_file_by_mode("syntax_errors.txt", "w+")
parser_tree_file = create_file_by_mode("parse_tree.txt", "w+", encoding='utf-8')
generated_code_file = create_file_by_mode("intermediate_code.txt", "w+")
semantic_errors_file = create_file_by_mode("semantic_errors.txt", "w+")

scanner = Scanner(
    input_file=in_file,
    output_file=out_file,
    lex_file=lex_file,
    sym_file=sym_file,
    symbol_table=symbol_table
)

code_generator = CodeGenerator(symbol_table=symbol_table, heap=heap_manager)

parser = Parser(errors_file=parser_errors_file, parse_tree_file=parser_tree_file,
                scanner=scanner, code_gen=code_generator)
parser.run()

code_generator.write_pb_to_file(generated_code_file, semantic_errors_file)

in_file.close()
out_file.close()
lex_file.close()
sym_file.close()
parser_errors_file.close()
semantic_errors_file.close()
generated_code_file.close()
