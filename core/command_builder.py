"""
命令构建模块，负责构建Nmap命令
"""

import os
import sys
import shutil
from nmap_modular.utils.constants import PORT_GROUPS, OUTPUT_FORMAT_MAP

class NmapCommandBuilder:
    """
    用于构建Nmap命令的类
    """
    
    @staticmethod
    def build_command(config):
        """
        根据配置构建Nmap命令
        
        参数:
            config: 包含扫描配置的字典
            
        返回:
            构建好的命令列表
        """
        target = config.get('target', '')
        timeout = config.get('timeout', '')
        threads_min = config.get('threads_min', '')
        threads_max = config.get('threads_max', '')
        params = config.get('params', '')
        result_file = config.get('result_file', '')
        scan_type = config.get('scan_type', '')
        fast_mode = config.get('fast_mode', False)
        port_input = config.get('port_input', '')
        port_checkboxes = config.get('port_checkboxes', [])
        
        # 创建日志目录
        logs_dir = 'logs'
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # 构建输出文件名
        output_filename = f"{scan_type}_ScanCacheLog.xml"
        output_file_path = os.path.join(logs_dir, output_filename)

        # 根据操作系统选择正确的nmap路径
        if sys.platform == 'win32':
            # 先检查相对路径是否存在
            relative_nmap_path = '.\\nmap\\nmap.exe'
            if os.path.isfile(relative_nmap_path) and os.access(relative_nmap_path, os.X_OK):
                nmap_path = relative_nmap_path
            else:
                # 检查是否已在系统中安装
                system_nmap = shutil.which('nmap')
                if system_nmap:
                    nmap_path = system_nmap
                else:
                    # 尝试常见安装位置
                    common_win_paths = [
                        'C:\\Program Files (x86)\\Nmap\\nmap.exe',
                        'C:\\Program Files\\Nmap\\nmap.exe'
                    ]
                    for path in common_win_paths:
                        if os.path.isfile(path) and os.access(path, os.X_OK):
                            nmap_path = path
                            break
                    else:
                        # 如果都找不到，还是用相对路径，后续可能会报错
                        nmap_path = relative_nmap_path
        elif sys.platform == 'darwin':
            # macOS上的非常规处理
            # 直接检查常见的nmap二进制路径
            possible_paths = [
                '/Applications/nmap.app/Contents/Resources/bin/nmap',  # 标准安装位置
                '/usr/local/bin/nmap',  # homebrew安装位置
                '/opt/homebrew/bin/nmap',  # M1/M2 Mac homebrew安装位置
                '/usr/bin/nmap',  # 其他可能的系统位置
            ]
            
            # 首先查找shutil.which找到的路径
            system_nmap = shutil.which('nmap')
            if system_nmap:
                nmap_path = system_nmap
            else:
                # 如果找不到，逐个检查可能的路径
                for path in possible_paths:
                    if os.path.isfile(path) and os.access(path, os.X_OK):
                        nmap_path = path
                        break
                else:
                    # 如果所有路径都无效，默认使用系统命令
                    nmap_path = 'nmap'
        else:  # Linux和其他系统
            system_nmap = shutil.which('nmap')
            if system_nmap:
                nmap_path = system_nmap
            else:
                nmap_path = '/usr/bin/nmap'  # 大多数Linux系统的默认位置
                
        cmd = [nmap_path, '--min-parallelism', threads_min]
        
        # 添加超时参数
        if timeout:
            cmd.extend(['--host-timeout', f'{timeout}s'])
            
        # 添加结果文件参数
        if result_file:
            _, file_extension = os.path.splitext(result_file)
            output_param = OUTPUT_FORMAT_MAP.get(file_extension, '-oN')
            cmd.extend([output_param, result_file])
                
        # 添加快速模式参数
        if fast_mode:
            cmd.extend(['-n', '--unique', '--min-hostgroup', '512', '--min-parallelism', '10', '--host-timeout', '10m', '--script-timeout', '3m'])
            
        # 添加用户自定义参数
        if params:
            user_params = params.split()
            cmd.extend(user_params)

        # 根据扫描类型添加特定参数
        if scan_type == '存活扫描':
            cmd.extend(['-sP', '-PU', '--disable-arp-ping'])
        else:
            # 添加端口参数
            if scan_type not in ['存活扫描', '系统识别', '端口识别']:
                if any(checkbox.isChecked() for checkbox in port_checkboxes):
                    ports = NmapCommandBuilder._get_selected_ports(port_checkboxes)
                    if ports:
                        cmd.extend(['-p', ','.join(map(str, ports))])
                else:
                    cmd.extend(['-p', port_input])
            
            # 添加排除打印机端口参数
            for checkbox in port_checkboxes:
                if checkbox.isChecked() and '排除打印机' in checkbox.text():
                    cmd.extend(['--exclude-ports', '515,631,9100,9101,9102'])
            
            # 根据扫描类型添加特定参数
            if scan_type == '默认扫描':
                cmd.extend(['-vvv', '-T4', '-sS', '-open'])
            elif scan_type == '服务识别':
                cmd.extend(['-vvv', '-sV', '-open'])
            elif scan_type == '系统识别':
                cmd.extend(['-vvv', '-O'])
            elif scan_type == '端口识别':
                # 处理Web扫描输入
                targets = NmapCommandBuilder._process_web_scan_input(target)
                if targets is None:
                    return None
                
                # 将所有的端口合并到一个-p参数中
                ports = [port for _, port in targets]
                unique_ips = list(set([ip for ip, _ in targets]))
                
                # 为每个唯一的IP地址添加-p参数和IP地址
                for ip in unique_ips:
                    cmd.append(ip)
                cmd.extend(['-vvv', '-sV', '-open', '-p', ','.join(ports)])
            elif scan_type == '暴力破解':
                # 获取当前工作目录的上级目录中的dict目录的绝对路径
                dict_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dict'))
                
                cmd.extend([
                    '--script=telnet-brute',
                    f'--script-args=userdb={dict_dir}/telnet_user.txt,passdb={dict_dir}/telnet_pass.txt,telnet-brute.timeout=5s',
                    '--script=ssh-brute',
                    f'--script-args=userdb={dict_dir}/ssh_user.txt,passdb={dict_dir}/ssh_pass.txt,ssh-brute.timeout=5s',
                    '--script=smb-brute',
                    f'--script-args=userdb={dict_dir}/smb_user.txt,passdb={dict_dir}/smb_pass.txt,smb-brute.timeout=5s',
                    '--script=ms-sql-brute',
                    f'--script-args=userdb={dict_dir}/mssql_user.txt,passdb={dict_dir}/mssql_pass.txt,ms-sql-brute.timeout=5s',
                    '--script=mysql-brute',
                    f'--script-args=userdb={dict_dir}/mysql_user.txt,passdb={dict_dir}/mysql_pass.txt,mysql-brute.timeout=5s',
                    '--script=oracle-brute',
                    f'--script-args=userdb={dict_dir}/oracle_user.txt,passdb={dict_dir}/oracle_pass.txt,oracle-brute.timeout=5s',
                    '--script=vnc-brute',
                    f'--script-args=userdb={dict_dir}/vnc_user.txt,passdb={dict_dir}/vnc_pass.txt,vnc-brute.timeout=5s',
                    '--script=mongodb-brute',
                    f'--script-args=userdb={dict_dir}/mongodb_user.txt,passdb={dict_dir}/mongodb_pass.txt,mongodb-brute.timeout=5s',
                    '--script=redis-brute',
                    f'--script-args=userdb={dict_dir}/redis_user.txt,passdb={dict_dir}/redis_pass.txt,redis-brute.timeout=5s',
                    '--script=ftp-brute',
                    f'--script-args=userdb={dict_dir}/ftp_user.txt,passdb={dict_dir}/ftp_pass.txt,ftp-brute.timeout=5s'
                ])
            elif scan_type == '漏洞扫描':
                cmd.extend(['-vvv', '--script', 'vuln'])

        # 添加目标和输出文件参数
        if scan_type != '端口识别':  # 端口识别模式已经添加了目标
            cmd.append(target)
        cmd.extend(['-oX', output_file_path])
        
        return cmd
    
    @staticmethod
    def _get_selected_ports(port_checkboxes):
        """
        获取选中的端口
        
        参数:
            port_checkboxes: 端口复选框列表
            
        返回:
            选中的端口列表
        """
        selected_ports = []
        exclude_ports = []
        
        # 将PORT_GROUPS中的键转换为列表
        port_groups = list(PORT_GROUPS.keys())
        
        for checkbox, port_group_name in zip(port_checkboxes, port_groups):
            if checkbox.isChecked():
                port_group = PORT_GROUPS[port_group_name]
                if '排除' in checkbox.text():
                    exclude_ports.extend(port_group)
                else:
                    selected_ports.extend(port_group)
                    
        selected_ports = [port for port in selected_ports if port not in exclude_ports]
        return selected_ports
    
    @staticmethod
    def _process_web_scan_input(input_text):
        """
        处理Web扫描输入
        
        参数:
            input_text: 输入文本
            
        返回:
            处理后的目标列表
        """
        # 分割输入的多个ip:port对
        targets = input_text.split(',')
        target_list = []
        for target in targets:
            try:
                ip, port = target.split(':')
                target_list.append((ip.strip(), port.strip()))
            except ValueError:
                return None
        return target_list
