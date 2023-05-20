# State and token types
NUM = 'NUM'
ID = 'ID'
KEYWORD = 'KEYWORD'
SYMBOL = 'SYMBOL'
COMMENT = 'COMMENT'
WHITESPACE = 'WHITESPACE'
START = 'START'
PANIC = 'PANIC'
EOF = 'EOF'


class Token:
    def __init__(self, token_type, token_value=''):
        self.type = token_type
        self.value = token_value

    def __str__(self):
        return f'({self.type}, {self.value})'
