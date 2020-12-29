from os import system as os_sys


def _show_info(win, msgType, name, output):
    if win:
        info = "{} {}:".format(name, msgType)
        output = "\n".join(["="*25, info, "="*25, output])
        os_sys("""start "" powershell -command "write-host \\"{}\\""; pause""".format(
            output.replace('\n', '`n')))
    else:
        print(output)
