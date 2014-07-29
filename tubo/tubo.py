#-*- coding: utf-8 -*-

from collections import deque
from functools import reduce # Py3 compatibility
import itertools

def pipeline(*args):
    """Encloses every argument using the following argument, recursively.
    At the end, if args has N elements, this returns the generator:

    args[N-1](...(args[3](args[2](args[0]))))

    """
    return reduce(lambda x, y: y(x), args)

def consume(iterator):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # feed the entire iterator into a zero-length deque
    deque(iterator, maxlen=0)
