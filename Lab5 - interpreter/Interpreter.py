"""
Interpreter implementation using the Visitor pattern with decorators.
This module executes the AST by visiting each node and performing the corresponding operations.
Uses NumPy for matrix and vector operations.
"""

import AST
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator
import numpy as np

# Increase recursion limit to handle deep AST structures
sys.setrecursionlimit(10000)


class Interpreter(object):
    """
    Interpreter that executes programs by traversing the AST.
    Uses a memory stack to manage variable scopes.
    Implements the Visitor pattern using decorators from visit.py.
    """
    def __init__(self):
        # Initialize memory stack with a global scope
        # This will hold all variables during program execution
        self.memory_stack = MemoryStack(Memory("global"))
    
    # Base visitor method decorated with @on('node')
    # This creates a dispatcher that routes to specific visit methods based on node type
    @on('node')
    def visit(self, node):
        pass
    
    # Program node: root of the AST, contains a list of instructions
    @when(AST.Program)
    def visit(self, node):
        # Execute all instructions in the program
        return node.instructions.accept(self)
    
    # Instructions node: a sequence of statements/instructions
    @when(AST.Instructions)
    def visit(self, node):
        # Execute each instruction sequentially
        # The result of the last instruction is returned
        result = None
        for instruction in node.instructions:
            result = instruction.accept(self)
        return result
    
    # Binary expressions: arithmetic operations (+, -, *, /) and element-wise operations (.+, .-, .*, ./)
    @when(AST.BinExpr)
    def visit(self, node):
        # First evaluate both operands recursively
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        # Map operators to their corresponding functions
        # Regular operators work on scalars, element-wise operators (with dot) work on matrices/vectors
        ops = {
            '+': operator.add,      # Scalar addition
            '-': operator.sub,      # Scalar subtraction
            '*': operator.mul,     # Scalar multiplication
            '/': operator.truediv,  # Scalar division
            '.+': np.add,          # Element-wise addition (NumPy)
            '.-': np.subtract,      # Element-wise subtraction (NumPy)
            '.*': np.multiply,      # Element-wise multiplication (NumPy)
            './': np.divide,        # Element-wise division (NumPy)
        }
        
        if node.op in ops:
            return ops[node.op](left, right)
        return None
    
    # Relational expressions: comparison operations (==, !=, <, >, <=, >=)
    @when(AST.RelExpr)
    def visit(self, node):
        # Evaluate both operands
        left = node.left.accept(self)
        right = node.right.accept(self)
        
        # Map comparison operators to their corresponding functions
        ops = {
            '==': operator.eq,  # Equal
            '!=': operator.ne,   # Not equal
            '<': operator.lt,    # Less than
            '>': operator.gt,    # Greater than
            '<=': operator.le,    # Less than or equal
            '>=': operator.ge,   # Greater than or equal
        }
        
        if node.op in ops:
            return ops[node.op](left, right)
        return None
    
    # Assignment statements: assign values to variables, vector elements, or matrix elements
    @when(AST.Assignment)
    def visit(self, node):
        # First evaluate the right-hand side expression
        value = node.right.accept(self)
        
        # Handle different types of left-hand sides
        if isinstance(node.left, AST.Variable):
            # Simple variable assignment
            var_name = node.left.name
            
            if node.op == '=':
                # Direct assignment: create or update variable
                self.memory_stack.set(var_name, value)
            else:
                # Compound assignment: +=, -=, *=, /=
                # Get current value, perform operation, then assign
                current = self.memory_stack.get(var_name)
                ops = {
                    '+=': operator.add,
                    '-=': operator.sub,
                    '*=': operator.mul,
                    '/=': operator.truediv,
                }
                if node.op in ops:
                    new_value = ops[node.op](current, value)
                    self.memory_stack.set(var_name, new_value)
        
        elif isinstance(node.left, AST.VectorElement):
            # Assignment to a vector element: vec[index] = value
            var_name = node.left.name
            index = node.left.index
            vec = self.memory_stack.get(var_name)
            vec[index] = value
        
        elif isinstance(node.left, AST.MatrixElement):
            # Assignment to a matrix element: mat[row, col] = value
            var_name = node.left.name
            row = node.left.row
            col = node.left.col
            mat = self.memory_stack.get(var_name)
            mat[row, col] = value
        
        return value
    
    # If statement: conditional execution
    @when(AST.If)
    def visit(self, node):
        # Evaluate the condition
        condition = node.condition.accept(self)
        if condition:
            # Execute then block if condition is true
            return node.then_block.accept(self)
        elif node.else_block:
            # Execute else block if condition is false and else block exists
            return node.else_block.accept(self)
        return None
    
    # While loop: execute body while condition is true
    @when(AST.While)
    def visit(self, node):
        result = None
        try:
            # Keep looping while condition evaluates to true
            while node.condition.accept(self):
                try:
                    # Execute loop body
                    result = node.body.accept(self)
                except ContinueException:
                    # Continue statement: skip to next iteration
                    continue
        except BreakException:
            # Break statement: exit the loop
            pass
        return result
    
    # For loop: iterate over a range
    @when(AST.For)
    def visit(self, node):
        result = None
        # Evaluate the range expression (e.g., 1:10)
        range_obj = node.range.accept(self)
        var_name = node.var.name
        
        try:
            # Iterate over each value in the range
            for i in range_obj:
                # Set the loop variable to current iteration value
                self.memory_stack.set(var_name, i)
                try:
                    # Execute loop body
                    result = node.body.accept(self)
                except ContinueException:
                    # Continue statement: skip to next iteration
                    continue
        except BreakException:
            # Break statement: exit the loop
            pass
        
        return result
    
    # Range expression: creates a range from start to end (inclusive)
    @when(AST.Range)
    def visit(self, node):
        # Evaluate start and end values
        start = node.start.accept(self)
        end = node.end.accept(self)
        # Create Python range (end+1 because range is exclusive at the end)
        return range(int(start), int(end) + 1)
    
    # Break statement: exit the innermost loop
    # Uses exception to break out of nested loops
    @when(AST.Break)
    def visit(self, node):
        raise BreakException()
    
    # Continue statement: skip to next iteration of the innermost loop
    # Uses exception to propagate through nested structures
    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()
    
    # Return statement: return a value from a function
    # Uses exception to propagate return value through call stack
    @when(AST.Return)
    def visit(self, node):
        # Evaluate the return expression
        value = node.expr.accept(self)
        raise ReturnValueException(value)
    
    # Print statement: output values to console
    @when(AST.Print)
    def visit(self, node):
        values = []
        # Evaluate each expression to print
        for val in node.values:
            result = val.accept(self)
            # Convert to string (NumPy arrays are handled specially)
            if isinstance(result, np.ndarray):
                values.append(str(result))
            else:
                values.append(str(result))
        # Print all values separated by spaces
        print(' '.join(values))
    
    # Literal values: return the stored value directly
    @when(AST.IntNum)
    def visit(self, node):
        return node.value
    
    @when(AST.FloatNum)
    def visit(self, node):
        return node.value
    
    @when(AST.String)
    def visit(self, node):
        return node.value
    
    # Variable reference: look up variable value in memory stack
    @when(AST.Variable)
    def visit(self, node):
        # Search memory stack from current scope to global scope
        return self.memory_stack.get(node.name)
    
    # Vector element access: get element at specific index
    @when(AST.VectorElement)
    def visit(self, node):
        # Get the vector from memory, then access the element
        vec = self.memory_stack.get(node.name)
        return vec[node.index]
    
    # Matrix element access: get element at specific row and column
    @when(AST.MatrixElement)
    def visit(self, node):
        # Get the matrix from memory, then access the element
        mat = self.memory_stack.get(node.name)
        return mat[node.row, node.col]
    
    # Vector literal: create a NumPy array from a list of elements
    @when(AST.Vector)
    def visit(self, node):
        # Evaluate each element and create a NumPy array
        elements = [elem.accept(self) for elem in node.elements]
        return np.array(elements)
    
    # Matrix literal: create a NumPy matrix from a list of rows
    @when(AST.Matrix)
    def visit(self, node):
        rows = []
        # Each row is itself a vector, evaluate it and add to rows list
        for row in node.rows:
            row_data = row.accept(self)
            rows.append(row_data)
        # Create 2D NumPy array from rows
        return np.array(rows)
    
    # Matrix functions: zeros, ones, eye (identity matrix)
    @when(AST.MatrixFunction)
    def visit(self, node):
        # Handle both single size (square matrix) and tuple (rows, cols)
        if isinstance(node.size, tuple):
            rows, cols = node.size
        else:
            rows = cols = node.size
        
        # Create the appropriate matrix using NumPy
        if node.name == 'zeros':
            return np.zeros((rows, cols))
        elif node.name == 'ones':
            return np.ones((rows, cols))
        elif node.name == 'eye':
            return np.eye(rows, cols)
        return None
    
    # Unary minus: negate a value
    @when(AST.UnaryMinus)
    def visit(self, node):
        # Evaluate the expression and negate it
        value = node.expr.accept(self)
        return -value
    
    # Matrix transposition: transpose a matrix
    @when(AST.Transposition)
    def visit(self, node):
        # Evaluate the matrix expression and transpose it
        mat = node.expr.accept(self)
        return mat.T