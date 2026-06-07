"""
Memory management for the interpreter.
Implements a stack-based memory system to handle variable scopes.
"""


class Memory:
    """
    Represents a single memory scope (e.g., global scope, function scope).
    Stores variables as a dictionary mapping names to values.
    """
    def __init__(self, name):
        # Name of the scope (for debugging/identification)
        self.name = name
        # Dictionary storing variable names and their values
        self.memory = {}
    
    def has_key(self, name):
        """Check if a variable exists in this scope."""
        return name in self.memory
    
    def get(self, name):
        """Get the value of a variable from this scope."""
        return self.memory.get(name)
    
    def put(self, name, value):
        """Store a variable in this scope."""
        self.memory[name] = value


class MemoryStack:
    """
    Stack-based memory system for managing variable scopes.
    Implements lexical scoping: variables are searched from current scope
    up to global scope. New variables are created in the current scope.
    """
    def __init__(self, memory=None):
        # Stack of Memory objects, with top of stack being current scope
        self.stack = []
        if memory is not None:
            # Initialize with a global scope
            self.stack.append(memory)
    
    def get(self, name):
        """
        Retrieve a variable value by searching from current scope to global scope.
        This implements lexical scoping rules.
        """
        # Search from top to bottom (current scope to global scope)
        for mem in reversed(self.stack):
            if mem.has_key(name):
                return mem.get(name)
        return None
    
    def insert(self, name, value):
        """
        Insert a new variable into the current (top) scope.
        Used when creating a new variable.
        """
        # Insert into current (top) scope
        if self.stack:
            self.stack[-1].put(name, value)
    
    def set(self, name, value):
        """
        Set a variable value. If variable exists in any scope, update it there.
        If variable doesn't exist, create it in the current scope.
        This implements the behavior where assignments update existing variables
        or create new ones in the current scope.
        """
        # Set in the scope where variable exists, or top scope
        for mem in reversed(self.stack):
            if mem.has_key(name):
                # Variable found: update it in its original scope
                mem.put(name, value)
                return
        # If not found, insert in current scope (create new variable)
        self.insert(name, value)
    
    def push(self, memory):
        """
        Push a new memory scope onto the stack.
        Used when entering a new scope (e.g., function call, block).
        """
        self.stack.append(memory)
    
    def pop(self):
        """
        Pop the top memory scope from the stack.
        Used when exiting a scope (e.g., returning from function).
        """
        if self.stack:
            return self.stack.pop()
        return None