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
    'Program': [['Declaration-list', '$', '#call_main']],
    'Declaration-list': [['Declaration', 'Declaration-list'], ['epsilon']],
    'Declaration': [['Declaration-initial', 'Declaration-prime']],
    'Declaration-initial': [['#p_type', 'Type-specifier', '#declare_id', 'ID']],
    'Declaration-prime': [['Fun-declaration-prime'], ['Var-declaration-prime']],
    'Var-declaration-prime': [['#dec_var', ';'], ['[', '#dec_array', 'NUM', ']', ';']],
    'Fun-declaration-prime': [['#dec_func', '(', 'Params', ')', 'Compound-stmt', '#end_func']],
    'Type-specifier': [['int'], ['void']],
    'Params': [['#p_type', 'int', '#declare_id', 'ID', 'Param-prime', 'Param-list'], ['void']],
    'Param-list': [[',', 'Param', 'Param-list'], ['epsilon']],
    'Param': [['Declaration-initial', 'Param-prime']],
    'Param-prime': [['[', ']', '#declare_entry_array'], ['epsilon']],
    'Compound-stmt': [['{', 'Declaration-list', 'Statement-list', '}']],
    'Statement-list': [['Statement', 'Statement-list'], ['epsilon']],
    'Statement': [['Expression-stmt'], ['Compound-stmt'], ['Selection-stmt'], ['Iteration-stmt'], ['Return-stmt']],
    'Expression-stmt': [['Expression', ';'], ['#break_jp', 'break', ';'], [';']],
    'Selection-stmt': [['if', '(', 'Expression', ')', '#save', 'Statement', 'else', '#jpf_save','Statement', '#jp']],
    'Iteration-stmt': [['repeat', '#label', 'Statement', 'until', '(', 'Expression', ')', '#until']],
    'Return-stmt': [['return', 'Return-stmt-prime']],
    'Return-stmt-prime': [[';'], ['Expression', ';']],
    'Expression': [['Simple-expression-zegond'], ['#p_id', 'ID', 'B']],
    'B': [['#push_eq', '=', 'Expression', '#assign'], ['[', 'Expression', ']', '#array_access', 'H'], ['Simple-expression-prime']],
    'H': [['#push_eq', '=', 'Expression', '#assign'], ['G', 'D', 'C']],
    'Simple-expression-zegond': [['Additive-expression-zegond', 'C']],
    'Simple-expression-prime': [['Additive-expression-prime', 'C']],
    'C': [['#push_op', 'Relop', 'Additive-expression', '#op'], ['epsilon']],
    'Relop': [['<'], ['==']],
    'Additive-expression': [['Term', 'D']],
    'Additive-expression-prime': [['Term-prime', 'D']],
    'Additive-expression-zegond': [['Term-zegond', 'D']],
    'D': [['#push_op', 'Addop', 'Term', '#op','D'], ['epsilon']],
    'Addop': [['+'], ['-']],
    'Term': [['Factor', 'G']],
    'Term-prime': [['Factor-prime', 'G']],
    'Term-zegond': [['Factor-zegond', 'G']],
    'G': [['#push_op', '*', 'Factor', '#op', 'G'], ['epsilon']],
    'Factor': [['(', 'Expression', ')'], ['#p_id', 'ID', 'Var-call-prime'], ['#p_num', 'NUM']],
    'Var-call-prime': [['(', '#start_call', 'Args', ')', '#end_call'], ['Var-prime']],
    'Var-prime': [['[', 'Expression', ']', '#array_access'], ['epsilon']],
    'Factor-prime': [['(', '#start_call', 'Args', ')', '#end_call'], ['epsilon']],
    'Factor-zegond': [['(', 'Expression', ')'], ['#p_num', 'NUM']],
    'Args': [['Arg-list'], ['epsilon']],
    'Arg-list': [['Expression', 'Arg-list-prime']],
    'Arg-list-prime': [[',', '#arg_input', 'Expression', 'Arg-list-prime'], ['epsilon', '#arg_input']]
}
