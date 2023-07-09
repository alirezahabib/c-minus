from anytree import Node, RenderTree

import grammar
import ctoken
from scanner import Scanner
import intercode_gen


class Parser:
    def __init__(self, scanner: Scanner):
        self.current_token = None
        self.current_value = None
        self.scanner = scanner
        self.syntax_errors = []  # [(line_number, error), ]
        self.transition_table = {}
        self.root = None
        self.create_transition_table()

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
                else:
                    self.error(f"missing {stack_top}")
                    stack.pop()
                    node_stack.pop().name = str(self.current_token)
                self.current_token, self.current_value = self.get_next_token()
            elif stack_top == '$':
                if stack_top != self.current_value:
                    self.error("Unexpected EOF")
                break
            elif stack_top[0] == '#':
                getattr(intercode_gen, stack_top[1:])()
                stack.pop()
                node_stack.pop()

            else:
                production_rule = self.transition_table[(stack_top, self.current_value)]
                # print(f'production_rule {(stack_top, self.current_value)}:', production_rule)

                if production_rule is None:
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
                    # print('stack before:', stack)
                    # print('rule:', production_rule)
                    # print('current_value:', self.current_value)
                    stack.pop()
                    node_stack.pop()
                    nodes = []
                    for symbol in production_rule:
                        nodes.append(Node(symbol, parent=node_stack_top))
                    for symbol in reversed(production_rule):
                        stack.append(symbol)
                        node_stack.append(nodes.pop())
                    # print('stack after:', stack)

                    self.print_parse_tree()
        self.print_parse_tree()

    def error(self, message):
        # print(f'#{self.scanner.reader.line_number} : syntax error, {message}')
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
