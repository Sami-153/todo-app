def tree_ref(tree, indices):
    curr = tree
    for i in indices:
        curr = curr[i]
    return curr

tree = (((1, 2), 3), (4, (5, 6)), 7, (8, 9, 10))
print(tree_ref(tree,(3,1)))
print(tree_ref(tree,(1,1,1)))
print(tree_ref(tree,(1,)))