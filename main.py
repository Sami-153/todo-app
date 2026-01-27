"""
Pascal LL(1) Parser - Main Entry Point
Run this to parse Pascal programs and see preorder traversal output
"""

import sys
import os
from parser import parse_string, parse_file
from lexer import Lexer


def print_banner():
    print("=" * 60)
    print("        PASCAL LL(1) PARSER")
    print("        Compiler Construction Lab 8")
    print("=" * 60)


def main():
    print_banner()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        debug = "--debug" in sys.argv or "-d" in sys.argv
        
        print(f"\nParsing file: {filename}")
        print("-" * 40)
        
        # Read and display source
        try:
            with open(filename, 'r') as f:
                source = f.read()
            print("Source Code:")
            print(source)
            print("-" * 40)
        except IOError as e:
            print(f"Error: {e}")
            return 1
        
        # Parse
        success, tree = parse_file(filename, debug=debug)
        
        if success and tree:
            tree.print_tree(include_epsilon=False)
            print("\nGraphical Parse Tree:")
            tree.print_graphical()
        
        return 0 if success else 1
    
    # Interactive mode
    print("\nNo file specified. Running in interactive mode.")
    print("Enter Pascal code (end with empty line):\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    
    source = "\n".join(lines)
    
    if source.strip():
        print("\n" + "-" * 40)
        success, tree = parse_string(source, debug=True)
        
        if success and tree:
            tree.print_tree(include_epsilon=False)
    else:
        print("No input provided.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
