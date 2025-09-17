
import sys
import os

# Enable colored terminal output on windows
if sys.platform == "win32":
        os.system('color') 

RESET   = '\033[0m'
BLACK   = '\033[30m'
RED     = '\033[31m'
GREEN   = '\033[32m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
MAGENTA = '\033[35m'
CYAN    = '\033[36m'
WHITE   = '\033[37m'