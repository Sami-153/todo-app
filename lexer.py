"""
Pascal Lexer/Scanner for LL(1) Parser
Tokenizes Pascal source code into a stream of tokens
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Keywords
    PROGRAM = auto()
    VAR = auto()
    BEGIN = auto()
    END = auto()
    INTEGER = auto()
    REAL = auto()
    BOOLEAN = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    WHILE = auto()
    DO = auto()
    READ = auto()
    WRITE = auto()
    DIV = auto()
    MOD = auto()
    
    # Identifiers and Literals
    ID = auto()
    NUM = auto()
    
    # Operators
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    ASSIGN = auto()        # :=
    EQUAL = auto()         # =
    NOT_EQUAL = auto()     # <>
    LESS = auto()          # <
    GREATER = auto()       # >
    LESS_EQUAL = auto()    # <=
    GREATER_EQUAL = auto() # >=
    
    # Punctuation
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    SEMICOLON = auto()     # ;
    COLON = auto()         # :
    COMMA = auto()         # ,
    DOT = auto()           # .
    
    # End of input
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', line={self.line}, col={self.column})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")


class Lexer:
    """Pascal Lexer - converts source code to tokens"""
    
    # Reserved words mapping
    KEYWORDS = {
        'program': TokenType.PROGRAM,
        'var': TokenType.VAR,
        'begin': TokenType.BEGIN,
        'end': TokenType.END,
        'integer': TokenType.INTEGER,
        'real': TokenType.REAL,
        'boolean': TokenType.BOOLEAN,
        'if': TokenType.IF,
        'then': TokenType.THEN,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'do': TokenType.DO,
        'read': TokenType.READ,
        'write': TokenType.WRITE,
        'div': TokenType.DIV,
        'mod': TokenType.MOD,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        """Get current character or None if at end"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        """Look ahead at next character"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def advance(self) -> str:
        """Move to next character and return current"""
        char = self.current_char()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def skip_comment(self):
        """Skip Pascal comments: { } or (* *)"""
        if self.current_char() == '{':
            self.advance()  # Skip {
            while self.current_char() and self.current_char() != '}':
                self.advance()
            if self.current_char() == '}':
                self.advance()  # Skip }
        elif self.current_char() == '(' and self.peek() == '*':
            self.advance()  # Skip (
            self.advance()  # Skip *
            while self.current_char():
                if self.current_char() == '*' and self.peek() == ')':
                    self.advance()  # Skip *
                    self.advance()  # Skip )
                    break
                self.advance()
    
    def read_number(self) -> Token:
        """Read a number literal (integer or real)"""
        start_line = self.line
        start_col = self.column
        result = ''
        
        while self.current_char() and self.current_char().isdigit():
            result += self.advance()
        
        # Check for real number
        if self.current_char() == '.' and self.peek() and self.peek().isdigit():
            result += self.advance()  # Add .
            while self.current_char() and self.current_char().isdigit():
                result += self.advance()
        
        return Token(TokenType.NUM, result, start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read an identifier or keyword"""
        start_line = self.line
        start_col = self.column
        result = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            result += self.advance()
        
        # Check if it's a keyword (case insensitive)
        lower_result = result.lower()
        if lower_result in self.KEYWORDS:
            return Token(self.KEYWORDS[lower_result], result, start_line, start_col)
        
        return Token(TokenType.ID, result, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Convert source code to list of tokens"""
        self.tokens = []
        
        while self.current_char():
            # Skip whitespace
            if self.current_char().isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char() == '{' or (self.current_char() == '(' and self.peek() == '*'):
                self.skip_comment()
                continue
            
            start_line = self.line
            start_col = self.column
            
            # Numbers
            if self.current_char().isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Two-character operators
            if self.current_char() == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, ':=', start_line, start_col))
                continue
            
            if self.current_char() == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col))
                continue
            
            if self.current_char() == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col))
                continue
            
            if self.current_char() == '<' and self.peek() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOT_EQUAL, '<>', start_line, start_col))
                continue
            
            # Single-character tokens
            char = self.current_char()
            
            if char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
            elif char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_col))
            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_col))
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_col))
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.EQUAL, '=', start_line, start_col))
            elif char == '<':
                self.advance()
                self.tokens.append(Token(TokenType.LESS, '<', start_line, start_col))
            elif char == '>':
                self.advance()
                self.tokens.append(Token(TokenType.GREATER, '>', start_line, start_col))
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))
            elif char == ';':
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col))
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_col))
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
            elif char == '.':
                self.advance()
                self.tokens.append(Token(TokenType.DOT, '.', start_line, start_col))
            else:
                raise LexerError(f"Unexpected character: '{char}'", start_line, start_col)
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '$', self.line, self.column))
        
        return self.tokens


def tokenize_input(input_string: str) -> List[Token]:
    """Helper function to tokenize input from user"""
    # For simple token input like "id = num + id ;"
    # Parse space-separated tokens
    simple_tokens = {
        'id': TokenType.ID,
        'num': TokenType.NUM,
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '=': TokenType.EQUAL,
        ':=': TokenType.ASSIGN,
        ';': TokenType.SEMICOLON,
        ':': TokenType.COLON,
        ',': TokenType.COMMA,
        '.': TokenType.DOT,
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        '<': TokenType.LESS,
        '>': TokenType.GREATER,
        '<=': TokenType.LESS_EQUAL,
        '>=': TokenType.GREATER_EQUAL,
        '<>': TokenType.NOT_EQUAL,
        'program': TokenType.PROGRAM,
        'var': TokenType.VAR,
        'begin': TokenType.BEGIN,
        'end': TokenType.END,
        'integer': TokenType.INTEGER,
        'real': TokenType.REAL,
        'boolean': TokenType.BOOLEAN,
        'if': TokenType.IF,
        'then': TokenType.THEN,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'do': TokenType.DO,
        'read': TokenType.READ,
        'write': TokenType.WRITE,
        'div': TokenType.DIV,
        'mod': TokenType.MOD,
    }
    
    tokens = []
    parts = input_string.strip().split()
    
    for i, part in enumerate(parts):
        if part.lower() in simple_tokens:
            tokens.append(Token(simple_tokens[part.lower()], part, 1, i+1))
        elif part.isdigit() or (part.replace('.', '').isdigit() and part.count('.') <= 1):
            tokens.append(Token(TokenType.NUM, part, 1, i+1))
        elif part.isidentifier():
            tokens.append(Token(TokenType.ID, part, 1, i+1))
        else:
            raise LexerError(f"Unknown token: {part}", 1, i+1)
    
    tokens.append(Token(TokenType.EOF, '$', 1, len(parts)+1))
    return tokens


if __name__ == "__main__":
    # Test the lexer
    test_code = """
    program test;
    var x, y: integer;
    begin
        x := 5;
        y := x + 10
    end.
    """
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
