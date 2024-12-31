
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import sys
from modules.main import *



def main():
    app = QApplication(sys.argv)
    window = FXTrend()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
