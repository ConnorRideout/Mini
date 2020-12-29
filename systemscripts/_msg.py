from os import system as os_sys


def _show_info(script, output, win, msgType='error'):
    if win:
        os_sys("""start "" powershell -command "write-host \\"{}\\""; pause""".format(
            output.replace('\n', '`n')))
    else:
        print(output)
