"""Functions which alter a given color with the requested method"""

import colorsys

HEX = "HEX"
RGB = "RGB"
HSV = "HSV"
HLS = "HLS"
FORMATS = "HEX, RGB, HSV, or HLS"


def argInfo(full=True):
    from textwrap import dedent

    insert = """
    percent(type: int; default=25)
        Percent by which to change the color. Integer between 1 and 100.""" if full else ""
    info = """\
    inputtype (type:string)
        The data type of the input. One of {0}.
    value (type:list of 3 ints OR string)
        The initial color. If 'inputtype' is "HEX", must be a string. 
        Otherwise, must be a list of 3 integers{1}
    returnas (type:string; default="HEX")
        The data type to return. One of {0}.
    bitdepth (type:int; default=8)
        The color bit depth.Either 8 or 16 """.format(FORMATS, insert)
    return dedent(info)


def _validation(intype, val, retype, bit):
    if bit not in [8, 16]:
        raise ValueError("'bitdepth' must be 8 or 16")
    if intype.upper() not in FORMATS:
        raise ValueError("'inputtype' must be '{}'".format(FORMATS))
    if retype.upper() not in FORMATS:
        raise ValueError("'returnas' must be '{}'".format(FORMATS))
    if intype.upper() == HEX:
        v = len(val.lstrip('#'))
        if v != 6 and v != 12:
            raise ValueError(
                "HEX values must have a length of 6 (8-bit) or 12 (16-bit)")
    elif not isinstance(val, (list, tuple)) or len(val) != 3:
        raise ValueError(
            "'value' must be a list or tuple of 3 integers if 'inputtype' is '{}'".format(intype.upper()))
    return


def _HEX(value, bit, retype=HSV):
    lv = len(v := value.lstrip('#'))
    lrgb = [int(v[i:i+lv//3], 16) for i in range(0, lv, lv//3)]
    rgb = _RGB(lrgb, bit, RGB)
    return rgb if retype == RGB else colorsys.rgb_to_hsv(*rgb)


def _RGB(value, bit, retype=HSV):
    rgb = [(n >> 8)/255 for n in value] if bit == 16 else [n/255 for n in value]
    return rgb if retype == RGB else colorsys.rgb_to_hsv(*rgb)


def _HSV(value, bit, retype=HSV):
    x, y, z = value
    hsv = [x/360, y/100, z/100]
    return [round(255*n) for n in colorsys.hsv_to_rgb(*hsv)] if retype == RGB else hsv


def _HLS(value, bit, retype=HSV):
    x, y, z = value
    rgb = colorsys.hls_to_rgb(x/360, y/100, z/100)
    return [round(255*n) for n in rgb] if retype == RGB else colorsys.rgb_to_hsv(*rgb)


def _output(newVal, retype):
    if retype == HEX:
        return '#'+''.join([format(round(255*n), '02x') for n in colorsys.hsv_to_rgb(*newVal)])
    elif retype == RGB:
        return [round(255*n) for n in colorsys.hsv_to_rgb(*newVal)]
    elif retype == HLS:
        a, b, c = colorsys.rgb_to_hls(*colorsys.hsv_to_rgb(*newVal))
    return [round(n) for n in [360*a, 100*b, 100*c]]


def lighten(inputtype, value, percent=25, returnas=HEX, bitdepth=8):
    """Lighten the given color."""
    intype, retype = inputtype.upper(), returnas.upper()
    _validation(intype, value, retype, bitdepth)
    H, S, V = globals()['_' + intype](value, bitdepth)
    newVal = [H, S, max(min(V + percent/100, 1), 0)]
    return _output(newVal, retype)


def darken(inputtype, value, percent=25, returnas=HEX, bitdepth=8):
    """Darken the given color."""
    return lighten(inputtype, value, -percent, returnas, bitdepth)


def saturate(inputtype, value, percent=25, returnas=HEX, bitdepth=8):
    """Increase the saturation of the given color."""
    intype, retype = inputtype.upper(), returnas.upper()
    _validation(intype, value, retype, bitdepth)
    H, S, V = globals()['_' + intype](value, bitdepth)
    newVal = [H, max(min(S+percent/100, 1), 0), V]
    return _output(newVal, retype)


def desaturate(inputtype, value, percent=25, returnas=HEX, bitdepth=8):
    """Decrease the saturation of the given color."""
    return saturate(inputtype, value, -percent, returnas, bitdepth)


def invert(inputtype, value, returnas=HEX, bitdepth=8):
    """Invert the given color."""
    intype, retype = inputtype.upper(), returnas.upper()
    _validation(intype, value, retype, bitdepth)
    conv = globals()['_' + intype](value, bitdepth, RGB)
    convRGB = [1-n for n in conv]
    newVal = colorsys.rgb_to_hsv(*convRGB)
    return _output(newVal, retype)


class _main:
    import argparse
    from traceback import format_exc
    from os import path, system

    def __init__(self):
        self.buildParser()
        self.subs = {}
        for funcName in ['lighten', 'darken', 'saturate', 'desaturate', 'invert']:
            self.createHelp(funcName, globals()[funcName])
        self.createHelp('invert', invert, False)
        self.getArgs()

    def buildParser(self):
        self.parser = self.argparse.ArgumentParser(
            prog=self.path.basename(self.path.dirname(__file__)),
            description=__doc__,
            add_help=False,
            formatter_class=self.argparse.RawTextHelpFormatter)
        self.parser.add_argument(
            '-h', '--help', help="show this help message", action='store_true')
        self.parser.add_argument(
            '-w', '--window', help="redirect help and errors to a new window", action='store_true')
        self.subpars = self.parser.add_subparsers(
            help="sub-command help")

    def createHelp(self, name, func, full=True):
        subpar = self.subpars.add_parser(
            name,
            description=func.__doc__,
            help=func.__doc__,
            add_help=False,
            formatter_class=self.argparse.RawTextHelpFormatter)
        subpar.add_argument(
            '-h', '--help', help="show this help message", action='store_true')
        subpar.add_argument(
            '-w', '--window', help="redirect help and errors to a new window", action='store_true')
        subpar.add_argument(
            '-a', '--args', help=argInfo(full), nargs='+')
        subpar.set_defaults(func=func)
        self.subs.update({func: {'n': name, 's': subpar}})

    def getArgs(self):
        from io import StringIO
        from contextlib import redirect_stdout
        sIO = StringIO()
        with redirect_stdout(sIO):
            all_args = self.parser.parse_args()
            if all_args.help:
                try:
                    self.subs[all_args.func]['s'].print_help()
                except Exception:
                    self.parser.print_help()
        out = sIO.getvalue()
        try:
            fname = self.subs[all_args.func]['n']
        except Exception:
            fname = "Main"
        if out:
            self._show_info(all_args.window, "help", fname, out)
            raise SystemExit
        else:
            try:
                self._show_info(all_args.window, "output", fname,
                                all_args.func(*all_args.args))
            except Exception:
                self._show_info(all_args.window, "error",
                                fname, self.format_exc())

    def _show_info(self, win, msgType, name, output):
        if win:
            info = "{} {}:".format(name, msgType)
            output = "\n".join(["="*25, info, "="*25, output])
            self.system("""start "" powershell -command "write-host \\"{}\\"; pause""".format(
                output.replace('\n', '`n')))
        else:
            print(output)
