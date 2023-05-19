from anytree import Node, RenderTree

from scanner import Scanner


class Parser:
    def __init__(self, scanner: Scanner):
        self.root: Node = None  # TODO
        self.scanner = scanner
        self.syntax_errors = []  # [(line_number, error), ]

    def parse(self):
        # TODO
        pass

    def repr_parse_tree(self):
        s = ''
        for pre, _, node in RenderTree(self.root):
            s += "%s%s" % (pre, node.name)
        return s

    def repr_syntax_errors(self):
        if not self.syntax_errors:
            return 'There is no syntax error.'
        return '\n'.join(map(lambda error:
                             f'#{str(error[0])} : syntax error, {error[1]}',
                             self.syntax_errors))
