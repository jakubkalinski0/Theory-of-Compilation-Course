# --- TreePrinter.py with explanatory comments added ---

from __future__ import print_function
import AST

# Decorator used to dynamically attach printTree methods to AST node classes
# It takes a class and adds the decorated function as one of its methods.
def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)  # attach method to class
        return func
    return decorator


class TreePrinter:

    # Program node: root of the AST
    @addToClass(AST.Program)
    def printTree(self, indent=0):
        if self.instructions:
            return self.instructions.printTree(indent)
        return ""

    # Instructions: sequence of instructions
    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        result = []
        for instruction in self.instructions:  # print each instruction
            result.append(instruction.printTree(indent))
        return "\n".join(result)

    # Binary expressions: +, -, *, /, .+, .-, .*, ./ etc.
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        s = "|  " * indent + self.op + "\n"  # operator
        s += self.left.printTree(indent + 1) + "\n"  # left operand
        s += self.right.printTree(indent + 1)  # right operand
        return s

    # Relational expressions: <, >, <=, >=, ==, !=
    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        s = "|  " * indent + self.op + "\n"
        s += self.left.printTree(indent + 1) + "\n"
        s += self.right.printTree(indent + 1)
        return s

    # Assignments: =, +=, -=, *=, /=
    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        s = "|  " * indent + self.op + "\n"
        s += self.left.printTree(indent + 1) + "\n"
        s += self.right.printTree(indent + 1)
        return s

    # If statement: includes THEN and optional ELSE
    @addToClass(AST.If)
    def printTree(self, indent=0):
        s = "|  " * indent + "IF\n"
        s += self.condition.printTree(indent + 1) + "\n"
        s += "|  " * indent + "THEN\n"
        s += self.then_block.printTree(indent + 1)
        if self.else_block:
            s += "\n" + "|  " * indent + "ELSE\n"
            s += self.else_block.printTree(indent + 1)
        return s

    # While loop
    @addToClass(AST.While)
    def printTree(self, indent=0):
        s = "|  " * indent + "WHILE\n"
        s += self.condition.printTree(indent + 1) + "\n"
        s += self.body.printTree(indent + 1)
        return s

    # For loop
    @addToClass(AST.For)
    def printTree(self, indent=0):
        s = "|  " * indent + "FOR\n"
        s += self.var.printTree(indent + 1) + "\n"  # loop variable
        s += self.range.printTree(indent + 1) + "\n"  # range
        s += self.body.printTree(indent + 1)  # body
        return s

    # Range of numbers, e.g., 1:10
    @addToClass(AST.Range)
    def printTree(self, indent=0):
        s = "|  " * indent + "RANGE\n"
        s += self.start.printTree(indent + 1) + "\n"
        s += self.end.printTree(indent + 1)
        return s

    # Break statement
    @addToClass(AST.Break)
    def printTree(self, indent=0):
        return "|  " * indent + "BREAK"

    # Continue statement
    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        return "|  " * indent + "CONTINUE"

    # Return statement
    @addToClass(AST.Return)
    def printTree(self, indent=0):
        s = "|  " * indent + "RETURN\n"
        s += self.expr.printTree(indent + 1)
        return s

    # Print statement, may include multiple expressions
    @addToClass(AST.Print)
    def printTree(self, indent=0):
        s = "|  " * indent + "PRINT\n"
        for i, val in enumerate(self.values):
            s += val.printTree(indent + 1)
            if i < len(self.values) - 1:
                s += "\n"
        return s

    # Integer number
    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        return "|  " * indent + str(self.value)

    # Floating point number
    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        return "|  " * indent + str(self.value)

    # String literal
    @addToClass(AST.String)
    def printTree(self, indent=0):
        return "|  " * indent + '"' + self.value + '"'

    # Variable reference
    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        return "|  " * indent + self.name

    # Vector element reference: name[index]
    @addToClass(AST.VectorElement)
    def printTree(self, indent=0):
        s = "|  " * indent + "REF\n"
        s += "|  " * (indent + 1) + self.name + "\n"
        s += "|  " * (indent + 1) + str(self.index)
        return s

    # Matrix element reference: name[row][col]
    @addToClass(AST.MatrixElement)
    def printTree(self, indent=0):
        s = "|  " * indent + "REF\n"
        s += "|  " * (indent + 1) + self.name + "\n"
        s += "|  " * (indent + 1) + str(self.row) + "\n"
        s += "|  " * (indent + 1) + str(self.col)
        return s

    # Matrix represented as nested vectors
    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        s = "|  " * indent + "VECTOR\n"
        for i, row in enumerate(self.rows):  # each row is itself a vector
            s += row.printTree(indent + 1)
            if i < len(self.rows) - 1:
                s += "\n"
        return s

    # Vector literal
    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        s = "|  " * indent + "VECTOR\n"
        for i, elem in enumerate(self.elements):
            s += elem.printTree(indent + 1)
            if i < len(self.elements) - 1:
                s += "\n"
        return s

    # Matrix function: zeros, ones, eye, etc.
    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        s = "|  " * indent + self.name + "\n"
        s += "|  " * (indent + 1) + str(self.size)
        return s

    # Unary minus: -expr
    @addToClass(AST.UnaryMinus)
    def printTree(self, indent=0):
        s = "|  " * indent + "-\n"
        s += self.expr.printTree(indent + 1)
        return s

    # Matrix/vector transpose: expr'
    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        s = "|  " * indent + "TRANSPOSE\n"
        s += self.expr.printTree(indent + 1)
        return s
