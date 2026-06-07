"""
Main entry point for the interpreter.
This module orchestrates the compilation pipeline:
1. Lexical analysis (scanner)
2. Syntactic analysis (parser)
3. Semantic analysis (type checker)
4. Interpretation (interpreter)
"""

import sys
import os
from scanner import Scanner
from parser import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':
    # Step 1: Open and read the source file
    # If filename is provided as command-line argument, use it; otherwise default to matrix.m
    try:
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        else:
            # Default to matrix.m in the same directory as the script
            # This ensures the file is found regardless of current working directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(script_dir, "pi.m")
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # Initialize scanner and parser for lexical and syntactic analysis
    scanner = Scanner()
    parser = Mparser()
    text = file.read()
    file.close()

    # Step 2: Lexical and Syntactic Analysis
    # Tokenize the source code and parse it into an Abstract Syntax Tree (AST)
    tokens = scanner.tokenize(text)
    ast = parser.parse(tokens)
    
    # If parsing failed, exit with error code
    if ast is None:
        print("Parsing failed")
        sys.exit(1)

    # Step 3: Semantic Analysis (Type Checking)
    # Verify that the program is semantically correct (type checking, scope rules, etc.)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    
    # Step 4: Interpretation
    # Only execute the program if no semantic errors were found
    # This ensures we don't try to run invalid programs
    if not typeChecker.errors:
        interpreter = Interpreter()
        try:
            # Start interpretation by visiting the root of the AST
            ast.accept(interpreter)
        except Exception as e:
            # Catch any runtime errors during execution
            print(f"Runtime error: {e}")
    else:
        print("Type checking failed, interpretation skipped")