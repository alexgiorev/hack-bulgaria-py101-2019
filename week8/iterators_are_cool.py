import copy
import itertools
from collections import deque


def isiterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True


def iterator_is_empty(iterator):
    try:
        next(iterator)
    except StopIteration:
        return True
    else:
        return False
    
# ================================================================================
# dfs versions

def deep_find_dfs(data, the_key):
    first_dict = next(filter(lambda dct: the_key in dct, dicts_dfs(data)),
                      None)
    
    if first_dict is None:
        raise KeyError
    return first_dict[the_key]


def deep_find_all_dfs(data, the_key):
    return (dct[the_key] for dct in dicts_dfs(data) if the_key in dct)


def dicts_dfs(data):
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
            if type(child) is dict:
                yield child
            stack.append(children(child))
            visited_ids.add(id(child))


# ================================================================================
# bfs versions

def deep_find_bfs(data, the_key):
    first_dict = next(filter(lambda dct: the_key in dct, dicts_bfs(data)),
                      None)
    
    if first_dict is None:
        raise KeyError
    return first_dict[the_key]


def deep_find_all_bfs(data, the_key):    
    return (dct[the_key] for dct in dicts_bfs(data) if the_key in dct)


def dicts_bfs(data):
    queue = deque() # take from the left, add to the right
    queue.append(data)    
    visited_ids = set()
    while queue:
        data = queue.popleft()        
        if id(data) in visited_ids:
            continue
        visited_ids.add(id(data))        
        if type(data) is dict:
            yield data
            for subdata in data.values():
                queue.append(subdata)
        elif isiterable(data):
            queue.extend(data)
            
# for when it doesn't matter which search algorithm is used
            
def deep_find(data, the_key):    
    return deep_find_dfs(data, the_key)


def deep_find_all(data, the_key):
    return deep_find_all_dfs(data, the_key)


def deep_update(data, key, val):
    for adict in filter(lambda d: key in d, dicts_dfs(data)):
        adict[key] = val


def deep_apply(func, data):
    for adict in dicts_dfs(data):
        for key in adict:
            func(key)

            
def deep_compare(obj1, obj2):
    table = set() # used to avoid infinite recursion
    
    def helper(obj1, obj2):
        ids = frozenset({id(obj1), id(obj2)})
        
        if ids in table:
            return True

        table.add(ids)
        
        if type(obj1) is dict:
            if type(obj2) is not dict:
                return False

            if len(obj1) != len(obj2):
                return False

            for key in obj1:
                if key not in obj2 or not helper(obj1[key], obj2[key]):
                    return False

            return True
        elif isiterable(obj1):
            if not isiterable(obj2):
                return False

            iter1, iter2 = iter(obj1), iter(obj2)

            for child1, child2 in zip(iter1, iter2):
                if not helper(child1, child2):
                    return False

            if not (iterator_is_empty(iter1) and iterator_is_empty(iter2)):
                return False

            return True
        else:
            return obj1 == obj2
    
    return helper(obj1, obj2)

def validate_schema(schema, data):
    if len(schema) != len(data):
        return False
    
    for part in schema:
        if type(part) is list:
            key, subschema = part

            if key not in data:
                return False

            if not validate_schema(subschema, data[key]):
                return False
        else:
            if part not in data:
                return False
    return True
    

