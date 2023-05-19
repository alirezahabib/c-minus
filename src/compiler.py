"""
C- compiler (Phase 2 - Parser)
Compiler Design | Sharif University of Technology
Soheil   Nazari  Mendejin    99102412
Alireza  Habibzadeh          99109393
"""

from parser import Parser
from scanner import Scanner, Reader, State


def main(file_name):
    with open(file_name, 'r') as input_file:
        scanner = Scanner(reader=Reader(input_file), start_state=State.states[0])
        parser = Parser(scanner)
        parser.parse()
    with open('parse_tree.txt', 'w') as output_file:
        output_file.write(parser.repr_parse_tree())
    with open('tokens.txt', 'w') as output_file:
        output_file.write(str(scanner))
    with open('symbol_table.txt', 'w') as output_file:
        output_file.write(str(scanner.symbol_table))
    with open('lexical_errors.txt', 'w') as output_file:
        output_file.write(scanner.repr_lexical_errors())


if __name__ == '__main__':
    main('input.txt')
