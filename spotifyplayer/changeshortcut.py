from win32com.client import Dispatch

from spotifyplayer.lib.constants import SPOTIFY_LINK, SPOTIFY_AHK


def changeShortcut(newPath: str) -> None:
    link = Dispatch("WScript.Shell").CreateShortcut(SPOTIFY_LINK)
    link.Targetpath = newPath
    link.save()


if __name__ == '__main__':
    changeShortcut(SPOTIFY_AHK)
