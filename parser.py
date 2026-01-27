"""
Table-Driven LL(1) Parser for Pascal
"""

from typing import List, Optional, Tuple
from lexer import Token, TokenType, Lexer
from grammar import (PARSE_TABLE, TOKEN_TO_TERMINAL, EPSILON, 
                     is_terminal, is_nonterminal, get_production, production_to_string)
from parse_tree import ParseTreeNode, ParseTree


class ParserError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        if token:
            super().__init__(f"Syntax Error at line {token.line}, col {token.column}: {message}")
        else:
            super().__init__(f"Syntax Error: {message}")


class LL1Parser:
    def __init__(self, tokens: List[Token], debug: bool = False):
        self.tokens = tokens
        self.pos = 0
        self.debug = debug
        self.stack: List[Tuple[str, Optional[ParseTreeNode]]] = []
    
    def current_token(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]
    
    def get_terminal(self, token: Token) -> str:
        return TOKEN_TO_TERMINAL.get(token.type, token.value)
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
    
    def parse(self) -> Tuple[bool, Optional[ParseTree]]:
        root = ParseTreeNode("Program")
        tree = ParseTree(root)
        self.stack = [('$', None), ('Program', root)]
        
        if self.debug:
            print("\n" + "=" * 60)
            print("LL(1) PARSING TRACE")
            print("=" * 60)
        
        step = 0
        while len(self.stack) > 0:
            step += 1
            top_symbol, top_node = self.stack.pop()
            current = self.current_token()
            current_terminal = self.get_terminal(current)
            
            if self.debug:
                stack_syms = [s[0] for s in self.stack] + [top_symbol]
                remaining = [self.get_terminal(t) for t in self.tokens[self.pos:]]
                print(f"Step {step}: Stack={stack_syms}, Input={remaining}")
            
            if top_symbol == '$' and current_terminal == '$':
                print("\n*** ACCEPTED ***")
                return True, tree
            
            if is_terminal(top_symbol) and top_symbol != EPSILON:
                if top_symbol == current_terminal:
                    if self.debug:
                        print(f"  MATCH '{top_symbol}'")
                    if top_node:
                        top_node.value = current.value
                    self.advance()
                else:
                    raise ParserError(f"Expected '{top_symbol}' but found '{current.value}'", current)
            
            elif top_symbol == EPSILON:
                if top_node:
                    top_node.add_child(ParseTreeNode(EPSILON))
            
            elif is_nonterminal(top_symbol):
                production = get_production(top_symbol, current_terminal)
                if production is None:
                    raise ParserError(f"No production for [{top_symbol}, {current_terminal}]", current)
                
                if self.debug:
                    print(f"  APPLY: {production_to_string(top_symbol, production)}")
                
                if production == [EPSILON]:
                    if top_node:
                        top_node.add_child(ParseTreeNode(EPSILON))
                else:
                    child_nodes = []
                    for symbol in production:
                        child = ParseTreeNode(symbol)
                        child_nodes.append(child)
                        if top_node:
                            top_node.add_child(child)
                    for i in range(len(production) - 1, -1, -1):
                        self.stack.append((production[i], child_nodes[i]))
        
        raise ParserError("Unexpected end of parsing")


def parse_string(source: str, debug: bool = False) -> Tuple[bool, Optional[ParseTree]]:
    lexer = Lexer(source)
    try:
        tokens = lexer.tokenize()
    except Exception as e:
        print(f"Lexer Error: {e}")
        return False, None
    
    parser = LL1Parser(tokens, debug=debug)
    try:
        return parser.parse()
    except ParserError as e:
        print(f"\n{e}")
        return False, None


def parse_file(filename: str, debug: bool = False) -> Tuple[bool, Optional[ParseTree]]:
    try:
        with open(filename, 'r') as f:
            source = f.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        return False, None
    return parse_string(source, debug)
