from typing import Union as U
import colorsys as clrsys

from .constants import *


class Worker:
    clr: U[str, list[int], tuple[int, int, int]]
    percent: int
    intype: str
    retype: str
    hsv: list[int]

    def __init__(self, c, p, i: str, r: str):
        self.clr = c
        self.percent = p
        self.intype = i.upper()
        self.retype = r.upper()
        self.validate()

    def validate(self) -> None:
        # percent
        if not isinstance(self.percent, (int, float)):
            raise TypeError('<percent> must be a number between 1 and 100')
        elif not (-100 < self.percent < 100):
            raise ValueError('<percent> must be between 1 and 100')
        # retype
        if not isinstance(self.retype, str):
            raise TypeError(f'<returnas> must be a string, one of {FORMATS}')
        elif self.retype not in FORMATS:
            raise ValueError(f'<returnas> must be one of {FORMATS}')
        # intype
        if not self.intype:
            if isinstance(self.clr, str):
                self.intype = HEX
            elif isinstance(self.clr, (list, tuple)):
                self.intype = RGB8
            else:
                raise TypeError(
                    f'<color> must be a string, or a list or tuple of 3 integers')
        if not isinstance(self.intype, str):
            raise TypeError(f'<inputtype> must be one of {FORMATS}')
        elif self.intype not in LST_FRM:
            raise ValueError(f'<inputtype> must be one of {FORMATS}')
        # clr
        if self.intype == HEX:
            if not isinstance(self.clr, str):
                raise TypeError(
                    '<color> must be a string for <inputtype> "HEX"')
            self.clr = self.clr.strip(' #')
            if len(self.clr) != 6:
                raise ValueError('HEX values must be 6 characters long')
        elif not isinstance(self.clr, (list, tuple)):
            raise TypeError(
                f'<color> must be a list or tuple of 3 integers for <inputtype> "{self.intype}"')
        elif len(self.clr) != 3:
            raise ValueError(
                f'<color> must be a list or tuple of 3 integers for <inputtype> "{self.intype}"')

    def adjust(self, v) -> float:
        adj = (v + self.percent / 100)
        return max(min(adj, 1), 0)

    def lightness(self) -> U[str, tuple]:
        self.hsv = getattr(self, self.intype)()
        self.hsv[2] = self.adjust(self.hsv[2])
        return self.output(self.hsv)

    def saturation(self) -> U[str, tuple]:
        self.hsv = getattr(self, self.intype)()
        self.hsv[1] = self.adjust(self.hsv[1])
        return self.output(self.hsv)

    def invert(self) -> U[str, tuple]:
        self.hsv = getattr(self, self.intype)()
        invRgb = [(1 - v) for v in clrsys.hsv_to_rgb(*self.hsv)]
        invHsv = clrsys.rgb_to_hsv(*invRgb)
        return self.output(invHsv)

    def HEX(self) -> list[int]:
        oldClr = self.clr
        self.clr = list()
        for i in range(0, 6, 2):
            clrSlice = oldClr[i: (i + 2)]
            self.clr.append(int(clrSlice, 16))
        return self.RGB(255)

    def RGB8(self): return self.RGB(255)
    def RGB16(self): return self.RGB(65535)

    def RGB(self, div: int) -> list[int]:
        newRgb = tuple((v / div) for v in self.clr)
        return list(clrsys.rgb_to_hsv(*newRgb))

    def HSV(self) -> list[int]:
        h, s, v = self.clr
        return [(h / 360), (s / 100), (v / 100)]

    def HLS(self) -> list[int]:
        h, l, s = self.clr
        hls = tuple((h / 360), (l / 100), (s / 100))
        newRgb = clrsys.hls_to_rgb(*hls)
        return list(clrsys.rgb_to_hsv(*newRgb))

    def output(self, newHsv: list[int]) -> U[str, tuple]:
        R = round
        if self.retype == HEX:
            newRgb = clrsys.hsv_to_rgb(*newHsv)
            newHex = (f'{R(255 * v):02x}' for v in newRgb)
            out = f"#{''.join(newHex)}"
        elif self.retype in (RGB8, RGB16):
            newRgb = clrsys.hsv_to_rgb(*newHsv)
            n = 255 if self.retype == RGB8 else 65535
            out = tuple(R(n * v) for v in newRgb)
        else:
            if self.retype == HLS:
                newRgb = clrsys.hsv_to_rgb(*newHsv)
                a, b, c = clrsys.rgb_to_hls(*newRgb)
            else:
                a, b, c = newHsv
            out = tuple(R(360 * a), R(100 * b), R(100 * c))
        return out


def lighten(color: U[str, list[int], tuple[int]], percent: int = 25, inputtype: str = "", returnas: str = HEX) -> U[str, tuple[int, int, int]]:
    """\
    Parameters
    ----------
    color : str | sequence[int, int, int]
        The initial color
    percent : int, optional (default is 25)
        Percent by which to change the color. Must be an integer between 1 and 100
    inputtype : str, optional (default is "HEX" or "RGB8")
        The data type of the input. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    returnas : str, optional (default is "HEX")
        The data type to return. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    """
    work = Worker(color, percent, inputtype, returnas)
    return work.lightness()


def darken(color: U[str, list[int], tuple[int]], percent: int = 25, inputtype: str = "", returnas: str = HEX) -> U[str, tuple[int, int, int]]:
    """\
    Parameters
    ----------
    color : str | sequence[int, int, int]
        The initial color
    percent : int, optional (default is 25)
        Percent by which to change the color. Must be an integer between 1 and 100
    inputtype : str, optional (default is "HEX" or "RGB8")
        The data type of the input. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    returnas : str, optional (default is "HEX")
        The data type to return. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    """
    work = Worker(color, -percent, inputtype, returnas)
    return work.lightness()


def saturate(color: U[str, list[int], tuple[int]], percent: int = 25, inputtype: str = "", returnas: str = HEX) -> U[str, tuple[int, int, int]]:
    """\
    Parameters
    ----------
    color : str | sequence[int, int, int]
        The initial color
    percent : int, optional (default is 25)
        Percent by which to change the color. Must be an integer between 1 and 100
    inputtype : str, optional (default is "HEX" or "RGB8")
        The data type of the input. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    returnas : str, optional (default is "HEX")
        The data type to return. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    """
    work = Worker(color, percent, inputtype, returnas)
    return work.saturation()


def desaturate(color: U[str, list[int], tuple[int]], percent: int = 25, inputtype: str = "", returnas: str = HEX) -> U[str, tuple[int, int, int]]:
    """\
    Parameters
    ----------
    color : str | sequence[int, int, int]
        The initial color
    percent : int, optional (default is 25)
        Percent by which to change the color. Must be an integer between 1 and 100
    inputtype : str, optional (default is "HEX" or "RGB8")
        The data type of the input. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    returnas : str, optional (default is "HEX")
        The data type to return. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    """
    work = Worker(color, -percent, inputtype, returnas)
    return work.saturation()


def invert(color: U[str, list[int], tuple[int]], inputtype: str = "", returnas: str = HEX) -> U[str, tuple[int, int, int]]:
    """\
    Parameters
    ----------
    color : str | sequence[int, int, int]
        The initial color
    inputtype : str, optional (default is "HEX" or "RGB8")
        The data type of the input. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    returnas : str, optional (default is "HEX")
        The data type to return. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"
    """
    work = Worker(color, 0, inputtype, returnas)
    return work.invert()
