"""
C- compiler (Phase 2 - Parser)
Compiler Design | Sharif University of Technology
Abolfazl Eshagh    9910105
Alireza  Habibzadeh          99109393
"""
import os

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
list_needed_files = ["output", "input", "semantic_errors"]
other_list = []
for i in range(10):
    list_needed_files += [f"test/Fixed_TestCases_3/TestCases/T{i+1}/input"]
    list_needed_files += [f"test/Fixed_TestCases_3/TestCases/T{i+1}/expected"]
    list_needed_files += [f"tester/results/result{i+1}"]
list_needed_files += [f"tester/output"]
list_needed_files += ["tester/out"]

# for i in range(10):
#     # other_list.append(f"test/T{i+1}/input.txt")
#     other_list.append(f"tester/results/result{i+1}.txt")
#     other_list.append(f"test/Fixed_TestCases_3/TestCases/T{i+1}/input.txt")
# other_list.append("tester/output.txt")
# list_needed_files += other_list
# list_needed_files.append("tester/results/output.txt")
print("this is list_needed_files", list_needed_files)
def create_file_by_mode(name, mode, encoding='utf-8'):
    name_pure = name.split(".")[0]
    # print("for name:", name, "we get:" ,name_pure)
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

# in_file = create_file_by_mode("input.txt", "r")
# out_file = create_file_by_mode("tokens.txt", "w+")
# lex_file = create_file_by_mode("lexical_errors.txt", "w+")
# sym_file = create_file_by_mode("symbol_table.txt", "w+")
# parser_errors_file = create_file_by_mode("syntax_errors.txt", "w+")
# parser_tree_file = create_file_by_mode("parse_tree.txt", "w+", encoding='utf-8')
# generated_code_file = create_file_by_mode("output.txt", "w+")
# semantic_errors_file = create_file_by_mode("semantic_errors.txt", "w+")
#
# scanner = Scanner(
#     input_file=in_file,
#     output_file=out_file,
#     lex_file=lex_file,
#     sym_file=sym_file,
#     symbol_table=symbol_table
# )
#
# code_generator = CodeGenerator(symbol_table=symbol_table, heap=heap_manager)
#
# parser = Parser(errors_file=parser_errors_file, parse_tree_file=parser_tree_file,
#                 scanner=scanner, code_gen=code_generator)
# parser.run()
#
# code_generator.write_pb_to_file(generated_code_file, semantic_errors_file)
#
#
#
#
# # tester()
# # print("test finished")
#
#
#
# in_file.close()
# out_file.close()
# lex_file.close()
# sym_file.close()
# parser_errors_file.close()
# semantic_errors_file.close()
# generated_code_file.close()
# tester()
# print("test finished")
import tester.vm as vm
import shutil
import filecmp
def tester():
    for i in range(10):
        ''' we wanna run the compiler on input.txt files stored in test folder, input.txt for testcase1 stored in T1 folder in test folder
            input.txt for testcase2 stored in T2 folder in test folder and so on
            we compile each input.txt file and store the output in output.txt file in tester folder
            we run vm on output.txt file wich stores the result in out.txt file in tester folder
            we compare the out.txt file in tester folder with expected.txt file in T1 folder for testcase1 and so on
            the input files will be provided and we need to read them
            the output files will not exist at i==0 and we have to create them and write the output in them
            for the next iterations we need to edit the output files and write the output in them
        '''

        in_file = create_file_by_mode(f"test/Fixed_TestCases_3/TestCases/T{i+1}/input.txt", "r")
        # print("IN FILE FOR I:", i+1, "is", in_file)
        out_file = create_file_by_mode("tokens.txt", "w+")
        lex_file = create_file_by_mode("lexical_errors.txt", "w+")
        sym_file = create_file_by_mode("symbol_table.txt", "w+")
        parser_errors_file = create_file_by_mode("syntax_errors.txt", "w+")
        parser_tree_file = create_file_by_mode("parse_tree.txt", "w+", encoding='utf-8')
        generated_code_file = create_file_by_mode("tester/output.txt", "w+")
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
        print("THIS IS I:", i+1)
        print(generated_code_file.read())

        vm.main()

        out_vm_file = create_file_by_mode("tester/out.txt", "r")
        expected_file = create_file_by_mode(f"test/Fixed_TestCases_3/TestCases/T{i+1}/expected.txt", "r")
        var_out = out_vm_file.read()
        var_expected = expected_file.read()
        result_file = create_file_by_mode(f"tester/results/result{i+1}.txt", "w+")
        # if var_out == var_expected write in result file "pass" else write "fail"
        print("var_out:", var_out)
        print("var_expected:", var_expected)
        if var_out == var_expected:
            result_file.write("pass")
        else:
            result_file.write("fail")


        # tester()
        # print("test finished")

        in_file.close()
        out_file.close()
        lex_file.close()
        sym_file.close()
        parser_errors_file.close()
        semantic_errors_file.close()
        generated_code_file.close()
        out_vm_file.close()
        expected_file.close()
        result_file.close()
        os.remove("tester/output.txt")
        # os.remove("tester/out.txt")






tester()
print("test finished")
