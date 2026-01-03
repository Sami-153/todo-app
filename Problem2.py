def depth(x):
    if not isinstance(x,(list,tuple)):
        return 0
    

    max_depth = 0
    for i in x:
        item_depth = depth(i)
        if item_depth > max_depth:
            max_depth = item_depth   

    return 1 + max_depth

print(depth('x'))
print(depth(('expt', 'x', 2)))
print(depth(('+', ('expt', 'x', 2), ('expt', 'y', 2))))
print(depth(('/', ('expt', 'x', 5), ('expt', ('-', ('expt', 'x', 2), 1), ('/', 5, 2)))))
