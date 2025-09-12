"""
Nmap扫描器主程序入口
"""

import sys
import os

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication
from src.gui.nmap_scanner_gui import NmapScannerGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NmapScannerGUI()
    ex.show()
    sys.exit(app.exec_())
