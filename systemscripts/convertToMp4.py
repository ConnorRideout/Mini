"""Convert all *.gif and *.webm files within this folder and its subfolders to mp4.

3rd-party Requirements
----------
FFmpeg (https://www.ffmpeg.org/)"""

from datetime import datetime
from subprocess import run
from pathlib import Path
from sys import stdout


class main:
    """\
    Parameters
    ----------
    workingdir : str
        The path to the directory that is to be searched
    """

    topfol: str
    gifstr: str
    cmds: dict[Path, str]

    def __init__(self, workingdir: str):
        self.topfol = Path(workingdir)
        gifstr = ("-pix_fmt yuv420p -vf "
                  "'scale=trunc(iw/2)*2:"
                  "trunc(ih/2)*2'")
        self.cmds = dict()
        for p_in in self.topfol.rglob('*.*'):
            ext = p_in.suffix
            if ext == '.gif':
                self.getInfo(p_in, gifstr)
            elif ext == '.webm':
                self.getInfo(p_in, '')
            else:
                continue
        self.run()

    def getInfo(self, p_in: Path, args: str) -> None:
        s = p_in.stat()
        dt = datetime.fromtimestamp
        frmt = "%A, %B %d, %Y %I:%M:%S %p"
        mt = dt(s.st_mtime).strftime(frmt)
        ct = dt(s.st_ctime).strftime(frmt)
        p_out = p_in.with_suffix(".mp4")
        fcmd = ('ffmpeg -hide_banner -y -i '
                f'"{p_in}" -movflags faststart '
                f'{args} "{p_out}"')
        tcmd = (f'$o = Get-Item -LiteralPath "{p_out}"; '
                f'$o.LastWriteTime = "{mt}"; '
                f'$o.CreationTime = "{ct}"')
        self.cmds[p_in] = f'{fcmd}; {tcmd}'

    def run(self) -> None:
        for p_in, cmd in self.cmds.items():
            p = p_in.relative_to(self.topfol).resolve()
            run(['powershell', '-command', cmd], stdout=stdout)
            print(f'\n\n{"="*50}\nCONVERTED <{p}>\n{"="*50}\n\n')
            p_in.unlink()
