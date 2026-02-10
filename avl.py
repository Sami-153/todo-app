class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        if not node:
            return
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        self.update_height(z)
        self.update_height(y)

        return y

    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        self.update_height(z)
        self.update_height(y)

        return y

    def insert(self, node, key):
        # Standard BST insertion
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        else:
            # Duplicate keys not allowed
            return node

        # Update height
        self.update_height(node)

        # Get balance factor
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    def get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, node, key):
        # Standard BST deletion
        if not node:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children
            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        if not node:
            return node

        # Update height
        self.update_height(node)

        # Get balance factor
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)

        # Left Right Case
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Right Right Case
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)

        # Right Left Case
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def delete_key(self, key):
        self.root = self.delete(self.root, key)

    def search(self, node, key):
        if not node or node.key == key:
            return node

        if key < node.key:
            return self.search(node.left, key)
        return self.search(node.right, key)

    def search_key(self, key):
        return self.search(self.root, key)

    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.key)
            self.inorder_traversal(node.right, result)

    def inorder(self):
        result = []
        self.inorder_traversal(self.root, result)
        return result

    def preorder_traversal(self, node, result):
        if node:
            result.append(node.key)
            self.preorder_traversal(node.left, result)
            self.preorder_traversal(node.right, result)

    def preorder(self):
        result = []
        self.preorder_traversal(self.root, result)
        return result


# Example usage
if __name__ == "__main__":
    avl = AVLTree()
    
    # Insert nodes
    keys = [10, 20, 30, 40, 50, 25]
    print("Inserting keys:", keys)
    for key in keys:
        avl.insert_key(key)
    
    print("Inorder traversal:", avl.inorder())
    print("Preorder traversal:", avl.preorder())
    
    # Search for a key
    search_key = 25
    result = avl.search_key(search_key)
    print(f"\nSearching for {search_key}: {'Found' if result else 'Not found'}")
    
    # Delete a key
    delete_key = 40
    print(f"\nDeleting key {delete_key}")
    avl.delete_key(delete_key)
    print("Inorder traversal after deletion:", avl.inorder())