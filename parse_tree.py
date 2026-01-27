"""
Parse Tree Implementation for Pascal LL(1) Parser
Builds a parse tree during parsing and provides preorder traversal output
"""

from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class ParseTreeNode:
    """
    A node in the parse tree.
    - symbol: The grammar symbol (terminal or nonterminal)
    - value: The actual token value (for terminals like identifiers or numbers)
    - children: List of child nodes
    """
    symbol: str
    value: str = ""
    children: List['ParseTreeNode'] = field(default_factory=list)
    
    def add_child(self, child: 'ParseTreeNode'):
        """Add a child node"""
        self.children.append(child)
    
    def is_terminal(self) -> bool:
        """Check if this node is a terminal (has no children and not epsilon)"""
        return len(self.children) == 0 and self.symbol != 'ε'
    
    def is_epsilon(self) -> bool:
        """Check if this is an epsilon node"""
        return self.symbol == 'ε'


class ParseTree:
    """
    Parse Tree for storing the syntactic structure of a Pascal program.
    Provides preorder traversal for output.
    """
    
    def __init__(self, root: Optional[ParseTreeNode] = None):
        self.root = root
    
    def preorder_traversal(self, include_epsilon: bool = False) -> List[str]:
        """
        Perform preorder traversal of the parse tree.
        Returns a list of node representations.
        
        Args:
            include_epsilon: Whether to include epsilon nodes in output
        """
        result = []
        self._preorder_helper(self.root, result, 0, include_epsilon)
        return result
    
    def _preorder_helper(self, node: Optional[ParseTreeNode], result: List[str], 
                         depth: int, include_epsilon: bool):
        """Recursive helper for preorder traversal"""
        if node is None:
            return
        
        # Skip epsilon nodes if not including them
        if node.is_epsilon() and not include_epsilon:
            return
        
        # Create indentation for tree structure visualization
        indent = "  " * depth
        
        # Format node output
        if node.value and node.value != node.symbol:
            node_str = f"{indent}{node.symbol} ({node.value})"
        else:
            node_str = f"{indent}{node.symbol}"
        
        result.append(node_str)
        
        # Recursively process children
        for child in node.children:
            self._preorder_helper(child, result, depth + 1, include_epsilon)
    
    def print_tree(self, include_epsilon: bool = False):
        """Print the parse tree in preorder"""
        print("\n" + "=" * 60)
        print("PARSE TREE (Preorder Traversal)")
        print("=" * 60)
        
        traversal = self.preorder_traversal(include_epsilon)
        for line in traversal:
            print(line)
        
        print("=" * 60)
    
    def get_tree_string(self, include_epsilon: bool = False) -> str:
        """Get the parse tree as a string"""
        traversal = self.preorder_traversal(include_epsilon)
        return '\n'.join(traversal)
    
    def print_graphical(self):
        """Print a more graphical representation of the tree"""
        print("\n" + "=" * 60)
        print("PARSE TREE (Graphical)")
        print("=" * 60)
        self._print_graphical_helper(self.root, "", True)
        print("=" * 60)
    
    def _print_graphical_helper(self, node: Optional[ParseTreeNode], 
                                 prefix: str, is_last: bool):
        """Recursive helper for graphical tree printing"""
        if node is None:
            return
        
        # Skip epsilon nodes in graphical output
        if node.is_epsilon():
            return
        
        # Print current node (using ASCII characters for Windows compatibility)
        connector = "+-- " if is_last else "|-- "
        
        # Use ASCII-safe symbol representation
        symbol = node.symbol if node.symbol != 'ε' else "eps"
        
        if node.value and node.value != node.symbol:
            print(f"{prefix}{connector}{symbol} ({node.value})")
        else:
            print(f"{prefix}{connector}{symbol}")
        
        # Prepare prefix for children (ASCII for Windows)
        child_prefix = prefix + ("    " if is_last else "|   ")
        
        # Filter out epsilon children for graphical display
        non_epsilon_children = [c for c in node.children if not c.is_epsilon()]
        
        # Print children
        for i, child in enumerate(non_epsilon_children):
            is_child_last = (i == len(non_epsilon_children) - 1)
            self._print_graphical_helper(child, child_prefix, is_child_last)


def build_sample_tree() -> ParseTree:
    """Build a sample parse tree for testing"""
    # Sample tree for: program test; begin x := 5 end.
    
    root = ParseTreeNode("Program")
    
    # program
    root.add_child(ParseTreeNode("program", "program"))
    
    # id (test)
    root.add_child(ParseTreeNode("id", "test"))
    
    # ;
    root.add_child(ParseTreeNode(";", ";"))
    
    # Block
    block = ParseTreeNode("Block")
    root.add_child(block)
    
    # Declarations (epsilon)
    decl = ParseTreeNode("Declarations")
    decl.add_child(ParseTreeNode("ε"))
    block.add_child(decl)
    
    # begin
    block.add_child(ParseTreeNode("begin", "begin"))
    
    # StmtList
    stmt_list = ParseTreeNode("StmtList")
    block.add_child(stmt_list)
    
    # Statement
    stmt = ParseTreeNode("Statement")
    stmt_list.add_child(stmt)
    
    # Assignment: x := 5
    stmt.add_child(ParseTreeNode("id", "x"))
    stmt.add_child(ParseTreeNode(":=", ":="))
    
    # Expression
    expr = ParseTreeNode("Expression")
    stmt.add_child(expr)
    
    # Term
    term = ParseTreeNode("Term")
    expr.add_child(term)
    
    # Factor
    factor = ParseTreeNode("Factor")
    term.add_child(factor)
    factor.add_child(ParseTreeNode("num", "5"))
    
    # TermP (epsilon)
    termp = ParseTreeNode("TermP")
    termp.add_child(ParseTreeNode("ε"))
    term.add_child(termp)
    
    # ExpressionP (epsilon)
    exprp = ParseTreeNode("ExpressionP")
    exprp.add_child(ParseTreeNode("ε"))
    expr.add_child(exprp)
    
    # StmtListP (epsilon)
    stmtlistp = ParseTreeNode("StmtListP")
    stmtlistp.add_child(ParseTreeNode("ε"))
    stmt_list.add_child(stmtlistp)
    
    # end
    block.add_child(ParseTreeNode("end", "end"))
    
    # .
    root.add_child(ParseTreeNode(".", "."))
    
    return ParseTree(root)


if __name__ == "__main__":
    # Test the parse tree
    tree = build_sample_tree()
    
    print("\n--- Preorder Traversal (without epsilon) ---")
    tree.print_tree(include_epsilon=False)
    
    print("\n--- Preorder Traversal (with epsilon) ---")
    tree.print_tree(include_epsilon=True)
    
    print("\n--- Graphical View ---")
    tree.print_graphical()
