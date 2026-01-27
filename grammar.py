"""
Pascal LL(1) Grammar Definition
Contains grammar productions, FIRST sets, FOLLOW sets, and LL(1) parsing table
"""

from lexer import TokenType

# ============================================================================
# GRAMMAR SYMBOLS
# ============================================================================

# Nonterminals
NONTERMINALS = [
    'Program', 'Block', 'Declarations', 'DeclList', 'DeclListP',
    'Decl', 'IdList', 'IdListP', 'Type',
    'StmtList', 'StmtListP', 'Statement', 'AssignStmt', 
    'IfStmt', 'ElsePart', 'WhileStmt', 'ReadStmt', 'WriteStmt',
    'ExprList', 'ExprListP', 'BoolExpr', 'RelOp',
    'Expression', 'ExpressionP', 'Term', 'TermP', 'Factor'
]

# Terminal symbols (mapped to TokenTypes)
TERMINALS = [
    'program', 'id', ';', '.', 'var', 'begin', 'end', ':', ',',
    'integer', 'real', 'boolean',
    ':=', 'if', 'then', 'else', 'while', 'do', 'read', 'write',
    '(', ')', '+', '-', '*', '/', 'div', 'mod',
    '<', '>', '<=', '>=', '=', '<>',
    'num', '$'
]

# Epsilon symbol
EPSILON = 'ε'

# ============================================================================
# PRODUCTIONS
# Stored as: nonterminal -> list of production alternatives
# Each production is a list of symbols (terminals/nonterminals)
# ============================================================================

PRODUCTIONS = {
    'Program': [['program', 'id', ';', 'Block', '.']],
    
    'Block': [['Declarations', 'begin', 'StmtList', 'end']],
    
    'Declarations': [
        ['var', 'DeclList'],
        [EPSILON]
    ],
    
    'DeclList': [['Decl', 'DeclListP']],
    
    'DeclListP': [
        ['Decl', 'DeclListP'],
        [EPSILON]
    ],
    
    'Decl': [['IdList', ':', 'Type', ';']],
    
    'IdList': [['id', 'IdListP']],
    
    'IdListP': [
        [',', 'id', 'IdListP'],
        [EPSILON]
    ],
    
    'Type': [
        ['integer'],
        ['real'],
        ['boolean']
    ],
    
    'StmtList': [['Statement', 'StmtListP']],
    
    'StmtListP': [
        [';', 'Statement', 'StmtListP'],
        [EPSILON]
    ],
    
    'Statement': [
        ['id', ':=', 'Expression'],     # Assignment
        ['IfStmt'],                      # If statement
        ['WhileStmt'],                   # While statement
        ['ReadStmt'],                    # Read statement
        ['WriteStmt'],                   # Write statement
        ['begin', 'StmtList', 'end'],   # Block statement
        [EPSILON]                        # Empty statement
    ],
    
    'AssignStmt': [['id', ':=', 'Expression']],
    
    'IfStmt': [['if', 'BoolExpr', 'then', 'Statement', 'ElsePart']],
    
    'ElsePart': [
        ['else', 'Statement'],
        [EPSILON]
    ],
    
    'WhileStmt': [['while', 'BoolExpr', 'do', 'Statement']],
    
    'ReadStmt': [['read', '(', 'IdList', ')']],
    
    'WriteStmt': [['write', '(', 'ExprList', ')']],
    
    'ExprList': [['Expression', 'ExprListP']],
    
    'ExprListP': [
        [',', 'Expression', 'ExprListP'],
        [EPSILON]
    ],
    
    'BoolExpr': [['Expression', 'RelOp', 'Expression']],
    
    'RelOp': [
        ['<'],
        ['>'],
        ['<='],
        ['>='],
        ['='],
        ['<>']
    ],
    
    'Expression': [['Term', 'ExpressionP']],
    
    'ExpressionP': [
        ['+', 'Term', 'ExpressionP'],
        ['-', 'Term', 'ExpressionP'],
        [EPSILON]
    ],
    
    'Term': [['Factor', 'TermP']],
    
    'TermP': [
        ['*', 'Factor', 'TermP'],
        ['/', 'Factor', 'TermP'],
        ['div', 'Factor', 'TermP'],
        ['mod', 'Factor', 'TermP'],
        [EPSILON]
    ],
    
    'Factor': [
        ['(', 'Expression', ')'],
        ['id'],
        ['num'],
        ['+', 'Factor'],
        ['-', 'Factor']
    ]
}

# ============================================================================
# FIRST SETS
# ============================================================================

FIRST = {
    'Program': {'program'},
    'Block': {'var', 'begin'},
    'Declarations': {'var', EPSILON},
    'DeclList': {'id'},
    'DeclListP': {'id', EPSILON},
    'Decl': {'id'},
    'IdList': {'id'},
    'IdListP': {',', EPSILON},
    'Type': {'integer', 'real', 'boolean'},
    'StmtList': {'id', 'if', 'while', 'read', 'write', 'begin', EPSILON},
    'StmtListP': {';', EPSILON},
    'Statement': {'id', 'if', 'while', 'read', 'write', 'begin', EPSILON},
    'AssignStmt': {'id'},
    'IfStmt': {'if'},
    'ElsePart': {'else', EPSILON},
    'WhileStmt': {'while'},
    'ReadStmt': {'read'},
    'WriteStmt': {'write'},
    'ExprList': {'(', 'id', 'num', '+', '-'},
    'ExprListP': {',', EPSILON},
    'BoolExpr': {'(', 'id', 'num', '+', '-'},
    'RelOp': {'<', '>', '<=', '>=', '=', '<>'},
    'Expression': {'(', 'id', 'num', '+', '-'},
    'ExpressionP': {'+', '-', EPSILON},
    'Term': {'(', 'id', 'num', '+', '-'},
    'TermP': {'*', '/', 'div', 'mod', EPSILON},
    'Factor': {'(', 'id', 'num', '+', '-'}
}

# ============================================================================
# FOLLOW SETS
# ============================================================================

FOLLOW = {
    'Program': {'$'},
    'Block': {'.'},
    'Declarations': {'begin'},
    'DeclList': {'begin'},
    'DeclListP': {'begin'},
    'Decl': {'id', 'begin'},
    'IdList': {':', ')'},
    'IdListP': {':', ')'},
    'Type': {';'},
    'StmtList': {'end'},
    'StmtListP': {'end'},
    'Statement': {';', 'end', 'else'},
    'AssignStmt': {';', 'end', 'else'},
    'IfStmt': {';', 'end', 'else'},
    'ElsePart': {';', 'end', 'else'},
    'WhileStmt': {';', 'end', 'else'},
    'ReadStmt': {';', 'end', 'else'},
    'WriteStmt': {';', 'end', 'else'},
    'ExprList': {')'},
    'ExprListP': {')'},
    'BoolExpr': {'then', 'do'},
    'RelOp': {'(', 'id', 'num', '+', '-'},
    'Expression': {')', ';', ',', 'then', 'do', '<', '>', '<=', '>=', '=', '<>'},
    'ExpressionP': {')', ';', ',', 'then', 'do', '<', '>', '<=', '>=', '=', '<>'},
    'Term': {'+', '-', ')', ';', ',', 'then', 'do', '<', '>', '<=', '>=', '=', '<>'},
    'TermP': {'+', '-', ')', ';', ',', 'then', 'do', '<', '>', '<=', '>=', '=', '<>'},
    'Factor': {'*', '/', 'div', 'mod', '+', '-', ')', ';', ',', 'then', 'do', '<', '>', '<=', '>=', '=', '<>'}
}

# ============================================================================
# LL(1) PARSING TABLE
# Format: PARSE_TABLE[nonterminal][terminal] = production (list of symbols)
# ============================================================================

PARSE_TABLE = {
    'Program': {
        'program': ['program', 'id', ';', 'Block', '.']
    },
    
    'Block': {
        'var': ['Declarations', 'begin', 'StmtList', 'end'],
        'begin': ['Declarations', 'begin', 'StmtList', 'end']
    },
    
    'Declarations': {
        'var': ['var', 'DeclList'],
        'begin': [EPSILON]
    },
    
    'DeclList': {
        'id': ['Decl', 'DeclListP']
    },
    
    'DeclListP': {
        'id': ['Decl', 'DeclListP'],
        'begin': [EPSILON]
    },
    
    'Decl': {
        'id': ['IdList', ':', 'Type', ';']
    },
    
    'IdList': {
        'id': ['id', 'IdListP']
    },
    
    'IdListP': {
        ',': [',', 'id', 'IdListP'],
        ':': [EPSILON],
        ')': [EPSILON]
    },
    
    'Type': {
        'integer': ['integer'],
        'real': ['real'],
        'boolean': ['boolean']
    },
    
    'StmtList': {
        'id': ['Statement', 'StmtListP'],
        'if': ['Statement', 'StmtListP'],
        'while': ['Statement', 'StmtListP'],
        'read': ['Statement', 'StmtListP'],
        'write': ['Statement', 'StmtListP'],
        'begin': ['Statement', 'StmtListP'],
        'end': ['Statement', 'StmtListP']
    },
    
    'StmtListP': {
        ';': [';', 'Statement', 'StmtListP'],
        'end': [EPSILON]
    },
    
    'Statement': {
        'id': ['id', ':=', 'Expression'],
        'if': ['IfStmt'],
        'while': ['WhileStmt'],
        'read': ['ReadStmt'],
        'write': ['WriteStmt'],
        'begin': ['begin', 'StmtList', 'end'],
        ';': [EPSILON],
        'end': [EPSILON],
        'else': [EPSILON]
    },
    
    'IfStmt': {
        'if': ['if', 'BoolExpr', 'then', 'Statement', 'ElsePart']
    },
    
    'ElsePart': {
        'else': ['else', 'Statement'],
        ';': [EPSILON],
        'end': [EPSILON]
    },
    
    'WhileStmt': {
        'while': ['while', 'BoolExpr', 'do', 'Statement']
    },
    
    'ReadStmt': {
        'read': ['read', '(', 'IdList', ')']
    },
    
    'WriteStmt': {
        'write': ['write', '(', 'ExprList', ')']
    },
    
    'ExprList': {
        '(': ['Expression', 'ExprListP'],
        'id': ['Expression', 'ExprListP'],
        'num': ['Expression', 'ExprListP'],
        '+': ['Expression', 'ExprListP'],
        '-': ['Expression', 'ExprListP']
    },
    
    'ExprListP': {
        ',': [',', 'Expression', 'ExprListP'],
        ')': [EPSILON]
    },
    
    'BoolExpr': {
        '(': ['Expression', 'RelOp', 'Expression'],
        'id': ['Expression', 'RelOp', 'Expression'],
        'num': ['Expression', 'RelOp', 'Expression'],
        '+': ['Expression', 'RelOp', 'Expression'],
        '-': ['Expression', 'RelOp', 'Expression']
    },
    
    'RelOp': {
        '<': ['<'],
        '>': ['>'],
        '<=': ['<='],
        '>=': ['>='],
        '=': ['='],
        '<>': ['<>']
    },
    
    'Expression': {
        '(': ['Term', 'ExpressionP'],
        'id': ['Term', 'ExpressionP'],
        'num': ['Term', 'ExpressionP'],
        '+': ['Term', 'ExpressionP'],
        '-': ['Term', 'ExpressionP']
    },
    
    'ExpressionP': {
        '+': ['+', 'Term', 'ExpressionP'],
        '-': ['-', 'Term', 'ExpressionP'],
        ')': [EPSILON],
        ';': [EPSILON],
        ',': [EPSILON],
        'then': [EPSILON],
        'do': [EPSILON],
        'end': [EPSILON],
        'else': [EPSILON],
        '<': [EPSILON],
        '>': [EPSILON],
        '<=': [EPSILON],
        '>=': [EPSILON],
        '=': [EPSILON],
        '<>': [EPSILON]
    },
    
    'Term': {
        '(': ['Factor', 'TermP'],
        'id': ['Factor', 'TermP'],
        'num': ['Factor', 'TermP'],
        '+': ['Factor', 'TermP'],
        '-': ['Factor', 'TermP']
    },
    
    'TermP': {
        '*': ['*', 'Factor', 'TermP'],
        '/': ['/', 'Factor', 'TermP'],
        'div': ['div', 'Factor', 'TermP'],
        'mod': ['mod', 'Factor', 'TermP'],
        '+': [EPSILON],
        '-': [EPSILON],
        ')': [EPSILON],
        ';': [EPSILON],
        ',': [EPSILON],
        'then': [EPSILON],
        'do': [EPSILON],
        'end': [EPSILON],
        'else': [EPSILON],
        '<': [EPSILON],
        '>': [EPSILON],
        '<=': [EPSILON],
        '>=': [EPSILON],
        '=': [EPSILON],
        '<>': [EPSILON]
    },
    
    'Factor': {
        '(': ['(', 'Expression', ')'],
        'id': ['id'],
        'num': ['num'],
        '+': ['+', 'Factor'],
        '-': ['-', 'Factor']
    }
}

# ============================================================================
# TOKEN TO TERMINAL MAPPING
# ============================================================================

TOKEN_TO_TERMINAL = {
    TokenType.PROGRAM: 'program',
    TokenType.VAR: 'var',
    TokenType.BEGIN: 'begin',
    TokenType.END: 'end',
    TokenType.INTEGER: 'integer',
    TokenType.REAL: 'real',
    TokenType.BOOLEAN: 'boolean',
    TokenType.IF: 'if',
    TokenType.THEN: 'then',
    TokenType.ELSE: 'else',
    TokenType.WHILE: 'while',
    TokenType.DO: 'do',
    TokenType.READ: 'read',
    TokenType.WRITE: 'write',
    TokenType.DIV: 'div',
    TokenType.MOD: 'mod',
    TokenType.ID: 'id',
    TokenType.NUM: 'num',
    TokenType.PLUS: '+',
    TokenType.MINUS: '-',
    TokenType.MULTIPLY: '*',
    TokenType.DIVIDE: '/',
    TokenType.ASSIGN: ':=',
    TokenType.EQUAL: '=',
    TokenType.NOT_EQUAL: '<>',
    TokenType.LESS: '<',
    TokenType.GREATER: '>',
    TokenType.LESS_EQUAL: '<=',
    TokenType.GREATER_EQUAL: '>=',
    TokenType.LPAREN: '(',
    TokenType.RPAREN: ')',
    TokenType.SEMICOLON: ';',
    TokenType.COLON: ':',
    TokenType.COMMA: ',',
    TokenType.DOT: '.',
    TokenType.EOF: '$'
}


def is_terminal(symbol: str) -> bool:
    """Check if a symbol is a terminal"""
    return symbol in TERMINALS or symbol == EPSILON


def is_nonterminal(symbol: str) -> bool:
    """Check if a symbol is a nonterminal"""
    return symbol in NONTERMINALS


def get_production(nonterminal: str, terminal: str):
    """Get production from parse table, or None if error"""
    if nonterminal in PARSE_TABLE:
        return PARSE_TABLE[nonterminal].get(terminal, None)
    return None


def production_to_string(nonterminal: str, production: list) -> str:
    """Convert production to readable string"""
    rhs = ' '.join(production) if production != [EPSILON] else 'ε'
    return f"{nonterminal} → {rhs}"


if __name__ == "__main__":
    # Print grammar info
    print("=" * 60)
    print("PASCAL LL(1) GRAMMAR")
    print("=" * 60)
    
    print("\nNonterminals:", len(NONTERMINALS))
    print("Terminals:", len(TERMINALS))
    
    print("\n" + "-" * 40)
    print("PRODUCTIONS:")
    print("-" * 40)
    for nt, prods in PRODUCTIONS.items():
        for prod in prods:
            print(f"  {production_to_string(nt, prod)}")
    
    print("\n" + "-" * 40)
    print("FIRST SETS:")
    print("-" * 40)
    for nt in NONTERMINALS:
        print(f"  FIRST({nt}) = {FIRST[nt]}")
    
    print("\n" + "-" * 40)
    print("FOLLOW SETS:")
    print("-" * 40)
    for nt in NONTERMINALS:
        print(f"  FOLLOW({nt}) = {FOLLOW[nt]}")
