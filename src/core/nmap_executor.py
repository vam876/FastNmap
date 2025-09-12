"""
Nmap执行模块，负责执行Nmap命令并处理输出
"""

import subprocess
import sys
from PyQt5.QtCore import QThread, pyqtSignal

class NmapThread(QThread):
    """
    用于在后台线程中执行Nmap命令的类
    """
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(bool)  # 新增错误信号，True表示有错误

    def __init__(self, command):
        """
        初始化NmapThread实例
        
        参数:
            command: 要执行的Nmap命令列表
        """
        super().__init__()
        self.command = command
        
    def run(self):
        """
        执行Nmap命令并发送输出信号
        """
        try:
            process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_signal.emit(output.strip())
        except FileNotFoundError as e:
            # 发送错误信息到输出信号，可以在GUI中显示错误信息
            if sys.platform == 'win32':
                error_msg = "错误：系统中未找到nmap可执行文件，请确保nmap存在于nmap目录下（./nmap/nmap.exe）。"
            elif sys.platform == 'darwin':
                error_msg = "错误：系统中未找到nmap可执行文件。\n\n请使用以下方式安装nmap：\n1. 访问 https://nmap.org/download 下载 macOS 版本安装包\n2. 或使用Homebrew安装: brew install nmap\n"
            else:
                error_msg = "错误：系统中未找到nmap可执行文件，请确保nmap已安装或存在于/usr/bin/nmap或/usr/local/bin/nmap位置。"
            self.output_signal.emit(error_msg)
            self.error_signal.emit(True)  # 发送错误信号
        except Exception as e:
            # 处理其他可能的异常
            self.output_signal.emit(f"未预见的错误：{str(e)}")
            self.error_signal.emit(True)  # 发送错误信号
