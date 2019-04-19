import copy
import time
import itertools
from collections import deque

def deep_find_dfs(data, the_key):
    try:
        return next(deep_find_all_dfs(data, the_key))
    except StopIteration:
        raise KeyError

def deep_find_bfs(data, the_key):    
    try:
        return next(deep_find_all_dfs(data, the_key))
    except StopIteration:
        raise KeyError

def deep_find_all_dfs(data, the_key):
    # returns an iterator yielding the values
    # corresponding to the_key in dfs order

    visited_ids = set()
    
    def visit(data):
        if id(data) in visited_ids:
            return iter([])
        
        visited_ids.add(id(data))
        
        if type(data) is dict:
            iter1 = iter([data[the_key]] if the_key in data else [])
            iter2 = map(visit, data.values())
            return itertools.chain(iter1, *iter2)
        else:
            # try to see if it is an iterable
            try:
                data_iter = iter(data)
            except TypeError:
                # data is not an iterator nor a dict
                return iter([])
            else:
                # data is an iterable
                return itertools.chain.from_iterable(map(visit, data_iter))
            
    return visit(data)

def deep_find_all_bfs(data, the_key):
    # returns an iterator yielding the values
    # corresponding to the_key in bfs order
    
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
                yield data[the_key]
            else:
                for subdata in data.values():
                    queue.append(subdata)
        else:
            try:
                data_iter = iter(data)
            except TypeError:
                # data is not an iterator, so skip it
                continue
            else:
                # data is an iterator
                queue.extend(data_iter)
