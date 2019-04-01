from fractions import Fraction
import operator
import math

operators = {'+': {'arity': 2, 'exec_proc': operator.add},
             '-': {'arity': 2, 'exec_proc': operator.sub},
             '*': {'arity': 2, 'exec_proc': operator.mul},
             '//': {'arity': 2, 'exec_proc': operator.floordiv},
             '/': {'arity': 2, 'exec_proc': operator.truediv},
             'sqrt': {'arity': 1, 'exec_proc': math.sqrt},
             'min': {'arity': 2, 'exec_proc': min},
             'max': {'arity': 2, 'exec_proc': max},
             'min3': {'arity': 3, 'exec_proc': min},
             'abs': {'arity': 1, 'exec_proc': abs},
             '**': {'arity': 2, 'exec_proc': operator.pow}}

data_types = [int, float, Fraction, complex, str]

def rpn_calc(expr_str):
    try:
        return evaluate_expr(parse(expr_str))
    except ValueError as ve:
        raise ValueError(f'cannot calculate "{expr_str}" in rpn: {ve}')

def iterator_is_empty(iterator):
    # returns True only if iterator is empty (calling next on it would raise StopIteration)
    # if iterator is not empty, it is forwarded by one element
    
    is_empty = False
    try:
        next(iterator)
    except StopIteration:
        is_empty = True
    return is_empty

def evaluate_expr(expr):
    # returns the value of @expr
    # a ValueError is raised if evaluating @expr is not possible
    
    if len(expr) == 1:
        if is_operation(expr[0]):
            raise ValueError('cannot evaluate an expression consisting only of an operation')
        return expr[0]
    if not is_operation(expr[-1]):
        raise ValueError('every expression with more than 1 items must end with an operation')
    
    operations_stack = []
    reversed_expr_iter = reversed(expr)
    for item in reversed_expr_iter:
        if is_operation(item):
            operations_stack.append({'op': item, 'stack': []})
        else:
            current_sub_stack = operations_stack[-1]['stack']
            current_operation = operations_stack[-1]['op']
            
            current_sub_stack.append(item)
            
            # squeeze the operations_stack as much as possible
            while len(current_sub_stack) == current_operation['arity']:
                latest_value = eval_operation(current_operation, reversed(current_sub_stack))
                operations_stack.pop()
                if not operations_stack:
                    break
                current_sub_stack = operations_stack[-1]['stack']
                current_operation = operations_stack[-1]['op']
                current_sub_stack.append(latest_value)
                
            if not operations_stack: # squeezed to the end
                if not iterator_is_empty(reversed_expr_iter):
                    raise ValueError(' too many items.')
                return latest_value
    raise ValueError('not enough items.')
                            
def is_operation(x):
    # x must be either an operation or a number
    # returns True if it is an operation
    return type(x) is dict

def eval_operation(op, args):
    # assumes @op is an operation and @args is an
    # iterable consisting of the arguments of the operation
    return op['exec_proc'](*args)

def parse(expr_str):
    # returns the expression corresponding to @expr_str
    # raise ValueError if parsing @expr_str is not possible
    if not expr_str:
        raise ValueError('cannot parse the empty string to an expression')
    return [parse_token(token) for token in expr_str.split()]

def parse_token(token):
    # if @token is not the name of an operation or
    # if it cannot be converted to a number (according to data_types),
    # a ValueError will be raised
    if token in operators:
        return operators[token]
    for data_type in data_types:
        try:
            return data_type(token)
        except ValueError:
            continue
    raise ValueError(f'"{token}" is not a valid token')

