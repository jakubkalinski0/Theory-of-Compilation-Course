from sly import Parser
from LAB_1_lexical_analyzer import Scanner

class MParser(Parser):

    # Import tokenów z poprzednich zajęć (skaner)
    tokens = Scanner.tokens

    # Główna nie-terminalna symbolika gramatyki
    # Parser zaczyna analizę od reguły "program"
    start = 'program'
    
    # Plik do zapisu debugowania parsera (opcjonalne)
    debugfile = 'parser2.out'

    # -----------------------------------------------
    # PRIORYTETY OPERATORÓW
    # -----------------------------------------------
    # Określają kolejność wiązania operatorów,
    # aby parser rozstrzygał niejednoznaczności.
    #
    # 'right' – prawostronne wiązanie
    # 'left' – lewostronne wiązanie
    # 'nonassoc' – brak łączenia (dla IF-ELSE)
    precedence = (
        ('nonassoc', 'IFX'),                 # IF bez ELSE
        ('nonassoc', 'ELSE'),                # IF z ELSE
      #  ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),  # x += y itp.
        ('nonassoc', '<', '>', 'LEQ', 'GEQ', 'NEQ', 'EQ'),              # operatory relacyjne
        ('left', '+', '-', 'DOTADD', 'DOTSUB'),                  # klasyczne dodawanie/odejmowanie
        ('left', '*', '/', 'DOTMUL', 'DOTDIV'),                  # mnożenie klasyczne
        ('right', 'UMINUS'),                 # unarny minus
        ('left', "'"),                       # transpozycja macierzowa
    )

    # -----------------------------------------------
    # GŁÓWNA KONSTRUKCJA PROGRAMU
    # -----------------------------------------------

    @_('instructions_opt')
    def program(self, p):
        # Program to lista instrukcji (może być pusta)
        pass

    @_('instructions')
    def instructions_opt(self, p):
        # Opcjonalna lista instrukcji
        pass

    @_('')
    def instructions_opt(self, p):
        # Pusta lista instrukcji (dozwolone)
        pass

    @_('instruction')
    def instructions(self, p):
        # Pojedyncza instrukcja
        pass

    @_('instruction instructions')
    def instructions(self, p):
        # Instrukcja + kolejne instrukcje
        pass

    # -----------------------------------------------
    # KONSTRUKCJE INSTRUKCYJNE
    # -----------------------------------------------
    #
    # Instrukcja może być:
    # - przypisaniem
    # - zwykłą instrukcją (break, continue, return)
    # - blokiem { ... }
    @_('assignment ";"',
       'statement ";"',
       '"{" instructions "}"')
    def instruction(self, p):
        pass

    # Instrukcja IF bez ELSE
    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        pass

    # Instrukcja IF z ELSE
    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        pass

    # WHILE(condition) instruction
    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        pass

    # FOR j = 1:10 instruction
    @_('FOR var "=" range instruction')
    def instruction(self, p):
        pass

    # Range: a:b
    @_('expression ":" expression')
    def range(self, p):
        pass

    # -----------------------------------------------
    # WARUNKI LOGICZNE
    # -----------------------------------------------
    @_('expression EQ expression',
       'expression NEQ expression',
       'expression LEQ expression',
       'expression GEQ expression',
       'expression "<" expression',
       'expression ">" expression')
    def condition(self, p):
        pass

    # -----------------------------------------------
    # PRZYPISANIA
    # -----------------------------------------------
    @_('MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN', '"="')
    def assignment_op(self, p):
        # Operator przypisania: =, +=, -=, *=, /=
        pass

    @_('var assignment_op expression',
       'matrix_element assignment_op expression',
       'vector_element assignment_op expression')
    def assignment(self, p):
        # Przypisania mogą dotyczyć zmiennej lub elementów macierzy/wektora
        pass

    # -----------------------------------------------
    # FUNKCJE TWORZĄCE MACIERZE
    # -----------------------------------------------
    @_('matrix_function_name "(" INTNUM ")"')
    def matrix_function(self, p):
        # Przykłady: zeros(5), ones(10), eye(3)
        pass

    @_('EYE', 'ONES', 'ZEROS')
    def matrix_function_name(self, p):
        pass

    # -----------------------------------------------
    # TWORZENIE MACIERZY Z WARTOŚCI
    # -----------------------------------------------
    @_('"[" vectors "]"')
    def matrix(self, p):
        # Macierz tworzona jako: [[1, 2], [3, 4]]
        pass

    @_('vectors "," vector',
       'vector')
    def vectors(self, p):
        # Kolejne wiersze macierzy
        pass

    @_('"[" variables "]"')
    def vector(self, p):
        # Wektor złożony z wartości
        pass

    @_('variables "," variable',
       'variable')
    def variables(self, p):
        # Lista parametrów w wierszu
        pass

    @_('number', 'var', 'element')
    def variable(self, p):
        # Zmienna w macierzy: liczba, identyfikator, element macierzy
        pass

    @_('vector_element', 'matrix_element')
    def element(self, p):
        pass

    # Element wektora: A[5]
    @_('ID "[" INTNUM "]"')
    def vector_element(self, p):
        pass

    # Element macierzy: A[2,3]
    @_('ID "[" INTNUM "," INTNUM "]"')
    def matrix_element(self, p):
        pass

    # Zmienna: identyfikator
    @_('ID')
    def var(self, p):
        pass

    # Liczby całkowite lub zmiennoprzecinkowe
    @_('INTNUM', 'FLOATNUM')
    def number(self, p):
        pass

    @_('STRING')
    def string(self, p):
        pass

    # -----------------------------------------------
    # WYRAŻENIA ARYTMETYCZNE I MACIERZOWE
    # -----------------------------------------------
    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression',
       'expression DOTADD expression',
       'expression DOTSUB expression',
       'expression DOTMUL expression',
       'expression DOTDIV expression')
    def expression(self, p):
        # Wyrażenia binarne: skalary i macierze
        pass

    @_('num_expression', 'matrix', 'matrix_function',
       'uminus', 'transposition', 'matrix_element', 'vector_element')
    def expression(self, p):
        # Inne rodzaje wyrażeń
        pass

    @_('number', 'var')
    def num_expression(self, p):
        # Proste wyrażenie numeryczne
        pass

    # Unary minus: -x
    @_('"-" expression %prec UMINUS')
    def uminus(self, p):
        pass

    # Transpozycja macierzy: A'
    @_('expression "\'"')
    def transposition(self, p):
        pass

    # -----------------------------------------------
    # STATEMENT: break, continue, return, print
    # -----------------------------------------------
    @_('BREAK')
    def statement(self, p):
        pass

    @_('CONTINUE')
    def statement(self, p):
        pass

    @_('RETURN expression')
    def statement(self, p):
        pass

    @_('PRINT print_vals')
    def statement(self, p):
        pass

    @_('print_vals "," print_val',
       'print_val')
    def print_vals(self, p):
        pass

    @_('string', 'expression')
    def print_val(self, p):
        pass

    # -----------------------------------------------
    # OBSŁUGA BŁĘDÓW PARSERA
    # -----------------------------------------------
    def error(self, p):
        if p:
            # Błąd syntaktyczny: wiemy, gdzie wystąpił
            print(f"Syntax error at line {p.lineno}: {p.type}('{p.value}')")
        else:
            # Koniec wejścia w nieoczekiwanym miejscu
            print("Unexpected end of input")
