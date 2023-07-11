"""
C- compiler (Phase 2 - Parser)
Compiler Design | Sharif University of Technology
Abolfazl Eshagh    9910105
Alireza  Habibzadeh          99109393
"""

from parser import Parser
from scanner import Scanner, Reader, State
# from intercode_gen import CodeGenerator
from parser import CodeGenerator

def main(file_name):
    with open(file_name, 'r') as input_file:
        scanner = Scanner(reader=Reader(input_file), start_state=State.states[0])
        generator = CodeGenerator(scanner)
        generator.pb.finalize()
        # print(generator.pb.block)
        parser = Parser.get_instance(scanner, generator)

        parser.parse()
    with open('parse_tree.txt', 'w', encoding="utf-8") as output_file:
        parser.print_parse_tree(output_file)
    with open('syntax_errors.txt', 'w') as output_file:
        output_file.write(parser.repr_syntax_errors())
    # with open("intermediate_code.txt", 'w') as output_file:
    #     output_file.write(generator.pb.block)
    print(generator.pb.block)
    # with open('tokens.txt', 'w') as output_file:
    #     output_file.write(str(scanner))
    # with open('symbol_table.txt', 'w') as output_file:
    #     output_file.write(str(scanner.symbol_table))
    # with open('lexical_errors.txt', 'w') as output_file:
    #     output_file.write(scanner.repr_lexical_errors())


if __name__ == '__main__':
    main('input.txt')
