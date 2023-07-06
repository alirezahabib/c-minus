

'''

1
Introduction
In programming assignment II, you implemented a top-down parser for C-minus, using the transition
diagrams method. In this assignment you are to implement an intermediate code generator for
certain parts of C-minus. This assignment also includes an optional part, which is the implementation
of a simple semantic analyzer for C-minus (see section 6). Note that you may use codes from text
books, with a reference to the used book in your code. However, using codes from the internet
and/or other students in this course is strictly forbidden and will result in Fail grade in the course.
Besides, even if you did not implement the parser in the previous assignment, you may not use the
parsers from other students/groups. In such a case, you must implement the parser, too.
2
Intermediate Code Generator
Specification
In this assignment, you will implement the intermediate code generator with the following
characteristics:
• The code generator is called by the parser to perform a code generation task, which can be
modifying the semantic stack and/or generating a number of three address codes.
• Code generation is performed in the same pass as other compilation tasks (because the
compiler is supposed to be a one-pass compiler).
• The parser calls a function called 'code_gen' and sends an action symbol as an argument to
'code_gen' at appropriate times during parsing.
• The code generator (i.e., the 'code_gen' function) executes the appropriate semantic routine
associated with the received action symbol (based on the technique introduced in Lecture 8).
• Generated three-address codes are saved in an output text file called 'output.txt'.
3
Augmented C-minus Grammar
To implement your intermediate code generator, you should first add the required action symbols to
the grammar of C-minus that was included in section 3 of programming assignment II. For each action
symbol, you need to write an appropriate semantic routine in Python that performs the required code
generation tasks, such as modifying the semantic stack and/or generating a number of three address
codes. Note that you should not change the given grammar in any way other than adding the
required action symbols to the right-hand side of the production rules.
4
Intermediate Code Generation
The intermediate code generation is performed with the same method that was introduced in Lecture
8. In the first part of implementing intermediate code generation in this assignment, all constructs
supported by the given C-minus grammar are to be implemented except for: return statements and
function calls. Therefore, the sample/test 'input.txt' files for this part of the assignment will be a
simple C-minus program which does not contain any type of error. In implementing the required
sematic routines for the intermediate code generation, you should pay attention to the following
points:
• Every input program may include only a number of global variables and contain just a main
function with the signature 'void main (void)'.
• All local variables of the main function are declared at the beginning of the function. That is,
there will not be any declaration of variables inside other constructs such as while loops.
• In conditional statements such as 'if' and/or 'while', if the expression value is zero, it will be
regarded as a 'false' condition; otherwise, it will be regarded to be 'true'. Moreover, the result
of a 'relop' operation that is true, will be '1'. Alternatively, if the result of a 'relop' operation
is 'false', its value will be '0'.
• You should implicitly define a function called 'output' with the signature 'void output (int a);'
which prints its argument (an integer) as the main program's output.


5 Available Three address Codes
In this project, you can only use the following three address codes. Three address codes produced
by your compiler will be executed by an interpreter called 'Tester', which can only interpret the
following three address codes. Otherwise, the tester program fails to run your three address codes.
Please note that the single and most important factor in evaluating your solution to this assignment
is that the output of your intermediate code generator will be successfully interpreted by the
'Tester' program and produce the expected output value. The 'Tester' program and its help file are
released together with this description.
Three address
code
Explanation
1 (ADD, A1, A2, R) The contents of A1 and A2 are added. The result will be saved in R.
2 (MULT, A1, A2, R) The contents of A1 and A2 are multiplied. The result will be saved in R.
3 (SUB, A1, A2, R) The content of A2 is subtracted from A1. The result will be saved in R.
4 (EQ, A1, A2, R) The contents of A1 and A2 are compared. If they are equal, '1' (i.e., as a
true value) will be saved in R; otherwise, '0' (i.e., as a false value) will be
saved in R.
5 (LT, A1, A2, R) If the content of A1 is less than the content of A2, '1' will be saved in R;
otherwise, '0' will be saved in R.
6 (ASSIGN, A, R, ) The content of A is assigned to R.
7 (JPF, A, L, ) If content of A is 'false', the control will be transferred to L; otherwise,
next three address code will be executed.
8 (JP, L, , ) The control is transferred to L.
9 (PRINT, A, , ) The content of A will be printed to the standard output.
As it was explained in Lecture 8, in three address codes, you can use three addressing modes of direct
address (e.g., 100), indirect address (e.g., @100), and immediate value (e.g., #100). For simplicity, you
can suppose that all memory locations are allocated statically. In other words, we don't have a runtime
stack or heap. Also, assume that four bytes of memory are required to store an integer. Therefore, the
address of all data memory locations is divisible by four. The following figures show a sample C-minus
program and the three address codes produced for it. Note that each three address code is preceded
by a line number starting from zero. The tester program outputs a value of '15' by running the three
address codes in the given sample. For more information about the tester program and the formatting
of the three address codes, please read the provided help file very carefully. As it was mentioned
earlier, the grading of the code generation part of this assignment is solely based on whether or not
the produced three address code can be successfully run by the Tester program and produce the
expected value.
Note that the three address codes produced for an input program such as the given sample in Fig. 1 do
not need to be identical to the code given in Fig 2. There can be a virtually infinite number of correct
three-address codes for such programs. As long as the produced code can be executed by the Tester
program and prints the expected value(s), it is acceptable.

lineno code
1 void main( void ) {
2 int prod;
3 int i;
4 prod = 1;
5 i = 1;
6 repeat {
7 prod = i * prod;
8 i = i + 2;
9 } until ( 6 < i )
10 output (prod);
11 }
Fig. 1 C-minus input sample (saved in “input.txt”)

produced three address codes
0 (JP, 1, , )
1 (ASSIGN, #1, 100, )
2 (ASSIGN, #1, 104, )
3 (MULT, 104, 100, 500)
4 (ASSIGN, 500, 100, )
5 (ADD, 104, #2, 504)
6 (ASSIGN, 504, 104, )
7 (LT, #6, 104, 508)
8 (JPF, 508, 3, )
9 (PRINT, 100, , )
Fig. 2 'Output.txt' Sample

'''
from enum import Enum

# where is it implemented?
import symbol_table as st


class OPERATIONS(Enum):
    ADD = "ADD"
    MULT = "MULT"
    SUB = "SUB"
    EQ = "EQ"
    LT = "LT"
    ASSIGN = "ASSIGN"
    JPF = "JPF"
    JP = "JP"
    PRINT = "PRINT"





class SS:
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            return -1

    def pop_mult(self, number):
        if len(self.stack) > number - 1:
            toReturn = []
            for i in range(number):
                toReturn.append(self.stack.pop())
            return toReturn
        else:
            return -1

    def top(self):
        if len(self.stack) != 0:
            return self.stack[-1]
        else:
            return -1

    def __str__(self):
        return str(self.stack)


-1 to be refactored probably
class Address:
    def __init__(self, address):
        self.address = address

    def set_indirect(self):
        self.address = "@" + str(self.address)
        return self

    def __str__(self):
        return str(self.address)

class PB:
    def __init__(self):
        self.block = []
        self.line = 0
        self.last_tmp = Address(500 - 4)
        self.last_addr = Address(100 - 4)

    def add_code(self, operation, op1, op2=None, op3=None):
        self.block.append([operation, op1, op2, op3])
        self.line += 1

    def add_to_index(self, index, operation, op1, op2=None, op3=None):
        self.block.insert(index, [operation, op1, op2, op3])
        self.line += 1

    def get_line(self):
        return self.line

    def get_tmp_address(self):
        self.last_tmp += 4
        return Address(self.last_tmp.address)

    def get_address(self):
        self.last_addr += 4
        return Address(self.last_addr.address)





# main class
class CodeGenerator:
    def __init__(self):
        self.ss = SS()
        self.pb = PB()
        self.st = st.SymbolTable()
        self.loop = []
        ...

    def add(self):
        op2 = self.ss.pop()
        op1 = self.ss.pop()
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("ADD", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def sub(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("SUB", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def mult(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("MUL", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def equals(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("EQ", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def less_than(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        tmp = self.pb.get_tmp_address()
        self.pb.add_code("LT", op1, op2, tmp)
        self.ss.push(tmp)
        # ...

    def assign(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        op2, op1 = self.ss.pop_mult(2)
        -1 to be implemented
        if op1 == "=":
            op1 = self.ss.pop()
        if is_array:
            self.pb.add_code("ASSIGN", op1, op2 + index*4)
        else:
            self.pb.add_code("ASSIGN", op1, op2)

        self.ss.push("=")
        self.ss.push(op1)


        # ...

    def jpf(self):
        # op2 = self.ss.pop()
        # op1 = self.ss.pop()
        addr = self.ss.pop_mult(2)
        op1 = self.ss.pop()
        # -1 to be implemented
        self.pb.add_to_index(addr, "JPF", op1, self.pb.get_line(), None)

        # ...

    def jp(self):
        addr = self.ss.pop()
        # -1 to be implemented
        self.pb.add_to_index(addr, "JP", self.pb.get_line(), None, None)
        # ...

    def output(self):
        op1 = self.ss.pop()
        self.pb.add_code("PRINT", op1, None, None)

        # ...
    def routine(self, name, params):
        sem_func = getattr(self, name)
        if sem_func is None or not callable(sem_func):
            -1 to be implemented
            return -1

        sem_func(*params)
        # ...
    def pid(self, name):
        self.ss.push(name)
    def pconst(self, value):
        self.ss.push(value)

    def save(self):
        self.ss.push(self.pb.get_line())
        self.pb.add_code(None,None)


    # def jpf(self):
    #     addr = self.ss.pop()
    #     self.pb.add_code[addr]("JPF", self.ss.pop(), self.pb.get_line(), None)

    def jpf_save(self):
        addr = self.ss.pop()
        # -1 to be implemented
        self.pb.add_to_index(addr, "JPF", self.ss.pop(), self.pb.get_line()+1, None)
        self.pb.add_code(None,None)
        self.ss.push(self.pb.get_line())


    # -1 to be refactored
    def loop(self):
        self.loop.append(self.pb.get_line()+1)
        self.pb.add_code(None,None)
    def until(self):
        expr = self.ss.pop()
        addr = self.ss.pop()
        self.pb.add_code("JPF", expr, addr, None)
        addr = self.pb.get_line()
        for address in self.loop:
            self.pb.add_to_index(address, "JP", addr, None, None)

















