from .constants import *
import colorsys as _clrsys

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Iterable, Union as U, Optional as O


class Worker:
    initConv: tuple[float, float, float]
    col: "U[str, list[int], tuple[int]]"
    percent: int
    intype: str
    retype: str
    bit: int

    def __init__(self, c: "U[str, Iterable]", p: int, i: str, r: str, b: int):
        self.clr = c
        self.percent = p
        self.intype = i.upper()
        self.retype = r.upper()
        self.bit = b
        self.validate()

    def validate(self) -> None:
        # percent
        if not isinstance(self.percent, int):
            raise TypeError('<percent> must be an integer between 1 and 100')
        elif not (-100 < self.percent < 100):
            raise ValueError('<percent> must be between 1 and 100')
        # bit
        if not isinstance(self.bit, int):
            raise TypeError('<bitdepth> must be 8 or 16')
        elif self.bit not in [8, 16]:
            raise ValueError('<bitdepth> must be 8 or 16')
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
                self.intype = RGB
            else:
                raise TypeError(f'<inputtype> must be one of {FORMATS}')
        if not isinstance(self.intype, str):
            raise TypeError(f'<inputtype> must be one of {FORMATS}')
        elif self.intype not in LST_FRM:
            raise ValueError(f'<inputtype> must be one of {FORMATS}')
        # col
        if self.intype == HEX:
            self.clr = self.clr.strip(' #')
            if len(self.clr) not in [6, 12]:
                raise ValueError(
                    "HEX values must have a length of 6 (8-bit) or 12 (16-bit)")
        elif not isinstance(self.clr, (list, tuple)):
            raise TypeError(
                f'<color> must be a list or tuple of 3 integers if <inputtype> is "{self.intype}"')
        elif len(self.clr) != 3:
            raise ValueError(
                f'<color> must be a list or tuple of 3 integers if <inputtype> is "{self.intype}"')

    def lightness(self) -> "U[str, list]":
        self.initConv = getattr(self, self.intype)()
        hue, sat, val = self.initConv
        val_adj = (val + self.percent / 100)
        val_new = max(min(val_adj, 1), 0)
        return self.output(hue, sat, val_new)

    def saturation(self) -> "U[str, list]":
        self.initConv = getattr(self, self.intype)()
        hue, sat, val = self.initConv
        sat_adj = (sat + self.percent / 100)
        sat_new = max(min(sat_adj, 1), 0)
        return self.output(hue, sat_new, val)

    def invert(self) -> "U[str, list]":
        self.initConv = getattr(self, self.intype)(True)
        invRgb = [(1 - n) for n in self.initConv]
        invHsv = _clrsys.rgb_to_hsv(*invRgb)
        return self.output(*invHsv)

    def HEX(self, retRgb: bool = False) -> tuple[int, int, int]:
        newCol = list()
        cLen = len(self.clr)
        for i in range(0, cLen, (cLen // 3)):
            colSlice = self.clr[i: (i + cLen // 3)]
            newCol.append(int(colSlice, 16))
        self.clr = newCol.copy()
        newRgb = self.RGB(True)
        return newRgb if retRgb else _clrsys.rgb_to_hsv(*newRgb)

    def RGB(self, retRgb: bool = False) -> tuple[int, int, int]:
        if self.bit == 8:
            newRgb = tuple((n / 255) for n in self.clr)
        else:
            newRgb = tuple(((n >> 8) / 255) for n in self.clr)
        return newRgb if retRgb else _clrsys.rgb_to_hsv(*newRgb)

    def HSV(self, retRgb: bool = False) -> tuple[int, int, int]:
        x, y, z = self.clr
        hsv = tuple((x / 360), (y / 100), (z / 100))
        return _clrsys.hsv_to_rgb(*hsv) if retRgb else hsv

    def HLS(self, retRgb: bool = False) -> tuple[int, int, int]:
        x, y, z = self.clr
        hls = [(x / 360), (y / 100), (z / 100)]
        newRgb = _clrsys.hls_to_rgb(*hls)
        return newRgb if retRgb else _clrsys.rgb_to_hsv(*newRgb)

    def output(self, *newVal: int) -> "U[str, list]":
        if self.retype == HEX:
            newRgb = _clrsys.hsv_to_rgb(*newVal)
            newHex = [format(round(255*n), '02x') for n in newRgb]
            out = f'#{"".join(newHex)}'
        elif self.retype == RGB:
            newRgb = _clrsys.hsv_to_rgb(*newVal)
            out = [round(255 * n) for n in newRgb]
        else:
            if self.retype == HLS:
                newRgb = _clrsys.hsv_to_rgb(*newVal)
                a, b, c = _clrsys.rgb_to_hls(*newRgb)
            else:
                a, b, c = newVal
            out = [round(n) for n in [(360 * a), (100 * b), (100 * c)]]
        return out


def lighten(color: "U[str, list[int], tuple[int]]", percent: int = 25, inputtype: str = "", returnas: str = HEX, bitdepth: int = 8):
    """Lightens the given color"""
    work = Worker(color, percent, inputtype, returnas, bitdepth)
    return work.lightness()


def darken(color: "U[str, list[int], tuple[int]]", percent: int = 25, inputtype: str = "", returnas: str = HEX, bitdepth: int = 8):
    """Darkens the given color"""
    work = Worker(color, -percent, inputtype, returnas, bitdepth)
    return work.lightness()


def saturate(color: "U[str, list[int], tuple[int]]", percent: int = 25, inputtype: str = "", returnas: str = HEX, bitdepth: int = 8):
    """Increases the saturation of the given color"""
    work = Worker(color, percent, inputtype, returnas, bitdepth)
    return work.saturation()


def desaturate(color: "U[str, list[int], tuple[int]]", percent: int = 25, inputtype: str = "", returnas: str = HEX, bitdepth: int = 8):
    """Decreases the saturation of the given color"""
    work = Worker(color, -percent, inputtype, returnas, bitdepth)
    return work.saturation()


def invert(color: "U[str, list[int], tuple[int]]", inputtype: str = "", returnas: str = HEX, bitdepth: int = 8):
    """Inverts the given color"""
    work = Worker(color, 0, inputtype, returnas, bitdepth)
    return work.invert()
