# Change Color

Return a given color value after selected modifications.


# Usage
```
lighten(inputType, value [, percent=25, returnType='HEX', bitDepth=8])
```
```
darken(inputType, value [, percent=25, returnType='HEX', bitDepth=8])
```
```
saturate(inputType, value [, percent=25, returnType='HEX', bitDepth=8])
```
```
desaturate(inputType, value [, percent=25, returnType='HEX', bitDepth=8])
```
```
invert(inputType, value [, returnType='HEX', bitDepth=8])
```

## Arguments
### inputtype
**`String`** _(required)_  
The data type of the input. One of `HEX`, `RGB`, `HSV`, or `HLS`.

### value
**`List` OR `string`** _(required)_  
The data. If `inputType` is `HEX`, must be a string. Otherwise, must be a list of 3 integers.

### percent
**`Int`** _(default=25)_  
Percent by which to change the color. Integer between 1 and 100.

### returnas
**`String`** _(default="HEX")_  
The data type to return. One of `HEX`, `RGB`, `HSV`, or `HLS`.

### bitdepth
**`Int`** _(default=8)_  
The color bit depth. Either 8 or 16.

# Changelog
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
    </tbody>
</table>
