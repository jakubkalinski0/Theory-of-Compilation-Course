"""
Abstract Syntax Tree (AST) node definitions.
Each class represents a construct in the language (expressions, statements, etc.).
All nodes implement the Visitor pattern through the accept() method.
"""


class Node:
    """
    Base class for all AST nodes.
    Implements the Visitor pattern: nodes accept visitors which can traverse and process them.
    """
    def __init__(self):
        # Line number in source code (for error reporting)
        self.lineno = 0
    
    def __str__(self):
        return self.printTree()
    
    def accept(self, visitor):
        """
        Accept a visitor and let it process this node.
        This is the entry point for the Visitor pattern.
        """
        return visitor.visit(self)


# Program structure nodes

class Program(Node):
    """
    Root node of the AST representing the entire program.
    Contains a list of instructions (statements) to execute.
    """
    def __init__(self, instructions):
        super().__init__()
        self.instructions = instructions


class Instructions(Node):
    """
    A sequence of instructions (statements).
    Used to group multiple statements together (e.g., in a block).
    """
    def __init__(self):
        super().__init__()
        self.instructions = []
    
    def add(self, instruction):
        """Add an instruction to the sequence."""
        self.instructions.append(instruction)

# Expression nodes

# Binary expressions: (+, -, *, /, .+, .-, .*, ./)
# Regular operators work on scalars, dot-prefixed operators work element-wise on matrices
class BinExpr(Node):
    """
    Binary expression: operation on two operands.
    Supports arithmetic operations: +, -, *, / (scalar) and .+, .-, .*, ./ (element-wise).
    """
    def __init__(self, op, left, right, lineno=0):
        super().__init__()
        self.op = op      # Operator symbol
        self.left = left  # Left operand (AST node)
        self.right = right  # Right operand (AST node)
        self.lineno = lineno

# Relational expressions: (<, >, <=, >=, ==, !=)
class RelExpr(Node):
    """
    Relational expression: comparison between two values.
    Returns a boolean value.
    """
    def __init__(self, op, left, right, lineno=0):
        super().__init__()
        self.op = op      # Comparison operator
        self.left = left  # Left operand
        self.right = right  # Right operand
        self.lineno = lineno

# Assignment operators: (=, +=, -=, *=, /=)
class Assignment(Node):
    """
    Assignment statement: assigns a value to a variable, vector element, or matrix element.
    Supports direct assignment (=) and compound assignments (+=, -=, *=, /=).
    """
    def __init__(self, op, left, right, lineno=0):
        super().__init__()
        self.op = op      # Assignment operator
        self.left = left  # Left-hand side (variable, vector element, or matrix element)
        self.right = right  # Right-hand side (expression to evaluate)
        self.lineno = lineno


# Control flow nodes

class If(Node):
    """
    If statement: conditional execution.
    Executes then_block if condition is true, else_block (if present) if false.
    """
    def __init__(self, condition, then_block, else_block=None, lineno=0):
        super().__init__()
        self.condition = condition  # Boolean expression
        self.then_block = then_block  # Instructions to execute if true
        self.else_block = else_block  # Optional instructions to execute if false
        self.lineno = lineno


class While(Node):
    """
    While loop: executes body repeatedly while condition is true.
    """
    def __init__(self, condition, body, lineno=0):
        super().__init__()
        self.condition = condition  # Boolean expression evaluated before each iteration
        self.body = body  # Instructions to execute in each iteration
        self.lineno = lineno


class For(Node):
    """
    For loop: iterates over a range of values.
    Sets loop variable to each value in the range and executes body.
    """
    def __init__(self, var, range_expr, body, lineno=0):
        super().__init__()
        self.var = var  # Loop variable (Variable node)
        self.range = range_expr  # Range expression (e.g., 1:10)
        self.body = body  # Instructions to execute in each iteration
        self.lineno = lineno


class Range(Node):
    """
    Range expression: defines a range from start to end (inclusive).
    Used in for loops: for i in 1:10
    """
    def __init__(self, start, end, lineno=0):
        super().__init__()
        self.start = start  # Start value (expression)
        self.end = end  # End value (expression)
        self.lineno = lineno


class Break(Node):
    """
    Break statement: exits the innermost loop.
    """
    def __init__(self, lineno=0):
        super().__init__()
        self.lineno = lineno


class Continue(Node):
    """
    Continue statement: skips to the next iteration of the innermost loop.
    """
    def __init__(self, lineno=0):
        super().__init__()
        self.lineno = lineno


class Return(Node):
    """
    Return statement: returns a value from a function.
    """
    def __init__(self, expr, lineno=0):
        super().__init__()
        self.expr = expr  # Expression to return
        self.lineno = lineno


class Print(Node):
    """
    Print statement: outputs values to the console.
    Can print multiple values separated by spaces.
    """
    def __init__(self, values, lineno=0):
        super().__init__()
        self.values = values  # List of expressions to print
        self.lineno = lineno


# Literal value nodes

class IntNum(Node):
    """
    Integer literal: represents an integer constant.
    """
    def __init__(self, value, lineno=0):
        super().__init__()
        self.value = value  # Integer value
        self.lineno = lineno


class FloatNum(Node):
    """
    Floating-point literal: represents a floating-point constant.
    """
    def __init__(self, value, lineno=0):
        super().__init__()
        self.value = value  # Float value
        self.lineno = lineno


class String(Node):
    """
    String literal: represents a string constant.
    """
    def __init__(self, value, lineno=0):
        super().__init__()
        self.value = value  # String value
        self.lineno = lineno

# Variable and data structure access nodes

class Variable(Node):
    """
    Variable reference: refers to a variable by name.
    The actual value is looked up in the memory stack during interpretation.
    """
    def __init__(self, name, lineno=0):
        super().__init__()
        self.name = name  # Variable name
        self.lineno = lineno


class VectorElement(Node):
    """
    Vector element access: accesses an element of a vector by index.
    Example: vec[0]
    """
    def __init__(self, name, index, lineno=0):
        super().__init__()
        self.name = name  # Vector variable name
        self.index = index  # Index expression (evaluated to integer)
        self.lineno = lineno


class MatrixElement(Node):
    """
    Matrix element access: accesses an element of a matrix by row and column.
    Example: mat[0, 1]
    """
    def __init__(self, name, row, col, lineno=0):
        super().__init__()
        self.name = name  # Matrix variable name
        self.row = row  # Row index expression
        self.col = col  # Column index expression
        self.lineno = lineno

# Data structure literal nodes

class Matrix(Node):
    """
    Matrix literal: creates a matrix from a list of rows.
    Each row is itself a vector (list of elements).
    Example: [[1, 2], [3, 4]]
    """
    def __init__(self, rows, lineno=0):
        super().__init__()
        self.rows = rows  # List of row nodes (each row is a Vector node)
        self.lineno = lineno


class Vector(Node):
    """
    Vector literal: creates a vector from a list of elements.
    Example: [1, 2, 3]
    """
    def __init__(self, elements, lineno=0):
        super().__init__()
        self.elements = elements  # List of element expressions
        self.lineno = lineno


class MatrixFunction(Node):
    """
    Matrix function call: creates a matrix using built-in functions.
    Supported functions: zeros, ones, eye (identity matrix).
    Example: zeros(3, 4) or eye(5)
    """
    def __init__(self, name, size, lineno=0):
        super().__init__()
        self.name = name  # Function name: 'zeros', 'ones', or 'eye'
        self.size = size  # Size: integer (square matrix) or tuple (rows, cols)
        self.lineno = lineno

# Unary operation nodes

class UnaryMinus(Node):
    """
    Unary minus: negates a value.
    Example: -5 or -x
    """
    def __init__(self, expr, lineno=0):
        super().__init__()
        self.expr = expr  # Expression to negate
        self.lineno = lineno


class Transposition(Node):
    """
    Matrix transposition: transposes a matrix.
    Example: A'
    """
    def __init__(self, expr, lineno=0):
        super().__init__()
        self.expr = expr  # Matrix expression to transpose
        self.lineno = lineno