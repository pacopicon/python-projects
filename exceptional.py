import sys
from math import log

def convert(s):
    '''Convert to an integer.'''
    try:
        return int(s)
    except (ValueError, TypeError) as err:
        print(f'Did not convert: {str(err)}', file=sys.stderr)
        raise

def string_log(s):
    v = convert(s)
    return log(v)

    #  from exceptional import convert