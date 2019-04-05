import itertools
import sys

def chain(iter1, iter2):
    for x in iter1:
        yield x
    for x in iter2:
        yield x

def compress(iterable, mask):
    return (x for x, boolean in zip(iterable, mask) if boolean)    
            
def cycle(iterable):
    while True:
        for x in iterable:
            yield x
