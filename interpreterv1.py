from brewparse import parse_program
from intbase import InterpreterBase
import matplotlib.pyplot as plt

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)   # call InterpreterBase's constructor

    def run(self, program):
        ast = parse_program(program) 
        self.variable_name_to_value = {} # dict to hold variables
        main_func_node = ast.dict['functions'][0]  #locate the node that holds details about the main() function
        #print("Found main function!")
        #print("Function name:", main_func_node.dict['name'])
        #print("Number of statements:", len(main_func_node.dict['statements']))
        self.run_func(main_func_node) #iterates through nodes and interprets the statements one after another

    def run_func(self, func_node):    #iterate through the nodes and run the functions
	    for statement_node in func_node.dict['statements']:
		    self.run_statement(statement_node)

    def run_statement(self, statement_node):  #check which type of statement and run the statement
        print("Statement name:", statement_node.elem_type)
        if statement_node.elem_type == 'vardef':  #variable definition
            print("variable definition statement found")
            self.do_definition(statement_node)
        elif statement_node.elem_type == '=': #assignment statements
            print("assignment statement found")
        #    do_assignment(statement_node)
        elif statement_node.elem_type == 'fcall': #function call statements
            print("function call found")
        #    do_func_call(statement_node)

    def do_definition(self,statement_node):
        var_name = statement_node.dict['name']
        print("var name is", var_name)
        self.variable_name_to_value[var_name] = None






def main():
    program = """def main() {
                        var x;
                        x = 5 + 6;
                        print("The sum is: ",x);    
                        }
                        """
    interpreter = Interpreter()
    interpreter.run(program)
main()