"""
Visitor pattern implementation using decorators.
This module provides a dispatch mechanism that automatically routes method calls
to the appropriate handler based on the type of the first parameter.

Usage:
    @on('node')
    def visit(self, node):
        pass
    
    @when(SomeClass)
    def visit(self, node):
        # Handle SomeClass nodes
        pass
"""

import inspect

__all__ = ['on', 'when']


def on(param_name):
    """
    Decorator that creates a dispatcher for a method.
    The dispatcher will route calls to methods decorated with @when based on
    the type of the parameter named 'param_name'.
    
    Args:
        param_name: Name of the parameter to dispatch on (typically 'node')
    
    Returns:
        A Dispatcher object that replaces the original function
    """
    def f(fn):
        dispatcher = Dispatcher(param_name, fn)
        return dispatcher
    return f


def when(param_type):
    """
    Decorator that registers a method as a handler for a specific type.
    When the dispatcher is called with an object of 'param_type', this method
    will be invoked.
    
    Args:
        param_type: The class type this method handles
    
    Returns:
        A wrapper function that delegates to the dispatcher
    """
    def f(fn):
        # Get the calling frame to access the function being decorated
        frame = inspect.currentframe().f_back
        func_name = fn.func_name if 'func_name' in dir(fn) else fn.__name__
        dispatcher = frame.f_locals[func_name]
        # If it's already wrapped, get the underlying dispatcher
        if not isinstance(dispatcher, Dispatcher):
            dispatcher = dispatcher.dispatcher
        # Register this method as a handler for the specified type
        dispatcher.add_target(param_type, fn)

        def ff(*args, **kw):
            return dispatcher(*args, **kw)
        ff.dispatcher = dispatcher
        return ff
    return f


class Dispatcher(object):
    """
    Dispatcher that routes method calls based on the type of a parameter.
    Maintains a mapping of types to handler functions.
    """
    def __init__(self, param_name, fn):
        # Find the index of the parameter we're dispatching on
        self.param_index = self.__argspec(fn).args.index(param_name)
        self.param_name = param_name
        # Dictionary mapping types to their handler functions
        self.targets = {}

    def __call__(self, *args, **kw):
        """
        Dispatch to the appropriate handler based on the type of the parameter.
        First tries exact type match, then checks for subclass matches.
        """
        # Get the type of the parameter we're dispatching on
        typ = args[self.param_index].__class__
        # Try exact type match first
        d = self.targets.get(typ)
        if d is not None:
            return d(*args, **kw)
        else:
            # If no exact match, check for subclass matches
            issub = issubclass
            t = self.targets
            ks = iter(t)
            return [t[k](*args, **kw) for k in ks if issub(typ, k)]

    def add_target(self, typ, target):
        """
        Register a handler function for a specific type.
        
        Args:
            typ: The class type to handle
            target: The function to call when this type is encountered
        """
        self.targets[typ] = target

    @staticmethod
    def __argspec(fn):
        """
        Get function argument specification.
        Uses getfullargspec for Python 3, falls back to getargspec for Python 2.
        """
        # Support for Python 3 type hints requires inspect.getfullargspec
        if hasattr(inspect, 'getfullargspec'):
            return inspect.getfullargspec(fn)
        else:
            return inspect.getargspec(fn)
