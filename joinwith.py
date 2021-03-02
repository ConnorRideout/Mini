from typing import TYPE_CHECKING as _TYPE_CHECKING
if _TYPE_CHECKING:
    from typing import Iterable, Optional as O


def joinwith(__iterable: "Iterable", __separator: str, __lastseparator: str, __formatstr: "O[str]" = None):
    joinlist = list()
    doformat = True if set('{}') <= set(str(__formatstr)) else False
    for i in __iterable:
        if doformat:
            i = __formatstr.format(i)
        joinlist.append(str(i))
    last = joinlist.pop()
    return f'{__separator.join(joinlist)}{__lastseparator}{last}'
