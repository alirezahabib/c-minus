terminals = [
    "ID",
    ";",
    "[",
    "NUM",
    "]",
    "(",
    ")",
    "int",
    "void",
    ",",
    "{",
    "}",
    "break",
    "if",
    "else",
    "repeat",
    "until",
    "return",
    "=",
    "<",
    "==",
    "+",
    "-",
    "*"
]

non_terminals = [
    "Program",
    "Declaration-list",
    "Declaration",
    "Declaration-initial",
    "Declaration-prime",
    "Var-declaration-prime",
    "Fun-declaration-prime",
    "Type-specifier",
    "Params",
    "Param-list",
    "Param",
    "Param-prime",
    "Compound-stmt",
    "Statement-list",
    "Statement",
    "Expression-stmt",
    "Selection-stmt",
    "Iteration-stmt",
    "Return-stmt",
    "Return-stmt-prime",
    "Expression",
    "B",
    "H",
    "Simple-expression-zegond",
    "Simple-expression-prime",
    "C",
    "Relop",
    "Additive-expression",
    "Additive-expression-prime",
    "Additive-expression-zegond",
    "D",
    "Addop",
    "Term",
    "Term-prime",
    "Term-zegond",
    "G",
    "Factor",
    "Var-call-prime",
    "Var-prime",
    "Factor-prime",
    "Factor-zegond",
    "Args",
    "Arg-list",
    "Arg-list-prime"
]

first = {
    "Program": [
        "int", "void", "epsilon"
    ],
    "Declaration-list": [
        "int", "void", "epsilon"
    ],
    "Declaration": [
        "int", "void"
    ],
    "Declaration-initial": [
        "int", "void"
    ],
    "Declaration-prime": [
        ";", "[", "("
    ],
    "Var-declaration-prime": [
        ";", "["
    ],
    "Fun-declaration-prime": ["("],
    "Type-specifier": [
        "int", "void"
    ],
    "Params": [
        "int", "void"
    ],
    "Param-list": [
        ",", "epsilon"
    ],
    "Param": [
        "int", "void"
    ],
    "Param-prime": [
        "[", "epsilon"
    ],
    "Compound-stmt": ["{"],
    "Statement-list": [
        "ID",
        ";",
        "NUM",
        "(",
        "{",
        "break",
        "if",
        "repeat",
        "return",
        "epsilon"
    ],
    "Statement": [
        "ID",
        ";",
        "NUM",
        "(",
        "{",
        "break",
        "if",
        "repeat",
        "return"
    ],
    "Expression-stmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "break"
    ],
    "Selection-stmt": ["if"],
    "Iteration-stmt": ["repeat"],
    "Return-stmt": ["return"],
    "Return-stmt-prime": [
        "ID", ";", "NUM", "("
    ],
    "Expression": [
        "ID", "NUM", "("
    ],
    "B": [
        "(",
        "[",
        "=",
        "<",
        "==",
        "+",
        "-",
        "*",
        "epsilon"
    ],
    "H": [
        "=",
        "<",
        "==",
        "+",
        "-",
        "*",
        "epsilon"
    ],
    "Simple-expression-zegond": [
        "NUM", "("
    ],
    "Simple-expression-prime": [
        "(",
        "<",
        "==",
        "+",
        "-",
        "*",
        "epsilon"
    ],
    "C": [
        "<", "==", "epsilon"
    ],
    "Relop": [
        "<", "=="
    ],
    "Additive-expression": [
        "ID", "NUM", "("
    ],
    "Additive-expression-prime": [
        "(",
        "+",
        "-",
        "*",
        "epsilon"
    ],
    "Additive-expression-zegond": [
        "NUM", "("
    ],
    "D": [
        "+", "-", "epsilon"
    ],
    "Addop": [
        "+", "-"
    ],
    "Term": [
        "ID", "NUM", "("
    ],
    "Term-prime": [
        "(", "*", "epsilon"
    ],
    "Term-zegond": [
        "NUM", "("
    ],
    "G": [
        "*", "epsilon"
    ],
    "Factor": [
        "ID", "NUM", "("
    ],
    "Var-call-prime": [
        "[", "(", "epsilon"
    ],
    "Var-prime": [
        "[", "epsilon"
    ],
    "Factor-prime": [
        "(", "epsilon"
    ],
    "Factor-zegond": [
        "NUM", "("
    ],
    "Args": [
        "ID", "NUM", "(", "epsilon"
    ],
    "Arg-list": [
        "ID", "NUM", "("
    ],
    "Arg-list-prime": [",", "epsilon"]
}

follow = {
    "Program": ["$"],
    "Declaration-list": [
        "ID",
        ";",
        "NUM",
        "(",
        "{",
        "}",
        "break",
        "if",
        "repeat",
        "return",
        "$"
    ],
    "Declaration": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "repeat",
        "return",
        "$"
    ],
    "Declaration-initial": [
        ";",
        "[",
        "(",
        ")",
        ","
    ],
    "Declaration-prime": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "repeat",
        "return",
        "$"
    ],
    "Var-declaration-prime": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "repeat",
        "return",
        "$"
    ],
    "Fun-declaration-prime": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "repeat",
        "return",
        "$"
    ],
    "Type-specifier": ["ID"],
    "Params": [")"],
    "Param-list": [")"],
    "Param": [
        ")", ","
    ],
    "Param-prime": [
        ")", ","
    ],
    "Compound-stmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "repeat",
        "until",
        "return",
        "$"
    ],
    "Statement-list": ["}"],
    "Statement": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "repeat",
        "until",
        "return"
    ],
    "Expression-stmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "repeat",
        "until",
        "return"
    ],
    "Selection-stmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "repeat",
        "until",
        "return"
    ],
    "Iteration-stmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "repeat",
        "until",
        "return"
    ],
    "Return-stmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "repeat",
        "until",
        "return"
    ],
    "Return-stmt-prime": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "repeat",
        "until",
        "return"
    ],
    "Expression": [
        ";", "]", ")", ","
    ],
    "B": [
        ";", "]", ")", ","
    ],
    "H": [
        ";", "]", ")", ","
    ],
    "Simple-expression-zegond": [
        ";", "]", ")", ","
    ],
    "Simple-expression-prime": [
        ";", "]", ")", ","
    ],
    "C": [
        ";", "]", ")", ","
    ],
    "Relop": [
        "ID", "NUM", "("
    ],
    "Additive-expression": [
        ";", "]", ")", ","
    ],
    "Additive-expression-prime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "=="
    ],
    "Additive-expression-zegond": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "=="
    ],
    "D": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "=="
    ],
    "Addop": [
        "ID", "NUM", "("
    ],
    "Term": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-"
    ],
    "Term-prime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-"
    ],
    "Term-zegond": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-"
    ],
    "G": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-"
    ],
    "Factor": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "Var-call-prime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "Var-prime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "Factor-prime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "Factor-zegond": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "Args": [")"],
    "Arg-list": [")"],
    "Arg-list-prime": [")"]
}

rules = {
    'Program': [['Declaration-list', '$']],
    'Declaration-list': [['Declaration', 'Declaration-list'], ['epsilon']],
    'Declaration': [['Declaration-initial', 'Declaration-prime']],
    'Declaration-initial': [['Type-specifier', 'ID']],
    'Declaration-prime': [['Fun-declaration-prime'], ['Var-declaration-prime']],
    'Var-declaration-prime': [[';'], ['[', 'NUM', ']', ';']],
    'Fun-declaration-prime': [['(', 'Params', ')', 'Compound-stmt']],
    'Type-specifier': [['int'], ['void']],
    'Params': [['int', 'ID', 'Param-prime', 'Param-list'], ['void']],
    'Param-list': [[',', 'Param', 'Param-list'], ['epsilon']],
    'Param': [['Declaration-initial', 'Param-prime']],
    'Param-prime': [['[', ']'], ['epsilon']],
    'Compound-stmt': [['{', 'Declaration-list', 'Statement-list', '}']],
    'Statement-list': [['Statement', 'Statement-list'], ['epsilon']],
    'Statement': [['Expression-stmt'], ['Compound-stmt'], ['Selection-stmt'], ['Iteration-stmt'], ['Return-stmt']],
    'Expression-stmt': [['Expression', ';'], ['break', ';'], [';']],
    'Selection-stmt': [['if', '(', 'Expression', ')', 'Statement', 'else', 'Statement']],
    'Iteration-stmt': [['repeat', 'Statement', 'until', '(', 'Expression', ')']],
    'Return-stmt': [['return', 'Return-stmt-prime']],
    'Return-stmt-prime': [[';'], ['Expression', ';']],
    'Expression': [['Simple-expression-zegond'], ['ID', 'B']],
    'B': [['=', 'Expression'], ['[', 'Expression', ']', 'H'], ['Simple-expression-prime']],
    'H': [['=', 'Expression'], ['G', 'D', 'C']],
    'Simple-expression-zegond': [['Additive-expression-zegond', 'C']],
    'Simple-expression-prime': [['Additive-expression-prime', 'C']],
    'C': [['Relop', 'Additive-expression'], ['epsilon']],
    'Relop': [['<'], ['==']],
    'Additive-expression': [['Term', 'D']],
    'Additive-expression-prime': [['Term-prime', 'D']],
    'Additive-expression-zegond': [['Term-zegond', 'D']],
    'D': [['Addop', 'Term', 'D'], ['epsilon']],
    'Addop': [['+'], ['-']],
    'Term': [['Factor', 'G']],
    'Term-prime': [['Factor-prime', 'G']],
    'Term-zegond': [['Factor-zegond', 'G']],
    'G': [['*', 'Factor', 'G'], ['epsilon']],
    'Factor': [['(', 'Expression', ')'], ['ID', 'Var-call-prime'], ['NUM']],
    'Var-call-prime': [['(', 'Args', ')'], ['Var-prime']],
    'Var-prime': [['[', 'Expression', ']'], ['epsilon']],
    'Factor-prime': [['(', 'Args', ')'], ['epsilon']],
    'Factor-zegond': [['(', 'Expression', ')'], ['NUM']],
    'Args': [['Arg-list'], ['epsilon']],
    'Arg-list': [['Expression', 'Arg-list-prime']],
    'Arg-list-prime': [[',', 'Expression', 'Arg-list-prime'], ['epsilon']]
}
