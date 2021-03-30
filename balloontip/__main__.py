try:
    from . import Balloontip
except ImportError:
    from pathlib import Path
    from subprocess import run
    pth = Path(__file__).parent
    run(f'py -m {pth.name}', cwd=pth.parent)
    raise SystemExit


if __name__ == "__main__":
    Balloontip('Demo Title', 'Balloontip body text here', 5)
