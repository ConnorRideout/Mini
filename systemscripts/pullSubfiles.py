"""Move all files in <topdir>'s subdirectories to <topdir>, recursively."""

from subprocess import Popen
from re import search, sub
from pathlib import Path


def main(topdir: str):
    """
    Parameters
    ----------
    topdir : str
        the top-most directory to recurse from
    """

    maindir = Path(topdir)
    while not maindir.is_dir():
        maindir = maindir.parent
    subdirs = [d for d in maindir.iterdir() if d.is_dir()]
    for d in subdirs:
        for file in d.rglob('*.*'):
            new = maindir.joinpath(file.name)
            while new.exists():
                m = search(r' \((\d+)\)$', new.stem)
                ct = (int(m.group(1)) + 1) if m else 1
                nm = sub(r' \(\d+\)$|$', f' ({ct})', new.stem, 1)
                new = new.with_stem(nm)
            file.rename(new)
        for fol in sorted(d.rglob('*')):
            fol.rmdir()
        d.rmdir()
    Popen(['powershell', '[system.media.systemsounds]::Beep.play()'])
