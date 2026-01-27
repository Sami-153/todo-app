# Pascal LL(1) Parser

## Lab 8 - Compiler Construction

A complete table-driven LL(1) parser for a Pascal subset, including lexer, symbol table, and parse tree with preorder traversal output.

---

## Project Structure

```
Lab8/
├── source_code/
│   ├── lexer.py           # Token scanner
│   ├── symbol_table.py    # Symbol table manager
│   ├── grammar.py         # Grammar, FIRST/FOLLOW, parse table
│   ├── parse_tree.py      # Parse tree with preorder traversal
│   ├── parser.py          # LL(1) table-driven parser
│   ├── main.py            # Entry point
│   └── README.md          # Project documentation
├── manual_work/
│   ├── first-follow-set.pdf   # FIRST/FOLLOW computation
│   └── parse_table.csv        # LL(1) table for Excel
├── lab_report/
│   └── 2022-CS-153-Report.pdf # Final Lab Report
└── test_results/
    ├── case_01_valid_assign.pas
    ├── case_02_valid_control_flow.pas
    ├── case_03_valid_loops.pas
    ├── case_04_valid_nested.pas
    ├── case_05_valid_types.pas
    ├── case_06_error_missing_semicolon.pas
    ├── case_07_error_incomplete_expr.pas
    ├── case_08_error_missing_then.pas
    ├── case_09_error_bad_identifier.pas
    └── case_10_error_unbalanced_parens.pas
```

---

## How to Run

### Parse a Pascal File
```bash
cd source_code
python main.py ../test_results/case_01_valid_assign.pas
```

### Run with Debug Trace
```bash
python main.py ../test_results/case_01_valid_assign.pas --debug
```

### Interactive Mode
```bash
python main.py
```
Then enter Pascal code and press Enter twice to parse.

---

## Test Cases

### Valid Programs
1. `case_01_valid_assign.pas`: Simple variable declaration and assignment.
2. `case_02_valid_control_flow.pas`: Arithmetic expressions and if-then-else.
3. `case_03_valid_loops.pas`: While-do loops with assignment.
4. `case_04_valid_nested.pas`: Nested if statements and blocks.
5. `case_05_valid_types.pas`: Usage of real and boolean types.

### Invalid Programs (Should Show Error)
6. `case_06_error_missing_semicolon.pas`: Syntax error, missing semicolon.
7. `case_07_error_incomplete_expr.pas`: Syntax error, unexpected end of expression.
8. `case_08_error_missing_then.pas`: Syntax error, missing 'then' keyword.
9. `case_09_error_bad_identifier.pas`: Lexical/Syntax error, identifier starting with a digit.
10. `case_10_error_unbalanced_parens.pas`: Syntax error, missing closing parenthesis.

---

## Output Format

The parser outputs:
1. **ACCEPTED** or **REJECTED** status
2. **Preorder traversal** of the parse tree
3. **Graphical tree** representation

Example output:
```
*** ACCEPTED ***

PARSE TREE (Preorder Traversal)
============================================================
Program
  program (program)
  id (test)
  ; (;)
  Block
    Declarations
      ε
    begin (begin)
    StmtList
      Statement
        id (x)
        := (:=)
        Expression
          ...
```

---

## Pascal Subset Supported

- Program structure: `program name; ... end.`
- Variable declarations: `var x, y: integer;`
- Types: `integer`, `real`, `boolean`
- Statements: assignment, if-then-else, while-do, read, write
- Expressions: arithmetic (+, -, *, /, div, mod)
- Comparisons: <, >, <=, >=, =, <>
