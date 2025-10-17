import sys
from sly import Lexer

class Scanner(Lexer):
    # Lista tokenów
    tokens = {
        ADD, SUB, MUL, DIV,
        DOTADD, DOTSUB, DOTMUL, DOTDIV,
        ASSIGN, ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
        LT, GT, LE, GE, NE, EQ,
        IF, ELSE, FOR, WHILE,
        BREAK, CONTINUE, RETURN,
        EYE, ZEROS, ONES,
        PRINT,
        ID, INTNUM, FLOATNUM, STRING
    }

    # Literały – pojedyncze znaki traktowane jako tokeny
    literals = { '(', ')', '[', ']', '{', '}', ':', '\'', ',', ';', "'" }

    # Ignorowane znaki
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Operatory przypisania
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    ASSIGN    = r'='

    # Macierzowe operatory binarne
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'

    # Operatory binarne
    ADD = r'\+'
    SUB = r'-'
    MUL = r'\*'
    DIV = r'/'

    # Operatory relacyjne
    LE = r'<='
    GE = r'>='
    NE = r'!='
    EQ = r'=='
    LT = r'<'
    GT = r'>'

    # Liczby zmiennoprzecinkowe (.5, 60., 1e3, 2.5E-2 itp.)
    @_(r'((\d+\.\d*)|(\.\d+))([eE][+-]?\d+)?|\d+[eE][+-]?\d+')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    # Liczby całkowite
    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    # Stringi
    @_(r'\"[^\n"]*\"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    # Identyfikatory i słowa kluczowe
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
    ID['if']       = IF
    ID['else']     = ELSE
    ID['for']      = FOR
    ID['while']    = WHILE
    ID['break']    = BREAK
    ID['continue'] = CONTINUE
    ID['return']   = RETURN
    ID['eye']      = EYE
    ID['zeros']    = ZEROS
    ID['ones']     = ONES
    ID['print']    = PRINT

    # Nowe linie (dla numerów linii)
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Błędy leksykalne
    def error(self, t):
        print(f"Nieoczekiwany znak {t.value[0]!r} w linii {self.lineno}")
        self.index += 1


if __name__ == '__main__':
    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"({tok.lineno}): {tok.type}({tok.value})")
