"""
HTML报告生成模块，负责生成资产监控的可视化报告
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any


class HTMLReportGenerator:
    """
    HTML报告生成器
    """
    
    def __init__(self):
        self.template_dir = "templates"
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
    
    def generate_monitor_report(self, target_name: str, history: List[Dict], 
                              differences: Dict, output_file: str) -> bool:
        """
        生成监控报告
        
        参数:
            target_name: 监控目标名称
            history: 历史扫描数据
            differences: 差异对比数据
            output_file: 输出文件路径
            
        返回:
            是否生成成功
        """
        try:
            # 准备报告数据
            report_data = {
                'target_name': target_name,
                'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_scans': len(history),
                'latest_scan': history[-1] if history else None,
                'previous_scan': history[-2] if len(history) > 1 else None,
                'history': history,
                'differences': differences
            }
            
            # 生成HTML内容
            html_content = self._generate_html(report_data)
            
            # 写入文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
            
        except Exception as e:
            print(f"生成报告失败: {str(e)}")
            return False
    
    def _generate_html(self, data: Dict) -> str:
        """
        生成HTML内容
        
        参数:
            data: 报告数据
            
        返回:
            HTML字符串
        """
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastNmap 资产监控报告 - {data['target_name']}</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>FastNmap 资产监控报告</h1>
            <div class="header-info">
                <div class="target-info">
                    <span class="label">监控目标:</span>
                    <span class="value">{data['target_name']}</span>
                </div>
                <div class="time-info">
                    <span class="label">生成时间:</span>
                    <span class="value">{data['generation_time']}</span>
                </div>
                <div class="github-info">
                    <span class="label">项目地址:</span>
                    <a href="https://github.com/vam876/FastNmap" target="_blank" class="github-link">
                        GitHub - FastNmap
                    </a>
                </div>
            </div>
        </header>

        <div class="summary-grid">
            <div class="summary-card">
                <div class="card-icon">SCAN</div>
                <div class="card-content">
                    <h3>总扫描次数</h3>
                    <div class="card-value">{data['total_scans']}</div>
                </div>
            </div>
            
            <div class="summary-card">
                <div class="card-icon">TIME</div>
                <div class="card-content">
                    <h3>最新扫描</h3>
                    <div class="card-value">{self._format_datetime(data['latest_scan']['timestamp']) if data['latest_scan'] else '无'}</div>
                </div>
            </div>
            
            <div class="summary-card difference">
                <div class="card-icon">DIFF</div>
                <div class="card-content">
                    <h3>变化检测</h3>
                    <div class="card-value">{self._count_total_changes(data['differences'])}</div>
                </div>
            </div>
        </div>

        {self._generate_differences_section(data['differences'])}
        
        {self._generate_current_assets_section(data['latest_scan'])}
        
        {self._generate_comparison_section(data['latest_scan'], data['previous_scan'])}
        
        {self._generate_history_section(data['history'])}
    </div>

    <script>
        {self._get_javascript()}
    </script>
</body>
</html>
        """
        return html
    
    def _get_css_styles(self) -> str:
        """获取CSS样式"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #0a0e1a 0%, #1a2332 100%);
            color: #e0f4ff;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #1a2332 0%, #2a4a6b 100%);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            border: 2px solid #4a9eff;
            box-shadow: 0 8px 32px rgba(74, 158, 255, 0.2);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #4a9eff, #00d9ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
        }
        
        .header-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .label {
            color: #a0c4ff;
            font-weight: 500;
            margin-right: 10px;
        }
        
        .value {
            color: #e0f4ff;
            font-weight: bold;
            background: rgba(74, 158, 255, 0.1);
            padding: 4px 12px;
            border-radius: 6px;
        }
        
        .github-link {
            color: #4a9eff;
            text-decoration: none;
            font-weight: bold;
            background: rgba(74, 158, 255, 0.1);
            padding: 4px 12px;
            border-radius: 6px;
            transition: all 0.3s ease;
            border: 1px solid rgba(74, 158, 255, 0.3);
        }
        
        .github-link:hover {
            background: rgba(74, 158, 255, 0.2);
            border-color: #4a9eff;
            transform: translateY(-1px);
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .summary-card {
            background: linear-gradient(135deg, #1a2332 0%, #2a3a52 100%);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid #2a4a6b;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .summary-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(74, 158, 255, 0.3);
            border-color: #4a9eff;
        }
        
        .summary-card.difference {
            border-color: #00d9ff;
        }
        
        .summary-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #4a9eff, #00d9ff);
        }
        
        .card-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
        }
        
        .card-content h3 {
            color: #a0c4ff;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        
        .card-value {
            font-size: 2.2em;
            font-weight: bold;
            color: #4a9eff;
        }
        
        .section {
            background: linear-gradient(135deg, #1a2332 0%, #2a3a52 100%);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid #2a4a6b;
        }
        
        .section h2 {
            color: #4a9eff;
            margin-bottom: 25px;
            font-size: 1.8em;
            border-bottom: 2px solid #2a4a6b;
            padding-bottom: 10px;
        }
        
        .differences-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .diff-card {
            background: rgba(26, 35, 50, 0.8);
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #4a9eff;
        }
        
        .diff-card.new {
            border-left-color: #10b981;
        }
        
        .diff-card.removed {
            border-left-color: #f59e0b;
        }
        
        .diff-card.changed {
            border-left-color: #6366f1;
        }
        
        .diff-card h3 {
            color: #a0c4ff;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .diff-list {
            list-style: none;
        }
        
        .diff-list li {
            padding: 8px 0;
            border-bottom: 1px solid rgba(42, 74, 107, 0.3);
            color: #e0f4ff;
        }
        
        .diff-list li:last-child {
            border-bottom: none;
        }
        
        .hosts-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(26, 35, 50, 0.6);
            border-radius: 8px;
            overflow: hidden;
        }
        
        .hosts-table th,
        .hosts-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid rgba(42, 74, 107, 0.5);
        }
        
        .hosts-table th {
            background: linear-gradient(135deg, #2a4a6b 0%, #4a9eff 100%);
            color: #ffffff;
            font-weight: bold;
        }
        
        .hosts-table tr:hover {
            background: rgba(74, 158, 255, 0.1);
        }
        
        .port-badge {
            display: inline-block;
            background: linear-gradient(45deg, #4a9eff, #00d9ff);
            color: #ffffff;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9em;
            margin: 2px;
            font-weight: bold;
        }
        
        .status-online {
            color: #10b981;
            font-weight: bold;
        }
        
        .status-offline {
            color: #f59e0b;
            font-weight: bold;
        }
        
        .timeline {
            position: relative;
            margin: 20px 0;
        }
        
        .timeline-item {
            background: rgba(26, 35, 50, 0.8);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #4a9eff;
            position: relative;
        }
        
        .timeline-date {
            color: #00d9ff;
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        
        .timeline-content {
            color: #e0f4ff;
        }
        
        .host-count {
            background: linear-gradient(45deg, #4a9eff, #00d9ff);
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.9em;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .header-info {
                flex-direction: column;
                gap: 15px;
            }
            
            .summary-grid {
                grid-template-columns: 1fr;
            }
            
            .differences-grid {
                grid-template-columns: 1fr;
            }
            
            .hosts-table {
                font-size: 0.9em;
            }
            
            .hosts-table th,
            .hosts-table td {
                padding: 10px;
            }
        }
        
        .no-data {
            text-align: center;
            color: #a0c4ff;
            font-style: italic;
            padding: 40px;
        }
        
        .highlight {
            background: rgba(74, 158, 255, 0.2);
            padding: 2px 6px;
            border-radius: 4px;
        }
        """
    
    def _generate_differences_section(self, differences: Dict) -> str:
        """生成差异对比部分"""
        if not any(differences.values()):
            return '<div class="section"><h2>变化检测</h2><div class="no-data">本次扫描无变化</div></div>'
        
        html = '<div class="section"><h2>变化检测</h2><div class="differences-grid">'
        
        # 新增主机
        if differences.get('new_hosts'):
            html += '<div class="diff-card new">'
            html += '<h3>[新增] 新增主机</h3>'
            html += '<ul class="diff-list">'
            for host in differences['new_hosts']:
                html += f'<li>+ {host}</li>'
            html += '</ul></div>'
        
        # 消失主机
        if differences.get('disappeared_hosts'):
            html += '<div class="diff-card removed">'
            html += '<h3>[离线] 离线主机</h3>'
            html += '<ul class="diff-list">'
            for host in differences['disappeared_hosts']:
                html += f'<li>- {host}</li>'
            html += '</ul></div>'
        
        # 新增端口
        if differences.get('new_ports'):
            html += '<div class="diff-card new">'
            html += '<h3>[新增] 新增端口</h3>'
            html += '<ul class="diff-list">'
            for port in differences['new_ports']:
                html += f'<li>+ {port}</li>'
            html += '</ul></div>'
        
        # 消失端口
        if differences.get('disappeared_ports'):
            html += '<div class="diff-card removed">'
            html += '<h3>[关闭] 关闭端口</h3>'
            html += '<ul class="diff-list">'
            for port in differences['disappeared_ports']:
                html += f'<li>- {port}</li>'
            html += '</ul></div>'
        
        # 服务变化
        if differences.get('changed_services'):
            html += '<div class="diff-card changed">'
            html += '<h3>[变化] 服务变化</h3>'
            html += '<ul class="diff-list">'
            for change in differences['changed_services']:
                html += f'<li>* {change["host"]}:{change["port"]}<br>'
                html += f'&nbsp;&nbsp;旧: {change["old_service"]}<br>'
                html += f'&nbsp;&nbsp;新: <span class="highlight">{change["new_service"]}</span></li>'
            html += '</ul></div>'
        
        html += '</div></div>'
        return html
    
    def _generate_current_assets_section(self, latest_scan: Dict) -> str:
        """生成当前资产部分"""
        if not latest_scan:
            return '<div class="section"><h2>当前资产</h2><div class="no-data">暂无扫描数据</div></div>'
        
        html = '<div class="section"><h2>当前资产</h2>'
        html += '<table class="hosts-table">'
        html += '<thead><tr><th>IP地址</th><th>状态</th><th>开放端口</th><th>主要服务</th></tr></thead>'
        html += '<tbody>'
        
        for host in latest_scan.get('hosts', []):
            ip = host.get('ip', 'Unknown')
            status = host.get('status', 'unknown')
            status_class = 'status-online' if status == 'up' else 'status-offline'
            
            # 获取开放端口
            open_ports = [p for p in host.get('ports', []) if p.get('state') == 'open']
            ports_str = ', '.join([f'<span class="port-badge">{p["port"]}</span>' for p in open_ports[:10]])
            if len(open_ports) > 10:
                ports_str += f' <span class="host-count">+{len(open_ports) - 10}</span>'
            
            # 获取主要服务
            services = list(set([p.get('service', 'unknown') for p in open_ports if p.get('service') != 'unknown']))
            services_str = ', '.join(services[:5])
            if len(services) > 5:
                services_str += f' <span class="host-count">+{len(services) - 5}</span>'
            
            html += f'<tr>'
            html += f'<td>{ip}</td>'
            html += f'<td><span class="{status_class}">{status.upper()}</span></td>'
            html += f'<td>{ports_str}</td>'
            html += f'<td>{services_str}</td>'
            html += f'</tr>'
        
        html += '</tbody></table></div>'
        return html
    
    def _generate_comparison_section(self, latest_scan: Dict, previous_scan: Dict) -> str:
        """生成对比分析部分"""
        if not latest_scan or not previous_scan:
            return '<div class="section"><h2>对比分析</h2><div class="no-data">需要至少两次扫描数据进行对比</div></div>'
        
        # 统计数据
        latest_hosts = len(latest_scan.get('hosts', []))
        previous_hosts = len(previous_scan.get('hosts', []))
        
        latest_ports = sum(len([p for p in host.get('ports', []) if p.get('state') == 'open']) 
                          for host in latest_scan.get('hosts', []))
        previous_ports = sum(len([p for p in host.get('ports', []) if p.get('state') == 'open']) 
                           for host in previous_scan.get('hosts', []))
        
        html = '<div class="section"><h2>对比分析</h2>'
        html += '<div class="summary-grid">'
        
        # 主机数量变化
        host_change = latest_hosts - previous_hosts
        host_icon = 'UP' if host_change > 0 else 'DOWN' if host_change < 0 else 'SAME'
        html += f'''
        <div class="summary-card">
            <div class="card-icon">{host_icon}</div>
            <div class="card-content">
                <h3>主机数量变化</h3>
                <div class="card-value">{host_change:+d}</div>
                <small>{previous_hosts} → {latest_hosts}</small>
            </div>
        </div>
        '''
        
        # 端口数量变化
        port_change = latest_ports - previous_ports
        port_icon = 'OPEN' if port_change > 0 else 'CLOSE' if port_change < 0 else 'SAME'
        html += f'''
        <div class="summary-card">
            <div class="card-icon">{port_icon}</div>
            <div class="card-content">
                <h3>开放端口变化</h3>
                <div class="card-value">{port_change:+d}</div>
                <small>{previous_ports} → {latest_ports}</small>
            </div>
        </div>
        '''
        
        html += '</div></div>'
        return html
    
    def _generate_history_section(self, history: List[Dict]) -> str:
        """生成历史记录部分"""
        if not history:
            return '<div class="section"><h2>扫描历史</h2><div class="no-data">暂无历史数据</div></div>'
        
        html = '<div class="section"><h2>扫描历史</h2>'
        
        # 添加展开/折叠控制按钮
        html += '''
        <div class="history-controls">
            <button onclick="toggleChangeDetails()" class="toggle-btn" id="toggleBtn">显示变化详情</button>
        </div>
        '''
        
        html += '<div class="timeline">'
        
        # 只显示最近10次扫描
        recent_history = history[-10:] if len(history) > 10 else history
        recent_history.reverse()  # 最新的在前
        
        for i, scan in enumerate(recent_history):
            timestamp = self._format_datetime(scan.get('timestamp', ''))
            host_count = len(scan.get('hosts', []))
            port_count = sum(len([p for p in host.get('ports', []) if p.get('state') == 'open']) 
                           for host in scan.get('hosts', []))
            
            # 计算与上一次扫描的变化
            changes_html = ""
            if i < len(recent_history) - 1:
                next_scan = recent_history[i + 1]
                changes_html = self._generate_scan_changes(scan, next_scan)
            
            html += f'''
            <div class="timeline-item">
                <div class="timeline-date">[{timestamp}]</div>
                <div class="timeline-content">
                    <div class="scan-summary">
                        发现 <span class="host-count">{host_count}</span> 台主机，
                        <span class="host-count">{port_count}</span> 个开放端口
                    </div>
                    {changes_html}
                </div>
            </div>
            '''
        
        if len(history) > 10:
            html += f'<div class="timeline-item"><div class="timeline-content">还有 {len(history) - 10} 条历史记录...</div></div>'
        
        html += '</div>'
        
        # 添加折叠功能的JavaScript和CSS
        html += '''
        <style>
        .history-controls {
            margin-bottom: 20px;
            text-align: right;
        }
        
        .toggle-btn {
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            cursor: pointer;
            font-size: 13px;
            font-weight: bold;
        }
        
        .toggle-btn:hover {
            background-color: #2563eb;
        }
        
        .scan-changes {
            margin-top: 10px;
            padding: 12px;
            background-color: rgba(30, 41, 59, 0.5);
            border-radius: 6px;
            border-left: 3px solid #3b82f6;
            display: none; /* 默认隐藏 */
        }
        
        .changes-title {
            font-weight: bold;
            color: #60a5fa;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .changes-list {
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.5;
        }
        
        .change-new {
            color: #34d399;
            font-weight: bold;
        }
        
        .change-removed {
            color: #f87171;
            font-weight: bold;
        }
        
        .change-host {
            color: #fbbf24;
            font-weight: bold;
        }
        
        .change-item {
            display: block;
            padding: 2px 0;
        }
        </style>
        
        <script>
        function toggleChangeDetails() {
            const changes = document.querySelectorAll('.scan-changes');
            const btn = document.getElementById('toggleBtn');
            const isHidden = changes.length > 0 && changes[0].style.display === 'none';
            
            changes.forEach(change => {
                change.style.display = isHidden ? 'block' : 'none';
            });
            
            btn.textContent = isHidden ? '隐藏变化详情' : '显示变化详情';
        }
        </script>
        '''
        
        html += '</div>'
        return html
    
    def _generate_scan_changes(self, current_scan: Dict, previous_scan: Dict) -> str:
        """生成单次扫描的变化信息"""
        if not previous_scan:
            return ""
        
        # 提取当前和上一次的主机及端口信息
        current_data = self._extract_hosts_ports(current_scan)
        previous_data = self._extract_hosts_ports(previous_scan)
        
        changes = []
        
        # 检查主机变化
        current_hosts = set(current_data.keys())
        previous_hosts = set(previous_data.keys())
        
        # 新增主机
        new_hosts = current_hosts - previous_hosts
        for host in new_hosts:
            ports_str = ','.join(str(p) for p in current_data[host])
            changes.append(f'<span class="change-item change-new">+主机 {host} (端口:{ports_str})</span>')
        
        # 离线主机
        offline_hosts = previous_hosts - current_hosts
        for host in offline_hosts:
            ports_str = ','.join(str(p) for p in previous_data[host])
            changes.append(f'<span class="change-item change-removed">-主机 {host} (端口:{ports_str})</span>')
        
        # 检查现存主机的端口变化
        common_hosts = current_hosts & previous_hosts
        for host in common_hosts:
            current_ports = set(current_data[host])
            previous_ports = set(previous_data[host])
            
            # 新增端口
            new_ports = current_ports - previous_ports
            if new_ports:
                ports_str = ','.join(str(p) for p in sorted(new_ports))
                changes.append(f'<span class="change-item change-new">+{host} 开放端口:{ports_str}</span>')
            
            # 关闭端口
            closed_ports = previous_ports - current_ports
            if closed_ports:
                ports_str = ','.join(str(p) for p in sorted(closed_ports))
                changes.append(f'<span class="change-item change-removed">-{host} 关闭端口:{ports_str}</span>')
        
        if changes:
            return f'''
            <div class="scan-changes">
                <div class="changes-title">相比上次扫描的变化:</div>
                <div class="changes-list">{'<br>'.join(changes)}</div>
            </div>
            '''
        else:
            return '''
            <div class="scan-changes">
                <div class="changes-title">相比上次扫描: 无变化</div>
            </div>
            '''
    
    def _extract_hosts_ports(self, scan: Dict) -> Dict:
        """提取扫描结果中的主机和端口信息"""
        result = {}
        for host in scan.get('hosts', []):
            ip = host.get('ip', '')
            ports = [p.get('port') for p in host.get('ports', []) if p.get('state') == 'open']
            if ip and ports:
                result[ip] = ports
        return result
    
    def _format_datetime(self, timestamp: str) -> str:
        """格式化时间戳"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return timestamp
    
    def _count_total_changes(self, differences: Dict) -> int:
        """统计总变化数"""
        total = 0
        for key, value in differences.items():
            if isinstance(value, list):
                total += len(value)
        return total
    
    def _get_javascript(self) -> str:
        """获取JavaScript代码"""
        return """
        // 添加页面交互效果
        document.addEventListener('DOMContentLoaded', function() {
            // 为表格行添加点击高亮效果
            const tableRows = document.querySelectorAll('.hosts-table tr');
            tableRows.forEach(row => {
                row.addEventListener('click', function() {
                    tableRows.forEach(r => r.classList.remove('highlight'));
                    this.classList.add('highlight');
                });
            });
            
            // 为卡片添加点击动画
            const cards = document.querySelectorAll('.summary-card');
            cards.forEach(card => {
                card.addEventListener('click', function() {
                    this.style.transform = 'scale(0.98)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 150);
                });
            });
            
            // 延迟显示动画
            const sections = document.querySelectorAll('.section');
            sections.forEach((section, index) => {
                section.style.opacity = '0';
                section.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    section.style.transition = 'all 0.5s ease';
                    section.style.opacity = '1';
                    section.style.transform = 'translateY(0)';
                }, index * 200);
            });
        });
        """ 