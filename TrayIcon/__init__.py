from threading import Thread as _Thread
from PIL import Image as _Image, ImageDraw as _ImageDraw
import pystray


class TrayIcon(_Thread):
    def __init__(self, title=None, icon=None):
        _Thread.__init__(self, daemon=True)
        if not icon:
            self.icon = _Image.new('RGB', (32, 32), 'white')
            icon_img_draw = _ImageDraw.Draw(self.icon)
            icon_img_draw.rectangle((16, 0, 32, 16), fill='black')
            icon_img_draw.rectangle((0, 16, 16, 32), fill='black')
        elif 'PIL.Image.Image' not in str(type(icon)):
            try:
                self.icon = _Image.open(icon)
            except Exception:
                raise ValueError(
                    "icon argument must be a valid image path or a PIL.Image.Image instance")
        else:
            self.icon = icon
        self.title = title or "Python Tray Icon"
        self.menu = None

    def run(self):
        self.__tray_icon.run()

    def show(self):
        self.__tray_icon = pystray.Icon(name=self.title,
                                        icon=self.icon,
                                        title=self.title,
                                        menu=self.menu)
        self.start()

    def hide(self):
        self.__tray_icon.visible = False
        self.__tray_icon.stop()
        return

    def update(self):
        self.__tray_icon.update_menu()

    class Menu(pystray.Menu):
        def __init__(self, parent=None):
            self.__items = list()
            pystray.Menu.__init__(self, lambda: self.__items)
            if parent:
                parent.menu = self
            self.__radios = dict()
            self.__checkboxes = dict()

        def add_command(self, label, command, default=False, visible=True, enabled=True):
            newItem = pystray.MenuItem(text=label,
                                       action=command,
                                       default=default,
                                       visible=visible,
                                       enabled=enabled)
            self.__items.append(newItem)

        def add_radiobutton(self, label, command=None, group='A', checked=False, default=False, visible=True, enabled=True):
            def set_state():
                def inner(*_):
                    self.__radios[group] = label
                if command:
                    command()
                return inner()

            def get_state(*_):
                def inner(*_):
                    return self.__radios[group] == label
                return inner()

            if checked:
                self.__radios[group] = label
            elif not self.__radios.get(group):
                self.__radios[group] = ''
            newItem = pystray.MenuItem(text=label,
                                       action=set_state,
                                       checked=get_state,
                                       radio=True,
                                       default=default,
                                       visible=visible,
                                       enabled=enabled)
            self.__items.append(newItem)

        def add_checkbutton(self, label, command=None, checked=False, default=False, visible=True, enabled=True):
            def on_check(_, item):
                self.__checkboxes[label] = not item.checked
                if command:
                    command()

            self.__checkboxes[label] = checked
            newItem = pystray.MenuItem(text=label,
                                       action=on_check,
                                       checked=lambda _: self.__checkboxes[label],
                                       default=default,
                                       visible=visible,
                                       enabled=enabled)
            self.__items.append(newItem)

        def add_cascade(self, label, menu, visible=True, enabled=True):
            newItem = pystray.MenuItem(label,
                                       menu,
                                       visible=visible,
                                       enabled=enabled)
            self.__items.append(newItem)

        def add_separator(self):
            newItem = pystray.Menu.SEPARATOR
            self.__items.append(newItem)

        def insert(self, index, itemtype, **kwargs):
            if itemtype == 'command':
                self.add_command(**kwargs)
            elif itemtype == 'radiobutton':
                self.add_radiobutton(**kwargs)
            elif itemtype == 'checkbutton':
                self.add_checkbutton(**kwargs)
            elif itemtype == 'cascade':
                self.add_cascade(**kwargs)
            elif itemtype == 'separator':
                self.add_separator()
            else:
                raise ValueError("unsupported value for itemtype")
            v = self.__items.pop()
            self.__items.insert(index, v)

        def get_radiobutton(self, group='A'):
            return self.__radios[group]

        def get_checkbutton(self, label):
            return self.__checkboxes[label]
