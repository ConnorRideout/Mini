# Balloon Tip

Creates a balloon tip on Windows.

# Usage
```
balloon_tip(title, msg [, timeout, iconPath])
```

## Arguments
### title
**`String`** _(required)_  
The text to display at the top of the balloon tip

### msg
**`String`** _(required)_  
The text to display as the body of the balloon tip

### timeout
**`Int`** _(default=7)_  
The number of seconds to display the balloon tip. `None` means the balloon tip  
will never be deleted.

### iconPath
**`String`** _(default=python's icon)_  
The path to an .ico file that will be the balloon tip's icon.

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
    </tbody>
</table>
