# [Spotify Player](https://github.com/Cryden13/Python/tree/main/spotifyplayer)

This is a small app that places a miniplayer on the Windows taskbar for spotify

## Usage

Compile the ahk file. Set the variables in `lib\constants.py` to the proper values, then run the compiled  
`SpotifyAHK.exe` once. Afterward, the player should automatically start when the Spotify shortcut is used

## Explanation of Variables

### Path Variables

- **SPOTIFY_EXE:** the path to the Spotify executable. The default location is %AppData%/Spotify/Spotify.exe
- **SPOTIFY_AHK:** the path to SpotifyAHK.exe. Should be in the same directory as `SpotifyPlayer.py` unless the ahk file was edited
- **SPOTIFY_LINK:** the path to either the pinned taskbar lnk file or the start menu lnk file
  - taskbar: `%appdata%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\Spotify.lnk`
  - start: `%appdata%\Microsoft\Windows\Start Menu\Programs\Spotify\Spotify.lnk`

### Text Variables

- **SPOTIFY_TITLE:** the initial title of Spotify when it first boots up (nothing playing)
- **APP_TITLE:** the preferred title for the player (usually doesn't show)
- **STARTUP_TEXT_LEFT:** the text to show on the left side of the player at startup
- **STARTUP_TEXT_RIGHT:** the text to show on the right side of the player at startup
- **SHUTDOWN_TXT_LEFT:** the text to show on the left side of the player at shutdown
- **SHUTDOWN_TXT_RIGHT:** the text to show on the right side of the player at shutdown
- **FONT_DEF:** the default font and font size

### Size Variables

- **LBL_W:** the width of the scrolling text on both sides of the player in pixels
- **BTN_SIZE:** the height and width of the buttons in pixels
- **OFFSET_X:** the amount to offset the player from the right side of the screen by in pixels
- **OFFSET_X_STEP:** the minimum horizontal amount the player must be dragged before moving in pixels
- **OFFSET_Y:** the amount to offset the player from the bottom of the screen by in pixels
- **OFFSET_Y_STEP:** the minimum vertical amount the player must be dragged before moving in pixels

### Other Variables

- **BTN_POINTS:** a dictionary of points for each button that are used to create the button's polygon
- **WINDOW_FLAGS:** the win32 flags for moving the Spotify window
- **DESKTOP_HWND:** the command that finds the desktop's Hwnd
- **Screen:** the screen class, which describes the app's dimensions

## Changelog

<table>
    <tbody>
        <tr>
            <th align="center">Version</th>
            <th align="left">Changes</th>
        </tr>
        <tr>
            <td align="center">1.0</td>
            <td>Initial release</td>
        </tr>
        <tr>
            <td align="center">1.1</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>changed automation program</li>
                        <li>added icons</li>
                        <li>added global vars</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed scrolling glitch</li>
                        <li>fixed button stalling</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">1.2</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>adjusted sizes</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed buttons</li>
                        <li>fixed info not updating</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">1.3</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>changed automation program</li>
                        <li>overhauled ui</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed ui bugs</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.0</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>majorly consolidated code</li>
                        <li>added trayicon menu</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed marque expiration</li>
                        <li>fixed text updating</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.1</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>added right-click menu</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed trayicon menu</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.2</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>consolidated code</li>
                        <li>reconfigured key sending</li>
                        <li>updated right-click menu</li>
                        <li>overhauled player startup</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed traymenu</li>
                        <li>fixed right-click menu</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">3.0</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>split the functions for readability</li>
                        <li>added more configurable variables</li>
                        <li>added an errorlog</li>
                        <li>re-configured the ahk</li>
                        <li>changed Spotify behavior when minimizing</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>removed the broken traymenu</li>
                        <li>fixed Thread errors</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">3.1</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>consolidated code</li>
                        <li>added more configurable variables</li>
                        <li>moved some functions to different classes</li>
                        <li>added type hinting</li>
                        <li>changed timings</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed issue with program not closing</li>
                        <li>fixed error where Spotify wouldn't become active</li>
                    </ul>
                </dl>
            </td>
        </tr>
    </tbody>
</table>
