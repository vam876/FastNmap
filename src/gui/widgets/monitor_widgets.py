"""
资产监控UI组件模块
"""

import os
import webbrowser
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QFileDialog, QTextEdit, QCheckBox, QRadioButton, QTabWidget, 
    QLabel, QButtonGroup, QMessageBox, QStatusBar, QProgressBar, QFrame, QSplitter,
    QToolButton, QMenu, QAction, QInputDialog, QTableWidget, QTableWidgetItem,
    QComboBox, QSpinBox, QGroupBox, QGridLayout, QHeaderView, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

from src.utils.constants import SCAN_TYPES


class MonitorConfigWidget(QWidget):
    """监控配置组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化配置界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 配置表单
        config_group = QGroupBox("监控配置")
        config_group.setStyleSheet(self.get_group_style())
        config_layout = QGridLayout(config_group)
        config_layout.setSpacing(12)
        
        # 监控名称
        config_layout.addWidget(QLabel("监控名称:"), 0, 0)
        self.monitor_name_input = QLineEdit()
        self.monitor_name_input.setPlaceholderText("例如：公司内网监控")
        config_layout.addWidget(self.monitor_name_input, 0, 1, 1, 2)
        
        # 监控目标 - 使用下拉框 + 自定义
        config_layout.addWidget(QLabel("监控目标:"), 1, 0)
        self.target_combo = QComboBox()
        self.target_combo.setEditable(True)
        self.target_combo.addItems([
            "127.0.0.1",
            "192.168.1.0/24", 
            "192.168.0.0/24",
            "10.0.0.0/24",
            "172.16.0.0/24",
            "localhost",
            "www.baidu.com",
            "自定义..."
        ])
        config_layout.addWidget(self.target_combo, 1, 1, 1, 2)
        
        # 扫描类型
        config_layout.addWidget(QLabel("扫描类型:"), 2, 0)
        self.scan_type_combo = QComboBox()
        self.scan_type_combo.addItems(SCAN_TYPES)
        # 移除自动填充，统一由command_builder构建
        # self.scan_type_combo.currentTextChanged.connect(self.update_scan_params)
        config_layout.addWidget(self.scan_type_combo, 2, 1)
        
        # 监控间隔
        config_layout.addWidget(QLabel("监控间隔:"), 2, 2)
        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(1)
        self.interval_spin.setMaximum(1440)
        self.interval_spin.setValue(60)
        self.interval_spin.setSuffix(" 分钟")
        config_layout.addWidget(self.interval_spin, 2, 3)
        
        # 端口设置
        config_layout.addWidget(QLabel("端口范围:"), 3, 0)
        self.ports_combo = QComboBox()
        self.ports_combo.setEditable(True)
        self.ports_combo.addItems([
            "22,80,443",
            "21,22,23,25,53,80,110,111,135,139,143,443,993,995,1723,3389,5900,8080",
            "80,443,8080,8443,8000,8008,8888,9080,9090",
            "21,22,23,25,53,110,143,993,995",
            "1433,3306,5432,1521,27017,6379",
            "3389,5900,5901,5902",
            "1-1000",
            "1-65535",
            "自定义..."
        ])
        self.ports_combo.setCurrentText("22,80,443")
        config_layout.addWidget(self.ports_combo, 3, 1, 1, 2)
        
        # 自定义参数
        config_layout.addWidget(QLabel("扫描参数:"), 4, 0)
        self.params_input = QLineEdit()
        self.params_input.setPlaceholderText("-vvv -T4 --open")
        self.params_input.setText("-vvv -T4 --open")
        config_layout.addWidget(self.params_input, 4, 1, 1, 2)
        
        # 初始化默认参数
        self.update_scan_params()
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("添加监控")
        self.add_btn.setStyleSheet(self.get_button_style("#2563eb"))
        self.add_btn.clicked.connect(self.add_monitor)
        button_layout.addWidget(self.add_btn)
        
        button_layout.addStretch()
        config_layout.addLayout(button_layout, 5, 0, 1, 4)
        
        layout.addWidget(config_group)
    
    def get_group_style(self):
        """获取组件样式"""
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #3b82f6;
                border: 2px solid #1e293b;
                border-radius: 8px;
                padding-top: 15px;
                margin-top: 10px;
                background-color: #0f172a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: #0a0e1a;
            }
        """
    
    def get_button_style(self, color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.adjust_color(color, 20)};
            }}
            QPushButton:pressed {{
                background-color: {self.adjust_color(color, -20)};
            }}
        """
    
    def adjust_color(self, color, amount):
        """调整颜色亮度"""
        # 简单的颜色调整逻辑
        if color == "#2563eb":
            return "#3b82f6" if amount > 0 else "#1d4ed8"
        return color
    
    def update_scan_params(self):
        """根据扫描类型更新默认参数"""
        scan_type = self.scan_type_combo.currentText()
        
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
        # 包含初始默认值用于比较
        initial_default = '-vvv -T4 --open'
        if not current_text or current_text in default_params.values() or current_text == initial_default:
            self.params_input.setText(params)
        
        # 更新占位符提示
        self.params_input.setPlaceholderText(params)
    
    def add_monitor(self):
        """添加监控目标"""
        if self.parent_window:
            self.parent_window.add_monitor_target()


class MonitorTargetsWidget(QWidget):
    """监控目标管理组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化目标管理界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 控制按钮区域
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("开始监控")
        self.start_btn.setStyleSheet(self.get_button_style("#059669"))
        self.start_btn.clicked.connect(self.start_selected_monitor)
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("停止监控")
        self.stop_btn.setStyleSheet(self.get_button_style("#dc2626"))
        self.stop_btn.clicked.connect(self.stop_selected_monitor)
        control_layout.addWidget(self.stop_btn)
        
        self.delete_btn = QPushButton("删除监控")
        self.delete_btn.setStyleSheet(self.get_button_style("#7c2d12"))
        self.delete_btn.clicked.connect(self.delete_selected_monitor)
        control_layout.addWidget(self.delete_btn)
        
        self.refresh_btn = QPushButton("刷新状态")
        self.refresh_btn.setStyleSheet(self.get_button_style("#374151"))
        self.refresh_btn.clicked.connect(self.refresh_targets)
        control_layout.addWidget(self.refresh_btn)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # 监控目标表格
        self.targets_table = QTableWidget()
        self.targets_table.setColumnCount(6)
        self.targets_table.setHorizontalHeaderLabels([
            "监控名称", "目标", "类型", "间隔(分钟)", "最后扫描", "状态"
        ])
        
        # 设置表格样式
        self.targets_table.setStyleSheet("""
            QTableWidget {
                background-color: #0f172a;
                border: 2px solid #1e293b;
                border-radius: 8px;
                color: #e2e8f0;
                gridline-color: #334155;
                selection-background-color: rgba(59, 130, 246, 0.3);
                alternate-background-color: #1a1f35;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #334155;
                background-color: #0f172a;
            }
            QTableWidget::item:alternate {
                background-color: #162033;
            }
            QTableWidget::item:selected {
                background-color: rgba(59, 130, 246, 0.4);
                color: #ffffff;
            }
            QTableWidget::item:hover {
                background-color: rgba(59, 130, 246, 0.2);
            }
            QHeaderView::section {
                background-color: #1e293b;
                color: #f8fafc;
                padding: 12px;
                border: none;
                font-weight: bold;
                border-bottom: 2px solid #3b82f6;
            }
        """)
        
        # 设置表格属性
        header = self.targets_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.targets_table.setAlternatingRowColors(True)
        self.targets_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.targets_table)
    
    def get_button_style(self, color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
        """
    
    def refresh_targets(self):
        """刷新监控目标列表"""
        if self.parent_window:
            self.parent_window.refresh_monitor_targets()
    
    def start_selected_monitor(self):
        """开始选中的监控"""
        current_row = self.targets_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请选择要启动的监控目标")
            return
        
        target_name = self.targets_table.item(current_row, 0).text()
        if self.parent_window and hasattr(self.parent_window, 'asset_monitor'):
            if self.parent_window.asset_monitor.start_monitoring(target_name):
                QMessageBox.information(self, "成功", f"监控 '{target_name}' 已启动")
                self.refresh_targets()
            else:
                QMessageBox.warning(self, "失败", f"监控 '{target_name}' 启动失败")
    
    def stop_selected_monitor(self):
        """停止选中的监控"""
        current_row = self.targets_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请选择要停止的监控目标")
            return
        
        target_name = self.targets_table.item(current_row, 0).text()
        if self.parent_window and hasattr(self.parent_window, 'asset_monitor'):
            self.parent_window.asset_monitor.stop_monitoring(target_name)
            QMessageBox.information(self, "成功", f"监控 '{target_name}' 已停止")
            self.refresh_targets()
    
    def delete_selected_monitor(self):
        """删除选中的监控"""
        if self.parent_window:
            self.parent_window.remove_monitor_target()


class MonitorResultsWidget(QWidget):
    """监控结果显示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化结果显示界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("清空日志")
        self.clear_btn.setStyleSheet(self.get_button_style("#6b7280"))
        self.clear_btn.clicked.connect(self.clear_results)
        control_layout.addWidget(self.clear_btn)
        
        self.report_btn = QPushButton("生成报告")
        self.report_btn.setStyleSheet(self.get_button_style("#7c3aed"))
        self.report_btn.clicked.connect(self.generate_report)
        control_layout.addWidget(self.report_btn)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # 结果显示区域
        results_group = QGroupBox("监控日志")
        results_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #3b82f6;
                border: 2px solid #1e293b;
                border-radius: 8px;
                padding-top: 15px;
                margin-top: 10px;
                background-color: #0f172a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: #0a0e1a;
            }
        """)
        results_layout = QVBoxLayout(results_group)
        
        # 状态显示文本框
        self.status_text = QTextEdit()
        self.status_text.setPlaceholderText("监控状态和进度信息将在这里显示...")
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        results_layout.addWidget(self.status_text)
        
        layout.addWidget(results_group)
    
    def get_button_style(self, color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
        """
    
    def clear_results(self):
        """清空结果"""
        self.status_text.clear()
    
    def generate_report(self):
        """生成报告"""
        if self.parent_window:
            self.parent_window.generate_html_report()
    
    def append_message(self, message):
        """追加消息"""
        self.status_text.append(message)


class AssetMonitorTabWidget(QTabWidget):
    """资产监控主标签页组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_tabs()
    
    def init_tabs(self):
        """初始化子标签页"""
        # 设置标签页样式
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #1e293b;
                border-radius: 8px;
                background-color: #0a0e1a;
                margin-top: -1px;
            }
            QTabBar::tab {
                background-color: #1e293b;
                color: #94a3b8;
                border: 1px solid #334155;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 30px;
                margin-right: 3px;
                font-weight: 600;
                font-size: 14px;
                min-width: 90px;
                text-align: center;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
                color: #ffffff;
                border-bottom: 2px solid #3b82f6;
                font-weight: bold;
                font-size: 14px;
            }
            QTabBar::tab:hover:!selected {
                background-color: #334155;
                color: #e2e8f0;
            }
        """)
        
        # 创建子标签页
        self.config_widget = MonitorConfigWidget(self.parent_window)
        self.targets_widget = MonitorTargetsWidget(self.parent_window)
        self.results_widget = MonitorResultsWidget(self.parent_window)
        
        self.addTab(self.config_widget, "监控配置")
        self.addTab(self.targets_widget, "监控目标")
        self.addTab(self.results_widget, "监控结果")
    
    def get_config_widget(self):
        """获取配置组件"""
        return self.config_widget
    
    def get_targets_widget(self):
        """获取目标组件"""
        return self.targets_widget
    
    def get_results_widget(self):
        """获取结果组件"""
        return self.results_widget 