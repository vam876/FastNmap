"""
Nmap扫描器GUI模块，负责用户界面的实现和交互逻辑

本模块包含了Nmap扫描器的图形用户界面实现，提供了用户与Nmap功能交互的各种控件和布局。
主要功能包括：
1. 配置和启动Nmap扫描
2. 显示和解析扫描结果
3. 提供各种扫描选项的设置界面
4. 导出扫描结果
"""

import os
import base64
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QFileDialog, QTextEdit, QCheckBox, QRadioButton, QTabWidget, 
    QLabel, QButtonGroup, QMessageBox, QStatusBar, QProgressBar, QFrame, QSplitter,
    QToolButton, QMenu, QAction, QInputDialog, QTableWidget, QTableWidgetItem,
    QComboBox, QSpinBox, QGroupBox, QGridLayout, QHeaderView
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QDateTime
from datetime import datetime
from PyQt5.QtGui import QIntValidator, QIcon, QPixmap, QFont, QColor, QPalette

from src.utils.constants import ico_base64, SCAN_TYPES
from src.core.nmap_executor import NmapThread
from src.core.command_builder import NmapCommandBuilder
from src.core.nmap_parser import NmapOutputParser
from src.core.asset_monitor import AssetMonitor
from src.core.html_report import HTMLReportGenerator
from src.gui.widgets.monitor_widgets import AssetMonitorTabWidget
from src.gui.tabs.asset_comparison import AssetComparisonWidget

class NmapScannerGUI(QWidget):
    """
    Nmap扫描器的图形用户界面
    """
    
    def __init__(self):
        """
        初始化GUI组件和变量
        
        初始化主窗口、设置图标并准备所有必要的变量，为UI构建做准备
        """
                # Base64 编码的图标字符串
        ico_base64 =  """
        AAABAAMAEBAAAAAAIABoBAAANgAAACAgAAAAACAAqBAAAJ4EAAAwMAAAAAAgAKglAABGFQAAKAAAABAAAAAgAAAAAQAgAAAAAABABAAAAAAAAAAAAAAAAAAAAAAAAP///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8BwqRnB8+vbm3gw4K948eF2eTHhdvhxILB07V0eceiYxX///8B////Af///wH///8B////Af///wG6nmUFxqZrUdK1etfcwIn/486d/9/Lnf/fy57/4cyb/97Ci//RsXbny692ZbebYgn///8B////Acy1hmHHpm2j0LWC39rCk//p2Lb/7+PJ/+XYu//dz67/1sio/+TXuv/s4Mb/7N28/93FmP/PtIHlyq97p8mwgGnVvpLp1LuO/+ncv//58t//+fLf/+bcxP/d0LT/kIJq/5mLcv/Vx6r/5NnB//fx3v/58t//8ObO/9S8kf/St4b7y7mRO9jFnefYwZb/4M2l//Lox//g0qz/0MCX/5eHaf+hk3f/x7eO/97Qqv/x58b/6Nq3/93Lpv/ax6Dzy7iQU////wHBq4AZ0LmNrdnDl//awpT/28mV/9nGiP/KtHT/zL2U/9vJjv/Xwor/3sug/9a8jv/VwprHx7OKKf///wH///8B////AbqkdwPEq3pP07+W3eDMpf/q4MH/5tqz/+XZsf/p4MD/5NOu/9XBmOXKsYRpx7KLBf///wH///8B////Af///wH///8B////AauQXgXKuJBN282tjd/Ttaff1LWr3M+vkcy7lFG4oXYH////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wEAAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//KAAAACAAAABAAAAAAQAgAAAAAACAEAAAAAAAAAAAAAAAAAAAAAAAAP///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8Bx6hoCcmqZzHNrWpt0rJul9S1cLPWt3G31rdxt9S1cLPStG+d0LBsecqsajvKrW4T////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////AcKkZxnIpWWj1rh31+bKivPr0JD77tOU/+7UlP/u1JT/7tOU/+vRkP3nzIz127594c2sbLPHomNT////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8BvqRsA8KmbBvDo2Z70rV449S0eP/lypD/6NCW/+LJkf/bw4v/2cCJ/9jAif/bwov/4MeP/+fOlf/s1Jv/17d7/9GwdPfLq2+lxKdrLb+jagf///8B////Af///wH///8B////Af///wH///8B////Af///wH///8BuJ1lA7ueZRHCo2hnyahtwdS4f/vYu4L/2b6H/97GlP/k0qn/3syk/+PSrf/m17P/5ta0/+PTrv/fzaX/4M2k/+HLm//Ss3v/3MGJ/8qmaP/Os3vXyaxyjbicZBmxk1oF////Af///wH///8B////AcuzhQ3Eq3glxKl1RcKhZ2vKsHydyq534dO5hP/Ut4L/1bmH/+POp//z58r/7+PI/+LUtf/n2bz/5Na3/+HSsv/Yyqr/49a2/+bZvP/j1bf/6Ny///br0v/jz6f/3smc/9i9iv/OrHP/yq1178esdqvDoWdvwadzS8GlcifHrn0TzbaIhc22hs3IqG/jyKZs+dK2g//Yv5D/2L2N/+rauf/z587/+fHc//Tr1f/l2L3/6NzC/+PWuv/bzaz/1cWk/8K1l//ay6n/4NO1/+fbwf/k2L3/7uPL//nv2f/37NX/6tm4/+PRq//Wu4v/1LuL/8+yfvnLs4PlyLB/z8u0hZ/Ru47307aE/8ysd//TuY7/3MWd//bt2P/69OL/+vPh//nz4f/68+L/6uHM/+XaxP/l2sL/286x/7aojP+HemP/p5qA/5+Qd//WyKv/4da8/+fcx//j2MH/+fPi//nz4f/68+H/+vTi//nx3//o2Lv/1LyT/9C1h//OrXb/z7F9/8+5j63ezKf/2b+S/9rGoP/fz6//9e3X//jx3P/48dz/+PHc//jx3f/j2L7/59zE/97Stf/Vx6b/intj/3hsVv+jl33/eWxV/8Cxk//bzrD/59zD/+DUuv/07Nj/+PHc//jx3P/48dz/9/Db/+rew//RuIr/3Mig/9a8jv/UwZrtwqyBH8+9l63OsHv/6d7A/9K2hf/YxJz/5tez//Dkxf/068//9ezQ/9/Sr//i1rX/08Wi/8Gykf+nmXz/o5V6/72ymv+ilXn/uquL/8O1k//i1rT/3tCt/+/myP/07M//9OvO//DmyP/g0rD/2cei/+XXtf/Uuov/z7yV08azikH///8Bwq2BHcixhKvbzq311LeF/+LTsf/OsHz/3cqg/+7ivf/y58P/39Cm/9/Qpv/ay53/0sCN/5yKZf91Zkj/oZR3/4NzUf/ItoX/18aW/+DRp//ayp//8OS///Hmwf/l1q7/2MKX/+DRrv/bw5j/4NSz/cy1idHEsIc1tZxuA////wH///8Bv6h9C8GsgVXOtIXZ2cSc+9/LpP/bxp3/1LqI/+DMnP/j0p//2siQ/97Mlf/UwYb/zLd6/7aha/+6q4n/0cGY/9jHkv/byZH/3MqT/9zKlf/k0qH/3cqf/9W7jf/XvY//4dGv/9G7kO3Jto1/waqAFf///wH///8B////Af///wH///8Bu6J2A8SwhjnKsoWr1b+U/9W5if/j1LD/0LB8/9zMoP/UwIb/2MSB/9rGg//Uv3j/0bty/8W3kf/h05//3s2R/9vHg//Runv/1LuE/9nDmP/fzab/2sKW/9K2hf/QvZXRx7GHX7+rfgv///8B////Af///wH///8B////Af///wH///8B////AbqkdwfCr4RVxqp2w97PrP3awpf/38yl/+HOqP/i1rL/28yc/9rIkf/Xxoz/1sSK/9jGjv/by5v/4dSu/+vjx//XvY3/4tKu/9a/lP/Otonfxa1/g8eyiw////8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////AbihcwO7pHchxbCEi8iyhenVu4z/6ty9//Xw2//18Nr/9O7X//Pt1v/z7db/9O7X//Xw2//18Nv/9fDb/9e7iv/Rv5fxxa1/o8WtgTW/o3EJ////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8Bq5BeE8SwhXXQv5mt3tGy2eTZvOnm3MHv597D8ejfxPHn3sPx5dq+69/StN3RwZyxyLWMf7ihdh3///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////AbymfBHBrIIzxLCGQcq4kFfMupRhybeQZcu5k2HGsolJxLGHNb+sgBWghVYD////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgAAAAwAAAAYAAAAAEAIAAAAAAAgCUAAAAAAAAAAAAAAAAAAAAAAAD///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wHAoGIly6pnVcinYnPJqWOJzKxkk86tZ5PPrWeTzKxlk8qpZIvJqWN5y6tnXc+wbzcbAAYD////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8Bx6hoT8qrZ6/Pr2rV1rdz6d2/e/ngw37/4MN+/+HDgP/hw3//4MN+/+DDf//dwHv72Ll178+vat3NrmrD0LNxe7icZxP///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////AcKkZzfHo2Pfy6lp9+HGhf/u1JX/8tmb//Tbnf/13J//9d2f//Xdn//13Z//9d2f//Xcn//0253/8tmb//HXmf/ny4v/1LZ198qnZ+/HomS7////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wHCqHMTvp9gm8+ycvPLp2n/0q9z//Xfpf/z3KL/6tKW/+TJjv/dwoT/17t9/9S4ev/UuHr/1rl7/9zBg//jyIz/6dGV//Laof/13qX/9N6k/86qbf/IoWP/yKpr182yeEn///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8Bv6RsD8OnbG/Ep2rtyKFj/+vUnv/nz5j/3cCG/93Eiv/YvoX/3MSP/9rEk//cx5v/4c+n/+LRqP/h0Kn/4tGo/93Jnf/YwpL/2cGM/9e9hP/dxIv/272D/86pbf/t16D/0LB0/8qoa//FqGyzv6NqK8CkbgX///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8BuJ1lDbyfZh+9oWdtx6Zq8cyqb//dxY//2r2E/9O1fP/XvYj/zq94/+fUq//v4MD/4dKw/+DQrf/l1rT/59i3/+ncu//q3Lz/5da2/+fXtv/k1bP/386s/+jZt//s3Lb/1biD/9G0ff/ex5L/zalt/8ihY//Vu4T/yq91/8qrcrG5nWUvt5phEZp7QgP///8B////Af///wH///8B////Af///wH///8B////Af///wGukFkNtZdgH7aYXzG7n2dTx613m8iueO/OtX//3siW/8unav/KpWn/1b6O/9m+jf/s27j//PPb/+/kyP/fz6//5Na2/+ncvv/n2rv/5ti5/+PVtf/h0rH/5de3/+jbvP/o273/59m7/9/Qr//l2Lr/+e/W//fs0f/fyqD/z652/9rEk//izZ3/yKFj/8una//Ms37/w6lytbufZ2e1ll03tJdeI6aITBP///8B////Af///wHHr4MNzbWGVcKodHnKsX+bx6p0y8ijZvvPtoP/2MKR/8qma//Ss33/1rqI/9zHnv/dxJj/+O7V//vy3f/78tv/9OnR/+DRs//l2Lv/6t3C/+XYvP/h1LX/3c6t/9vLqf+5rJD/3M2q/97Qr//k17n/6NzA/+jbwP/g0rT/6Nq///rx2v/68dr/8uPF/+/hw//WvY3/1bqH/9e9i//Jo2b/zq93/9G5h//IoWP/y7OBy8WreKW/o29/x657W8ivgSHLtYaT0bqM98+4if/IpGj/yqtz/8mma//OrXX/3MSY/93JoP/YvI3/4cuj//vz3//78+D/+vLe//nx3f/68t7/5di//+TYvf/q38j/5tvB/9/Stf/Zy6n/2suq/869nf+5rJD/1MSj/9vMqf/bza7/49e7/+nexf/o3cT/39O4//Ho0f/68t3/+vHd//vz3//26tP/8eTJ/+fYt//Zv5P/4tKs/9K1g//St4T/0ryO/8uzg//JsYD/zreI+8u0hcHSvpT918KW/86sdP/IpWz/zKt1/9jBnP/OrXb/6Ni5//rz4v/79eT/+vTj//rz4v/58+L/+vPi//r04v/z7Nn/4NO7/+fcx//q4Mr/4da8/9nLrv/Xyav/pZZ8/4N2X/+5rJD/jn9n/7+wlP/azK3/3M+0/+fdxf/o3sn/5dnC/+TZw//79eT/+fPi//nz4v/68+L/+vTj//v15P/68+L/9u7Z/9zGof/Stov/2cKb/8mpc//Kp23/zapx/8uobv/LsoTj0LJ+/9zClf/Wu4z/z7KA/9K9lv/hz63/+vPh//rz4f/68+H/+vPh//rz4f/68+H/+vPh//v04//r4cz/4NS8/+zizv/k2cL/3NCz/9rMrv+qmoD/c2VQ/31xXv+5rJD/dGhU/4d5Yv/Jup3/2cyt/+HVvP/p38n/59zG/97Tu//38N7/+vPi//rz4f/68+H/+vPh//rz4f/68+H/+fPh/+rcwP/WwZn/0r+Y/9e/lP/MqW//6tm4/8+3iv/Lt5BV1sah/+fbvv/cxJj/28OX/+HTs//SwJr/6t/E//jx2//38Nr/9/Da//fw2v/38Nr/9/Da//jx3P/i17v/4tW6/+nfxv/g07f/2Mqo/9HBn/+HeF7/fHBa/3ZqU/+5rJD/fHFa/3JkTf+qm37/2Mmm/9zPsP/n3cL/5drA/97RtP/w6NH/9/Db//fw2v/38Nr/9/Da//fw2v/38Nr/9+/Y/+HTs//NsX//1rqK/+bWtf/XvIz/1cSe/9G/mdX///8BwqyBidbGo//Kpmv/1ryM//Tu2P/ZwZX/zK97/9/Rrv/x6Mz/9u3S//Xt0v/17dL/9e3S//fv1P/e0rL/4dSz/+bbvv/bzqz/uayQ/7mskP+5rJD/uayQ/7mskP/Rybb/uayQ/7mskP+5rJD/uayQ/7mskP/j2Lj/5Ni5/93Qrv/t48b/9u7T//Xt0v/17dL/9u3S//Xt0v/v5cn/18ik/9jKqP/y7Nb/y6dt/9rDl//Ww53/yriQ4bylehv///8Bz8ajA8KtgYHJqnP939Cv/+7nzv/Qr3j/zqx0/9zPr//Os4H/0K94//Lnxv/z6cn/8+nJ//Tqy//h063/282l/+LWsf/dzqb/1MSX/9G/kv+OfV3/cWNI/3ttU/+5rJD/fXBV/3NkR/+yoHr/08GS/9rKoP/h1K3/4NKs/9nKov/t4sD/9OrK//Ppyf/z6cn/8ebF/+HUr//Twp3/1b2P/9/Jn//s5cr/3Mif/9C4iv/GsonFtZxuG////wH///8B////Af///wG3oHFZyriQ1dnLqv/Prnf/5ti4/+revv/OrXb/0baG/93Npf/q3LT/8ea+//LnwP/k1qv/2MaY/+LUqf/f0KL/1MOQ/9G+iP+7p3v/gnFQ/25eQP+5rJD/b19B/5iGX//Nuob/0r+K/9rJmv/i06j/3c2g/9jHmv/w5L3/8ufA//DkvP/o2rL/z7SB/9O5i//q4sf/38if/9nBlP/o3sL/ybSK88WtgJ/Er4YP////Af///wH///8B////Af///wH///8Bv6l+LcKtgqHIpmz/5da2/9nBlf/fyqD/6uLH/9W8jv/Mq3P/4dCk/+zer//t36//2MWP/93MmP/h0J3/2ceQ/9C8gf/QvH//v6p2/5+LX/+5rJD/q5hq/9XEmf/Uwoz/1cKK/93Mlv/h0J3/2ceS/9/Nm//y5bf/59ep/9jDlP/LqG//6eDG/8+ud//r3sD/28ae/9K6jf/MupLXwaqAX////wH///8B////Af///wH///8B////Af///wH///8B////Abuidg27pHVjzr2Y3dO+lP/NqnL/8evT/9CveP/Vuov/3Mqk/8qma//gz5z/2saJ/9nEh//ey5H/3cqP/9bBg//Qunj/z7hz/9C5dv+5rJD/4NGk/+nfwP/i1ar/3MmO/9/Mkv/byIv/2MSF/9/MlP/StX7/0baE/+TZu//OrXf/6t7A/82rc//h0q//zLiP/8iyhqu/q34x////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8BwKuALcSpdrPKsH//6N7D/8ihY//y7NT/2sOX/8unbf/dz6v/2Mib/865e//TvXf/3MiB/9zIgv/YxHv/1L91/9K8cP+5rJD/3cyN/+HRmP/fzY3/3cmC/9jDe//OuHb/zK50/9K3hP/l2rz/zq12/+ndvv/ex53/2cCU/8yteP/NuI3pv6p+W8WwhxH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Abqkdw28pnlLyLaN3cmnbf/v58//28SZ/97Hnf/r4sj/0K95/+PUsP/czqf/0r+L/8+6e//Runb/zrdw/823bv/LtGr/zLVr/863cf/OuHj/0L2G/9rLof/m3b3/6Nu7/9Cvef/s5Mr/0LB6/+PUsv/VvpP/ya59/8Oug5PHs4sf////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8BuaF0FbyleIfJt4/50baH/9jAlP/fyZ//07WB//bx3P/28Nv/9fDa//Ls1P/v587/7eXK/+zkyf/s48n/7ebL//Dpz//z7df/9fDa//bw2//28dz/9/Ld/8ihY//s48j/zqx1/8ixg//Gr4TJwqZ0Sa2RXwX///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wG9pHonvKd5r8Ovg/XUu4390rSA//bw2//28dz/9vHc//fy3f/38t3/9/Ld//fy3f/38t3/9/Ld//fy3f/38t3/9vHc//bx3P/28Nv/9O/Z/8ihY//Kt475xrKJzbiidEn///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////AauQXivCroKXyLWM39fIpe3k2bz57OTK//Hq0v/x6tP/8evU//Lr1P/y7NX/8uzV//Hr1P/x6tP/7ubN/+TZvfvYyqjvyreO48i1jKe5oXY/////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8BYjQABb+qgEvAq4GHw66Esci1i8XMu5PNz76Y09HBnNXSw57X08Of19C/mdPLuJDJxbKIucSxh4/Cr4RToIVWDf///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////AR0AAAO6o3oXxLGLJb+pgCm0nG0rtJxsLcGviSWqj2QP////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wH///8B////Af///wEAAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8AAAAAAAD//wAAAAAAAP//AAAAAAAA//8=
        """
        super().__init__()
        # 存储文本编辑框的字典，用于在不同标签页中显示扫描过程和结果
        self.text_edits = {'扫描过程': None, '扫描结果': None}
        self.current_output = ""  # 用于缓存当前输出的字符串
        self.scan_type = ""  # 用于缓存用户选择的扫描类型
        self.thread = None  # 存储NmapThread实例，用于执行扫描任务
        self.is_scanning = False  # 扫描状态标志
        # 使用深色模式作为唯一主题
        self.scan_progress = 0  # 扫描进度
        self.scan_configs = {}  # 存储扫描配置
        self.scan_history = []  # 扫描历史记录
        
        # 初始化资产监控组件
        self.asset_monitor = AssetMonitor()
        self.html_generator = HTMLReportGenerator()
        
        # 连接资产监控信号
        self.asset_monitor.scan_completed.connect(self.on_monitor_scan_completed)
        self.asset_monitor.scan_progress.connect(self.on_monitor_progress)
        self.asset_monitor.scan_error.connect(self.on_monitor_error)
        
        # 设置窗口图标 - 从base64编码的字符串加载
        logo = QPixmap()
        logo.loadFromData(base64.b64decode(ico_base64))
        self.setWindowIcon(QIcon(logo))
        
        # 创建定时器用于更新状态栏
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # 每秒更新一次
        
        # 初始化用户界面
        self.initUI()

    def initUI(self):
        """
        初始化用户界面
        
        """
        # 设置现代化科技风格样式表
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0e1a;
                color: #e0f4ff;
                font-family: 'Segoe UI', 'Microsoft YaHei', 'Arial', sans-serif;
            }
            QLineEdit, QTextEdit {
                background-color: #1a2332;
                border: 1px solid #2a4a6b;
                border-radius: 6px;
                padding: 8px;
                color: #e0f4ff;
                selection-background-color: #4a9eff;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #4a9eff;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a9eff, stop:1 #2575d6);
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5aa6ff, stop:1 #3585e6);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a8eef, stop:1 #1565c6);
            }
            QTabWidget::pane {
                border: 2px solid #2a4a6b;
                border-radius: 8px;
                background-color: #0f1419;
                margin-top: -1px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a2332, stop:1 #0f1419);
                color: #a0c4ff;
                border: 1px solid #2a4a6b;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 10px 16px;
                margin-right: 2px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a9eff, stop:1 #2575d6);
                color: #ffffff;
                border-bottom: 2px solid #4a9eff;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a3a52, stop:1 #1a2332);
                color: #d0e4ff;
            }
            QCheckBox, QRadioButton {
                color: #e0f4ff;
                spacing: 8px;
                font-weight: 500;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #1a2332;
                border: 2px solid #2a4a6b;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4a9eff, stop:1 #0d7be6);
                border: 2px solid #4a9eff;
                border-radius: 4px;
            }
            QRadioButton::indicator:unchecked {
                background-color: #1a2332;
                border: 2px solid #2a4a6b;
                border-radius: 10px;
            }
            QRadioButton::indicator:checked {
                background: qradial-gradient(cx:0.5, cy:0.5, radius:0.5,
                    stop:0 #ffffff, stop:0.6 #4a9eff, stop:1 #2575d6);
                border: 2px solid #4a9eff;
                border-radius: 10px;
            }
            QLabel {
                color: #e0f4ff;
                font-weight: 500;
            }
        """)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # 增加组件间的间距
        layout.setContentsMargins(15, 15, 15, 15)  # 设置外边距

        # 第1行：目标地址输入区
        url_layout = QHBoxLayout()
        
        # 创建并配置地址输入框
        self.url_line_edit = QLineEdit()
        self.url_line_edit.setPlaceholderText("输入扫描目标或加载文件...")
        self.url_line_edit.setText("127.0.0.1")  # 设置默认值
        self.url_line_edit.setMinimumHeight(35)  # 增加高度使其更易于交互
        
        # 添加导入按钮
        self.load_button = QPushButton('导入')
        self.load_button.setMinimumHeight(35)
        self.load_button.clicked.connect(self.load_file)
        
        # 创建操作按钮区域
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setSpacing(10)
        
        # 定义操作按钮及其样式（与程序整体风格一致的深色系）
        actions = [
            ('开始', '#1e293b', '#334155', True),   # 深蓝灰，特殊光效
            ('停止', '#1e293b', '#334155', False),  # 深蓝灰
            ('导出', '#1e293b', '#334155', False),  # 深蓝灰
            ('结果', '#1e293b', '#334155', False),  # 深蓝灰
            ('清空', '#1e293b', '#334155', False)   # 深蓝灰
        ]
        
        # 创建操作按钮
        self.action_buttons = {}
        for action_info in actions:
            if len(action_info) == 4:
                action, bg_color, hover_color, special_glow = action_info
            else:
                action, bg_color, hover_color = action_info
                special_glow = False
            
            btn = QPushButton(action)
            btn.setMinimumHeight(35)
            btn.setFixedWidth(60)  # 固定宽度
            
            if special_glow and action == '开始':
                # 开始按钮特殊光效样式
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 {bg_color}, stop:1 #0f172a);
                        color: #e0f4ff;
                        border: 2px solid #4a9eff;
                        border-radius: 6px;
                        padding: 8px 12px;
                        font-weight: 600;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #3b82f6, stop:1 #1e40af);
                        border: 3px solid #60a5fa;
                        color: #ffffff;
                    }}
                    QPushButton:pressed {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #1e40af, stop:1 #3b82f6);
                        border-color: #93c5fd;
                    }}
                    QPushButton:disabled {{
                        background-color: #0f172a;
                        color: #6b7280;
                        border-color: #1e293b;
                    }}
                """)
            else:
                # 普通按钮样式
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 {bg_color}, stop:1 #0f172a);
                        color: #e0f4ff;
                        border: 2px solid #2a4a6b;
                        border-radius: 6px;
                        padding: 8px 12px;
                        font-weight: 600;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 {hover_color}, stop:1 #1a2332);
                        border-color: #4a9eff;
                        color: #ffffff;
                    }}
                    QPushButton:pressed {{
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #0f172a, stop:1 {bg_color});
                        border-color: #89b4fa;
                    }}
                    QPushButton:disabled {{
                        background-color: #0f172a;
                        color: #6b7280;
                        border-color: #1e293b;
                    }}
                """)
            
            # 连接按钮事件
            if action == '开始':
                btn.clicked.connect(self.start_scan)
            elif action == '停止':
                btn.clicked.connect(self.stop_scan)
            elif action == '导出':
                btn.clicked.connect(lambda: self.export_scan_process())
            elif action == '结果':
                btn.clicked.connect(lambda: self.export_scan_results())
            elif action == '清空':
                btn.clicked.connect(self.clear_text)
            
            self.action_buttons[action] = btn
            action_buttons_layout.addWidget(btn)
        
        # 将组件添加到布局
        url_layout.addWidget(self.url_line_edit)
        url_layout.addWidget(self.load_button)
        url_layout.addLayout(action_buttons_layout)
        layout.addLayout(url_layout)

        # 第2行：扫描选项设置区
        options_layout = QHBoxLayout()
        options_layout.setSpacing(8)  # 设置组件间的间距
        
        # 创建并配置端口输入框
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("80,443-445")
        self.port_input.setMinimumHeight(30)
        
        # 超时设置
        self.timeout_input = QLineEdit('')  # 空字符串作为默认值
        self.timeout_input.setPlaceholderText("300")
        self.timeout_input.setFixedWidth(60)  # 增加宽度使其更易读
        self.timeout_input.setMinimumHeight(30)
        
        # 线程设置
        self.threads_input = QLineEdit('50')  # 默认值为50
        self.threads_input.setPlaceholderText("线程")
        self.threads_input.setFixedWidth(60)
        self.threads_input.setMinimumHeight(30)
        
        # 扫描类型参数
        self.scan_type_input = QLineEdit('3')  # 默认值为3
        self.scan_type_input.setPlaceholderText("0-5")
        self.scan_type_input.setFixedWidth(60)
        self.scan_type_input.setMinimumHeight(30)
        self.scan_type_input.setValidator(QIntValidator(0, 5, self))  # 限制只能输入0-5的数字
        
        # 附加参数输入框
        self.params_input = QLineEdit()
        self.params_input.setPlaceholderText("附加参数")
        self.params_input.setFixedWidth(100)
        self.params_input.setMinimumHeight(30)
        
        # 结果文件路径输入框
        self.result_file_edit = QLineEdit()
        self.result_file_edit.setPlaceholderText("选择结果保存路径")
        self.result_file_edit.setFixedWidth(150)
        self.result_file_edit.setMinimumHeight(30)
        
        # 文件选择按钮
        self.result_file_button = QPushButton('选择文件')
        self.result_file_button.setMinimumHeight(30)
        self.result_file_button.clicked.connect(self.select_result_file)

        # 添加标签和对应的输入框到布局
        labels = ['端口', '超时(s)', '线程', '-T 参数', '附加参数', '保存位置']
        
        # 创建样式化的标签
        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; color: #4a9eff;")
            options_layout.addWidget(label)
            
            # 根据标签索引添加相应的输入控件
            if i == 0:
                options_layout.addWidget(self.port_input)
            elif i == 1:
                options_layout.addWidget(self.timeout_input)
            elif i == 2:
                options_layout.addWidget(self.threads_input)
            elif i == 3:
                options_layout.addWidget(self.scan_type_input)
            elif i == 4:
                options_layout.addWidget(self.params_input)
            elif i == 5:  # 最后一个输入框后面是选择文件按钮
                options_layout.addWidget(self.result_file_edit)
                options_layout.addWidget(self.result_file_button)

        # 添加选项布局到主布局
        layout.addLayout(options_layout)


        
        # 端口选项复选框区域
        port_checkbox_layout = QHBoxLayout()
        port_checkbox_layout.setSpacing(10)
        
        # 创建端口选项分组标题
        port_group_label = QLabel("端口选项：")
        port_group_label.setStyleSheet("font-weight: bold; color: #4a9eff; font-size: 14px;")
        port_checkbox_layout.addWidget(port_group_label)
        
        # 定义端口选项
        ports = ['全端口1-65535', '轻量端口', 'HTTP端口', '高危端口', '数据库端口', '弱口令端口', 'Top1000', 'Top100', '排除打印机']
        self.port_checkboxes = []
        
        # 创建并配置复选框
        for port in ports:
            checkbox = QCheckBox(port)
            checkbox.setStyleSheet("""
                QCheckBox {
                    spacing: 8px;
                    color: #e0f4ff;
                    padding: 4px 8px;
                    border-radius: 4px;
                    background-color: rgba(26, 35, 50, 0.5);
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 3px;
                }
                QCheckBox::indicator:unchecked {
                    background-color: #1a2332;
                    border: 2px solid #2a4a6b;
                }
                QCheckBox::indicator:checked {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #4a9eff, stop:1 #2575d6);
                    border: 2px solid #4a9eff;
                }
                QCheckBox:hover {
                    background-color: rgba(74, 158, 255, 0.15);
                }
            """)
            checkbox.stateChanged.connect(self.on_port_checkbox_changed)
            self.port_checkboxes.append(checkbox)
            port_checkbox_layout.addWidget(checkbox)

        layout.addLayout(port_checkbox_layout)
        

        # 第4行：扫描类型选择区
        scan_type_layout = QHBoxLayout()
        scan_type_layout.setSpacing(15)  # 增加间距
        
        # 创建扫描类型标题
        scan_type_label = QLabel("扫描类型：")
        scan_type_label.setStyleSheet("font-weight: bold; color: #4a9eff; font-size: 14px;")
        scan_type_layout.addWidget(scan_type_label)
        
        # 创建单选按钮组
        self.scan_type_group = QButtonGroup(self)
        
        # 定义各扫描类型的颜色 - 科技蓝色调
        scan_type_colors = {
            '默认扫描': "#4a9eff",
            '存活扫描': "#00d9ff",
            '服务识别': "#6366f1",
            '系统识别': "#8b5cf6",
            '端口识别': "#06b6d4",
            '暴力破解': "#f59e0b",
            '漏洞扫描': "#10b981"
        }
        
        # 创建并配置单选按钮
        for i, scan_type in enumerate(SCAN_TYPES):
            radio = QRadioButton(scan_type)
            color = scan_type_colors.get(scan_type, "#4a9eff")
            radio.setStyleSheet(f"""
                QRadioButton {{
                    spacing: 8px;
                    color: #e0f4ff;
                    padding: 6px 12px;
                    border-radius: 6px;
                    background-color: rgba(26, 35, 50, 0.6);
                }}
                QRadioButton::indicator {{
                    width: 18px;
                    height: 18px;
                    border-radius: 9px;
                }}
                QRadioButton::indicator:unchecked {{
                    background-color: #1a2332;
                    border: 2px solid #2a4a6b;
                }}
                QRadioButton::indicator:checked {{
                    background: qradial-gradient(cx:0.5, cy:0.5, radius:0.5,
                        stop:0 #ffffff, stop:0.6 {color}, stop:1 {color});
                    border: 2px solid {color};
                }}
                QRadioButton:hover {{
                    background-color: rgba(74, 158, 255, 0.2);
                    border: 1px solid rgba(74, 158, 255, 0.3);
                }}
            """)
            # 设置默认选中第一个选项
            if i == 0:
                radio.setChecked(True)
            # 连接信号，当选择改变时自动更新参数
            # radio.toggled.connect(self.update_scan_params_main)
            self.scan_type_group.addButton(radio)
            scan_type_layout.addWidget(radio)
            
        # 添加到主布局
        layout.addLayout(scan_type_layout)
        
        # 第6行：极速模式区
        fast_mode_layout = QHBoxLayout()
        fast_mode_layout.setContentsMargins(0, 10, 0, 10)  # 设置上下边距
        
        # 创建并配置极速模式复选框
        self.fast_mode_checkbox = QCheckBox('Fast Mode - 加速扫描')
        self.fast_mode_checkbox.setStyleSheet("""
            QCheckBox {
                spacing: 12px;
                color: #00d9ff;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 217, 255, 0.15), stop:1 rgba(74, 158, 255, 0.15));
                border: 1px solid rgba(0, 217, 255, 0.3);
                border-radius: 8px;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #1a2332;
                border: 2px solid #2a4a6b;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00d9ff, stop:1 #4a9eff);
                border: 2px solid #00d9ff;
            }
            QCheckBox:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 217, 255, 0.25), stop:1 rgba(74, 158, 255, 0.25));
                border: 1px solid rgba(0, 217, 255, 0.5);
            }
        """)
        fast_mode_layout.addWidget(self.fast_mode_checkbox)
        
        # 添加到主布局
        layout.addLayout(fast_mode_layout)
        
        # 第7行：标签页区域
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #45475a;
                border-radius: 5px;
                background-color: #1e1e2e;
                padding: 5px;
            }
            QTabBar::tab {
                background-color: #313244;
                color: #cdd6f4;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 10px 15px;
                margin-right: 3px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #45475a;
                color: #89b4fa;
                border-bottom: 2px solid #89b4fa;
            }
            QTabBar::tab:hover:!selected {
                background-color: #45475a;
            }
        """)
        
        # 创建标签页
        tabs = ['扫描过程', '扫描结果', '资产监控', '资产对比', '使用帮助']
        tab_icons = [
            "\uf120",  # 终端图标代表扫描过程
            "\uf080",  # 图表图标代表扫描结果
            "\uf1b2",  # 立方体图标代表资产监控
            "\uf200",  # 对比图标代表资产对比
            "\uf059"   # 问号图标代表使用帮助
        ]
        
        # 初始化标签页内容
        for i, tab in enumerate(tabs):
            # 资产监控标签页需要特殊处理
            if tab == '资产监控':
                self.monitor_tab_widget = AssetMonitorTabWidget(self)
                self.tab_widget.addTab(self.monitor_tab_widget, tab)
                continue
            
            # 资产对比标签页需要特殊处理
            if tab == '资产对比':
                self.asset_comparison_widget = AssetComparisonWidget(self)
                self.tab_widget.addTab(self.asset_comparison_widget, tab)
                continue
                
            tab_edit = QTextEdit()
            tab_edit.setObjectName(tab)  # 设置对象名称
            
            # 对扫描结果标签页启用HTML支持
            if tab == '扫描结果':
                tab_edit.setAcceptRichText(True)
                tab_edit.document().setDefaultStyleSheet("""
                    .host-section { margin-bottom: 20px; }
                    .scan-results { width: 100%; }
                """)
            # 为扫描过程标签页启用HTML支持与自定义样式
            elif tab == '扫描过程':
                tab_edit.setAcceptRichText(True)
                tab_edit.setReadOnly(True)
                tab_edit.document().setDefaultStyleSheet("""
                    /* 扫描过程输出样式 */
                    .output-container { 
                        font-family: 'Consolas', 'Courier New', monospace; 
                        line-height: 1.5; 
                        padding: 5px;
                    }
                    .nmap-header { 
                        color: #89b4fa; 
                        font-weight: bold; 
                        font-size: 14px; 
                    }
                    .nmap-command { 
                        color: #cba6f7; 
                        font-weight: bold; 
                        background-color: #1e1e2e; 
                        border-radius: 3px; 
                        padding: 2px 5px; 
                    }
                    .nmap-progress { 
                        color: #a6e3a1; 
                        font-style: italic; 
                    }
                    .nmap-port { 
                        color: #f9e2af; 
                        font-weight: bold; 
                    }
                    .nmap-service { 
                        color: #74c7ec; 
                    }
                    .nmap-version { 
                        color: #fab387; 
                    }
                    .nmap-done { 
                        color: #a6e3a1; 
                        font-weight: bold; 
                        border-top: 1px solid #45475a; 
                        padding-top: 5px; 
                    }
                    .nmap-warning { 
                        color: #f9e2af; 
                        font-weight: bold; 
                    }
                    .nmap-error { 
                        color: #f38ba8; 
                        font-weight: bold; 
                        background-color: rgba(243, 139, 168, 0.1); 
                        border-radius: 3px; 
                        padding: 2px 5px; 
                    }
                    .nmap-timestamp { 
                        color: #7f849c; 
                        font-style: italic; 
                        font-size: 11px; 
                    }
                    .scan-divider {
                        border-top: 1px dashed #45475a;
                        margin: 10px 0;
                    }
                    .matrix-effect {
                        color: #a6e3a1;
                        font-family: 'Courier New', monospace;
                        letter-spacing: 2px;
                        animation: pulse 1.5s infinite;
                    }
                    
                    /* 文件路径和 IP 地址的样式 */
                    .file-path {
                        color: #f5c2e7;
                        font-style: italic;
                    }
                    .ip-address {
                        color: #74c7ec;
                        font-weight: bold;
                    }
                """)
            
            # 配置文本编辑器样式
            tab_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #1a2332;
                    color: #e0f4ff;
                    border: 2px solid #2a4a6b;
                    border-radius: 8px;
                    padding: 12px;
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 13px;
                    line-height: 1.6;
                }
                QTextEdit:focus {
                    border: 2px solid #4a9eff;
                    background-color: #1f2937;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #2a4a6b;
                    width: 12px;
                    margin: 0px;
                    border-radius: 6px;
                }
                QScrollBar::handle:vertical {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4a9eff, stop:1 #00d9ff);
                    min-height: 24px;
                    border-radius: 6px;
                    margin: 2px;
                }
                QScrollBar::handle:vertical:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5aa6ff, stop:1 #20e9ff);
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)
            
            # 添加到标签页和字典
            self.tab_widget.addTab(tab_edit, tab)
            self.text_edits[tab] = tab_edit
            
            # 如果是使用帮助标签页，创建专门的HTML帮助页面
            if tab == '使用帮助':
                # 移除之前创建的QTextEdit
                self.tab_widget.removeTab(self.tab_widget.count() - 1)
                
                # 创建滚动区域和QLabel来显示HTML内容
                from PyQt5.QtWidgets import QScrollArea
                from PyQt5.QtCore import QUrl
                from PyQt5.QtGui import QDesktopServices
                
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setStyleSheet("""
                    QScrollArea {
                        border: none;
                        background-color: #0a0e1a;
                    }
                """)
                
                help_label = QLabel()
                help_label.setWordWrap(True)
                help_label.setOpenExternalLinks(True)  # QLabel支持此属性
                help_label.setStyleSheet("""
                    QLabel {
                        background-color: #0a0e1a;
                        color: #e0f4ff;
                        padding: 20px;
                    }
                """)
                
                help_text = """
                <div style="padding: 20px; font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif; background-color: #0a0e1a; color: #e0f4ff;">
                
                <h1 style="color: #4a9eff; text-align: center; border-bottom: 2px solid #4a9eff; padding-bottom: 15px; margin-bottom: 30px;">
                    FastNmap - 专业网络安全扫描工具
                </h1>
                
                <div style="background: rgba(74, 158, 255, 0.1); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4a9eff;">
                    <h2 style="color: #4a9eff; margin-top: 0; margin-bottom: 15px;">基本操作流程</h2>
                    <ol style="line-height: 2; color: #e0f4ff; font-size: 14px;">
                        <li style="margin-bottom: 8px;">在顶部输入框中输入目标 IP 地址、域名或网段</li>
                        <li style="margin-bottom: 8px;">选择扫描类型，系统会自动推荐最优参数</li>
                        <li style="margin-bottom: 8px;">选择端口范围或使用预设端口组合</li>
                        <li style="margin-bottom: 8px;">调整扫描参数（可选，系统已智能配置）</li>
                        <li style="margin-bottom: 8px;">点击"开始"按钮启动扫描任务</li>
                    </ol>
                </div>

                <div style="background: rgba(16, 185, 129, 0.1); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10b981;">
                    <h2 style="color: #10b981; margin-top: 0; margin-bottom: 15px;">扫描类型详解</h2>
                    <table style="width: 100%; border-collapse: collapse; color: #e0f4ff; font-size: 14px;">
                        <tr style="background: rgba(74, 158, 255, 0.1);">
                            <td style="padding: 12px; border: 1px solid #334155; font-weight: bold; color: #4a9eff;">默认扫描</td>
                            <td style="padding: 12px; border: 1px solid #334155;">SYN半连接扫描，快速准确，推荐日常使用</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #334155; font-weight: bold; color: #10b981;">存活扫描</td>
                            <td style="padding: 12px; border: 1px solid #334155;">主机发现，快速检测网段内活跃主机</td>
                        </tr>
                        <tr style="background: rgba(74, 158, 255, 0.05);">
                            <td style="padding: 12px; border: 1px solid #334155; font-weight: bold; color: #f59e0b;">服务识别</td>
                            <td style="padding: 12px; border: 1px solid #334155;">深度检测端口服务类型和版本信息</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #334155; font-weight: bold; color: #f97316;">系统识别</td>
                            <td style="padding: 12px; border: 1px solid #334155;">操作系统指纹识别，了解目标系统</td>
                        </tr>
                        <tr style="background: rgba(74, 158, 255, 0.05);">
                            <td style="padding: 12px; border: 1px solid #334155; font-weight: bold; color: #8b5cf6;">端口识别</td>
                            <td style="padding: 12px; border: 1px solid #334155;">指定端口扫描，支持自定义端口范 格式 ip:port (127.0.0.1:80)</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px; border: 1px solid #334155; font-weight: bold; color: #ef4444;">暴力破解</td>
                            <td style="padding: 12px; border: 1px solid #334155;">内置字典攻击，检测弱密码服务</td>
                        </tr>
                        <tr style="background: rgba(74, 158, 255, 0.05);">
                            <td style="padding: 12px; border: 1px solid #334155; font-weight: bold; color: #06b6d4;">漏洞扫描</td>
                            <td style="padding: 12px; border: 1px solid #334155;">NSE脚本引擎，检测已知安全漏洞</td>
                        </tr>
                    </table>
                </div>

                <div style="background: rgba(251, 146, 60, 0.1); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #f59e0b;">
                    <h2 style="color: #f59e0b; margin-top: 0; margin-bottom: 15px;">智能功能特性</h2>
                    <ul style="line-height: 2; color: #e0f4ff; font-size: 14px; list-style-type: none; padding-left: 0;">
                        <li style="margin-bottom: 10px; padding-left: 20px; position: relative;">
                            <span style="position: absolute; left: 0; color: #4a9eff;">▶</span>
                            <strong style="color: #4a9eff;">智能参数推荐</strong>: 根据扫描类型自动配置最优参数
                        </li>
                        <li style="margin-bottom: 10px; padding-left: 20px; position: relative;">
                            <span style="position: absolute; left: 0; color: #10b981;">▶</span>
                            <strong style="color: #10b981;">端口预设组合</strong>: 内置常用端口组，快速选择扫描范围
                        </li>
                        <li style="margin-bottom: 10px; padding-left: 20px; position: relative;">
                            <span style="position: absolute; left: 0; color: #f59e0b;">▶</span>
                            <strong style="color: #f59e0b;">实时扫描监控</strong>: 查看扫描进度和实时输出信息
                        </li>
                        <li style="margin-bottom: 10px; padding-left: 20px; position: relative;">
                            <span style="position: absolute; left: 0; color: #8b5cf6;">▶</span>
                            <strong style="color: #8b5cf6;">多格式结果导出</strong>: 支持CSV、TXT等多种格式导出
                        </li>
                        <li style="margin-bottom: 10px; padding-left: 20px; position: relative;">
                            <span style="position: absolute; left: 0; color: #ef4444;">▶</span>
                            <strong style="color: #ef4444;">扫描配置保存</strong>: 常用配置一键保存和加载
                        </li>
                    </ul>
                </div>

                <div style="background: rgba(139, 92, 246, 0.1); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #8b5cf6;">
                    <h2 style="color: #8b5cf6; margin-top: 0; margin-bottom: 15px;">资产监控系统</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; color: #e0f4ff; font-size: 14px;">
                        <div style="background: rgba(74, 158, 255, 0.1); padding: 15px; border-radius: 6px;">
                            <h4 style="color: #4a9eff; margin: 0 0 10px 0;">定时监控</h4>
                            <p style="margin: 0; line-height: 1.6;">设置监控间隔，自动定期扫描目标资产</p>
                        </div>
                        <div style="background: rgba(16, 185, 129, 0.1); padding: 15px; border-radius: 6px;">
                            <h4 style="color: #10b981; margin: 0 0 10px 0;">变化检测</h4>
                            <p style="margin: 0; line-height: 1.6;">智能对比扫描结果，发现新增或变化的资产</p>
                        </div>
                        <div style="background: rgba(251, 146, 60, 0.1); padding: 15px; border-radius: 6px;">
                            <h4 style="color: #f59e0b; margin: 0 0 10px 0;">可视化对比</h4>
                            <p style="margin: 0; line-height: 1.6;">直观展示资产变化趋势和统计信息</p>
                        </div>
                        <div style="background: rgba(139, 92, 246, 0.1); padding: 15px; border-radius: 6px;">
                            <h4 style="color: #8b5cf6; margin: 0 0 10px 0;">HTML报告</h4>
                            <p style="margin: 0; line-height: 1.6;">自动生成专业的资产监控分析报告</p>
                        </div>
                    </div>
                </div>

                <div style="background: rgba(74, 158, 255, 0.1); padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4a9eff;">
                    <h2 style="color: #4a9eff; margin-top: 0; margin-bottom: 15px;">使用技巧</h2>
                    <div style="color: #e0f4ff; font-size: 14px; line-height: 1.8;">
                        <p style="margin-bottom: 12px;"><strong style="color: #10b981;">网段扫描:</strong> 使用网段扫描（如192.168.1.0/24）可快速发现网络内主机</p>
                        <p style="margin-bottom: 12px;"><strong style="color: #f59e0b;">详细输出:</strong> 附加参数中添加-vvv可查看详细的扫描过程信息</p>
                        <p style="margin-bottom: 12px;"><strong style="color: #8b5cf6;">分步扫描:</strong> 大范围扫描建议先用存活扫描确定目标，再进行详细扫描</p>
                        <p style="margin-bottom: 12px;"><strong style="color: #ef4444;">安全提醒:</strong> 暴力破解功能请仅在授权环境下使用</p>
                    </div>
                </div>

                <div style="text-align: center; margin: 30px 0; padding: 25px; 
                           background: linear-gradient(135deg, rgba(74, 158, 255, 0.1), rgba(139, 92, 246, 0.1));
                           border-radius: 8px; border: 1px solid #334155;">
                    <h2 style="color: #4a9eff; margin-bottom: 15px;">开源项目支持</h2>
                    <p style="margin: 15px 0; color: #94a3b8; font-size: 14px;">FastNmap 是一个开源项目，欢迎贡献代码和反馈问题</p>
                    <div style="margin: 20px 0;">
                        <a href="https://github.com/vam876/FastNmap" 
                           style="display: inline-block; padding: 15px 30px; 
                                  background: linear-gradient(135deg, #4a9eff, #8b5cf6); 
                                  color: white; text-decoration: none; border-radius: 8px; 
                                  font-weight: bold; font-size: 16px; transition: all 0.3s ease;">
                            点击访问 GitHub 仓库
                        </a>
                    </div>
                    <p style="margin: 15px 0 0 0; font-size: 13px; color: #6b7280;">
                        <span style="color: #f59e0b;">★</span> Star 支持项目发展 | 
                        <span style="color: #ef4444;">⚠</span> Issue 反馈问题和建议
                    </p>
                </div>

                <div style="text-align: center; margin-top: 30px; padding: 20px; 
                           background: rgba(107, 114, 128, 0.1); border-radius: 8px; border-top: 2px solid #4a9eff;">
                    <p style="margin: 0; color: #94a3b8; font-size: 13px;">
                        <strong style="color: #4a9eff;">FastNmap v0.2.0</strong> | 
                        <span style="color: #10b981;">程序依赖Nmap运行</span> | 
                        <span style="color: #ef4444; font-weight: bold;">请在授权环境下使用本工具</span>
                    </p>
                </div>
                
                </div>
                """
                
                help_label.setText(help_text)
                scroll_area.setWidget(help_label)
                
                # 将滚动区域添加到标签页
                self.tab_widget.addTab(scroll_area, tab)
                self.text_edits[tab] = help_label  # 保存引用
            
        # 添加标签页到主布局
        layout.addWidget(self.tab_widget)
        
        # 添加状态栏
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a2332, stop:1 #0f1419);
                color: #e0f4ff;
                border-top: 2px solid #2a4a6b;
                padding: 6px;
                font-weight: 500;
            }
        """)
        layout.addWidget(self.status_bar)
        
        # 添加进度条到状态栏
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #2a4a6b;
                border-radius: 6px;
                background-color: #0a0e1a;
                text-align: center;
                color: #e0f4ff;
                font-weight: bold;
                height: 20px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a9eff, stop:1 #00d9ff);
                border-radius: 4px;
                margin: 1px;
            }
        """)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 添加状态标签
        self.status_label = QLabel("就绪 | 准备就绪")
        self.status_bar.addWidget(self.status_label)
        
        # 设置主窗口属性
        self.setLayout(layout)
        self.setWindowTitle('FastNmap v0.2.0 - Nmap图形化扫描工具')
        self.setGeometry(300, 300, 1000, 700)  # 增大窗口尺寸
        self.show()

    def load_file(self):
        """
        加载文件功能
        
        打开文件选择对话框，允许用户选择包含扫描目标的文件。
        选择文件后，文件路径将被设置到目标输入框中。
        """
        # 打开文件选择对话框
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            '选择目标文件', 
            '', 
            'Text Files (*.txt);;All Files (*)'
        )
        # 如果用户选择了文件，将文件路径设置到输入框
        if filename:
            self.url_line_edit.setText(filename)

    def select_result_file(self):
        """
        选择结果文件保存路径
        
        打开文件保存对话框，允许用户选择扫描结果的保存位置和格式。
        支持多种文件格式，包括文本、JSON和XML。
        """
        # 打开文件保存对话框
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            '保存扫描结果', 
            '', 
            'Text Files (*.txt);;JSON Files (*.json);;XML Files (*.xml);;All Files (*)'
        )
        # 如果用户选择了保存路径，将路径设置到结果文件输入框
        if filename:
            self.result_file_edit.setText(filename)

    def on_port_checkbox_changed(self):
        """处理端口复选框状态变化"""
        any_checked = any(checkbox.isChecked() for checkbox in self.port_checkboxes)
        if any_checked:
            self.port_input.setDisabled(True)
        else:
            self.port_input.setEnabled(True)

    def perform_action(self):
        """执行按钮动作"""
        action = self.sender().text()
        if action == '开始扫描':
            self.start_scan()
        elif action == '停止扫描':
            self.stop_scan()
        elif action == '清空文本':
            self.clear_text()
        elif action == '导出扫描过程':
            self.export_scan_process()
        elif action == '导出扫描结果':
            self.export_scan_results()

    def export_scan_process(self):
        """导出扫描过程"""
        self.export_data()
    
    def export_scan_results(self):
        """导出扫描结果"""
        self.export_result_csv()
    
    def create_help_mouse_handler(self, text_edit):
        """创建帮助页面的鼠标点击处理器"""
        def mouse_press_handler(event):
            # 获取点击位置的文本
            cursor = text_edit.cursorForPosition(event.pos())
            cursor.select(cursor.WordUnderCursor)
            selected_text = cursor.selectedText()
            
            # 检查是否点击了GitHub链接
            if "github.com/vam876/FastNmap" in text_edit.toPlainText():
                # 如果在链接区域附近点击，打开链接
                from PyQt5.QtCore import QUrl
                from PyQt5.QtGui import QDesktopServices
                if event.button() == 1:  # 左键点击
                    # 检查点击位置是否在链接文本附近
                    full_text = text_edit.toPlainText()
                    cursor_pos = cursor.position()
                    text_around = full_text[max(0, cursor_pos-50):cursor_pos+50]
                    
                    if any(keyword in text_around.lower() for keyword in ['github', '访问', '仓库', '项目']):
                        QDesktopServices.openUrl(QUrl("https://github.com/vam876/FastNmap"))
                        return
            
            # 默认处理
            QTextEdit.mousePressEvent(text_edit, event)
        
        return mouse_press_handler
    
    # 移除了toggle_theme方法，应用固定的深色主题样式
    
    def update_status(self):
        """
        更新状态栏信息
        
        定期更新状态栏信息，显示当前扫描状态和进度。
        减少不必要的UI更新，提高性能。
        """
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        
        if self.is_scanning and hasattr(self, "scan_active") and self.scan_active:
            # 只在实际扫描执行中才更新进度
            if self.scan_progress < 95:  # 最高只显示到95%，留出5%给最终完成时使用
                self.scan_progress += 1
                self.progress_bar.setValue(self.scan_progress)
            
            # 更新状态标签 - 每5秒完整更新一次，减少UI更新频率
            if hasattr(self, "last_status_update"):
                if (QDateTime.currentDateTime().toMSecsSinceEpoch() - self.last_status_update) > 5000:
                    scan_type = self.scan_type_group.checkedButton().text() if self.scan_type_group.checkedButton() else "未知"
                    target = self.url_line_edit.text()
                    self.status_label.setText(f"扫描中 | 类型: {scan_type} | 目标: {target} | 进度: {self.scan_progress}% | {current_time}")
                    self.last_status_update = QDateTime.currentDateTime().toMSecsSinceEpoch()
            else:
                self.last_status_update = QDateTime.currentDateTime().toMSecsSinceEpoch()
                scan_type = self.scan_type_group.checkedButton().text() if self.scan_type_group.checkedButton() else "未知"
                target = self.url_line_edit.text()
                self.status_label.setText(f"扫描中 | 类型: {scan_type} | 目标: {target} | 进度: {self.scan_progress}% | {current_time}")
        else:
            # 非扫描状态，只更新时间
            self.status_label.setText(f"就绪 | {current_time}")
    
    def save_config(self):
        """
        保存当前扫描配置
        
        将当前的扫描配置保存为命名配置，便于以后使用。
        """
        config_name, ok = QInputDialog.getText(self, '保存配置', '请输入配置名称:')
        if ok and config_name:
            # 收集当前配置
            config = {
                'target': self.url_line_edit.text(),
                'timeout': self.timeout_input.text(),
                'threads': self.threads_input.text(),
                'scan_type_index': self.scan_type_group.checkedId(),
                'fast_mode': self.fast_mode_checkbox.isChecked(),
                'port_input': self.port_input.text(),
                'port_checkboxes': [cb.isChecked() for cb in self.port_checkboxes],
                'params': self.params_input.text(),
                'result_file': self.result_file_edit.text()
            }
            
            # 保存配置
            self.scan_configs[config_name] = config
            QMessageBox.information(self, '成功', f'配置 "{config_name}" 已保存')
            
            # 更新菜单
            self.update_config_menu()
    
    def load_config(self, config_name):
        """
        加载保存的扫描配置
        
        从保存的配置中加载指定的配置，并应用到界面上。
        
        参数:
            config_name: 配置名称
        """
        if config_name in self.scan_configs:
            config = self.scan_configs[config_name]
            
            # 应用配置
            self.url_line_edit.setText(config['target'])
            self.timeout_input.setText(config['timeout'])
            self.threads_input.setText(config['threads'])
            
            # 设置扫描类型
            button = self.scan_type_group.button(config['scan_type_index'])
            if button:
                button.setChecked(True)
                
            # 设置极速模式
            self.fast_mode_checkbox.setChecked(config['fast_mode'])
            
            # 设置端口
            self.port_input.setText(config['port_input'])
            
            # 设置端口复选框
            for i, checked in enumerate(config['port_checkboxes']):
                if i < len(self.port_checkboxes):
                    self.port_checkboxes[i].setChecked(checked)
            
            # 设置其他参数
            self.params_input.setText(config['params'])
            self.result_file_edit.setText(config['result_file'])
            
            QMessageBox.information(self, '成功', f'配置 "{config_name}" 已加载')
    
    def update_config_menu(self):
        """
        更新配置菜单
        
        根据当前保存的配置更新菜单项。
        """
        # 如果菜单不存在，创建它
        if not hasattr(self, 'config_menu'):
            self.config_menu = QMenu(self)
            self.config_button = QToolButton()
            self.config_button.setText('配置')
            self.config_button.setMenu(self.config_menu)
            self.config_button.setPopupMode(QToolButton.InstantPopup)
            self.status_bar.addPermanentWidget(self.config_button)
            
            # 添加保存配置选项
            save_action = QAction('保存当前配置', self)
            save_action.triggered.connect(self.save_config)
            self.config_menu.addAction(save_action)
            self.config_menu.addSeparator()
        
        # 清除现有的配置项
        for action in self.config_menu.actions():
            if action.text() != '保存当前配置' and not action.isSeparator():
                self.config_menu.removeAction(action)
        
        # 添加保存的配置
        for config_name in self.scan_configs.keys():
            action = QAction(config_name, self)
            action.triggered.connect(lambda checked, name=config_name: self.load_config(name))
            self.config_menu.addAction(action)
    
    def update_scan_params_main(self):
        """根据扫描类型更新主界面的默认参数"""
        if not hasattr(self, 'scan_type_group') or not self.scan_type_group.checkedButton():
            return
        
        scan_type = self.scan_type_group.checkedButton().text()
        
        # 定义不同扫描类型的默认参数
        default_params = {
            '默认扫描': '-vvv -T4 -sS --open',
            '存活扫描': '-vvv -T4 -sn',
            '服务识别': '-vvv -sV --open',
            '系统识别': '-vvv -O',
            '端口识别': '-vvv -sS -sV --open',
            '暴力破解': '-vvv -T4 --script brute',
            '漏洞扫描': '-vvv --script vuln'
        }
        
        # 获取默认参数
        params = default_params.get(scan_type, '-vvv -T4 --open')
        
        # 如果用户没有修改过参数，则自动更新
        current_text = self.params_input.text()
        if not current_text or current_text in default_params.values():
            self.params_input.setText(params)
        
        # 更新占位符提示
        self.params_input.setPlaceholderText(params)
    
    def start_scan(self):
        """
        开始扫描
        
        验证输入，构建扫描命令，并启动扫描线程。
        同时更新UI状态和进度指示。
        """
        if not self.url_line_edit.text():
            QMessageBox.warning(self, "警告", "请输入目标地址")
            return
            
        # 检查是否选择了扫描类型
        if not self.scan_type_group.checkedButton():
            QMessageBox.warning(self, "警告", "请选择扫描类型")
            return
            
        selected_scan_type = self.scan_type_group.checkedButton().text()
        if selected_scan_type not in ['存活扫描', '系统识别', '端口识别']:
            # 检查端口输入框是否为空，以及是否勾选了端口选项
            port_text = self.port_input.text()
            if not port_text and not any(checkbox.isChecked() for checkbox in self.port_checkboxes):
                QMessageBox.warning(self, "警告", "请输入端口或勾选端口选项")
                return
                
        # 构建命令
        config = {
            'target': self.url_line_edit.text(),
            'timeout': self.timeout_input.text(),
            'threads_min': self.threads_input.text(),
            'threads_max': self.threads_input.text(),
            'params': self.params_input.text(),
            'result_file': self.result_file_edit.text(),
            'scan_type': selected_scan_type,
            'fast_mode': self.fast_mode_checkbox.isChecked(),
            'port_input': self.port_input.text(),
            'port_checkboxes': self.port_checkboxes
        }
        
        command = NmapCommandBuilder.build_command(config)
        if command:
            # 重置扫描状态
            self.is_scanning = True
            self.scan_active = False  # 初始化为非活动状态，等待第一个输出后才置为True
            self.scan_progress = 0
            self.progress_bar.setValue(0)
            self.status_label.setText(f"开始扫描 | 类型: {selected_scan_type} | 目标: {self.url_line_edit.text()}")
            
            # 启动扫描线程
            self.thread = NmapThread(command)
            self.thread.output_signal.connect(self.live_output)
            self.thread.error_signal.connect(self.handle_error)
            self.thread.start()
            self.clear_current_output()  # 清空缓存变量

    def process_web_scan_input(self, input_text):
        """处理Web扫描输入"""
        # 分割输入的多个ip:port对
        targets = input_text.split(',')
        target_list = []
        for target in targets:
            try:
                ip, port = target.split(':')
                target_list.append((ip.strip(), port.strip()))
            except ValueError:
                QMessageBox.warning(self, "错误", "输入格式必须为 ip:port，多个请用逗号分隔")
                return None
        return target_list

    def update_output_text(self, output):
        """以现代化网络安全风格更新扫描输出文本"""
        output_text_edit = self.text_edits.get('扫描过程')
        if not output_text_edit:
            return
            
        # 输出类型正则表达式
        import re
        # 命令和参数
        cmd_pattern = re.compile(r'(nmap\s+[\w\-\./\s]+)')
        # 进度条
        progress_pattern = re.compile(r'(\d+\.\d+%\s+\w+)')
        # 端口信息
        port_pattern = re.compile(r'(\d+\/\w+)\s+(\w+)\s+(\w+)')
        # IP地址
        ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        # 文件路径
        file_pattern = re.compile(r'(/[\w\-\./]+)')
        # 扫描完成
        scan_done_pattern = re.compile(r'(Nmap\s+done:.*)')
        # 错误信息
        error_pattern = re.compile(r'(\[(ERROR|\!)\].*|\berror\b|\bfailed\b|\bQUITTING\b)', re.IGNORECASE)
        # 警告信息
        warning_pattern = re.compile(r'(\[WARNING\].*|\bwarning\b)', re.IGNORECASE)
        
        # 添加时间戳
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 格式化输出
        formatted_output = output
        
        # 处理Nmap启动信息
        if "Starting Nmap" in output:
            formatted_output = f'<div class="output-container"><span class="nmap-header">[扫描开始]</span> <span class="nmap-timestamp">{timestamp}</span><br>'
            # 提取并高亮显示命令
            cmd_match = cmd_pattern.search(output)
            if cmd_match:
                cmd = cmd_match.group(1)
                formatted_output += f'<span class="nmap-command">{cmd}</span><br>'
            formatted_output += output + "</div>"
        
        # 处理扫描完成信息
        elif scan_done_pattern.search(output):
            formatted_output = f'<div class="nmap-done">[扫描完成] <span class="nmap-timestamp">{timestamp}</span><br>'
            formatted_output += re.sub(scan_done_pattern, r'<span class="nmap-done">\1</span>', output)
            formatted_output += "</div>"
            # 添加分隔线
            formatted_output += '<div class="scan-divider"></div>'
            
        # 处理错误信息
        elif error_pattern.search(output):
            formatted_output = f'<div class="nmap-error">[错误] <span class="nmap-timestamp">{timestamp}</span><br>'
            formatted_output += re.sub(error_pattern, r'<span class="nmap-error">\1</span>', output)
            formatted_output += "</div>"
        
        # 处理警告信息
        elif warning_pattern.search(output):
            formatted_output = f'<div class="nmap-warning">[警告] <span class="nmap-timestamp">{timestamp}</span><br>'
            formatted_output += re.sub(warning_pattern, r'<span class="nmap-warning">\1</span>', output)
            formatted_output += "</div>"
        
        # 处理端口信息
        elif port_pattern.search(output):
            formatted_output = '<div class="output-container">'
            # 高亮显示端口信息
            formatted_output += re.sub(port_pattern, r'<span class="nmap-port">\1</span> <span class="nmap-state">\2</span> <span class="nmap-service">\3</span>', output)
            formatted_output += "</div>"
        
        # 处理扫描进度
        elif progress_pattern.search(output):
            formatted_output = '<div class="nmap-progress">'
            formatted_output += re.sub(progress_pattern, r'<span class="matrix-effect">\1</span>', output)
            formatted_output += "</div>"
        
        # 处理IP地址
        elif ip_pattern.search(output):
            formatted_output = '<div class="output-container">'
            formatted_output += re.sub(ip_pattern, r'<span class="ip-address">\g<0></span>', output)
            formatted_output += "</div>"
        
        # 其他普通输出添加基本样式
        else:
            formatted_output = f'<div class="output-container">{output}</div>'
        
        # 将格式化输出添加到文本编辑器
        output_text_edit.insertHtml(formatted_output + "<br>")

    def stop_scan(self):
        """
        停止扫描
        
        终止正在运行的扫描线程，并更新UI状态。
        """
        if self.thread and self.thread.isRunning():
            self.thread.terminate()
            
            # 更新扫描状态
            self.is_scanning = False
            self.status_label.setText("已停止 | 扫描被用户终止")
            self.progress_bar.setValue(0)
            
            # 在扫描过程文本框中添加停止信息
            output_text_edit = self.text_edits.get('扫描过程')
            if output_text_edit:
                from datetime import datetime
                timestamp = datetime.now().strftime("%H:%M:%S")
                stop_html = f'''
                <div class="nmap-error">
                    <span class="nmap-timestamp">{timestamp}</span> 
                    [!] 扫描被用户终止
                </div>
                <div class="scan-divider"></div>
                '''
                output_text_edit.insertHtml(stop_html)

    def handle_error(self, has_error):
        """
        处理错误信号
        
        当nmap执行出错时停止进度条更新并更新UI状态
        
        参数:
            has_error: 是否发生错误
        """
        if has_error:
            self.is_scanning = False  # 设置扫描状态为非扫描中
            self.scan_active = False  # 确保进度条停止更新
            self.status_label.setText("错误 | nmap执行失败")
            self.progress_bar.setValue(0)  # 重置进度条
    
    def clear_text(self):
        """清空文本"""
        output_text_edit = self.text_edits.get('扫描过程')
        if output_text_edit:
            output_text_edit.clear()

    def export_data(self):
        """导出扫描过程文本数据"""
        # 获取扫描过程的QTextEdit控件
        text_edit_to_export = self.text_edits.get('扫描过程')
        
        if text_edit_to_export is None:
            QMessageBox.warning(self, '错误', '未找到对应的文本编辑框。')
            return
        
        # 获取要导出的文本框内容
        text_to_export = text_edit_to_export.toPlainText()
        filename, _ = QFileDialog.getSaveFileName(self, '导出扫描过程', '', 'Text Files (*.txt);;All Files (*)')

        # 如果用户选择了文件路径，则保存文件
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(text_to_export)
                QMessageBox.information(self, '成功', '扫描过程已成功导出到文件。')
            except Exception as e:
                QMessageBox.warning(self, '错误', f'导出数据时发生错误：{str(e)}')
    
    def export_result_csv(self):
        """导出扫描结果为CSV格式"""
        # 获取扫描结果的QTextEdit控件
        text_edit_to_export = self.text_edits.get('扫描结果')
        
        if text_edit_to_export is None:
            QMessageBox.warning(self, '错误', '未找到扫描结果编辑框。')
            return
        
        # 获取当前选中的扫描类型
        selected_scan_type = self.scan_type_group.checkedButton().text() if self.scan_type_group.checkedButton() else "未知"
        
        try:
            # 获取当前XML结果文件
            output_filename = f"{selected_scan_type}_ScanCacheLog.xml"
            output_file_path = os.path.join('logs', output_filename)
            
            if not os.path.exists(output_file_path):
                QMessageBox.warning(self, '错误', '扫描结果文件不存在，请先进行扫描。')
                return
            
            # 解析XML获取结果
            tree = ET.parse(output_file_path)
            root = tree.getroot()
            
            # 根据扫描类型准备CSV数据
            csv_data = []
            
            # CSV表头和数据准备
            if selected_scan_type == '默认扫描':
                # 默认扫描 - 端口、状态、服务
                header = ['IP', '端口', '状态', '服务']
                for host in root.findall('.//host'):
                    ip = host.find('address').get('addr')
                    for port in host.findall('.//port'):
                        port_id = port.get('portid')
                        state = port.find('state').get('state')
                        service = port.find('service')
                        service_name = service.get('name') if service is not None else '未知服务'
                        csv_data.append([ip, port_id, state, service_name])
            
            elif selected_scan_type == '存活扫描':
                # 存活扫描 - IP和状态
                header = ['IP', '状态', '响应方式', 'TTL值']
                for host in root.findall('.//host'):
                    ip = host.find('address').get('addr')
                    status = host.find('status')
                    state = status.get('state') if status is not None else '未知'
                    reason = status.get('reason') if status is not None else '未知'
                    ttl = status.get('reason_ttl') if status is not None else '未知'
                    csv_data.append([ip, state, reason, ttl])
            
            elif selected_scan_type == '服务识别' or selected_scan_type == '端口识别':
                # 服务识别和端口识别 - 详细服务信息
                header = ['IP', '端口', '状态', '服务', '产品', '版本', '操作系统']
                for host in root.findall('.//host'):
                    ip = host.find('address').get('addr')
                    for port in host.findall('.//port'):
                        port_id = port.get('portid')
                        state = port.find('state').get('state')
                        service = port.find('service')
                        service_name = service.get('name') if service is not None else '未知服务'
                        product = service.get('product') if service is not None and 'product' in service.attrib else '未知产品'
                        version = service.get('version') if service is not None and 'version' in service.attrib else '未知版本'
                        os_type = service.get('ostype') if service is not None and 'ostype' in service.attrib else '未知系统'
                        csv_data.append([ip, port_id, state, service_name, product, version, os_type])
            
            elif selected_scan_type == '系统识别':
                # 系统识别 - 操作系统信息
                header = ['IP', '操作系统', '准确度', '类型']
                for host in root.findall('.//host'):
                    ip = host.find('address').get('addr')
                    os_elem = host.find('.//os')
                    if os_elem is not None:
                        for os_match in os_elem.findall('.//osmatch'):
                            name = os_match.get('name')
                            accuracy = os_match.get('accuracy')
                            os_class = os_match.find('.//osclass')
                            os_type = os_class.get('type') if os_class is not None else '未知'
                            csv_data.append([ip, name, accuracy, os_type])
                    else:
                        csv_data.append([ip, '未识别', '0', '未知'])
            
            elif selected_scan_type == '暴力破解':
                header = ['IP', '端口', '服务', '脚本', '结果']
                for host in root.findall('.//host'):
                    ip = host.find('address').get('addr')
                    for port in host.findall('.//port'):
                        port_id = port.get('portid')
                        service = port.find('service')
                        service_name = service.get('name') if service is not None else '未知服务'
                        
                        for script in port.findall('.//script'):
                            script_id = script.get('id')
                            output = script.get('output')
                            
                            # 检查是否有table元素（通常包含有效凭据）
                            accounts_table = script.find('.//table[@key="Accounts"]')
                            if accounts_table is not None:
                                # 有账户表，提取账户信息
                                for account in accounts_table.findall('.//table'):
                                    username = account.find('./elem[@key="username"]')
                                    password = account.find('./elem[@key="password"]')
                                    state = account.find('./elem[@key="state"]')
                                    if username is not None and password is not None:
                                        result = f"{username.text}:{password.text} - {state.text if state is not None else 'Valid'}"
                                        csv_data.append([ip, port_id, service_name, script_id, result])
                            elif output:
                                # 处理普通输出
                                output_clean = output.replace('\n', ' ').strip()
                                if output_clean:
                                    csv_data.append([ip, port_id, service_name, script_id, output_clean])
            
            elif selected_scan_type == '漏洞扫描':
                header = ['IP', '端口', '漏洞名称', '风险级别', '详细信息']
                for host in root.findall('.//host'):
                    ip = host.find('address').get('addr')
                    
                    # 检查端口上的漏洞
                    for port in host.findall('.//port'):
                        port_id = port.get('portid')
                        
                        for script in port.findall('.//script'):
                            if 'vulns' in script.get('id', ''):
                                script_id = script.get('id')
                                output = script.get('output')
                                output_clean = output.replace('\n', ' ').strip() if output else ""
                                
                                # 确定风险级别
                                risk_level = '中危'
                                if output and ('HIGH' in output or 'CRITICAL' in output):
                                    risk_level = '高危'
                                elif output and 'LOW' in output:
                                    risk_level = '低危'
                                    
                                csv_data.append([ip, port_id, script_id, risk_level, output_clean])
                    
                    # 检查主机级别的漏洞
                    for vuln in host.findall('.//vuln'):
                        vuln_name = vuln.get('name', '未知漏洞')
                        vuln_info = vuln.get('info', '无详细信息')
                        
                        # 确定风险级别
                        risk_level = '中危'
                        vuln_text = (vuln_name + vuln_info).lower()
                        if 'critical' in vuln_text or 'high' in vuln_text:
                            risk_level = '高危'
                        elif 'low' in vuln_text:
                            risk_level = '低危'
                            
                        csv_data.append([ip, 'N/A', vuln_name, risk_level, vuln_info])
            
            else:
                # 默认情况
                header = ['IP', '端口', '状态', '服务']
                for host in root.findall('.//host'):
                    ip = host.find('address').get('addr')
                    for port in host.findall('.//port'):
                        port_id = port.get('portid')
                        state = port.find('state').get('state')
                        service = port.find('service')
                        service_name = service.get('name') if service is not None else '未知服务'
                        csv_data.append([ip, port_id, state, service_name])
            
            # 导出为CSV文件
            filename, _ = QFileDialog.getSaveFileName(self, f'导出{selected_scan_type}结果', '', 'CSV Files (*.csv);;All Files (*)')
            
            if filename:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(header)  # 写入表头
                    csv_writer.writerows(csv_data)  # 写入数据
                QMessageBox.information(self, '成功', f'{selected_scan_type}结果已成功导出为CSV格式。')
        
        except Exception as e:
            QMessageBox.warning(self, '错误', f'导出CSV数据时发生错误：{str(e)}')

    def clear_current_output(self):
        """清空当前输出缓存"""
        self.current_output = ""

    def live_output(self, process_output):
        """处理实时输出"""
        full_output = "".join(process_output).strip()
        self.update_output_text(full_output)  # 实时显示输出
        self.current_output += full_output + "\n"  # 将实时输出添加到缓存变量
        
        # 如果收到有效输出且没有错误消息，则认为扫描已经实际启动
        if not hasattr(self, "scan_active") or not self.scan_active:
            # 检查是否收到nmap实际运行的输出
            valid_nmap_outputs = [
                "Starting Nmap", 
                "Scanning",
                "Initiating", 
                "PORT"
            ]
            
            # 检查是否是错误消息
            error_indicators = [
                "错误", 
                "error",
                "QUITTING",
                "failed", 
                "Sorry"
            ]
            
            if any(indicator in full_output for indicator in valid_nmap_outputs) and \
               not any(error in full_output.lower() for error in error_indicators):
                self.scan_active = True

        # 检查是否完成扫描
        if "Nmap done" in full_output:
            self.parse_nmap_output()  # 解析输出
            self.current_output = ""  # 清空缓存变量
            self.scan_active = False  # 扫描结束，重置标志

    def parse_nmap_output(self):
        """
        解析Nmap输出
        
        解析Nmap扫描完成后的XML输出文件，并将结果显示在结果标签页中。
        同时更新扫描状态和进度。
        """
        selected_scan_type = self.scan_type_group.checkedButton().text()
        result_text, error = NmapOutputParser.parse_nmap_output(selected_scan_type, logs_dir='logs', html_format=True)
        
        if error:
            QMessageBox.warning(self, "错误", error)
            self.status_label.setText(f"错误 | {error}")
        elif result_text:
            # 判断是否是HTML格式
            if result_text.strip().startswith('<'):
                self.text_edits['扫描结果'].setHtml(result_text)  # 使用setHtml显示HTML内容
            else:
                self.text_edits['扫描结果'].setText(result_text)  # 普通文本使用setText
            
            # 将HTML标签删除后再保存到历史记录
            plain_text = result_text
            if result_text.strip().startswith('<'):
                # 简单处理来移除HTML标签，实际项目中应该使用正则表达式或HTML解析器
                plain_text = "扫描结果已以现代化风格显示"
            
            # 添加到扫描历史
            scan_info = {
                'timestamp': QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss'),
                'target': self.url_line_edit.text(),
                'scan_type': selected_scan_type,
                'result': plain_text[:100] + '...' if len(plain_text) > 100 else plain_text
            }
            self.scan_history.append(scan_info)
            
            # 更新状态
            self.is_scanning = False
            self.status_label.setText(f"完成 | 扫描完成: {selected_scan_type}")
            self.progress_bar.setValue(100)



    def add_monitor_target(self):
        """添加监控目标"""
        config_widget = self.monitor_tab_widget.get_config_widget()
        
        name = config_widget.monitor_name_input.text().strip()
        target = config_widget.target_combo.currentText().strip()
        
        if not name or not target:
            QMessageBox.warning(self, "警告", "请填写监控名称和目标")
            return
        
        # 检查名称是否重复
        if name in self.asset_monitor.get_monitor_targets():
            QMessageBox.warning(self, "警告", "监控名称已存在，请使用不同的名称")
            return
        
        config = {
            'target': target,
            'scan_type': config_widget.scan_type_combo.currentText(),
            'interval_minutes': config_widget.interval_spin.value(),
            'ports': config_widget.ports_combo.currentText().strip(),
            'params': config_widget.params_input.text().strip()
        }
        
        if self.asset_monitor.add_monitor_target(name, config):
            # 启动监控
            if self.asset_monitor.start_monitoring(name):
                QMessageBox.information(self, "成功", f"已添加并启动监控: {name}")
                self.refresh_monitor_targets()
                # 清空输入框
                config_widget.monitor_name_input.clear()
                config_widget.target_combo.setCurrentText("")
            else:
                QMessageBox.warning(self, "警告", f"添加成功但启动监控失败: {name}")
        else:
            QMessageBox.warning(self, "错误", "添加监控目标失败")

    def remove_monitor_target(self):
        """删除选中的监控目标"""
        targets_widget = self.monitor_tab_widget.get_targets_widget()
        current_row = targets_widget.targets_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请选择要删除的监控目标")
            return
        
        target_name = targets_widget.targets_table.item(current_row, 0).text()
        
        reply = QMessageBox.question(self, "确认", 
                                   f"确定要删除监控目标 '{target_name}' 吗？\n这将删除所有相关的历史数据。",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.asset_monitor.delete_monitor_target(target_name):
                QMessageBox.information(self, "成功", f"已删除监控目标: {target_name}")
                self.refresh_monitor_targets()
            else:
                QMessageBox.warning(self, "错误", "删除监控目标失败")

    def refresh_monitor_targets(self):
        """刷新监控目标列表"""
        targets_widget = self.monitor_tab_widget.get_targets_widget()
        targets = self.asset_monitor.get_monitor_targets()
        targets_widget.targets_table.setRowCount(len(targets))
        
        row = 0
        for name, config in targets.items():
            targets_widget.targets_table.setItem(row, 0, QTableWidgetItem(name))
            targets_widget.targets_table.setItem(row, 1, QTableWidgetItem(config.get('target', '')))
            targets_widget.targets_table.setItem(row, 2, QTableWidgetItem(config.get('scan_type', '')))
            targets_widget.targets_table.setItem(row, 3, QTableWidgetItem(str(config.get('interval_minutes', ''))))
            
            # 格式化最后扫描时间
            last_scan = config.get('last_scan_time', '')
            if last_scan:
                try:
                    dt = datetime.fromisoformat(last_scan)
                    formatted_time = dt.strftime('%m-%d %H:%M')
                except:
                    formatted_time = '解析错误'
            else:
                formatted_time = '未扫描'
            targets_widget.targets_table.setItem(row, 4, QTableWidgetItem(formatted_time))
            
            # 状态
            status = "运行中" if name in self.asset_monitor.active_timers else "已停止"
            status_item = QTableWidgetItem(status)
            if status == "运行中":
                status_item.setBackground(QColor("#059669"))
            else:
                status_item.setBackground(QColor("#dc2626"))
            targets_widget.targets_table.setItem(row, 5, status_item)
            
            row += 1

    def generate_html_report(self):
        """生成HTML报告"""
        targets_widget = self.monitor_tab_widget.get_targets_widget()
        current_row = targets_widget.targets_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请选择要生成报告的监控目标")
            return
        
        target_name = targets_widget.targets_table.item(current_row, 0).text()
        
        # 获取历史数据
        history = self.asset_monitor.get_target_history(target_name, 50)
        if not history:
            QMessageBox.warning(self, "警告", "该监控目标暂无历史数据")
            return
        
        # 计算差异
        differences = {}
        if len(history) >= 2:
            differences = self.asset_monitor._compare_with_previous(target_name, history[-1])
        
        # 选择保存位置
        filename, _ = QFileDialog.getSaveFileName(
            self, f'保存 {target_name} 监控报告', 
            f'{target_name}_monitor_report.html', 
            'HTML Files (*.html);;All Files (*)'
        )
        
        if filename:
            if self.html_generator.generate_monitor_report(target_name, history, differences, filename):
                QMessageBox.information(self, "成功", f"监控报告已生成: {filename}")
                # 询问是否打开报告
                reply = QMessageBox.question(self, "打开报告", 
                                           "是否立即打开生成的报告？",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    import webbrowser
                    webbrowser.open(f'file://{os.path.abspath(filename)}')
            else:
                QMessageBox.warning(self, "错误", "生成报告失败")

    def on_monitor_scan_completed(self, result_data):
        """处理监控扫描完成事件"""
        target_name = result_data.get('target_name', '未知')
        differences = result_data.get('differences', {})
        
        # 更新状态显示
        status_msg = f"[{datetime.now().strftime('%H:%M:%S')}] {target_name} 扫描完成\n"
        
        # 显示变化信息
        if any(differences.values()):
            status_msg += "检测到以下变化:\n"
            if differences.get('new_hosts'):
                status_msg += f"  新增主机: {', '.join(differences['new_hosts'])}\n"
            if differences.get('disappeared_hosts'):
                status_msg += f"  离线主机: {', '.join(differences['disappeared_hosts'])}\n"
            if differences.get('new_ports'):
                status_msg += f"  新增端口: {', '.join(differences['new_ports'])}\n"
            if differences.get('disappeared_ports'):
                status_msg += f"  关闭端口: {', '.join(differences['disappeared_ports'])}\n"
            if differences.get('changed_services'):
                status_msg += f"  服务变化: {len(differences['changed_services'])} 个\n"
        else:
            status_msg += "无变化\n"
        
        results_widget = self.monitor_tab_widget.get_results_widget()
        results_widget.append_message(status_msg)
        
        # 刷新监控目标列表
        self.refresh_monitor_targets()
        
        # 刷新资产对比页面
        if hasattr(self, 'asset_comparison_widget'):
            self.asset_comparison_widget.refresh_targets()

    def on_monitor_progress(self, message):
        """处理监控进度消息"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        results_widget = self.monitor_tab_widget.get_results_widget()
        results_widget.append_message(f"[{timestamp}] {message}")

    def on_monitor_error(self, error_message):
        """处理监控错误消息"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        results_widget = self.monitor_tab_widget.get_results_widget()
        results_widget.append_message(f"[{timestamp}] 错误: {error_message}")
        
        # 刷新监控目标列表以更新状态
        self.refresh_monitor_targets()
