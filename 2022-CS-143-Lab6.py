RED = "RED"
BLACK = "BLACK"


class Symbol:
    def __init__(self, name, data_type, scope, line_no):
        self.name = name
        self.data_type = data_type
        self.scope = scope
        self.line_no = line_no
        self.attributes = {}


class RBNode:
    def __init__(self, key, symbol):
        self.key = key
        self.symbol = symbol
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None


class SymbolTableRBT:
    def __init__(self):
        self.NIL = RBNode(None, None)
        self.NIL.color = BLACK
        self.root = self.NIL

    # ---------------- ROTATIONS ----------------
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    # ---------------- INSERT ----------------
    def insert(self, name, data_type, scope, line_no):
        symbol = Symbol(name, data_type, scope, line_no)
        node = RBNode(name, symbol)
        node.left = self.NIL
        node.right = self.NIL

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if node.key < current.key:
                current = current.left
            elif node.key > current.key:
                current = current.right
            else:
                print("\nIdentifier already exists.")
                return

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self.fix_insert(node)
        print("\nIdentifier inserted successfully.")

    def fix_insert(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
        self.root.color = BLACK

    # ---------------- SEARCH ----------------
    def lookup(self, name):
        current = self.root
        while current != self.NIL:
            if name == current.key:
                return current.symbol
            elif name < current.key:
                current = current.left
            else:
                current = current.right
        return None

    # ---------------- ATTRIBUTES ----------------
    def set_attribute(self, name, key, value):
        sym = self.lookup(name)
        if sym:
            sym.attributes[key] = value
            print("\nAttribute added successfully.")
        else:
            print("\nIdentifier not found.")

    def get_attribute(self, name, key):
        sym = self.lookup(name)
        if sym:
            return sym.attributes.get(key, None)
        return None

    # ---------------- DISPLAY ----------------
    def inorder(self, node, rows):
        if node != self.NIL:
            self.inorder(node.left, rows)
            rows.append(node.symbol)
            self.inorder(node.right, rows)

    def display(self):
        rows = []
        self.inorder(self.root, rows)

        if not rows:
            print("\nSymbol Table is empty.")
            return

        print("\n" + "-" * 90)
        print(f"{'Identifier':<15}{'Type':<15}{'Scope':<15}{'Line No':<10}{'Attributes'}")
        print("-" * 90)

        for s in rows:
            attrs = ", ".join(f"{k}:{v}" for k, v in s.attributes.items())
            print(f"{s.name:<15}{s.data_type:<15}{s.scope:<15}{s.line_no:<10}{attrs}")

        print("-" * 90)

    # ---------------- FREE ----------------
    def free(self):
        self.root = self.NIL
        print("\nSymbol Table cleared.")


# ---------------- MENU ----------------
def menu():
    print("""
1. Insert Identifier
2. Lookup Identifier
3. Set Attribute
4. Get Attribute
5. Display Symbol Table
6. Free Symbol Table
7. Exit
""")


# ---------------- DRIVER ----------------
if __name__ == "__main__":
    st = SymbolTableRBT()

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Identifier Name: ")
            dtype = input("Data Type: ")
            scope = input("Scope: ")
            line = int(input("Line Number: "))
            st.insert(name, dtype, scope, line)

        elif choice == "2":
            name = input("Enter Identifier Name: ")
            sym = st.lookup(name)
            if sym:
                print("\nIdentifier Found")
                print(f"Name: {sym.name}")
                print(f"Type: {sym.data_type}")
                print(f"Scope: {sym.scope}")
                print(f"Line No: {sym.line_no}")
                print(f"Attributes: {sym.attributes}")
            else:
                print("\nIdentifier not found.")

        elif choice == "3":
            name = input("Identifier Name: ")
            key = input("Attribute Name: ")
            value = input("Attribute Value: ")
            st.set_attribute(name, key, value)

        elif choice == "4":
            name = input("Identifier Name: ")
            key = input("Attribute Name: ")
            value = st.get_attribute(name, key)
            if value is not None:
                print(f"\nAttribute Value: {value}")
            else:
                print("\nAttribute not found.")

        elif choice == "5":
            st.display()

        elif choice == "6":
            st.free()

        elif choice == "7":
            print("\nExiting Symbol Table.")
            break

        else:
            print("\nInvalid choice. Try again.")
