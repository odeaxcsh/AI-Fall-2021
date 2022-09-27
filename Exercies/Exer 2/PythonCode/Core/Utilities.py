from functools import wraps
from typing import List, Tuple

def renumerate(lst, start = 0):
    return ((len(lst)-1-j, item) for j, item in enumerate(lst, -start))


def toTuple(li: List[List]):
    return tuple(tuple(innerList) for innerList in li)


def toList(tuple: Tuple[Tuple]):
    return [list(innerTuple) for innerTuple in tuple]


# helper functoin to allow lambda argument unpacking in python 3 >= 
def star(f):
    @wraps(f)
    def f_inner(args):
        return f(*args)
    return f_inner