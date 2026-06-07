# Theory of Compilation

A course project from AGH UST that builds a compiler and interpreter for a MATLAB-like matrix language. The work is split into five labs, each adding the next stage of the compilation pipeline.

## Requirements

- Python 3
- [sly](https://github.com/dabeaz/sly) (lexer and parser)
- [NumPy](https://numpy.org/) (Lab 5 only, for matrix operations)

```bash
pip install sly numpy
```

## Project structure

| Lab | Folder | Description |
|-----|--------|-------------|
| 1 | `Lab1 - lecixal analyzer/` | Lexical analyzer (tokenizer) |
| 2 | `Lab2 - matrix parser/` | Syntax parser |
| 3 | `Lab3 - AST/` | Abstract syntax tree construction |
| 4 | `Lab4 - type checker/` | Semantic analysis and type checking |
| 5 | `Lab5 - interpreter/` | Full interpreter |

Each lab folder is self-contained and includes the modules needed to run that stage.

## Language features

The source language uses `.m` files with MATLAB-inspired syntax:

- Scalar, vector, and matrix types
- Matrix literals, indexing (`A[i]`, `A[i,j]`), transpose (`'`)
- Built-in functions: `zeros`, `ones`, `eye`
- Arithmetic and element-wise operators (`+`, `.*`, `.+`, and others)
- Compound assignments (`+=`, `-=`, and others)
- Control flow: `if`/`else`, `while`, `for`, `break`, `continue`, `return`
- `print` statement
- Comments starting with `#`

## Running the labs

Run commands from inside each lab folder.

### Lab 1: Lexical analyzer

```bash
cd "Lab1 - lecixal analyzer"
python scanner.py example1.m
```

Prints a list of tokens with line numbers.

### Lab 2: Syntax parser

```bash
cd "Lab2 - matrix parser"
python main.py example1.m
```

Validates that the input file matches the grammar. Parser debug output is written to `parser2.out`.

### Lab 3: AST

```bash
cd "Lab3 - AST"
python main.py example1.m
```

Parses the input and writes the AST tree to `result.m`. Reference outputs are in `example1.tree`, `example2.tree`, and `example3.tree`.

### Lab 4: Type checker

```bash
cd "Lab4 - type checker"
python main.py test.m
```

Runs semantic analysis and reports type errors, scope issues, and invalid control flow.

### Lab 5: Interpreter

```bash
cd "Lab5 - interpreter"
python main.py pi.m
python main.py matrix.m
```

Runs the full pipeline: scan, parse, type check, then execute. Sample programs `pi.m` and `matrix.m` are included.

## Pipeline overview

1. **Lab 1** scans the source file into tokens
2. **Lab 2** parses tokens and checks syntax
3. **Lab 3** builds an abstract syntax tree
4. **Lab 4** performs semantic analysis and type checking
5. **Lab 5** interprets and runs the program

## License

MIT License. See [LICENSE](LICENSE).
