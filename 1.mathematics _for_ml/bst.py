class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    # Insert
    def insert(self, root, key):
        if root is None:
            return Node(key)

        if key < root.data:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        return root

    # Search
    def search(self, root, key):
        if root is None or root.data == key:
            return root

        if key < root.data:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    # Inorder Traversal (sorted output)
    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.data, end=" ")
            self.inorder(root.right)


bst = BST()

# Insert elements
values = [50, 30, 70, 20, 40, 60, 80]
for v in values:
    bst.root = bst.insert(bst.root, v)

# Traversal
print("Inorder Traversal:")
bst.inorder(bst.root)   # 20 30 40 50 60 70 80

# Search
key = 40
result = bst.search(bst.root, key)

if result:
    print("\nFound:", key)
else:
    print("\nNot Found")