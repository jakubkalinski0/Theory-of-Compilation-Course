import sys
from sly import Lexer

class Scanner(Lexer):

    # Lista tokenów zwracanych przez skaner.
    # Uwaga: znaki jednowyrazowe (literals) nie muszą pojawiać się tutaj.
    tokens = {
        DOTADD, DOTMUL, DOTDIV, DOTSUB,            # operatory macierzowe element-po-elemencie
        ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,# operatory przypisania z działaniem
        LEQ, GEQ, NEQ, EQ,                         # operatory relacyjne
        IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN,
        EYE, ZEROS, ONES, PRINT,                   # słowa kluczowe
        INTNUM, FLOATNUM, STRING, ID               # identyfikatory i liczby
    }
    
    # Jednoliterowe tokeny traktowane jako osobne leksemy.
    literals = {
        '+', '-', '*', '/', '=', '<', '>',
        '(', ')', '[', ']', '{', '}',
        ':', ',', ';', "'"
    }
    
    # Ignorowane białe znaki: spacja i tabulacja.
    ignore = ' \t'

    # Komentarze zaczynające się od # do końca linii.
    ignore_comment = r'\#.*'
    
    # --- Operatory macierzowe element-po-elemencie ---
    DOTADD = r'\.\+'
    DOTSUB = r'\.\-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'
    
    # --- Operatory przypisania ---
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    
    # --- Operatory relacyjne ---
    LEQ = r'<='
    GEQ = r'>='
    NEQ = r'!='
    EQ  = r'=='
    
    # --- Identyfikatory i słowa kluczowe ---
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        # Słowa kluczowe mapowane na osobne tokeny
        keywords = {
            'if': 'IF',
            'else': 'ELSE',
            'for': 'FOR',
            'while': 'WHILE',
            'break': 'BREAK',
            'continue': 'CONTINUE',
            'return': 'RETURN',
            'eye': 'EYE',
            'zeros': 'ZEROS',
            'ones': 'ONES',
            'print': 'PRINT'
        }
        # Jeśli leksem to słowo kluczowe -> zmień typ tokena
        t.type = keywords.get(t.value, 'ID')
        return t
    
    # --- Liczby zmiennoprzecinkowe ---
    # Obsługuje formaty:
    #  - 12.34
    #  - .45
    #  - 10.
    #  - 1.5e10 / 1e-3 (notacja naukowa)
    @_(r'(\d*\.\d+|\d+\.)([eE][+-]?\d+)?|\d+[eE][+-]?\d+')
    def FLOATNUM(self, t):
        t.value = float(t.value)    # zamiana na Pythonowy float
        return t

    # --- Liczby całkowite ---
    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t
    
    # --- Stringi ---
    # Obsługuje znaki ucieczki: \"
    @_(r'"([^"\\]|\\.)*"')
    def STRING(self, t):
        t.value = t.value[1:-1]     # usuwamy cudzysłowy
        self.lineno += t.value.count('\n')  # jeśli string zawiera \n, aktualizujemy liczenie linii
        return t
    
    # --- Nowe linie ---
    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value) # aktualizacja numeru linii
    
    # --- Obsługa błędów ---
    def error(self, t):
        # Wyświetlenie błędu leksykalnego
        print(f"Line {self.lineno}: Illegal character '{t.value[0]}'")
        self.index += 1             # przesuwamy analizator o jeden znak


if __name__ == '__main__':
    lexer = Scanner()

    # Odczytujemy nazwę pliku z argumentów programu
    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
    
    try:
        with open(filename, "r") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    # Tokenizacja całego pliku i wypisywanie wyników
    for tok in lexer.tokenize(text):
        if tok.type in lexer.literals:
            # Token jednowyrazowy: pokazujemy go w formie np. +(+)
            print(f"({tok.lineno}): {tok.value}({tok.value})")
        else:
            # Token słowny lub liczba: np. ID(A), INTNUM(5)
            print(f"({tok.lineno}): {tok.type}({tok.value})")
