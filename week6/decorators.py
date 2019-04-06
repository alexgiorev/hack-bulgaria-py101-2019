import datetime
import string
from timeit import default_timer as timer

def accepts(*types):
    def decorator(func):
        def check_types(args):
            for i, (_type, arg) in enumerate(zip(types, args), start=1):
                if type(arg) is not _type:
                    raise TypeError(f'Argument {i} of {func.__name__} is not {_type}')
            
        def result(*args):
            check_types(args)
            return func(*args)

        result.__name__ = func.__name__
        return result
    return decorator

def ccypher(astr, shift):
    # returns the ceaser cypher of @astr with a shift of @shift
    def encrypt_char(c):
        if c.isalpha():
            was_lower = c.islower()
            c = c.lower()
            ci = string.ascii_lowercase.index(c)
            newc = string.ascii_lowercase[(ci + shift) % len(string.ascii_lowercase)]
            return newc if was_lower else newc.upper() 
        else:
            return c
    return ''.join(map(encrypt_char, astr))

def encrypt(shift):
    def decorator(func):
        def result(*args, **kwargs):
            return_str = func(*args, **kwargs)
            return ccypher(return_str, shift)
        result.__name__ = func.__name__
        return result
    return decorator

def log(filename):
    def decorator(func):
        def result(*args, **kwargs):
            with open(filename, 'a') as f:
                f.write(f'{func.__name__} was called at {datetime.datetime.now()}\n')
            return func(*args, **kwargs)
        result.__name__ = func.__name__
        return result
    return decorator

def performance(filename):
    def decorator(func):
        def result(*args, **kwargs):
            start = timer()
            return_value = func(*args, **kwargs)
            end = timer()
            time_taken = end - start
            with open(filename, 'a') as f:
                f.write(f'{func.__name__} was called and took {time_taken} seconds to complete\n')
            return return_value
        result.__name__ = func.__name__
        return result
    return decorator
