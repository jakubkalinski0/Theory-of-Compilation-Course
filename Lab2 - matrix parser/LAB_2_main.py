import sys
from LAB_1_lexical_analyzer import Scanner
from LAB_2_matrix_parser import MParser


if __name__ == '__main__':

    lexer = Scanner()
    parser = MParser()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.txt"
    with open(filename, "r") as file:
        text = file.read()

    parser.parse(lexer.tokenize(text))
