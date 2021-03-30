from warnings import simplefilter

try:
    from .lib.constants import SPOTIFY_EXE, SPOTIFY_AHK
    from .changeshortcut import changeShortcut
    from .player import GUI
except ImportError:
    from pathlib import Path
    from subprocess import run
    pth = Path(__file__).parent
    run(['py', '-m', pth.name], cwd=pth.parent)
    raise SystemExit


def main():
    try:
        simplefilter('ignore', category=UserWarning)
        changeShortcut(SPOTIFY_EXE)
        gui = GUI()
        gui.mainloop()
    except:
        from pathlib import Path
        from subprocess import Popen
        from traceback import format_exc
        errLog = Path(__file__).parent.joinpath('lib', 'errorlog.txt')
        errLog.write_text(format_exc())
        Popen(['powershell',
               '-command',
               f'[system.media.systemsounds]::Hand.play(); Start-Process "{errLog}"'])
    finally:
        changeShortcut(SPOTIFY_AHK)


if __name__ == '__main__':
    main()
