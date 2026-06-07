# Każda klasa reprezentuje węzeł AST. Węzły tworzone są podczas parsowania
# i później drukowane przez TreePrinter.

class Node:
    # Klasa bazowa — wszystkie węzły AST ją dziedziczą
    def __str__(self):
        return self.printTree()

class Program(Node):
    # Program jest korzeniem drzewa — przechowuje listę instrukcji
    def __init__(self, instructions):
        self.instructions = instructions

class Instructions(Node):
    # Lista instrukcji (blok kodu). Instrukcje trzymane są w liście.
    def __init__(self):
        self.instructions = []

    def add(self, instruction):
        # Dodawanie kolejnej instrukcji do listy
        self.instructions.append(instruction)

class BinExpr(Node):
    # Wyrażenie binarne (np. +, -, *, /, .+, .-, ...)
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class RelExpr(Node):
    # Wyrażenia relacyjne (np. <, >, ==, !=, <=, >=)
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Assignment(Node):
    # Przypisanie: zwykłe (=) lub z operatorem złożonym (+=, -=, ...)
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class If(Node):
    # Instrukcja warunkowa
    # THEN-block i ELSE-block to obiekty Instructions
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class While(Node):
    # Pętla while
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class For(Node):
    # Pętla for — w tym języku działa na zakresach liczb
    def __init__(self, var, range_expr, body):
        self.var = var
        self.range = range_expr
        self.body = body

class Range(Node):
    # Zakres dla pętli for: od start do end
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Break(Node):
    # Instrukcja przerwania pętli
    pass

class Continue(Node):
    # Instrukcja przejścia do kolejnej iteracji
    pass

class Return(Node):
    # Zwraca wyrażenie z funkcji (jeśli byłyby definiowane)
    def __init__(self, expr):
        self.expr = expr

class Print(Node):
    # Instrukcja wypisania — lista wartości
    def __init__(self, values):
        self.values = values

class IntNum(Node):
    # Liczba całkowita
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    # Liczba zmiennoprzecinkowa
    def __init__(self, value):
        self.value = value

class String(Node):
    # Stała tekstowa
    def __init__(self, value):
        self.value = value

class Variable(Node):
    # Zmienna (np. A, B, myVar)
    def __init__(self, name):
        self.name = name

class VectorElement(Node):
    # Element wektora: A[i]
    def __init__(self, name, index):
        self.name = name
        self.index = index

class MatrixElement(Node):
    # Element macierzy: A[i, j]
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col

class Matrix(Node):
    # Macierz: lista wierszy (wektorów)
    def __init__(self, rows):
        self.rows = rows

class Vector(Node):
    # Wektor: lista elementów
    def __init__(self, elements):
        self.elements = elements

class MatrixFunction(Node):
    # Funkcje macierzowe: zeros(n), ones(n), eye(n)
    def __init__(self, name, size):
        self.name = name
        self.size = size

class UnaryMinus(Node):
    # Negacja unarna: -x
    def __init__(self, expr):
        self.expr = expr

class Transposition(Node):
    # Transpozycja macierzy: A'
    def __init__(self, expr):
        self.expr = expr