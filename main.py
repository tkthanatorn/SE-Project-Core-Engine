from src.luancher import Launcher
from src.utils import LogHeader

if __name__ == '__main__':
    # Display Application Header
    LogHeader()

    # Luanching
    luancher = Launcher()
    luancher.update()
