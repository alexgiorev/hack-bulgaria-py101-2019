import copy
from collections import deque


def isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def deep_find_dfs(data, the_key):
    first_dict = next(dicts_with_the_key_dfs(data, the_key), None)
    if first_dict is None:
        raise KeyError
    return first_dict[the_key]


def deep_find_all_dfs(data, the_key):
    return map(lambda dct: dct[the_key], dicts_with_the_key_dfs(data, the_key))


def deep_find_bfs(data, the_key):
    first_dict = next(dicts_with_the_key_bfs(data, the_key), None)
    if first_dict is None:
        raise KeyError
    return first_dict[the_key]


def deep_find_all_bfs(data, the_key):
    return map(lambda dct: dct[the_key], dicts_with_the_key_bfs(data, the_key))


def dicts_with_the_key_dfs(data, the_key):
    def children(data):
        return (data.values() if type(data) is dict
                else iter(data) if isiterable(data)
                else iter([]))
        
    def first_non_visited(children):
        return next(filter(lambda child: id(child) not in visited_ids, children), None)
    
    visited_ids = set()
    stack = [iter([data])]
    
    while stack:
        current_children = stack[-1]
        child = first_non_visited(current_children)
        if child is None:
            stack.pop()
        else:
            if type(child) is dict and the_key in child:
                yield child
            else:
                stack.append(children(child))
            visited_ids.add(id(child))

            
def dicts_with_the_key_bfs(data, the_key):
    queue = deque() # take from the left, add to the right
    queue.append(data)    
    visited_ids = set()
    while queue:
        data = queue.popleft()        
        if id(data) in visited_ids:
            continue
        visited_ids.add(id(data))        
        if type(data) is dict:
            if the_key in data:
                yield data
            else:
                for subdata in data.values():
                    queue.append(subdata)
        elif isiterable(data):
            queue.extend(data)

            
# for when it doesn't matter which search algorithm is used
            
def deep_find(data, the_key):    
    return deep_find_dfs(data, the_key)


def deep_find_all(data, the_key):
    return deep_find_all_dfs(data, the_key)


def dicts_with_the_key(data, the_key):
    return dicts_with_the_key_dfs(data, the_key)


def deep_update(data, key, val):
    for adict in dicts_with_the_key(data, key):
        adict[key] = val
