from win32comext.shell import shell
from shutil import copy as sh_copy
from subprocess import run
from pathlib import Path
from time import sleep
from re import match
from typing import Union as U

# app vars
sleep_time = 1.5
resHack_exe = Path(
    'C:\\Admin Tools\\_Resources\\resource_hacker\\ResourceHacker.exe')
restart_exp_exe = Path('C:\\Admin Tools\\Restart Explorer.exe')
# vivaldi vars
vivaldi_app_dir = Path('C:\\Program Files\\Vivaldi\\Application')
vivaldi_exe = vivaldi_app_dir.joinpath('vivaldi.exe')
vivaldi_update_exe = vivaldi_app_dir.joinpath('update_notifier.exe')
vivaldi_dir = [f for f in vivaldi_app_dir.iterdir()
               if match(r'(\d|\.)+', f.name)][0]
vivaldi_dll = vivaldi_dir.joinpath('vivaldi.dll')
# resources
resource_dir_top = Path('C:\\Admin Tools\\_Resources\\vivaldi')
main_icon = resource_dir_top.joinpath('vivaldi_icon.ico')
html_icon = resource_dir_top.joinpath('vivaldi_html.ico')
res_dir = resource_dir_top.joinpath('newResources')

# work list
work: list[list[U[Path, str]]] = [
    # [exe/dll, resource, icongroup_name]
    # main vivaldi icon, rarely works
    [vivaldi_exe, main_icon, 'IDR_MAINFRAME'],
    [vivaldi_exe, html_icon, 'IDR_X006_HTML_DOC'],  # html vivaldi icon

    [vivaldi_update_exe, main_icon, '101'],  # vivaldi updater

    [vivaldi_dll, main_icon, '101'],  # vivaldi.dll icon

    [vivaldi_exe, main_icon, 'IDR_MAINFRAME'],  # main vivaldi icon, again
]


# path checker
for [varname, var] in [[n, v] for n, v in globals().items() if isinstance(v, Path)]:
    if not var.exists():
        raise ValueError(f'{varname} > the path could not be found ({var})')

print('-=-=-= CLOSING VIVALDI AND INITIALIZING =-=-=-')
sleep(sleep_time)
# kill vivaldi process
run(['powershell', '-command', 'Stop-Process -Name "Vivaldi" | Wait-Process'])
sleep(sleep_time * 5)

# hack icon into application
print('-=-=-= HACKING ICON INTO RESOURCES =-=-=-')
sleep(sleep_time)
for [exe, res, icon_group] in work:
    sleep(sleep_time)
    run(f'"{resHack_exe}" -open "{exe}" -save "{exe}" '
        f'-action addoverwrite -res "{res}" -mask ICONGROUP,{icon_group}')
    print('\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    sleep(sleep_time)

# copy alterred images/icons
print('-=-=-= COPYING ALTERRED IMAGES/ICONS TO SOURCE =-=-=-')
sleep(sleep_time)
for old_fpath in [f for f in res_dir.rglob('*') if not f.is_dir()]:
    new_fpath = vivaldi_dir.joinpath(old_fpath.relative_to(res_dir))
    sh_copy(old_fpath, new_fpath)
sleep(sleep_time)
print('')

# update explorer
print('-=-=-= UPDATING ICONS AND RESTARTING EXPLORER =-=-=-')
sleep(sleep_time)
event = SHCNE_ASSOCCHANGED = 0x08000000
flags = SHCNF_IDLIST = 0x0000
shell.SHChangeNotify(event, flags, None, None)
run(f'nircmd elevate "{restart_exp_exe}"')
sleep(sleep_time * 5)
run('nircmd stdbeep')
print(
    f'\n-=-=-= Process complete! Closing in {round(sleep_time * 4)} seconds... =-=-=-')
sleep(round(sleep_time * 4))
