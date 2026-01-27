"""
Symbol Table Manager for Pascal LL(1) Parser
Manages identifiers, their types, and scopes
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum, auto


class SymbolType(Enum):
    INTEGER = auto()
    REAL = auto()
    BOOLEAN = auto()
    PROGRAM = auto()
    UNKNOWN = auto()


@dataclass
class Symbol:
    name: str
    symbol_type: SymbolType
    scope_level: int
    line_declared: int = 0
    
    def __repr__(self):
        return f"Symbol({self.name}, {self.symbol_type.name}, scope={self.scope_level})"


class SymbolTable:
    """
    Symbol Table for managing identifiers in Pascal programs.
    Supports nested scopes for block structures.
    """
    
    def __init__(self):
        self.scopes: List[Dict[str, Symbol]] = [{}]  # Stack of scope dictionaries
        self.current_scope_level = 0
    
    def enter_scope(self):
        """Enter a new scope (e.g., entering a block)"""
        self.current_scope_level += 1
        self.scopes.append({})
    
    def exit_scope(self):
        """Exit current scope (e.g., leaving a block)"""
        if self.current_scope_level > 0:
            self.scopes.pop()
            self.current_scope_level -= 1
    
    def insert(self, name: str, symbol_type: SymbolType, line: int = 0) -> bool:
        """
        Insert a symbol into the current scope.
        Returns True if successful, False if symbol already exists in current scope.
        """
        name_lower = name.lower()  # Pascal is case-insensitive
        
        if name_lower in self.scopes[-1]:
            return False  # Symbol already declared in current scope
        
        symbol = Symbol(
            name=name,
            symbol_type=symbol_type,
            scope_level=self.current_scope_level,
            line_declared=line
        )
        self.scopes[-1][name_lower] = symbol
        return True
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol in all scopes (from innermost to outermost).
        Returns the Symbol if found, None otherwise.
        """
        name_lower = name.lower()
        
        # Search from innermost scope outward
        for scope in reversed(self.scopes):
            if name_lower in scope:
                return scope[name_lower]
        
        return None
    
    def lookup_current_scope(self, name: str) -> Optional[Symbol]:
        """Look up a symbol only in the current scope"""
        name_lower = name.lower()
        return self.scopes[-1].get(name_lower)
    
    def get_all_symbols(self) -> List[Symbol]:
        """Get all symbols from all scopes"""
        all_symbols = []
        for scope in self.scopes:
            all_symbols.extend(scope.values())
        return all_symbols
    
    def print_table(self):
        """Print the symbol table for debugging"""
        print("\n" + "=" * 60)
        print("SYMBOL TABLE")
        print("=" * 60)
        print(f"{'Name':<15} {'Type':<12} {'Scope Level':<12} {'Line':<8}")
        print("-" * 60)
        
        for level, scope in enumerate(self.scopes):
            for name, symbol in scope.items():
                print(f"{symbol.name:<15} {symbol.symbol_type.name:<12} {symbol.scope_level:<12} {symbol.line_declared:<8}")
        
        print("=" * 60 + "\n")


# Type conversion helper
def token_type_to_symbol_type(type_name: str) -> SymbolType:
    """Convert Pascal type name to SymbolType"""
    type_map = {
        'integer': SymbolType.INTEGER,
        'real': SymbolType.REAL,
        'boolean': SymbolType.BOOLEAN,
    }
    return type_map.get(type_name.lower(), SymbolType.UNKNOWN)


if __name__ == "__main__":
    # Test the symbol table
    st = SymbolTable()
    
    # Insert program name
    st.insert("TestProgram", SymbolType.PROGRAM, 1)
    
    # Insert variables
    st.insert("x", SymbolType.INTEGER, 3)
    st.insert("y", SymbolType.INTEGER, 3)
    
    # Enter a new scope (begin block)
    st.enter_scope()
    st.insert("temp", SymbolType.REAL, 5)
    
    # Lookup tests
    print("Lookup 'x':", st.lookup("x"))
    print("Lookup 'temp':", st.lookup("temp"))
    print("Lookup 'unknown':", st.lookup("unknown"))
    
    st.print_table()
    
    # Exit scope
    st.exit_scope()
    print("\nAfter exiting scope:")
    print("Lookup 'temp':", st.lookup("temp"))  # Should be None
    
    st.print_table()
