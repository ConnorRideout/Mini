"""Resize all files in a directory to 2k and convert them to jpg."""

from os import chdir as os_chdir, listdir as os_listdir, path as os_path, system as os_sys


def main(runFile):
    """\
    runFile (type:string)
        The path to the file that's running this script"""

    os_chdir(os_path.dirname(runFile))
    file_name = os_path.basename(runFile)
    files = [f for f in os_listdir() if os_path.isfile(
        f) and f != file_name and os_path.splitext(f)[1] != '.lnk']
    files = ' '.join(['"{}"'.format(f) for f in files])

    def ask_reform(): return os_sys(
        'nircmd qboxcomtop "Reformat files to jpg?" "Reformat" returnval 1')
    args = [files, 't', '.jpg'] if ask_reform() else [files, 'f', '']
    os_sys(
        'magick convert {} -resize 2560x1440 -set filename:f "%{}" +adjoin "(2k) %[filename:f]{}"'.format(*args))
