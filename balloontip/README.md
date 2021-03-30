# [Balloon Tip](https://github.com/Cryden13/Python/tree/main/balloontip)

Creates a popup balloontip on Windows 10

## Usage

`Balloontip`( title, msg [, timeout, iconpath, silent] )

## Parameters

1. ### `title` _(required)_

   **String**  
   The text to display at the top of the balloontip

2. ### `msg` _(required)_

   **String**  
   The text to display as the body of the balloontip

3. ### `timeout` _(optional)_

   **Integer OR Float** _(default=7)_  
   The number of seconds to keep the balloontip active. Keep in mind that after about 4 seconds it will be put into the action center

4. ### `icon` _(optional)_

   **String** _(default="default")_  
   The balloontip's icon. Can be one of "default", "info", "warning", "error", or an *.ico image file path. If "default" or None, it will be set to the default python icon

5. ### `silent` _(optional)_

   **bool** _(default=False)_  
   Whether to play a sound when the balloontip is displayed

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
                        <li>condensed code</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed messages not showing</li>
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
                        <li>added overrideable clicking methods</li>
                        <li>added more notations</li>
                        <li>added type hints</li>
                        <li>updated built-in icon list</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed timeout errors</li>
                        <li>fixed error messages</li>
                    </ul>
                </dl>
            </td>
        </tr>
    </tbody>
</table>
