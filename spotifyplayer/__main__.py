
from contextlib import redirect_stderr
from warnings import simplefilter
from os import path as os_path

from .lib.constants import SPOTIFY_EXE, SPOTIFY_AHK
from .changeshortcut import changeShortcut
from .player import GUI


def main():
    errFile = os_path.join(os_path.dirname(__file__), 'lib', 'errorlog.txt')
    with open(errFile, 'w') as f:
        with redirect_stderr(f):
            simplefilter('ignore', category=UserWarning)
            changeShortcut(SPOTIFY_EXE)
            gui = GUI()
            gui.mainloop()
            changeShortcut(SPOTIFY_AHK)


if __name__ == '__main__':
    main()
