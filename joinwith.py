from typing import TYPE_CHECKING as _TYPE_CHECKING
if _TYPE_CHECKING:
    from typing import Iterable, Optional as O


def joinwith(__iterable: "Iterable", __separator: str, __lastseparator: str, __before: "O[str]" = None, __after: "O[str]" = None):
    b = __before if __before else ''
    a = __after if __after else ''
    joinlist = list()
    for i in __iterable:
        joinlist.append(f'{b}{i}{a}')
    last = joinlist.pop()
    return f'{__separator.join(joinlist)}{__lastseparator}{last}'
