from typing import Iterable, Optional


def joinwith(__iterable: Iterable, __separator: str, __lastseparator: str, __formatstr: str = None) -> str:
    """-----
    Join the elements of an iterable into a string, with formatting and a special last separator.

    Parameters
    ----------
    __iterable (Iterable): The iterable to join

    __separator (str): The string to put between all but the last two iterable elements

    __lastseparator (str): The string to put between the last two iterable elements

    __formatstr (str, optional): [default=None] A format string to apply to all elements before joining


    Returns:
    --------
    str : The joined, formatted string
    """

    joinlist = list()
    doformat = True if set('{}') <= set(str(__formatstr)) else False
    for i in __iterable:
        if doformat:
            i = __formatstr.format(i)
        joinlist.append(str(i))
    if len(joinlist) > 1:
        last = joinlist.pop()
        return f'{__separator.join(joinlist)}{__lastseparator}{last}'
    else:
        return joinlist[0]
