from os import chdir

from .constants import PATH
from .sorter import GUI

if __name__ == '__main__':
    chdir(PATH)
    GUI().mainloop()
