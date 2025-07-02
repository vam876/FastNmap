"""
Nmap扫描器主程序入口
"""

import sys
import os

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from nmap_modular.gui.nmap_scanner_gui import NmapScannerGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NmapScannerGUI()
    sys.exit(app.exec_())
