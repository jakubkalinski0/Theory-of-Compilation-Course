#!/usr/bin/python

"""
Symbol table implementation for type checking.
Manages variable symbols and their types/shapes in a hierarchical scope structure.
Used by TypeChecker to track variable declarations and perform scope analysis.
"""

class Symbol:
    """
    Base class for symbols in the symbol table.
    """
    pass

class VariableSymbol(Symbol):
    """
    Represents a variable symbol with its type and shape information.
    Used during type checking to track variable declarations.
    """
    def __init__(self, name, type, shape=None):
        self.name = name  # Variable name
        self.type = type  # Type: 'int', 'float', 'vector', 'matrix', 'string'
        self.shape = shape  # Shape: None for scalars, (n,) for vectors, (m,n) for matrices

class SymbolTable(object):
    """
    Hierarchical symbol table for managing variable scopes.
    Implements a tree structure where each scope can have a parent scope.
    Used for lexical scoping: variables are searched from current scope up to root.
    """
    def __init__(self, parent, name):
        self.parent = parent  # Parent scope (None for root scope)
        self.name = name  # Scope name (for debugging)
        self.symbols = {}  # Dictionary mapping variable names to symbols
    
    def put(self, name, symbol):
        """
        Add a symbol to the current scope.
        
        Args:
            name: Variable name
            symbol: VariableSymbol object
        """
        self.symbols[name] = symbol
    
    def get(self, name):
        """
        Look up a symbol by name, searching from current scope up to root.
        
        Args:
            name: Variable name to look up
        
        Returns:
            VariableSymbol if found, None otherwise
        """
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent is not None:
            # Search in parent scope
            return self.parent.get(name)
        return None
    
    def getParentScope(self):
        """Get the parent scope."""
        return self.parent
    
    def pushScope(self, name):
        """
        Create and return a new child scope.
        Used when entering a new scope (e.g., function, block).
        
        Args:
            name: Name of the new scope
        
        Returns:
            New SymbolTable with this table as parent
        """
        return SymbolTable(self, name)
    
    def popScope(self):
        """
        Exit current scope and return to parent scope.
        
        Returns:
            Parent scope SymbolTable
        """
        return self.parent