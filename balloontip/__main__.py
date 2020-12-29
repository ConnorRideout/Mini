
try:
    from . import balloon_tip as btip
except:
    from __init__ import balloon_tip as btip


def example():

    btip('Demo', 'Type text here', 10)


if __name__ == "__main__":
    example()
