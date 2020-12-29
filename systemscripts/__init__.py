"""Scripts for use with command line"""


import argparse
from contextlib import redirect_stdout
from io import StringIO
from os import path as os_path, listdir as os_listdir
from textwrap import *
from traceback import format_exc

from ._msg import _show_info
from . import alterImages, createBorder, createSym, listItemsInDir, lnkToSym


class _run:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=os_path.basename(os_path.dirname(__file__)),
            description=__doc__,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser.add_argument(
            '-h', '--help', help="show this help message", action='store_true')
        self.parser.add_argument(
            '-w', '--window', help="redirect help and errors to a new window", action='store_true')
        self.subs = {}
        self.subpars = self.parser.add_subparsers(
            help="sub-command help")
        glos = {na: fn for na, fn in globals().items() if na[0] != '_'}
        for funcName in [f[:-3] for f in os_listdir(os_path.dirname(__file__)) if f[0] != '_']:
            self.createHelp(funcName, glos[funcName])
        self.getArgs()

    def createHelp(self, name, script):
        subpar = self.subpars.add_parser(
            name,
            description=script.__doc__,
            help=script.__doc__,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter)
        subpar.add_argument(
            '-h', '--help', help="show this help message", action='store_true')
        subpar.add_argument(
            '-w', '--window', help="redirect help and errors to a new window", action='store_true')
        subpar.add_argument(
            '-a', '--args', help=dedent(script.main.__doc__), nargs='+')
        subpar.set_defaults(func=script.main)
        self.subs.update({script.main: {'n': name, 's': subpar}})

    def getArgs(self):
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
            _show_info(fname, out, all_args.window, 'help')
            raise SystemExit
        else:
            try:
                all_args.func(*all_args.args)
            except Exception:
                _show_info(fname, format_exc(), all_args.window)
