from brewparse import parse_program
from intbase import InterpreterBase
import matplotlib.pyplot as plt

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase's constructor

    def run(self, program):
        parsed_program = parse_program(program, True)
        return parsed_program





def main():
    program = """def main() {
                        var x;
                        x = 5 + 6;
                        print("The sum is: ",x);    
                        }
                        """
    interpreter = Interpreter()
    ast = interpreter.run(program)
    print("printing AST")
    print(ast)

main()