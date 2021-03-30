# [Change Color](https://github.com/Cryden13/Python/tree/main/changecolor)

A collection of methods which take a color, alter it, and return the resulting color.

## Usage

from changecolor import . . .

- `lighten` ( color [, percent, inputtype, returntype] )
- `darken` ( color [, percent, inputtype, returntype] )
- `saturate` ( color [, percent, inputtype, returntype] )
- `desaturate` ( color [, percent, inputtype, returntype] )
- `invert` ( color [, inputtype, returntype] )

## Parameters

1. ### `color` _(required)_

   **String OR Sequence**  
   The initial color. If `inputtype` is "HEX", must be a string. Otherwise, must be a sequence of 3 integers

2. ### `percent` _(optional)_

   **Integer** _(default=25)_  
   Percent by which to change the color. Integer between 1 and 100, where 100 would change black to white or vice versa

3. ### `inputtype` _(optional)_

   **String** _(default=None)_  
   The data type of the input. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS". If not specified, it will be assumed to be "HEX" if `color` is a string, else "RGB8"

4. ### `returnas` _(optional)_

   **String** _(default="HEX")_  
   The data type to return. One of "HEX", "RGB8", "RGB16", "HSV", or "HLS"

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
            <td align="center">2.0</td>
            <td>
                <dl>
                    <dt>new</dt>
                    <ul>
                        <li>overhauled the functions</li>
                        <li>updated to use argparse</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed output</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">2.1</td>
            <td>
                <dl>
                    <dt>new</dr>
                    <ul>
                        <li>added typing hints</li>
                        <li>rearranged functions into modules</li>
                        <li>updated argument names</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed error with HLS/HSV inputtypes</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">3.0</td>
            <td>
                <dl>
                    <dt>new</dr>
                    <ul>
                        <li>changed how bitdepth works</li>
                        <li>changed required params</li>
                        <li>overhauled functions</li>
                        <li>updated help</li>
                    </ul>
                    <dt>bugfixes</dt>
                    <ul>
                        <li>fixed error with bitdepth</li>
                        <li>fixed input errors</li>
                    </ul>
                </dl>
            </td>
        </tr>
        <tr>
            <td align="center">3.1</td>
            <td>
                <dl>
                    <dt>new</dr>
                    <ul>
                        <li>added many notations</li>
                        <li>updated help</li>
                    </ul>
                </dl>
            </td>
        </tr>
    </tbody>
</table>
