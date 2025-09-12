"""
资产监控模块，负责定时扫描、结果存储和差异对比
"""

import os
import json
import time
import threading
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from src.core.command_builder import NmapCommandBuilder
from src.core.nmap_executor import NmapThread


class AssetMonitor(QObject):
    """
    资产监控类，负责定时扫描和结果比较
    """
    # 信号定义
    scan_completed = pyqtSignal(dict)  # 扫描完成信号
    scan_progress = pyqtSignal(str)    # 扫描进度信号
    scan_error = pyqtSignal(str)       # 扫描错误信号
    
    def __init__(self):
        super().__init__()
        self.monitor_configs = {}  # 监控配置存储
        self.monitor_results = {}  # 监控结果存储
        self.active_timers = {}    # 活动定时器存储
        self.data_dir = "monitor_data"  # 数据存储目录
        
        # 确保数据目录存在
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # 加载已保存的配置和结果
        self.load_configurations()
        
    def add_monitor_target(self, target_name: str, config: Dict) -> bool:
        """
        添加监控目标
        
        参数:
            target_name: 监控目标名称
            config: 监控配置字典
            
        返回:
            bool: 是否添加成功
        """
        try:
            # 验证配置
            required_fields = ['target', 'scan_type', 'interval_minutes']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"缺少必要字段: {field}")
            
            # 添加时间戳
            config['created_time'] = datetime.now().isoformat()
            config['last_scan_time'] = None
            config['enabled'] = True
            
            # 保存配置
            self.monitor_configs[target_name] = config
            self.monitor_results[target_name] = []
            
            # 保存到文件
            self.save_configurations()
            
            return True
        except Exception as e:
            self.scan_error.emit(f"添加监控目标失败: {str(e)}")
            return False
    
    def start_monitoring(self, target_name: str) -> bool:
        """
        开始监控指定目标
        
        参数:
            target_name: 监控目标名称
            
        返回:
            bool: 是否启动成功
        """
        if target_name not in self.monitor_configs:
            self.scan_error.emit(f"监控目标不存在: {target_name}")
            return False
            
        config = self.monitor_configs[target_name]
        if not config.get('enabled', True):
            self.scan_error.emit(f"监控目标已禁用: {target_name}")
            return False
            
        # 停止现有定时器
        self.stop_monitoring(target_name)
        
        # 创建新的定时器
        timer = QTimer()
        interval_ms = config['interval_minutes'] * 60 * 1000  # 转换为毫秒
        timer.timeout.connect(lambda: self._perform_scan(target_name))
        timer.start(interval_ms)
        
        self.active_timers[target_name] = timer
        
        # 立即执行一次扫描
        self._perform_scan(target_name)
        
        self.scan_progress.emit(f"开始监控 {target_name}，间隔 {config['interval_minutes']} 分钟")
        return True
    
    def stop_monitoring(self, target_name: str):
        """
        停止监控指定目标
        
        参数:
            target_name: 监控目标名称
        """
        if target_name in self.active_timers:
            self.active_timers[target_name].stop()
            del self.active_timers[target_name]
            self.scan_progress.emit(f"停止监控 {target_name}")
    
    def _perform_scan(self, target_name: str):
        """
        执行扫描
        
        参数:
            target_name: 监控目标名称
        """
        if target_name not in self.monitor_configs:
            return
            
        config = self.monitor_configs[target_name]
        
        # 构建扫描命令
        scan_config = {
            'target': config['target'],
            'timeout': config.get('timeout', '300'),
            'threads_min': config.get('threads', '50'),
            'threads_max': config.get('threads', '50'),
            'params': config.get('params', '-vvv'),
            'result_file': '',
            'scan_type': config['scan_type'],
            'fast_mode': config.get('fast_mode', False),
            'port_input': config.get('ports', '80,443,22,21,25,53,110,993,995,143,993'),
            'port_checkboxes': []
        }
        
        # 创建线程执行扫描
        thread = threading.Thread(target=self._execute_scan_thread, args=(target_name, scan_config))
        thread.daemon = True
        thread.start()
    
    def _execute_scan_thread(self, target_name: str, scan_config: Dict):
        """
        在线程中执行扫描
        
        参数:
            target_name: 监控目标名称
            scan_config: 扫描配置
        """
        try:
            self.scan_progress.emit(f"开始扫描 {target_name}...")
            
            # 构建命令
            command = NmapCommandBuilder.build_command(scan_config)
            if not command:
                self.scan_error.emit(f"构建扫描命令失败: {target_name}")
                return
            
            # 创建特定的输出文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.data_dir, f"{target_name}_{timestamp}.xml")
            
            # 修改命令中的输出文件
            if '-oX' in command:
                index = command.index('-oX')
                if index + 1 < len(command):
                    command[index + 1] = output_file
            
            # 执行扫描
            import subprocess
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            output = ""
            
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    output += line
            
            return_code = process.wait()
            
            if return_code == 0 and os.path.exists(output_file):
                # 解析结果
                scan_result = self._parse_scan_result(output_file, target_name)
                if scan_result:
                    # 保存结果
                    self._save_scan_result(target_name, scan_result)
                    
                    # 比较差异
                    differences = self._compare_with_previous(target_name, scan_result)
                    
                    # 更新最后扫描时间
                    self.monitor_configs[target_name]['last_scan_time'] = datetime.now().isoformat()
                    self.save_configurations()
                    
                    # 发送完成信号
                    self.scan_completed.emit({
                        'target_name': target_name,
                        'scan_result': scan_result,
                        'differences': differences,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    self.scan_progress.emit(f"扫描完成 {target_name}")
                else:
                    self.scan_error.emit(f"解析扫描结果失败: {target_name}")
            else:
                self.scan_error.emit(f"扫描执行失败: {target_name}, 返回码: {return_code}")
                
        except Exception as e:
            self.scan_error.emit(f"扫描异常: {target_name}, 错误: {str(e)}")
    
    def _parse_scan_result(self, xml_file: str, target_name: str) -> Optional[Dict]:
        """
        解析扫描结果XML文件
        
        参数:
            xml_file: XML文件路径
            target_name: 目标名称
            
        返回:
            解析后的结果字典
        """
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'target_name': target_name,
                'hosts': []
            }
            
            for host in root.findall('.//host'):
                host_info = {'ip': '', 'ports': [], 'status': 'unknown'}
                
                # 获取IP地址
                address = host.find('address')
                if address is not None:
                    host_info['ip'] = address.get('addr', '')
                
                # 获取主机状态
                status = host.find('status')
                if status is not None:
                    host_info['status'] = status.get('state', 'unknown')
                
                # 获取端口信息
                for port in host.findall('.//port'):
                    port_info = {
                        'port': port.get('portid', ''),
                        'protocol': port.get('protocol', 'tcp'),
                        'state': 'unknown',
                        'service': 'unknown',
                        'version': ''
                    }
                    
                    # 端口状态
                    port_state = port.find('state')
                    if port_state is not None:
                        port_info['state'] = port_state.get('state', 'unknown')
                    
                    # 服务信息
                    service = port.find('service')
                    if service is not None:
                        port_info['service'] = service.attrib.get('name', 'unknown')
                        port_info['version'] = service.attrib.get('version', '')
                    else:
                        port_info['service'] = 'unknown'
                        port_info['version'] = ''
                    
                    host_info['ports'].append(port_info)
                
                result['hosts'].append(host_info)
            
            return result
            
        except Exception as e:
            self.scan_error.emit(f"解析XML文件失败: {str(e)}")
            return None
    
    def _save_scan_result(self, target_name: str, result: Dict):
        """
        保存扫描结果
        
        参数:
            target_name: 目标名称
            result: 扫描结果
        """
        if target_name not in self.monitor_results:
            self.monitor_results[target_name] = []
            
        self.monitor_results[target_name].append(result)
        
        # 只保留最近50次扫描结果
        if len(self.monitor_results[target_name]) > 50:
            self.monitor_results[target_name] = self.monitor_results[target_name][-50:]
        
        # 保存到文件
        result_file = os.path.join(self.data_dir, f"{target_name}_history.json")
        try:
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(self.monitor_results[target_name], f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.scan_error.emit(f"保存结果文件失败: {str(e)}")
    
    def _compare_with_previous(self, target_name: str, current_result: Dict) -> Dict:
        """
        与上次扫描结果比较
        
        参数:
            target_name: 目标名称
            current_result: 当前扫描结果
            
        返回:
            差异字典
        """
        differences = {
            'new_hosts': [],
            'disappeared_hosts': [],
            'new_ports': [],
            'disappeared_ports': [],
            'changed_services': []
        }
        
        if target_name not in self.monitor_results or len(self.monitor_results[target_name]) == 0:
            # 第一次扫描，所有都是新的
            for host in current_result['hosts']:
                if host.get('status') == 'up':
                    differences['new_hosts'].append(host['ip'])
                for port in host['ports']:
                    if port['state'] == 'open':
                        differences['new_ports'].append(f"{host['ip']}:{port['port']}")
            return differences
        
        # 获取上一次扫描结果（比较时要排除当前结果）
        if len(self.monitor_results[target_name]) >= 2:
            previous_result = self.monitor_results[target_name][-2]  # 上一次的结果
        else:
            # 如果只有一次扫描，视为第一次扫描
            for host in current_result['hosts']:
                if host.get('status') == 'up':
                    differences['new_hosts'].append(host['ip'])
                for port in host['ports']:
                    if port['state'] == 'open':
                        differences['new_ports'].append(f"{host['ip']}:{port['port']}")
            return differences
        
        # 构建主机和端口集合
        current_hosts = {host['ip']: host for host in current_result['hosts']}
        previous_hosts = {host['ip']: host for host in previous_result['hosts']}
        
        # 比较主机
        current_host_ips = set(current_hosts.keys())
        previous_host_ips = set(previous_hosts.keys())
        
        differences['new_hosts'] = list(current_host_ips - previous_host_ips)
        differences['disappeared_hosts'] = list(previous_host_ips - current_host_ips)
        
        # 比较端口
        for ip in current_host_ips & previous_host_ips:
            current_host = current_hosts[ip]
            previous_host = previous_hosts[ip]
            
            # 构建端口集合
            current_ports = {f"{port['port']}/{port['protocol']}": port 
                           for port in current_host['ports'] if port['state'] == 'open'}
            previous_ports = {f"{port['port']}/{port['protocol']}": port 
                            for port in previous_host['ports'] if port['state'] == 'open'}
            
            current_port_keys = set(current_ports.keys())
            previous_port_keys = set(previous_ports.keys())
            
            # 新增端口
            for port_key in current_port_keys - previous_port_keys:
                differences['new_ports'].append(f"{ip}:{port_key}")
            
            # 消失端口
            for port_key in previous_port_keys - current_port_keys:
                differences['disappeared_ports'].append(f"{ip}:{port_key}")
            
            # 服务变化
            for port_key in current_port_keys & previous_port_keys:
                current_port = current_ports[port_key]
                previous_port = previous_ports[port_key]
                
                if current_port['service'] != previous_port['service'] or \
                   current_port['version'] != previous_port['version']:
                    differences['changed_services'].append({
                        'host': ip,
                        'port': port_key,
                        'old_service': f"{previous_port['service']} {previous_port['version']}".strip(),
                        'new_service': f"{current_port['service']} {current_port['version']}".strip()
                    })
        
        return differences
    
    def get_monitor_targets(self) -> Dict:
        """
        获取所有监控目标
        
        返回:
            监控配置字典
        """
        return self.monitor_configs
    
    def get_target_history(self, target_name: str, limit: int = 10) -> List[Dict]:
        """
        获取目标的历史扫描结果
        
        参数:
            target_name: 目标名称
            limit: 返回记录数限制
            
        返回:
            历史记录列表
        """
        if target_name not in self.monitor_results:
            return []
        
        history = self.monitor_results[target_name]
        return history[-limit:] if len(history) > limit else history
    
    def delete_monitor_target(self, target_name: str) -> bool:
        """
        删除监控目标
        
        参数:
            target_name: 目标名称
            
        返回:
            是否删除成功
        """
        try:
            # 停止监控
            self.stop_monitoring(target_name)
            
            # 删除配置和结果
            if target_name in self.monitor_configs:
                del self.monitor_configs[target_name]
            if target_name in self.monitor_results:
                del self.monitor_results[target_name]
            
            # 删除历史文件
            result_file = os.path.join(self.data_dir, f"{target_name}_history.json")
            if os.path.exists(result_file):
                os.remove(result_file)
            
            # 保存配置
            self.save_configurations()
            
            return True
        except Exception as e:
            self.scan_error.emit(f"删除监控目标失败: {str(e)}")
            return False
    
    def save_configurations(self):
        """保存监控配置到文件"""
        config_file = os.path.join(self.data_dir, "monitor_configs.json")
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.monitor_configs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.scan_error.emit(f"保存配置失败: {str(e)}")
    
    def load_configurations(self):
        """从文件加载监控配置"""
        config_file = os.path.join(self.data_dir, "monitor_configs.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self.monitor_configs = json.load(f)
            except Exception as e:
                self.scan_error.emit(f"加载配置失败: {str(e)}")
        
        # 加载历史结果
        for target_name in self.monitor_configs.keys():
            result_file = os.path.join(self.data_dir, f"{target_name}_history.json")
            if os.path.exists(result_file):
                try:
                    with open(result_file, 'r', encoding='utf-8') as f:
                        self.monitor_results[target_name] = json.load(f)
                except Exception as e:
                    self.scan_error.emit(f"加载历史结果失败: {str(e)}")
                    self.monitor_results[target_name] = []
            else:
                self.monitor_results[target_name] = [] 