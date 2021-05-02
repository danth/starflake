import itertools


def group_by(iterable, key):
    """
    Group the iterable using the given key function.

    This is equivalent to itertools.groupby, but the iterable is sorted first.
    """

    sorted_iterable = sorted(iterable, key=key)
    return itertools.groupby(sorted_iterable, key)
