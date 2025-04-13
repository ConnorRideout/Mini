from typing import Iterable as __Iter


def joinwith(iterable: __Iter, separator: str, lastseparator: str, formatstr: str = None) -> str:
    """-----
    Join the elements of an iterable into a string, with formatting and a special last separator.

    Parameters
    ----------
    iterable (Iterable): The iterable to join

    separator (str): The string to put between all but the last two iterable elements

    lastseparator (str): The string to put between the last two iterable elements

    formatstr (str, optional): [default=None] A format string to apply to all elements before joining


    Returns:
    --------
    str : The joined, formatted string
    """

    joinlist = list()
    for i in iterable:
        if set('{}') <= set(str(formatstr)):
            i = formatstr.format(i)
        joinlist.append(str(i))
    if len(joinlist) > 1:
        last = joinlist.pop()
        return f'{separator.join(joinlist)}{lastseparator}{last}'
    else:
        return joinlist[0]
