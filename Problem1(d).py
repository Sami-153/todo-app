def count_pattern(pattern, lst):
    lst_length = len(lst)
    pattern_length = len(pattern)
    if lst_length < pattern_length:
        return 0
    i= 0
    count= 0
    while i <= lst_length - pattern_length:
        start = i
        end = i + pattern_length
        current_window = lst[start:end]
        if current_window == pattern:
            count+=1 
        i+=1
    return count

print(count_pattern(('a', 'b'), ('a', 'b', 'c', 'e', 'b', 'a', 'b', 'f')))  # Output: 2
print(count_pattern(('a', 'b', 'a'), ('g', 'a', 'b', 'a', 'b', 'a', 'b', 'a')))  # Output: 3
