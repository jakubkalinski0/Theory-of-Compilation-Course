"""
Custom exceptions for control flow in the interpreter.
These exceptions are used to implement break, continue, and return statements
that can break out of deeply nested structures (loops, functions).
"""


class ReturnValueException(Exception):
    """
    Exception raised when a return statement is executed.
    Carries the return value to be propagated back through the call stack.
    """
    def __init__(self, value):
        self.value = value
        
class BreakException(Exception):
    """
    Exception raised when a break statement is executed.
    Propagates up through nested loops until caught by the loop handler.
    """
    pass

class ContinueException(Exception):
    """
    Exception raised when a continue statement is executed.
    Propagates up through nested structures until caught by the loop handler.
    """
    pass
