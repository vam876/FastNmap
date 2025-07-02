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
    QToolButton, QMenu, QAction, QInputDialog
)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QDateTime
from PyQt5.QtGui import QIntValidator, QIcon, QPixmap, QFont, QColor, QPalette

from nmap_modular.utils.constants import ico_base64, SCAN_TYPES
from nmap_modular.core.nmap_executor import NmapThread
from nmap_modular.core.command_builder import NmapCommandBuilder
from nmap_modular.core.nmap_parser import NmapOutputParser

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
        # 设置现代化样式表
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif;
            }
            QLineEdit, QTextEdit {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 4px;
                padding: 5px;
                color: #cdd6f4;
            }
            QPushButton {
                background-color: #7f849c;
                color: #1e1e2e;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #89b4fa;
            }
            QPushButton:pressed {
                background-color: #74c7ec;
            }
            QTabWidget::pane {
                border: 1px solid #45475a;
                border-radius: 4px;
                background-color: #1e1e2e;
            }
            QTabBar::tab {
                background-color: #313244;
                color: #cdd6f4;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #45475a;
                color: #89b4fa;
            }
            QCheckBox, QRadioButton {
                color: #cdd6f4;
                spacing: 5px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QLabel {
                color: #cdd6f4;
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
        
        # 将组件添加到布局
        url_layout.addWidget(self.url_line_edit)
        url_layout.addWidget(self.load_button)
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
            label.setStyleSheet("font-weight: bold; color: #89b4fa;")
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

        # 第3行：端口选项区
        port_checkbox_layout = QHBoxLayout()
        port_checkbox_layout.setSpacing(10)  # 增加间距
        
        # 创建端口选项分组标题
        port_group_label = QLabel("端口选项：")
        port_group_label.setStyleSheet("font-weight: bold; color: #89b4fa; font-size: 14px;")
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
                    color: #cdd6f4;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 3px;
                }
                QCheckBox::indicator:unchecked {
                    background-color: #313244;
                    border: 1px solid #45475a;
                }
                QCheckBox::indicator:checked {
                    background-color: #89b4fa;
                    border: 1px solid #89b4fa;
                }
            """)
            checkbox.stateChanged.connect(self.on_port_checkbox_changed)
            self.port_checkboxes.append(checkbox)
            port_checkbox_layout.addWidget(checkbox)
            
        # 添加到主布局
        layout.addLayout(port_checkbox_layout)

        # 第4行：操作按钮区
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)  # 增加按钮间的间距
        
        # 定义操作按钮及其样式
        actions = [
            ('开始扫描', '#89b4fa', '#74c7ec'),  # 蓝色主要按钮
            ('停止扫描', '#f38ba8', '#eb6f92'),  # 红色停止按钮
            ('清空文本', '#a6e3a1', '#94e2d5'),  # 绿色清空按钮
            ('导出扫描过程', '#89b4fa', '#94e2d5'),  # 绿色导出扫描过程按钮
            ('导出扫描结果', '#fab387', '#f9e2af')  # 橙色导出扫描结果按钮
        ]
        
        # 创建并配置按钮
        for action, bg_color, hover_color in actions:
            btn = QPushButton(action)
            btn.setMinimumHeight(40)  # 增加按钮高度
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: #1e1e2e;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
            """)
            btn.clicked.connect(self.perform_action)
            action_layout.addWidget(btn)     
            
        # 添加到主布局
        layout.addLayout(action_layout)

        # 第5行：扫描类型选择区
        scan_type_layout = QHBoxLayout()
        scan_type_layout.setSpacing(15)  # 增加间距
        
        # 创建扫描类型标题
        scan_type_label = QLabel("扫描类型：")
        scan_type_label.setStyleSheet("font-weight: bold; color: #89b4fa; font-size: 14px;")
        scan_type_layout.addWidget(scan_type_label)
        
        # 创建单选按钮组
        self.scan_type_group = QButtonGroup(self)
        
        # 定义各扫描类型的颜色
        scan_type_colors = {
            '默认扫描': "#89b4fa",
            '存活扫描': "#a6e3a1",
            '服务识别': "#fab387",
            '系统识别': "#f9e2af",
            '端口识别': "#cba6f7",
            '暴力破解': "#f38ba8",
            '漏洞扫描': "#74c7ec"
        }
        
        # 创建并配置单选按钮
        for i, scan_type in enumerate(SCAN_TYPES):
            radio = QRadioButton(scan_type)
            color = scan_type_colors.get(scan_type, "#89b4fa")
            radio.setStyleSheet(f"""
                QRadioButton {{
                    spacing: 8px;
                    color: #cdd6f4;
                    padding: 5px;
                    border-radius: 4px;
                }}
                QRadioButton::indicator {{
                    width: 18px;
                    height: 18px;
                    border-radius: 9px;
                }}
                QRadioButton::indicator:unchecked {{
                    background-color: #313244;
                    border: 1px solid #45475a;
                }}
                QRadioButton::indicator:checked {{
                    background-color: {color};
                    border: 1px solid {color};
                }}
                QRadioButton:hover {{
                    background-color: rgba(69, 71, 90, 0.5);
                }}
            """)
            # 设置默认选中第一个选项
            if i == 0:
                radio.setChecked(True)
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
                spacing: 10px;
                color: #f9e2af;
                font-weight: bold;
                font-size: 14px;
                padding: 5px 10px;
                background-color: rgba(69, 71, 90, 0.3);
                border-radius: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #313244;
                border: 1px solid #45475a;
            }
            QCheckBox::indicator:checked {
                background-color: #f9e2af;
                border: 1px solid #f9e2af;
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
        tabs = ['扫描过程', '扫描结果', '扫描设置', '使用帮助']
        tab_icons = [
            "\uf120",  # 终端图标代表扫描过程
            "\uf080",  # 图表图标代表扫描结果
            "\uf013",  # 齿轮图标代表扫描设置
            "\uf059"   # 问号图标代表使用帮助
        ]
        
        # 初始化标签页内容
        for i, tab in enumerate(tabs):
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
                    background-color: #313244;
                    color: #cdd6f4;
                    border: 1px solid #45475a;
                    border-radius: 5px;
                    padding: 10px;
                    font-family: 'Arial', sans-serif;
                    font-size: 13px;
                    line-height: 1.5;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #45475a;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #89b4fa;
                    min-height: 20px;
                    border-radius: 5px;
                }
            """)
            
            # 添加到标签页和字典
            self.tab_widget.addTab(tab_edit, tab)
            self.text_edits[tab] = tab_edit
            
            # 如果是使用帮助标签页，添加帮助文本
            if tab == '使用帮助':
                help_text = """
                <h2 style="color: #89b4fa;">FastNmap - Nmap图形化扫描工具使用指南</h2>
                <p><b>基本操作：</b></p>
                <ol>
                    <li>在顶部输入框中输入目标 IP 地址或域名</li>
                    <li>选择扫描类型（默认扫描、存活扫描等）</li>
                    <li>根据需要设置端口和其他参数</li>
                    <li>附加参数输入-vvv，可以看到更加详细的输出结果</li>
                    <li>点击"开始扫描"按钮开始扫描</li>
                </ol>
                <p><b>扫描类型说明：</b></p>
                <ul>
                    <li><span style="color: #89b4fa;">默认扫描</span>: 基本端口扫描，使用 SYN 半连接方式</li>
                    <li><span style="color: #a6e3a1;">存活扫描</span>: 只检测主机是否在线，不扫描端口</li>
                    <li><span style="color: #fab387;">服务识别</span>: 检测端口上运行的服务和版本</li>
                    <li><span style="color: #f9e2af;">系统识别</span>: 尝试识别目标系统的操作系统</li>
                    <li><span style="color: #cba6f7;">端口识别</span>: 用于识别特定端口的服务，格式为：ip:端口 如172.16.1.1:8080</li>
                    <li><span style="color: #f38ba8;">暴力破解</span>: 尝试nse脚本实现常见凭证破解服务</li>
                    <li><span style="color: #74c7ec;">漏洞扫描</span>: 使用内置nse脚本检测目标主机的已知漏洞</li>
                </ul>
                <p><b>端口选项：</b></p>
                <p>可以手动输入端口或选择预定义的端口组，如"高危端口"、"HTTP端口"等。勾选端口选项后会覆盖手动输入的端口信息</p>
                <p><b>其他功能：</b></p>
                <ul>
                    <li>导出扫描过程: 将扫描过程保存到文件</li>
                    <li>导出扫描结果: 将扫描结果导出为CSV格式</li>
                </ul>
                <p><b>开源地址：</b></p>
                <ul>
                    <li>https://github.com/vam876/FastNmap</li>
                </ul>
                
                """
                tab_edit.setHtml(help_text)
            
        # 添加标签页到主布局
        layout.addWidget(self.tab_widget)
        
        # 添加状态栏
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #313244;
                color: #cdd6f4;
                border-top: 1px solid #45475a;
                padding: 3px;
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
                border: 1px solid #45475a;
                border-radius: 3px;
                background-color: #1e1e2e;
                text-align: center;
                color: #cdd6f4;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 2px;
            }
        """)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # 添加状态标签
        self.status_label = QLabel("就绪 | 准备就绪")
        self.status_bar.addWidget(self.status_label)
        
        # 设置主窗口属性
        self.setLayout(layout)
        self.setWindowTitle('FastNmap GUI v0.1.0 - Nmap图形化扫描工具')
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
            self.export_data()
        elif action == '导出扫描结果':
            self.export_result_csv()

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
            if not self.port_input.text() and not any(checkbox.isChecked() for checkbox in self.port_checkboxes):
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
