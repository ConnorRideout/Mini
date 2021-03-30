"""A collection of functions which take a color, alter it, and return the resulting color"""

from argparse import (ArgumentParser as ArgParser,
                      RawTextHelpFormatter as HelpFrmt)
from contextlib import redirect_stdout
from typing import (Callable as C,
                    Union as U)
from traceback import format_exc
from textwrap import dedent
from subprocess import run
from pathlib import Path
from io import StringIO

try:
    from .worker import *
except ImportError:
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit


class _main:
    pKwargs = dict(add_help=False,
                   formatter_class=HelpFrmt)
    hArgs = ['-h', '--help']
    hKwargs = dict(help="show this help message",
                   action='store_true')
    wArgs = ['-w', '--window']
    wKwargs = dict(help="redirect help and errors to a new window",
                   action='store_true')
    subPars: dict[C, dict[str, U[str, ArgParser]]]
    parser: ArgParser

    def __init__(self):
        self.subPars = dict()
        self.buildParser()
        funcInfo = {'lighten': [lighten, dedent(lighten.__doc__)],
                    'darken': [darken, dedent(darken.__doc__)],
                    'saturate': [saturate, dedent(saturate.__doc__)],
                    'desaturate': [desaturate, dedent(desaturate.__doc__)],
                    'invert': [invert, dedent(invert.__doc__)]}
        for name, info in funcInfo.items():
            self.createHelp(name, *info)
        self.getArgs()

    def buildParser(self) -> None:
        progName = Path(__file__).parent.name
        self.parser = ArgParser(prog=progName,
                                description=__doc__,
                                **self.pKwargs)
        self.parser.add_argument(*self.hArgs, **self.hKwargs)
        self.parser.add_argument(*self.wArgs, **self.wKwargs)
        self.subparse = self.parser.add_subparsers(
            help="Method description:")

    def createHelp(self, name: str, fn: C, helpStr: str) -> None:
        desc = f'{name.title()}s the given color'
        subpar = self.subparse.add_parser(name=name,
                                          description=desc,
                                          help=desc,
                                          **self.pKwargs)
        subpar.add_argument(*self.hArgs, **self.hKwargs)
        subpar.add_argument(*self.wArgs, **self.wKwargs)
        subpar.add_argument('-a', '--args',
                            help=helpStr,
                            nargs='+')
        subpar.set_defaults(func=fn)
        self.subPars[fn] = dict(n=name, s=subpar)

    def getArgs(self) -> None:
        sIO = StringIO()
        with redirect_stdout(sIO):
            all_args = self.parser.parse_args()
            if all_args.help:
                try:
                    self.subPars[all_args.func]['s'].print_help()
                except Exception:
                    self.parser.print_help()
        out = sIO.getvalue()
        try:
            fname = self.subPars[all_args.func]['n']
        except Exception:
            fname = "Main"
        if out:
            self.show_info(all_args.window, "help", fname, out)
            raise SystemExit
        else:
            try:
                args = all_args.args
                clr = all_args.func(*args)
                self.show_info(all_args.window, "output",
                               fname, f'{args[0]} is now {clr}')
            except Exception:
                self.show_info(all_args.window, "error", fname, format_exc())

    @staticmethod
    def show_info(win: bool, msgType: str, name: str, msg: str) -> None:
        if win:
            info = f"{name} {msgType}:"
            output = (f"\"{'='*25}`n"
                      f"{info}`n"
                      f"{'='*25}`n"
                      f"{msg}`n`n"
                      "Press <return> to close\"")
            run(['powershell', 'Read-Host',
                 output.replace('\n', '`n')],
                creationflags=16)
        else:
            print(msg)


if __name__ == "__main__":
    _main()
