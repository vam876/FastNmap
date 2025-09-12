"""
资产对比组件模块
"""

import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QTextEdit, QLabel, QComboBox, QGroupBox, QGridLayout, 
    QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget,
    QScrollArea, QFrame, QSplitter
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont


class AssetComparisonWidget(QWidget):
    """资产对比主组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.init_ui()
        # 延迟刷新目标列表，确保asset_monitor已经初始化
        QTimer.singleShot(100, self.refresh_targets)
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 控制区域
        control_layout = QHBoxLayout()
        
        # 监控目标选择
        control_layout.addWidget(QLabel("选择监控目标:"))
        self.target_combo = QComboBox()
        self.target_combo.currentTextChanged.connect(self.refresh_comparison)
        control_layout.addWidget(self.target_combo)
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新对比")
        refresh_btn.setStyleSheet(self.get_button_style("#3b82f6"))
        refresh_btn.clicked.connect(self.refresh_comparison)
        control_layout.addWidget(refresh_btn)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # 主要内容区域 - 使用分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：对比统计
        stats_widget = self.create_stats_widget()
        splitter.addWidget(stats_widget)
        
        # 右侧：详细对比
        details_widget = self.create_details_widget()
        splitter.addWidget(details_widget)
        
        # 设置分割比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
    
    def create_stats_widget(self):
        """创建统计信息组件"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #1e293b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #64748b;
            }
        """)
        
        # 内容组件
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # 简单对比统计
        stats_group = QGroupBox("对比统计")
        stats_group.setStyleSheet(self.get_group_style())
        stats_layout = QVBoxLayout(stats_group)
        
        # 简单的文本显示
        self.stats_text = QTextEdit()
        self.stats_text.setMaximumHeight(80)
        self.stats_text.setReadOnly(True)
        self.stats_text.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        stats_layout.addWidget(self.stats_text)
        layout.addWidget(stats_group)
        
        # 历史趋势
        trend_group = QGroupBox("历史趋势")
        trend_group.setStyleSheet(self.get_group_style())
        trend_layout = QVBoxLayout(trend_group)
        
        self.trend_text = QTextEdit()
        self.trend_text.setMinimumHeight(200)  # 改为最小高度
        self.trend_text.setMaximumHeight(400)  # 增加最大高度
        self.trend_text.setReadOnly(True)
        self.trend_text.setStyleSheet("""
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
            QScrollBar:vertical {
                background-color: #1e293b;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 4px;
            }
        """)
        trend_layout.addWidget(self.trend_text)
        
        layout.addWidget(trend_group)
        layout.addStretch()
        
        # 设置内容到滚动区域
        scroll_area.setWidget(content_widget)
        
        return scroll_area
    
    def create_details_widget(self):
        """创建详细对比组件"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 详细对比标签页
        self.details_tabs = QTabWidget()
        self.details_tabs.setStyleSheet("""
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
                padding: 8px 15px;
                margin-right: 2px;
                font-weight: 500;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
                color: #ffffff;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #334155;
                color: #e2e8f0;
            }
        """)
        
        # 创建各个对比标签页
        self.create_new_assets_tab()
        self.create_current_assets_tab()
        self.create_changes_tab()
        
        layout.addWidget(self.details_tabs)
        
        return widget
    
    def create_new_assets_tab(self):
        """创建新增资产标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 新增主机表格
        hosts_group = QGroupBox("新增主机")
        hosts_group.setStyleSheet(self.get_group_style())
        hosts_layout = QVBoxLayout(hosts_group)
        
        self.new_hosts_table = QTableWidget()
        self.new_hosts_table.setColumnCount(3)
        self.new_hosts_table.setHorizontalHeaderLabels(["IP地址", "状态", "发现时间"])
        self.setup_table_style(self.new_hosts_table)
        hosts_layout.addWidget(self.new_hosts_table)
        
        layout.addWidget(hosts_group)
        
        # 新增端口表格
        ports_group = QGroupBox("新增端口")
        ports_group.setStyleSheet(self.get_group_style())
        ports_layout = QVBoxLayout(ports_group)
        
        self.new_ports_table = QTableWidget()
        self.new_ports_table.setColumnCount(4)
        self.new_ports_table.setHorizontalHeaderLabels(["主机", "端口", "服务", "发现时间"])
        self.setup_table_style(self.new_ports_table)
        ports_layout.addWidget(self.new_ports_table)
        
        layout.addWidget(ports_group)
        
        self.details_tabs.addTab(widget, "新增资产")
    
    def create_current_assets_tab(self):
        """创建当前资产标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        current_group = QGroupBox("当前所有资产")
        current_group.setStyleSheet(self.get_group_style())
        current_layout = QVBoxLayout(current_group)
        
        self.current_assets_table = QTableWidget()
        self.current_assets_table.setColumnCount(4)
        self.current_assets_table.setHorizontalHeaderLabels(["IP地址", "状态", "开放端口", "主要服务"])
        self.setup_table_style(self.current_assets_table)
        current_layout.addWidget(self.current_assets_table)
        
        layout.addWidget(current_group)
        
        self.details_tabs.addTab(widget, "当前资产")
    
    def create_changes_tab(self):
        """创建变化记录标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        changes_group = QGroupBox("详细变化记录")
        changes_group.setStyleSheet(self.get_group_style())
        changes_layout = QVBoxLayout(changes_group)
        
        self.changes_table = QTableWidget()
        self.changes_table.setColumnCount(5)
        self.changes_table.setHorizontalHeaderLabels(["时间", "类型", "主机", "端口/服务", "详情"])
        self.setup_table_style(self.changes_table)
        changes_layout.addWidget(self.changes_table)
        
        layout.addWidget(changes_group)
        
        self.details_tabs.addTab(widget, "变化记录")
    
    def setup_table_style(self, table):
        """设置表格样式"""
        table.setStyleSheet("""
            QTableWidget {
                background-color: #0f172a;
                border: 1px solid #1e293b;
                border-radius: 6px;
                color: #e2e8f0;
                gridline-color: #334155;
                selection-background-color: rgba(59, 130, 246, 0.3);
                alternate-background-color: #1a1f35;
            }
            QTableWidget::item {
                padding: 8px;
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
            QHeaderView::section {
                background-color: #1e293b;
                color: #f8fafc;
                padding: 8px;
                border: none;
                font-weight: bold;
                border-bottom: 2px solid #3b82f6;
            }
        """)
        
        header = table.horizontalHeader()
        header.setStretchLastSection(True)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
    
    def create_stat_card(self, title, value, color="#3b82f6"):
        """创建统计卡片"""
        card = QFrame()
        card.setMinimumHeight(90)   # 增加最小高度
        card.setMaximumHeight(110)  # 增加最大高度  
        card.setMinimumWidth(120)   # 增加最小宽度
        card.setMaximumWidth(200)   # 增加最大宽度，让文字有更多空间
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #1e293b, stop:1 #0f172a);
                border: 1px solid {color};
                border-radius: 8px;
                padding: 10px;
                margin: 4px;
            }}
            QFrame:hover {{
                border-color: {self.adjust_color(color, 20)};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #334155, stop:1 #1e293b);
            }}
            QLabel {{
                color: #e2e8f0;
                background: transparent;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        layout.setContentsMargins(8, 8, 8, 8)
        
        title_label = QLabel(title)
        title_label.setWordWrap(True)  # 启用自动换行
        title_label.setStyleSheet("""
            font-size: 11px; 
            color: #94a3b8; 
            font-weight: 600;
            text-align: center;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(str(value))
        value_label.setWordWrap(True)  # 启用自动换行
        value_label.setStyleSheet(f"""
            font-size: 20px; 
            font-weight: bold; 
            color: {color};
            text-align: center;
        """)
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        return card
    
    def adjust_color(self, color, amount):
        """调整颜色亮度"""
        # 简单的颜色调整，让悬停效果更明显
        if color == "#3b82f6":
            return "#60a5fa" if amount > 0 else "#2563eb"
        elif color == "#10b981":
            return "#34d399" if amount > 0 else "#059669"
        elif color == "#f59e0b":
            return "#fbbf24" if amount > 0 else "#d97706"
        elif color == "#ef4444":
            return "#f87171" if amount > 0 else "#dc2626"
        return color
    
    def get_group_style(self):
        """获取组样式"""
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
    
    def clear_layout(self, layout):
        """递归清理layout中的所有widget"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
    
    def refresh_targets(self):
        """刷新监控目标列表"""
        self.target_combo.clear()
        if self.parent_window and hasattr(self.parent_window, 'asset_monitor'):
            targets = self.parent_window.asset_monitor.get_monitor_targets()
            if targets:
                self.target_combo.addItems(targets.keys())
                # 自动选择第一个目标
                if self.target_combo.count() > 0:
                    self.target_combo.setCurrentIndex(0)
    
    def refresh_comparison(self):
        """刷新对比数据"""
        target_name = self.target_combo.currentText()
        if not target_name:
            self.show_no_data_message()
            return
        
        self.load_comparison_data(target_name)
    
    def load_comparison_data(self, target_name):
        """加载对比数据"""
        if not self.parent_window or not hasattr(self.parent_window, 'asset_monitor'):
            return
        
        # 获取历史数据
        history = self.parent_window.asset_monitor.get_target_history(target_name, limit=10)
        
        if len(history) < 2:
            self.show_no_data_message()
            return
        
        # 分析对比数据
        latest_scan = history[0]
        previous_scan = history[1]
        
        # 更新统计信息
        self.update_stats(latest_scan, previous_scan, len(history))
        
        # 更新详细对比
        self.update_detailed_comparison(target_name, history)
        
        # 更新趋势信息
        self.update_trend_info(history)
    
    def update_stats(self, latest, previous, total_scans):
        """更新统计信息"""
        # 计算统计数据
        latest_hosts = len(latest.get('hosts', []))
        previous_hosts = len(previous.get('hosts', []))
        host_change = latest_hosts - previous_hosts
        
        latest_ports = sum(len(host.get('ports', [])) for host in latest.get('hosts', []))
        previous_ports = sum(len(host.get('ports', [])) for host in previous.get('hosts', []))
        port_change = latest_ports - previous_ports
        
        # 生成简单的文本统计
        stats_text = f"""总扫描次数: {total_scans}
主机变化: {previous_hosts} → {latest_hosts} ({host_change:+d})
端口变化: {previous_ports} → {latest_ports} ({port_change:+d})"""
        
        self.stats_text.setPlainText(stats_text)
    
    def update_detailed_comparison(self, target_name, history):
        """更新详细对比"""
        if len(history) < 2:
            return
        
        latest_scan = history[0]
        
        # 获取差异信息
        if self.parent_window and hasattr(self.parent_window, 'asset_monitor'):
            differences = self.parent_window.asset_monitor._compare_with_previous(target_name, latest_scan)
        else:
            differences = {}
        
        # 更新新增资产
        self.update_new_assets(differences, latest_scan.get('timestamp', ''))
        
        # 更新当前资产
        self.update_current_assets(latest_scan)
        
        # 更新变化记录
        self.update_changes_history(target_name, history)
    
    def update_new_assets(self, differences, timestamp):
        """更新新增资产表格"""
        # 新增主机
        new_hosts = differences.get('new_hosts', [])
        self.new_hosts_table.setRowCount(len(new_hosts))
        
        for row, host_ip in enumerate(new_hosts):
            self.new_hosts_table.setItem(row, 0, QTableWidgetItem(host_ip))
            self.new_hosts_table.setItem(row, 1, QTableWidgetItem("在线"))
            self.new_hosts_table.setItem(row, 2, QTableWidgetItem(timestamp))
        
        # 新增端口
        new_ports = differences.get('new_ports', [])
        self.new_ports_table.setRowCount(len(new_ports))
        
        for row, port_info in enumerate(new_ports):
            if ':' in port_info:
                host, port = port_info.split(':', 1)
                self.new_ports_table.setItem(row, 0, QTableWidgetItem(host))
                self.new_ports_table.setItem(row, 1, QTableWidgetItem(port))
                self.new_ports_table.setItem(row, 2, QTableWidgetItem("未知"))
                self.new_ports_table.setItem(row, 3, QTableWidgetItem(timestamp))
    
    def update_current_assets(self, latest_scan):
        """更新当前资产表格"""
        hosts = latest_scan.get('hosts', [])
        self.current_assets_table.setRowCount(len(hosts))
        
        for row, host in enumerate(hosts):
            ip = host.get('ip', '')
            status = host.get('status', 'unknown')
            ports = [str(p.get('port', '')) for p in host.get('ports', []) if p.get('state') == 'open']
            services = []
            for p in host.get('ports', []):
                if p.get('state') == 'open':
                    service_info = p.get('service', {})
                    if isinstance(service_info, dict):
                        service_name = service_info.get('name', '')
                    elif isinstance(service_info, str):
                        service_name = service_info
                    else:
                        service_name = ''
                    if service_name:
                        services.append(service_name)
            
            self.current_assets_table.setItem(row, 0, QTableWidgetItem(ip))
            self.current_assets_table.setItem(row, 1, QTableWidgetItem(status))
            self.current_assets_table.setItem(row, 2, QTableWidgetItem(', '.join(ports[:5])))  # 限制显示5个端口
            self.current_assets_table.setItem(row, 3, QTableWidgetItem(', '.join(services[:3])))  # 限制显示3个服务
    
    def update_changes_history(self, target_name, history):
        """更新变化历史"""
        # 这里可以实现更详细的变化历史记录
        # 暂时显示基本信息
        self.changes_table.setRowCount(min(len(history), 10))
        
        for row, scan in enumerate(history[:10]):
            timestamp = scan.get('timestamp', '')
            hosts_count = len(scan.get('hosts', []))
            ports_count = sum(len(host.get('ports', [])) for host in scan.get('hosts', []))
            
            self.changes_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.changes_table.setItem(row, 1, QTableWidgetItem("扫描"))
            self.changes_table.setItem(row, 2, QTableWidgetItem(f"{hosts_count}台"))
            self.changes_table.setItem(row, 3, QTableWidgetItem(f"{ports_count}个端口"))
            self.changes_table.setItem(row, 4, QTableWidgetItem("定期扫描"))
    
    def update_trend_info(self, history):
        """更新趋势信息"""
        trend_text = []
        
        for i, scan in enumerate(history[:5]):  # 显示最近5次扫描
            timestamp = scan.get('timestamp', '')
            hosts_count = len(scan.get('hosts', []))
            ports_count = sum(len(host.get('ports', [])) for host in scan.get('hosts', []))
            
            prefix = "最新" if i == 0 else f"第{i+1}次"
            trend_text.append(f"[{prefix}] {timestamp}")
            trend_text.append(f"  主机: {hosts_count}台, 端口: {ports_count}个\n")
        
        self.trend_text.setPlainText('\n'.join(trend_text))
    
    def show_no_data_message(self):
        """显示无数据消息"""
        # 清空所有表格
        for table in [self.new_hosts_table, self.new_ports_table, 
                     self.current_assets_table, self.changes_table]:
            table.setRowCount(0)
        
        # 显示无数据消息
        self.stats_text.setPlainText("数据不足，需要至少2次扫描才能进行对比")
        self.trend_text.setPlainText("暂无足够的历史数据进行对比分析\n请等待更多扫描结果...") 