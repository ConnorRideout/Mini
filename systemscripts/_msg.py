from subprocess import Popen


def _show_info(win: bool, msgType: str, name: str, msg: str):
    if win:
        info = f"{name} {msgType}:"
        output = (f"\"{'='*25}`n"
                  f"{info}`n"
                  f"{'='*25}`n"
                  f"{msg}`n`n"
                  "Press <return> to close\"")
        Popen(['powershell', 'Read-Host',
               output.replace('\n', '`n')],
              creationflags=16)
    else:
        print(msg)
