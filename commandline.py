from subprocess import (CREATE_NEW_CONSOLE as _NEW,
                        CREATE_NO_WINDOW as _NONE,
                        DETACHED_PROCESS as _DETACHED)
from subprocess import (IDLE_PRIORITY_CLASS as _LOWEST,
                        BELOW_NORMAL_PRIORITY_CLASS as _LOW,
                        ABOVE_NORMAL_PRIORITY_CLASS as _HIGH,
                        HIGH_PRIORITY_CLASS as _HIGHEST)
from win32con import (SW_HIDE as _HIDE,
                      SW_SHOWMAXIMIZED as _MAX,
                      SW_SHOWMINNOACTIVE as _MIN)
from subprocess import (STARTF_USESHOWWINDOW as _USE_WIN,
                        TimeoutExpired as _TimeoutExpired,
                        CompletedProcess as _CompProcess,
                        STARTUPINFO as _STARTUP,
                        Popen as _Popen,
                        PIPE as _PIPE)
from typing import (Optional as _O,
                    Union as _U)
from pathlib import Path as _Path
import shlex as _shlex


__all__ = ['RunCmd', 'openfile', 'askyesno', 'openatfile']


class RunCmd(_Popen):
    """Run a command using subprocess.Popen

    Methods
    -------
    `close_after`(timeout: float) -> subprocess.CompletedProcess
        Wait for the process to exit, forcing it to close after timeout is reached.

    Class Methods
    -------------
    `openfile`(filename: str, visibility: str, **kwargs) -> None
        Opens the specified file.

    `askyesno`(question: str, default: str = "y", **kwargs) -> bool | None
        Asks the user a yes/no question in a powershell console.
    """

    def __init__(self, command: _U[str, tuple[str]], console: str = "default",
                 capture_output: bool = False, visibility: str = "show",
                 priority: str = "default", **kwargs):
        """-----
        Parameters
        ----------
        command (str | tuple): The command to run

        console (str, optional): [default="default"] What console to use. One of "default" (use parent's console), "new", "none", or "detached". Passed to Popen.creationflags

        capture_output (bool, optional): [default=False] If True, the process's stdout and stderr will be captured

        visibility (str, optional): [default="show"] How the new process will be shown. One of "show", "hide", "min", or "max". Passed to STARTUPINFO

        priority (str, optional): [default="default"] The priority of the new process. One of "lowest", "low", "default", "high", or "highest"

        **kwargs (additional keyword arguments, optional): [default=text=True] Any additional subprocess.Popen keyword arguments
        """

        vars: dict[str, dict[str, int]]
        vars = dict(c=dict(default=0,
                           new=_NEW,
                           none=_NONE,
                           detached=_DETACHED),
                    p=dict(lowest=_LOWEST,
                           low=_LOW,
                           default=0,
                           high=_HIGH,
                           highest=_HIGHEST),
                    s=dict(hide=_HIDE,
                           max=_MAX,
                           min=_MIN))
        # get args
        kwargs['shell'] = kwargs.pop('shell', False)
        kwargs['text'] = kwargs.pop('text', True)
        if kwargs['shell'] and isinstance(command, (list, tuple)):
            args = _shlex.join(command)
        elif not kwargs['shell'] and isinstance(command, str):
            args = [f'"{cmd}"' if ' ' in cmd and _Path(cmd).exists() else cmd
                    for cmd in _shlex.split(command)]
        else:
            args = command
        # set stdout and stderr
        if capture_output:
            kwargs.update(stdout=_PIPE,
                          stderr=_PIPE)
        # get creationflags
        if (console, priority) != ('default', 'default'):
            creationflags: int = (kwargs.pop('creationflags', 0) |
                                  vars['c'].get(console, 0) |
                                  vars['p'].get(priority, 0))
            kwargs.update(creationflags=creationflags)
        # get startupinfo
        if visibility in vars['s']:
            startupinfo: _STARTUP = kwargs.pop('startupinfo', _STARTUP())
            startupinfo.dwFlags |= _USE_WIN
            startupinfo.wShowWindow |= vars['s'].get(visibility)
            kwargs.update(startupinfo=startupinfo)
        # run
        _Popen.__init__(self, args, **kwargs)

    def close_after(self, timeout: float) -> _CompProcess:
        """-----
        Wait for the process to exit, forcing it to close after timeout is reached.

        Parameters
        ----------
        timeout (float): How many seconds to wait before forcibly closing the process

        Returns:
        --------
        subprocess.CompletedProcess : A representation of the finished process
        """

        try:
            out, err = self.communicate(timeout=timeout)
        except _TimeoutExpired:
            self.kill()
            out, err = self.communicate()
        finally:
            return _CompProcess(self.args, self.returncode, out, err)


def openfile(filepath: _U[str, _Path], windowstyle: str = "show", **kwargs) -> None:
    """-----
    Opens the specified file.

    Parameters
    ----------
    filepath (str | pathlib.Path): The filepath to open

    windowstyle (str, optional): [default="show"] The state of the window of the opened file. One of "show", "hide", "min", or "max"

    **kwargs (keyword arguments, optional): [default=None] Any `RunCmd` keyword arguments
    """

    vis = dict(show='Normal',
               hide='Hidden',
               min='Minimized',
               max='Maximized')
    cmd = ['powershell', 'Start-Process',
           '-FilePath', f'"{filepath}"',
           '-WindowStyle', vis.get(windowstyle, 'Normal')]
    RunCmd(cmd, **kwargs)


def askyesno(question: str, default: _O[str] = "y", timeout: float = None, **kwargs) -> _O[bool]:
    """-----
    Asks the user a yes/no question in a powershell console.

    Parameters
    ----------
    question (str): The question to ask the user

    default (str | None, optional): [default="y"] Which option is the default. Either "y", "n", "x", or None. If user input is blank and default="x", returns None; else asks again

    timeout (float | None, optional): [default=None] How many seconds to wait before returning the default answer

    **kwargs (keyword arguments, optional): [default=None] Any `runcmd` keyword arguments

    Returns:
    --------
    bool | None : True if the user selected yes, False if no. Otherwise None
    """

    ans = f"y|n{'|' if default else ''}"
    choice = ('[y] / n' if default == 'y'
              else 'y / [n]' if default == 'n'
              else 'y / n / [cancel]' if default == 'x'
              else 'y / n')
    y, n = (f"y{'|' if default == 'y' else ''}",
            f"n{'|' if default == 'n' else ''}")
    cmd = (f"$ans = Read-Host '{question} ( {choice} )';"
           f"while($ans -inotmatch '^({ans})$') {{"
           f"$ans = Read-Host 'Invalid answer. {question} ( {choice} )' }};"
           f"if ($ans -imatch '^({n})$') {{Exit 0}} "
           f"elseif ($ans -imatch '^({y})$') {{Exit 1}} "
           "else {Exit 2}")
    proc = RunCmd(['powershell', '-command', cmd], **kwargs)
    if timeout:
        ans = proc.close_after(timeout).returncode
        return ((ans == 1) if ans in [0, 1]
                else None if default == None
                else (default == 'y'))
    else:
        ans = proc.wait()
        return False if ans == 0 else True if ans == 1 else None


def openatfile(filepath: _U[str, _Path]) -> None:
    """-----
    Open windows Explorer with the given file selected.

    Parameters
    ----------
    filepath (str | Path): The path to the file to select
    """

    cmd = ['explorer.exe', '/select,', filepath]
    RunCmd(cmd, 'none')
