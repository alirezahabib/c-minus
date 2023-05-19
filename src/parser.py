from anytree import Node, RenderTree

from scanner import Scanner


class Parser:
    def __init__(self, scanner: Scanner):
        self.root: Node = None # TODO
        self.scanner = scanner

    def parse(self):
        # TODO
        pass

    def repr_parse_tree(self):
        s = ''
        for pre, _, node in RenderTree(self.root):
            s += "%s%s" % (pre, node.name)
        return s
