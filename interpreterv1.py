from brewparse import parse_program
from intbase import InterpreterBase, ErrorType
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

    def run_func(self, main_func_node):    #iterate through the nodes and run the statements
	    for statement_node in main_func_node.dict['statements']:
		    self.run_statement(statement_node)

    def run_statement(self, statement_node):  #check which type of statement and run the statement
        #print("Statement name:", statement_node.elem_type)
        if statement_node.elem_type == 'vardef':  #variable definition
            #print("variable definition statement found")
            self.do_definition(statement_node)
        elif statement_node.elem_type == '=': #assignment statements
            #print("assignment statement found")
            self.do_assignment(statement_node)
        elif statement_node.elem_type == 'fcall': #function call statements
            #print("function call found")
            self.do_func_call(statement_node)

    def do_definition(self,statement_node): #define a variable and store in dictionary
        var_name = statement_node.dict['name']
        #print("var name is", var_name)
        # Check if variable is already declared
        if var_name in self.variable_name_to_value:
            self.error(ErrorType.NAME_ERROR, "Variable already declared")
        self.variable_name_to_value[var_name] = None

    def do_assignment(self,statement_node):  #assign variable
        var_name = statement_node.dict['var']
        expression_node = statement_node.dict['expression']
        #print("assigning to variable:", var_name)
        #print("expression to evaluate:", expression_node.elem_type)
        result = self.do_expression(expression_node)      #use helper to evaluate expression node
        self.variable_name_to_value[var_name] = result            #store value of expression into variable on  left side of expression
        #print("variable", var_name)
        #print("assigned value:", result) 

    def do_expression(self,expression_node): #evaluate expression and return value
        if expression_node.elem_type == "int": # integer literal
            return expression_node.dict['val']
        elif expression_node.elem_type == "string": #string literal
            return expression_node.dict['val']
        elif expression_node.elem_type == "+": #addition
            left_val = self.do_expression(expression_node.dict['op1'])
            right_val = self.do_expression(expression_node.dict['op2'])
            if isinstance(left_val,int) == False:
                self.error(ErrorType.TYPE_ERROR, "Left operand must be integer")
            if isinstance(right_val,int) == False:
                self.error(ErrorType.TYPE_ERROR, "Right operand must be integer")
            return left_val + right_val
        elif expression_node.elem_type == "-": #subtraction
            left_val = self.do_expression(expression_node.dict['op1'])
            right_val = self.do_expression(expression_node.dict['op2'])
            if isinstance(left_val,int) == False:
                self.error(ErrorType.TYPE_ERROR, "Left operand must be integer")
            if isinstance(right_val,int)== False:
                self.error(ErrorType.TYPE_ERROR, "Right operand must be integer")
            return left_val - right_val
        elif expression_node.elem_type == "qname": #qualified name variable expression
            var_name = expression_node.dict['name']
            if var_name not in self.variable_name_to_value:
                self.error(ErrorType.NAME_ERROR, "Variable {var_name} not defined")
            if self.variable_name_to_value[var_name] is None:
                self.error(ErrorType.NAME_ERROR, "Variable {var_name} not assigned")
            return self.variable_name_to_value[var_name]
        elif expression_node.elem_type == "fcall": #fcall to inputi
            func_name = expression_node.dict['name']
            args = expression_node.dict['args']
            if func_name == "inputi":
                evaluated_args = []
                for arg in args:
                    evaluated_arg = self.do_expression(arg)
                    evaluated_args.append(evaluated_arg)
                if len(evaluated_args) > 1:
                    self.error(ErrorType.NAME_ERROR, "No inputi() function found that takes > 1 parameter")
                if len(evaluated_args) == 1:
                    prompt = evaluated_args[0]
                    self.output(prompt)
                user_input = self.get_input()
                return int(user_input)
            else:
                self.error(ErrorType.NAME_ERROR, "Unknown function")
    def do_func_call(self,statement_node):
        func_name = statement_node.dict['name']
        args = statement_node.dict['args']
        #print("Calling function", func_name)
        #print("Number of args:", len(args))
        # Evaluate all arguments
        evaluated_args = []
        for arg in args:
            evaluated_arg = self.do_expression(arg)
            evaluated_args.append(evaluated_arg)
        if func_name == "print":
            output = "".join(str(arg) for arg in evaluated_args)
            self.output(output)
        elif func_name == "inputi":
            if len(evaluated_args) > 1:
                self.error(ErrorType.NAME_ERROR, "No inputi() function found that takes > 1 parameter")
            if len(evaluated_args) == 1: #check for prompt first
                prompt = evaluated_args[0]
                self.output(prompt)
                user_input = self.get_input()
                integer_value = int(user_input) #technically dont need to store if called as a statement but for syntax iits okay
        else:
            self.error(ErrorType.NAME_ERROR, "Unknown function")


    