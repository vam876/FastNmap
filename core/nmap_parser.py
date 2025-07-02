"""
Nmap输出解析模块，负责解析Nmap扫描结果
"""

import os
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QMessageBox
import re
from functools import partial

class NmapOutputParser:
    """
    用于解析Nmap输出结果的类
    """
    
    @staticmethod
    def parse_nmap_output(scan_type, logs_dir='logs', html_format=True):
        """
        解析Nmap输出的XML文件
        
        参数:
            scan_type: 扫描类型
            logs_dir: 日志目录
            html_format: 是否返回HTML格式的结果
            
        返回:
            解析后的结果文本
        """
        output_filename = f"{scan_type}_ScanCacheLog.xml"
        output_file_path = os.path.join(logs_dir, output_filename)
        
        if not os.path.exists(output_file_path):
            return None, "扫描结果文件不存在"
            
        try:
            tree = ET.parse(output_file_path)
            root = tree.getroot()
            
            # 根据扫描类型选择不同的解析方法
            if scan_type == '默认扫描':
                result_text = NmapOutputParser._parse_default_scan(root, html_format)
            elif scan_type == '存活扫描':
                result_text = NmapOutputParser._parse_alive_scan(root, html_format)
            elif scan_type == '服务识别':
                result_text = NmapOutputParser._parse_service_scan(root, html_format)
            elif scan_type == '系统识别':
                result_text = NmapOutputParser._parse_os_scan(root, html_format)
            elif scan_type == '端口识别':
                result_text = NmapOutputParser._parse_port_scan(root, html_format)
            elif scan_type == '暴力破解':
                result_text = NmapOutputParser._parse_brute_force_scan(root, html_format)
            elif scan_type == '漏洞扫描':
                result_text = NmapOutputParser._parse_vulnerability_scan(root, html_format)
            
            # 确保返回字符串被正确格式化
            result = result_text.strip() if result_text else "没有可用的扫描结果"
                
            return result, None
        except Exception as e:
            return None, f"解析扫描结果时出错: {str(e)}"
    
    @staticmethod
    def _render_html_results(title, headers, data_rows, extra_html=""):
        """
        通用HTML渲染方法，应用于所有类型的扫描结果
        
        参数:
            title: 扫描结果标题
            headers: 表格头列表，形如[{'name': '端口', 'class': 'col-port'}]
            data_rows: 数据行的列表，每行是一个字典
            extra_html: 任何额外要添加的HTML
            
        返回:
            完整的HTML格式的扫描结果
        """
        # 获取通用CSS样式
        css = NmapOutputParser._get_common_css()
        
        # 生成表格头
        headers_html = ""
        for header in headers:
            header_class = header.get('class', '')
            headers_html += f"<th class='{header_class}'>{header['name']}</th>\n"
        
        # 生成表格内容
        rows_html = ""
        if data_rows:
            for row in data_rows:
                row_class = row.get('class', '')
                cells_html = ""
                for header in headers:
                    cell_key = header.get('key', header['name'].lower())
                    cell_value = row.get(cell_key, '')
                    cell_class = row.get(f"{cell_key}_class", '')
                    cells_html += f"<td class='{cell_class}'>{cell_value}</td>\n"
                rows_html += f"<tr class='{row_class}'>\n{cells_html}</tr>\n"
        else:
            # 如果没有数据行，显示空结果消息
            empty_cols = len(headers)
            rows_html = f"<tr><td colspan='{empty_cols}' class='no-results'>没有可用的扫描结果</td></tr>"
        
        # 生成完整的HTML
        html = f"""
        <div class='scan-container'>
            {css}
            <div class="host-section">
                <h3 class="host-title">{title}</h3>
                <table class="scan-results">
                    <thead>
                        <tr>
                            {headers_html}
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
                {extra_html}
            </div>
        </div>
        """
        
        return html
    
    @staticmethod
    def _parse_default_scan(root, html_format=True):
        """解析默认扫描结果"""
        if html_format:
            headers = [
                {'name': '端口', 'class': 'col-port', 'key': 'port'},
                {'name': '状态', 'class': 'col-state', 'key': 'state'},
                {'name': '服务', 'class': 'col-service', 'key': 'service'}
            ]
            
            all_hosts_data = []
            host_html = ""
            hosts_found = 0
            
            for host in root.findall('.//host'):
                hosts_found += 1
                ip = host.find('address').get('addr')
                data_rows = []
                
                for port in host.findall('.//port'):
                    port_id = port.get('portid')
                    state = port.find('state').get('state')
                    state_class = NmapOutputParser._get_state_class(state)
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else '未知服务'
                    
                    # 为服务类型添加颜色编码
                    service_class = NmapOutputParser._get_service_class(service_name)
                    
                    data_rows.append({
                        'port': f"{ip}:{port_id}",
                        'state': state,
                        'state_class': state_class,
                        'service': service_name,
                        'class': service_class
                    })
                
                # 生成每个主机的HTML
                if data_rows:
                    host_html += NmapOutputParser._render_html_results(
                        f"主机：{ip}",
                        headers,
                        data_rows,
                        f"<div class='host-section'></div>"
                    )
                else:
                    host_html += f"""
                    <div class="host-section">
                        <h3 class="host-title">主机：{ip}</h3>
                        <div class="no-results">没有发现开放的端口</div>
                    </div>
                    """
            
            if hosts_found == 0:
                css = NmapOutputParser._get_common_css()
                return f"""
                <div class='scan-container'>
                    {css}
                    <div class="no-results">没有找到主机或所有主机都没有响应</div>
                </div>
                """
            
            return f"<div class='scan-container'>{NmapOutputParser._get_common_css()}{host_html}</div>"
        else:
            # 文本格式的输出
            result_text = "扫描结果: \n"
            has_hosts = False
            
            for host in root.findall('.//host'):
                has_hosts = True
                ip = host.find('address').get('addr')
                result_text += f"主机：{ip}\n"
                has_ports = False
                
                for port in host.findall('.//port'):
                    has_ports = True
                    port_id = port.get('portid')
                    state = port.find('state').get('state')
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else '未知服务'
                    result_text += f"{ip}:{port_id}:{service_name} ({state})\n"
                
                if not has_ports:
                    result_text += "没有发现开放的端口\n"
            
            if not has_hosts:
                result_text += "没有找到主机\n"
                
            return result_text
    
    @staticmethod
    def _parse_alive_scan(root, html_format=True):
        """解析存活扫描结果"""
        if html_format:
            # 获取通用CSS样式
            css = NmapOutputParser._get_common_css()
            
            # 准备标题和数据
            title = "存活扫描结果"
            headers = [
                {'name': 'IP地址', 'class': 'col-ip', 'key': 'ip'},
                {'name': '状态', 'class': 'col-state', 'key': 'state'}
            ]
            
            data_rows = []
            host_count = 0
            
            for host in root.findall('.//host'):
                host_count += 1
                ip = host.find('address').get('addr')
                status = host.find('.//status')
                state = status.get('state') if status is not None else '未知'
                state_class = 'status-open' if state == 'up' else ''
                
                data_rows.append({
                    'ip': ip,
                    'state': state,
                    'state_class': state_class
                })
            
            if host_count == 0:
                return f"""
                <div class='scan-container'>
                    {css}
                    <div class="no-results">没有找到存活主机</div>
                </div>
                """
                
            # 使用通用渲染方法生成HTML
            return NmapOutputParser._render_html_results(title, headers, data_rows)
        else:
            # 文本格式的输出
            result_text = "存活扫描结果: \n"
            host_found = False
            
            for host in root.findall('.//host'):
                host_found = True
                ip = host.find('address').get('addr')
                status = host.find('.//status')
                state = status.get('state') if status is not None else '未知'
                result_text += f"存活主机：{ip} (状态: {state})\n"
            
            if not host_found:
                result_text += "未找到存活主机\n"
                
            return result_text
    
    @staticmethod
    def _parse_service_scan(root, html_format=True):
        """解析服务识别结果"""
        if html_format:
            # 获取通用CSS样式
            css = NmapOutputParser._get_common_css()
            
            # HTML格式的现代化输出
            html_output = []
            host_count = 0
            
            for host in root.findall('.//host'):
                host_count += 1
                ip = host.find('address').get('addr')
                ports_data = []
                port_count = 0
                
                for port in host.findall('.//port'):
                    port_count += 1
                    port_id = port.get('portid')
                    state = port.find('state').get('state')
                    state_class = NmapOutputParser._get_state_class(state)
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else '未知服务'
                    service_product = service.get('product') if service is not None and 'product' in service.attrib else '未知产品'
                    service_version = service.get('version') if service is not None and 'version' in service.attrib else '未知版本'
                    
                    # 为服务类型添加颜色编码
                    service_class = NmapOutputParser._get_service_class(service_name)
                    
                    ports_data.append({
                        'port': port_id,
                        'state': state,
                        'state_class': state_class,
                        'service': service_name,
                        'product': service_product,
                        'version': service_version,
                        'class': service_class
                    })
                
                # 生成HTML表格
                if port_count > 0:
                    html_output.append(f"""
                    <div class="host-section">
                        <h3 class="host-title">主机：{ip}</h3>
                        <table class="scan-results">
                            <thead>
                                <tr>
                                    <th class="col-port">端口</th>
                                    <th class="col-state">状态</th>
                                    <th class="col-service">服务</th>
                                    <th class="col-product">产品</th>
                                    <th class="col-version">版本</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join([f'''
                                <tr class="{p['class']}">
                                    <td>{ip}:{p['port']}</td>
                                    <td class="{p['state_class']}">{p['state']}</td>
                                    <td>{p['service']}</td>
                                    <td>{p['product']}</td>
                                    <td>{p['version']}</td>
                                </tr>''' for p in ports_data])}
                            </tbody>
                        </table>
                    </div>
                    """)
                else:
                    html_output.append(f"""
                    <div class="host-section">
                        <h3 class="host-title">主机：{ip}</h3>
                        <div class="no-results">没有发现开放的端口</div>
                    </div>
                    """)
            
            # 如果没有找到主机
            if host_count == 0:
                html_output = [f"""
                <div class="no-results">没有找到主机或所有主机都没有响应</div>
                """]
            
            return f"<div class='scan-container'>{css}{''.join(html_output)}</div>"
        else:
            # 文本格式 (原始)
            result_text = "扫描结果: \n"
            for host in root.findall('.//host'):
                ip = host.find('address').get('addr')
                result_text += f"主机：{ip}\n"
                has_ports = False
                
                for port in host.findall('.//port'):
                    has_ports = True
                    port_id = port.get('portid')
                    state = port.find('state').get('state')
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else '未知服务'
                    service_product = service.get('product') if service is not None and 'product' in service.attrib else '未知产品'
                    service_version = service.get('version') if service is not None and 'version' in service.attrib else '未知版本'
                    result_text += f"{ip}:{port_id}---{service_name}---{service_product}---{service_version}\n"
                
                if not has_ports:
                    result_text += "没有发现开放的端口\n"
            
            return result_text
            
    @staticmethod
    def _get_common_css():
        """返回通用的CSS样式，用于所有扫描结果的呈现"""
        return """
        <style>
            /* 全局样式 */
            .scan-container {
                font-family: 'Arial', 'Helvetica', sans-serif;
                margin: 0;
                padding: 0;
                width: 100%;
                color: #cdd6f4;
            }
            
            /* 主机部分 */
            .host-section {
                margin-bottom: 30px;
                background-color: #313244;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            
            /* 主机标题 */
            .host-title {
                background-color: #1e1e2e;
                color: #cdd6f4;
                padding: 15px 20px;
                margin: 0;
                font-size: 16px;
                font-weight: bold;
                border-bottom: 2px solid #45475a;
            }
            
            /* 表格样式 */
            .scan-results {
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
                box-sizing: border-box;
            }
            
            /* 表头 */
            .scan-results thead {
                background-color: #45475a;
            }
            
            .scan-results th {
                padding: 12px 15px;
                text-align: left;
                font-weight: 600;
                font-size: 14px;
                color: #cdd6f4;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            /* 表格单元格 */
            .scan-results td {
                padding: 10px 15px;
                border-bottom: 1px solid #45475a;
                font-size: 14px;
                color: #cdd6f4;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            /* 奇偶行样式 */
            .scan-results tr:nth-child(even) {
                background-color: #313244;
            }
            
            .scan-results tr:nth-child(odd) {
                background-color: #1e1e2e;
            }
            
            /* 鼠标悬停效果 */
            .scan-results tr:hover {
                background-color: #45475a !important;
            }
            
            /* 服务类型颜色 */
            tr.service-http td:nth-child(3) {
                color: #74c7ec; /* 蓝色 - HTTP/HTTPS */
                font-weight: bold;
            }
            
            tr.service-ssh td:nth-child(3) {
                color: #f9e2af; /* 黄色 - SSH/Telnet */
                font-weight: bold;
            }
            
            tr.service-ftp td:nth-child(3) {
                color: #a6e3a1; /* 绿色 - FTP */
                font-weight: bold;
            }
            
            tr.service-database td:nth-child(3) {
                color: #cba6f7; /* 紫色 - 数据库 */
                font-weight: bold;
            }
            
            tr.service-critical td:nth-child(3) {
                color: #f38ba8; /* 红色 - 危险服务 */
                font-weight: bold;
            }
            
            /* 端口列宽度 */
            .scan-results .col-port {
                width: 25%;
            }
            
            /* 状态列宽度 */
            .scan-results .col-state {
                width: 15%;
            }
            
            /* 服务列宽度 */
            .scan-results .col-service {
                width: 20%;
            }
            
            /* 产品列宽度 */
            .scan-results .col-product {
                width: 25%;
            }
            
            /* 版本列宽度 */
            .scan-results .col-version {
                width: 15%;
            }
            
            /* 空结果提示 */
            .no-results {
                padding: 30px;
                text-align: center;
                font-style: italic;
                color: #cdd6f4;
                background-color: #313244;
                border-radius: 10px;
            }
            
            /* 设置所有列的基本宽度并支持自适应 */
            .scan-results th, .scan-results td {
                min-width: 100px; /* 最小宽度 */
                max-width: 300px; /* 最大宽度 */
            }
            
            /* 安全状态颜色指示器 */
            .status-open {
                color: #f38ba8; /* 红色表示开放状态 */
                font-weight: bold;
            }
            
            .status-closed {
                color: #a6e3a1; /* 绿色表示关闭状态 */
            }
            
            .status-filtered {
                color: #f9e2af; /* 黄色表示过滤状态 */
            }
        </style>
        """
        
    @staticmethod
    def _get_service_class(service_name):
        """根据服务名称生成相应的CSS类"""
        service_name = service_name.lower()
        
        if service_name in ['http', 'https']:
            return 'service-http'
        elif service_name in ['ssh', 'telnet']:
            return 'service-ssh'
        elif service_name in ['ftp', 'sftp', 'ftps']:
            return 'service-ftp'
        elif service_name in ['mysql', 'mssql', 'oracle', 'postgresql', 'mongodb', 'redis']:
            return 'service-database'
        elif service_name in ['rtsp', 'sip']:
            return 'service-critical'
        else:
            return 'service-unknown'
            
    @staticmethod
    def _get_state_class(state):
        """根据端口状态生成相应的CSS类"""
        state = state.lower()
        
        if state == 'open':
            return 'status-open'
        elif state == 'closed':
            return 'status-closed'
        elif state == 'filtered':
            return 'status-filtered'
        else:
            return ''
    
    @staticmethod
    def _parse_os_scan(root, html_format=True):
        """解析系统识别结果"""
        if html_format:
            # 获取通用CSS样式
            css = NmapOutputParser._get_common_css()
            
            # 准备标题和数据
            title = "系统识别结果"
            headers = [
                {'name': 'IP地址', 'class': 'col-ip', 'key': 'ip'},
                {'name': '操作系统', 'class': 'col-os', 'key': 'os'},
                {'name': '准确度', 'class': 'col-accuracy', 'key': 'accuracy'}
            ]
            
            data_rows = []
            host_count = 0
            
            for host in root.findall('.//host'):
                host_count += 1
                ip = host.find('address').get('addr')
                os_matches = host.findall('.//osmatch')
                
                if not os_matches:
                    # 如果没有OS匹配结果
                    data_rows.append({
                        'ip': ip,
                        'os': '未知',
                        'accuracy': '0%'
                    })
                else:
                    # 取前三个匹配结果
                    for os_match in os_matches[:3]:
                        os_name = os_match.get('name')
                        accuracy = os_match.get('accuracy') + '%'
                        
                        # 根据准确度设置颜色类别
                        accuracy_class = ''
                        try:
                            acc_value = int(os_match.get('accuracy'))
                            if acc_value >= 90:
                                accuracy_class = 'status-high-confidence'
                            elif acc_value >= 70:
                                accuracy_class = 'status-medium-confidence'
                            else:
                                accuracy_class = 'status-low-confidence'
                        except (ValueError, TypeError):
                            pass
                        
                        data_rows.append({
                            'ip': ip,
                            'os': os_name,
                            'accuracy': accuracy,
                            'accuracy_class': accuracy_class
                        })
            
            if host_count == 0:
                return f"""
                <div class='scan-container'>
                    {css}
                    <div class="no-results">没有找到主机或没有系统识别信息</div>
                </div>
                """
                
            # 使用通用渲染方法生成HTML
            return NmapOutputParser._render_html_results(title, headers, data_rows)
        else:
            # 文本格式的输出
            result_text = "系统识别结果: \n"
            hosts = []
            for host in root.findall('.//host'):
                ip = host.find('address').get('addr')
                os_matches = host.findall('.//osmatch')
                if not os_matches:
                    hosts.append(f"{ip} (未知系统)\n")
                else:
                    for os_match in os_matches[:3]:  # 只取前三个匹配结果
                        hosts.append(f"{ip} ({os_match.get('name')} (准确度: {os_match.get('accuracy')}%))\n")
            if hosts:
                result_text += "\n".join(hosts)
            else:
                result_text += "没有找到系统识别信息\n"
            return result_text
    
    @staticmethod
    def _parse_port_scan(root, html_format=True):
        """解析端口识别结果"""
        if html_format:
            # 获取通用CSS样式
            css = NmapOutputParser._get_common_css()
            
            # 准备标题和数据
            title = "端口扫描结果"
            headers = [
                {'name': '端口', 'class': 'col-port', 'key': 'port'},
                {'name': '状态', 'class': 'col-state', 'key': 'state'},
                {'name': '服务', 'class': 'col-service', 'key': 'service'},
                {'name': '产品', 'class': 'col-product', 'key': 'product'},
                {'name': '版本', 'class': 'col-version', 'key': 'version'}
            ]
            
            html_output = []
            host_count = 0
            
            for host in root.findall('.//host'):
                host_count += 1
                ip = host.find('address').get('addr')
                ports_data = []
                port_count = 0
                
                for port in host.findall('.//port'):
                    port_count += 1
                    port_id = port.get('portid')
                    state = port.find('state').get('state')
                    state_class = NmapOutputParser._get_state_class(state)
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else '未知服务'
                    service_product = service.get('product') if service is not None and 'product' in service.attrib else '未知产品'
                    service_version = service.get('version') if service is not None and 'version' in service.attrib else '未知版本'
                    
                    # 为服务类型添加颜色编码
                    service_class = NmapOutputParser._get_service_class(service_name)
                    
                    ports_data.append({
                        'port': f"{ip}:{port_id}",
                        'state': state,
                        'state_class': state_class,
                        'service': service_name,
                        'product': service_product,
                        'version': service_version,
                        'class': service_class
                    })
                
                # 生成每个主机的数据行
                data_rows = ports_data
                
                # 使用通用渲染方法生成HTML
                host_html = NmapOutputParser._render_html_results(
                    f"主机：{ip}", 
                    headers, 
                    data_rows,
                    f"<div class='host-section'></div>"
                )
                
                html_output.append(host_html)
            
            # 如果没有找到主机
            if host_count == 0:
                return f"""
                <div class='scan-container'>
                    {css}
                    <div class="no-results">没有找到主机或所有主机都没有响应</div>
                </div>
                """
            
            return f"<div class='scan-container'>{css}{''.join(html_output)}</div>"
        else:
            # 文本格式的输出
            result_text = "端口扫描结果: \n"
            host_found = False
            
            for host in root.findall('.//host'):
                host_found = True
                ip = host.find('address').get('addr')
                result_text += f"主机：{ip}\n"
                port_found = False
                
                for port in host.findall('.//port'):
                    port_found = True
                    port_id = port.get('portid')
                    state = port.find('state').get('state')
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else '未知服务'
                    service_product = service.get('product') if service is not None and 'product' in service.attrib else '未知产品'
                    service_version = service.get('version') if service is not None and 'version' in service.attrib else '未知版本'
                    result_text += f"{ip}:{port_id} - {state} - {service_name} - {service_product} - {service_version}\n"
                
                if not port_found:
                    result_text += "没有发现开放的端口\n"
            
            if not host_found:
                result_text += "未找到主机\n"
                
            return result_text
    
    @staticmethod
    def _parse_brute_force_scan(root, html_format=True):
        """解析暴力破解结果"""
        if html_format:
            # 获取通用CSS样式
            css = NmapOutputParser._get_common_css()
            
            # 准备标题和数据
            title = "暴力破解扫描结果"
            headers = [
                {'name': 'IP地址', 'class': 'col-ip', 'key': 'ip'},
                {'name': '端口', 'class': 'col-port', 'key': 'port'},
                {'name': '服务', 'class': 'col-service', 'key': 'service'},
                {'name': '脚本', 'class': 'col-script', 'key': 'script'},
                {'name': '结果', 'class': 'col-output', 'key': 'output'}
            ]
            
            data_rows = []
            host_count = 0
            result_count = 0
            
            for host in root.findall('.//host'):
                host_count += 1
                ip = host.find('address').get('addr')
                
                for port in host.findall('.//port'):
                    port_id = port.get('portid')
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else '未知服务'
                    
                    for script in port.findall('.//script'):
                        script_id = script.get('id')
                        output = script.get('output')
                        
                        # 判断是否有结果
                        has_result = False
                        row_class = ''
                        
                        # 检查是否有table元素（通常包含有效凭据）
                        accounts_table = script.find('.//table[@key="Accounts"]')
                        if accounts_table is not None:
                            # 有账户表，说明发现了有效凭据
                            has_result = True
                            row_class = 'brute-force-success'
                            # 提取账户信息并格式化输出
                            creds = []
                            for account in accounts_table.findall('.//table'):
                                username = account.find('./elem[@key="username"]')
                                password = account.find('./elem[@key="password"]')
                                state = account.find('./elem[@key="state"]')
                                if username is not None and password is not None:
                                    creds.append(f"{username.text}:{password.text} - {state.text if state is not None else 'Valid'}")
                            
                            if creds:
                                output = "有效凭据: " + ", ".join(creds)
                        
                        # 检查其他结果类型
                        elif output:
                            # 判断是否包含关键词
                            keywords = ["密码", "password", "successful", "Valid credentials", "valid"]
                            if any(keyword.lower() in output.lower() for keyword in keywords):
                                has_result = True
                                row_class = 'brute-force-success'
                            # 判断是否为拒绝认证
                            elif "authentication not allowed" in output.lower():
                                has_result = True
                                row_class = 'brute-force-error'
                            # 判断是否为错误信息但仍需显示
                            elif "error" in output.lower() or "failed" in output.lower() or "rejected" in output.lower():
                                has_result = True
                                row_class = 'brute-force-error'
                        
                        if has_result:
                            result_count += 1
                            data_rows.append({
                                'ip': ip,
                                'port': port_id,
                                'service': service_name,
                                'script': script_id,
                                'output': output.replace('\n', '<br>') if output else "未知结果",
                                'class': row_class
                            })
            
            if host_count == 0 or result_count == 0:
                return f"""
                <div class='scan-container'>
                    {css}
                    <div class="no-results">没有找到破解结果</div>
                </div>
                """
                
            # 使用通用渲染方法生成HTML
            return NmapOutputParser._render_html_results(title, headers, data_rows)
        else:
            # 文本格式的输出
            result_text = "暴力破解扫描结果: \n"
            host_found = False
            result_found = False
            
            for host in root.findall('.//host'):
                host_found = True
                ip = host.find('address').get('addr')
                host_results = []
                
                for port in host.findall('.//port'):
                    port_id = port.get('portid')
                    service = port.find('service')
                    service_name = service.get('name') if service is not None else '未知服务'
                    
                    for script in port.findall('.//script'):
                        script_id = script.get('id')
                        output = script.get('output')
                        
                        # 判断是否有结果
                        has_result = False
                        
                        # 检查是否有table元素（通常包含有效凭据）
                        accounts_table = script.find('.//table[@key="Accounts"]')
                        if accounts_table is not None:
                            # 有账户表，说明发现了有效凭据
                            has_result = True
                            # 提取账户信息并格式化输出
                            creds = []
                            for account in accounts_table.findall('.//table'):
                                username = account.find('./elem[@key="username"]')
                                password = account.find('./elem[@key="password"]')
                                state = account.find('./elem[@key="state"]')
                                if username is not None and password is not None:
                                    creds.append(f"{username.text}:{password.text} - {state.text if state is not None else 'Valid'}")
                            
                            if creds:
                                output = "有效凭据: " + ", ".join(creds)
                        
                        # 检查其他结果类型
                        elif output:
                            # 判断是否包含关键词
                            keywords = ["密码", "password", "successful", "Valid credentials", "valid"]
                            if any(keyword.lower() in output.lower() for keyword in keywords):
                                has_result = True
                            # 判断是否为拒绝认证或其他有意义的结果
                            elif "authentication not allowed" in output.lower() or "error" in output.lower():
                                has_result = True
                        
                        if has_result:
                            result_found = True
                            host_results.append(f"端口: {port_id} | 服务: {service_name} | 脚本: {script_id} | 输出: {output}")
                
                if host_results:
                    result_text += f"主机: {ip}\n"
                    result_text += "\n".join(host_results) + "\n\n"
            
            if not host_found:
                result_text += "未找到主机\n"
            elif not result_found:
                result_text += "未发现可破解的账号\n"
                
            return result_text
    
    @staticmethod
    def _parse_vulnerability_scan(root, html_format=True):
        """解析漏洞扫描结果"""
        if html_format:
            # 获取通用CSS样式
            css = NmapOutputParser._get_common_css()
            
            # 准备标题和数据
            title = "漏洞扫描结果"
            headers = [
                {'name': 'IP地址', 'class': 'col-ip', 'key': 'ip'},
                {'name': '漏洞名称', 'class': 'col-vuln-name', 'key': 'name'},
                {'name': '风险级别', 'class': 'col-risk-level', 'key': 'risk_level'},
                {'name': '详细信息', 'class': 'col-vuln-info', 'key': 'info'}
            ]
            
            data_rows = []
            host_count = 0
            vuln_count = 0
            
            # 查看是否有预脚本输出
            prescript_output = ""
            prescript = root.find('prescript')
            if prescript is not None and prescript.get('output'):
                prescript_output = prescript.get('output').replace('&#xa;', '<br>')
            
            for host in root.findall('.//host'):
                host_count += 1
                ip = host.find('address').get('addr')
                
                # 先查找 script 标签中的漏洞信息
                for port in host.findall('.//port'):
                    port_id = port.get('portid')
                    
                    for script in port.findall('.//script'):
                        if 'vulns' in script.get('id', ''):
                            vuln_count += 1
                            script_id = script.get('id')
                            output = script.get('output')
                            
                            # 确定风险级别
                            risk_level = '中危'
                            risk_class = 'risk-medium'
                            if 'HIGH' in output or 'CRITICAL' in output:
                                risk_level = '高危'
                                risk_class = 'risk-high'
                            elif 'LOW' in output:
                                risk_level = '低危'
                                risk_class = 'risk-low'
                            
                            data_rows.append({
                                'ip': f"{ip}:{port_id}",
                                'name': script_id,
                                'risk_level': risk_level,
                                'risk_level_class': risk_class,
                                'info': output.replace('\n', '<br>')
                            })
                
                # 然后查找 vuln 标签
                for vuln in host.findall('.//vuln'):
                    vuln_count += 1
                    vuln_name = vuln.get('name', '未知漏洞')
                    vuln_info = vuln.get('info', '无详细信息')
                    
                    # 确定风险级别
                    risk_level = '中危'
                    risk_class = 'risk-medium'
                    
                    # 根据漏洞名称或信息判断风险级别
                    vuln_text = (vuln_name + vuln_info).lower()
                    if 'critical' in vuln_text or 'high' in vuln_text:
                        risk_level = '高危'
                        risk_class = 'risk-high'
                    elif 'low' in vuln_text:
                        risk_level = '低危'
                        risk_class = 'risk-low'
                    
                    data_rows.append({
                        'ip': ip,
                        'name': vuln_name,
                        'risk_level': risk_level,
                        'risk_level_class': risk_class,
                        'info': vuln_info
                    })
            
            # 生成输出
            if prescript_output:
                extra_html = f"<div class='prescript-output'>{prescript_output}</div>"
            else:
                extra_html = ""
                
            if host_count == 0 or vuln_count == 0:
                return f"""
                <div class='scan-container'>
                    {css}
                    {extra_html}
                    <div class="no-results">没有发现漏洞</div>
                </div>
                """
                
            # 使用通用渲染方法生成HTML
            return NmapOutputParser._render_html_results(title, headers, data_rows, extra_html)
        else:
            # 文本格式的输出
            result_text = "漏洞扫描结果: \n"
            
            # 查看是否有预脚本输出
            prescript = root.find('prescript')
            if prescript is not None and prescript.get('output'):
                result_text += prescript.get('output').replace('&#xa;', '\n') + '\n'
            
            host_found = False
            vuln_found = False
            
            for host in root.findall('.//host'):
                host_found = True
                ip = host.find('address').get('addr')
                host_vulns = []
                
                # 先查找 script 标签中的漏洞信息
                for port in host.findall('.//port'):
                    port_id = port.get('portid')
                    
                    for script in port.findall('.//script'):
                        if 'vulns' in script.get('id', ''):
                            vuln_found = True
                            script_id = script.get('id')
                            output = script.get('output')
                            host_vulns.append(f"端口: {port_id} | 脚本: {script_id} | 输出: {output}")
                
                # 然后查找 vuln 标签
                for vuln in host.findall('.//vuln'):
                    vuln_found = True
                    vuln_name = vuln.get('name', '未知漏洞')
                    vuln_info = vuln.get('info', '无详细信息')
                    host_vulns.append(f"漏洞: {vuln_name} | 信息: {vuln_info}")
                
                if host_vulns:
                    result_text += f"主机: {ip}\n"
                    result_text += "\n".join(host_vulns) + "\n\n"
            
            if not host_found:
                result_text += "未找到主机\n"
            elif not vuln_found:
                result_text += "未发现漏洞\n"
                
            return result_text
