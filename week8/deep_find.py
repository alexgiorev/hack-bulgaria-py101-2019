import copy
import time
from collections import deque

def deep_find_dfs(data, the_key):
    visited_ids = set()
    
    def visit(data):
        # if @data has the key, returns it
        # otherwise, raises KeyError

        if id(data) in visited_ids:
            raise KeyError
        
        visited_ids.add(id(data)) # TODO: is this line buggy?
        
        if type(data) is dict:            
            if the_key in data:
                return data[the_key]
            
            for key, node in data.items():
                try:
                    return visit(node)
                except KeyError:
                    # node is searched and it does not have the_key
                    continue
            # at this point, none of @data's children have the_key 
            raise KeyError
        else:
            # try to see if it is an iterable
            try:
                iterator = iter(data)
            except TypeError:
                # not an iterator nor a dict, so fail
                raise KeyError

            # at this point, iterator is bound to an iterator, so traverse it
            for data in iterator:
                try:
                    return visit(data)
                except KeyError:
                    continue

            # at this point, none of the entries in iterator have the_key
            raise KeyError
        
    return visit(data)

def deep_find_bfs(data, the_key):
    queue = deque() # read from the left, pop to the right
    queue.append(data)
    
    visited_ids = set()
    
    while queue:
        data = queue.popleft()
        
        if id(data) in visited_ids:
            continue

        visited_ids.add(id(data))
        
        if type(data) is dict:
            if the_key in data:
                return data[the_key]

            for subdata in data.values():
                queue.append(subdata)
        else:
            # try with an iterable
            try:
                iterator = iter(data)
            except TypeError:
                # data is not an iterator
                continue
            else:
                # data is an iterator
                queue.extend(iterator)
    raise KeyError
    

def deep_find_all(data, the_key):
    visited_ids = set()
    
    def visit(data):
        # returns an iterator

        if id(data) in visited_ids:
            return iter([])
        
        visited_ids.add(id(data)) # TODO: is this line buggy?
        
        if type(data) is dict:
            if the_key in data:
                iter1 = iter([data[the_key]])
            else:
                iter1 = iter([])

            iter2 = map(visit, data.values())
            
            return itertools.chain(iter1, iter2)
        else:
            # try to see if it is an iterable
            try:
                iterator = iter(data)
            except TypeError:
                # not an iterator nor a dict, so fail
                raise KeyError

            # at this point, iterator is bound to an iterator, so traverse it
            for data in iterator:
                try:
                    return visit(data)
                except KeyError:
                    continue

            # at this point, none of the entries in iterator have the_key
            raise KeyError
        
    return visit(data)


test_data1 = {'a': 1, 'b': 2, 'c': 3}

test_data2 = {'d1': {'a': 10, 'b': 20},
              'd2': {'a': 10, 'c': 200}}

test_data3 = {'l1': [{'a': 10, 'b': 20}, {'c': 30, 'd': 40}],
              'd1': {'d11': {'x': 50}, 'd12': {'y': 60}, 'd13': {'a': -10, 'b': -20, 'c': -30, 'd': -40}},
              't1': ({'A': 100, 'B': 200}, {'C': 300, 'D': 400})}

test_data4 = copy.deepcopy(test_data3)

test_data4['d2'] = test_data4 # add cycle
