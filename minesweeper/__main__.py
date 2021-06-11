# from minesweeper import init
from minesweeper.init import initialize


def main():
    """Change working directory to project folder and call mainloop."""
    # srcDir = os.path.dirname(__file__)
    # os.chdir(srcDir)
    initialize()


if __name__ == "__main__":
    main()
