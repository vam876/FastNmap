# FastNmap - Nmap图形化扫描工具


FastNmap是一个强大、现代化的Nmap图形界面工具，为网络管理员和安全研究人员提供了友好的可视化界面，让“扫描之王”Nmap的功能变得简单易用，同时集成了高级功能，包括漏洞扫描、端口服务识别、操作系统识别、资产监控、资产对比与资产管理等。


[![Python](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/vam876/FastNmap)
[![Nmap](https://img.shields.io/badge/Nmap-red.svg)](https://nmap.org/)


- **最新版本**: 0.6.0 （全新界面）
- **更新日期**: 2025/12/16
- **下载地址**:  [新版下载](https://github.com/vam876/FastNmap/releases/tag/V0.6.0)   |   [旧版下载](https://github.com/vam876/FastNmap/releases/tag/V0.2.0)
  
<img width="1508" height="843" alt="image" src="https://github.com/user-attachments/assets/ab0af72c-a572-4d8c-91d2-7032acae67b3" />

<img width="1409" height="859" alt="image" src="https://github.com/user-attachments/assets/51166d48-a9ba-42af-8f4d-0de244dc223c" />

<img width="1499" height="852" alt="image" src="https://github.com/user-attachments/assets/4cb87899-e849-460c-ab8b-968c33e5952a" />

## ✨ 核心特性

### 新版架构
<img width="1176" height="872" alt="05" src="https://github.com/user-attachments/assets/809fea60-a719-4c40-aa6d-280b65aa0a64" />


### 🔍 多样化扫描功能
- **多种扫描类型**: 默认扫描、存活检测、服务识别、系统识别、端口识别、暴力破解、漏洞扫描
- **灵活的端口配置**: 预定义端口组、自定义端口范围、智能端口选择
- **高级扫描选项**: 自定义时间控制、线程管理、超时设置、附加参数
- **实时结果显示**: 实时扫描进度显示和详细的 XML 输出解析
  
<img width="1121" height="772" alt="扫描" src="https://github.com/user-attachments/assets/3f9a92e8-2fa8-40b1-99ac-a7adc4caa31e" />


### 📊 资产监控系统
- **持续监控**: 为网络资产安排定期扫描任务
- **变化检测**: 自动检测新主机、服务和端口变化
- **历史记录追踪**: 维护扫描历史并支持对比功能
- **智能警报**: 突出显示扫描结果之间的差异

<img width="1122" height="565" alt="资产监控1" src="https://github.com/user-attachments/assets/c85a953a-fd24-43c7-bf5f-56bcbe97d200" />
<img width="1122" height="565" alt="资产监控1" src="https://github.com/user-attachments/assets/c55a8297-c868-4bb5-8d47-777eed550345" />

<img width="1128" height="752" alt="资产监控3" src="https://github.com/user-attachments/assets/66c7a3ae-cbd0-4d0a-a467-a4c51a0de836" />

### 📈 报告与分析
- **HTML报告**: 生成美观、交互式的 HTML 报告
- **资产对比**: 当前扫描与历史扫描的可视化对比
- **趋势分析**: 历史数据分析和趋势展示
- **多种导出格式**: 支持多种导出格式以便集成其他系统

<img width="1090" height="938" alt="报告1" src="https://github.com/user-attachments/assets/24dcd200-9aa8-4714-b122-97cf84eaa2d0" />
<img width="1066" height="885" alt="报告2" src="https://github.com/user-attachments/assets/7453410d-c90c-4b5c-a867-d46b0299b9fe" />


### 🎨 现代化界面
- **深色主题**: 专业的深色界面配以科技感美学设计
- **响应式设计**: 适应不同窗口大小和分辨率
- **标签页界面**: 有组织的工作流程，为不同功能设置专用标签页
- **实时更新**: 实时进度指示和状态更新

## 🚀 快速开始

### 环境要求
- Python 3 或更高版本
- PyQt5 GUI框架
- Nmap 网络扫描器（需要单独安装）

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/vam876/FastNmap.git
cd FastNmap
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **安装 Nmap**
   - **Windows**: 从 [https://nmap.org/download.html](https://nmap.org/download.html) 下载安装
   - **Linux**: `sudo apt-get install nmap` 或 `sudo yum install nmap`
   - **macOS**: `brew install nmap`

4. **运行 FastNmap**
```bash
python main.py
```

## 📋 使用指南

### 基础扫描
1. 在目标输入框中输入 IP 地址、主机名或网络范围
2. 从可用选项中选择扫描类型
3. 配置端口（可选 - 使用智能默认值）
4. 点击"开始"按钮开始扫描

### 资产监控
1. 导航到"资产监控"标签页
2. 添加要监控的目标
3. 配置扫描间隔和参数
4. 开始监控以进行持续的资产跟踪

### 资产对比
1. 转到"资产对比"标签页
2. 选择已监控的目标
3. 查看详细对比和变化
4. 生成报告用于文档记录

## 🔧 扫描类型详解

| 扫描类型 | 说明 | 使用场景 |
|----------|------|----------|
| **默认扫描** | 快速 SYN 扫描与服务检测 | 通用网络发现 | 
| **服务识别** | 详细的服务版本检测 | 服务清单 | 
| **系统识别** | 操作系统指纹识别 | 资产分类 |
| **端口识别** | 专注的端口扫描与服务信息 | 端口分析 | 
| **暴力破解** | 自动化凭据测试 | 安全测试 | 
| **漏洞扫描** | 已知漏洞检测 | 安全评估 |

### 特殊功能

#### 端口识别的 IP:端口格式
端口识别支持 `127.0.0.1:445` 格式，系统会自动解析：
- IP地址：用作扫描目标
- 端口号：用作扫描端口
- 示例：输入 `192.168.1.100:80` 将扫描 192.168.1.100 的 80 端口

## ⚙️ 系统配置

### 目录结构
```
FastNmap/                               # 项目根目录
├── src/                                # 源代码
│   ├── __init__.py
│   ├── core/                           # 核心业务模块
│   │   ├── __init__.py
│   │   ├── command_builder.py        # Nmap 命令构造器
│   │   ├── nmap_executor.py          # 扫描执行与调度
│   │   ├── nmap_parser.py            # XML 结果解析
│   │   ├── asset_monitor.py          # 资产持续监控
│   │   └── html_report.py            # HTML 报告生成
│   ├── gui/                            # 图形界面
│   │   ├── __init__.py
│   │   ├── main_window.py              # 主窗口
│   │   ├── tabs/                       # 各功能页
│   │   │   ├── __init__.py
│   │   │   ├── scan_tab.py
│   │   │   ├── monitor_tab.py
│   │   │   └── compare_tab.py
│   │   └── widgets/                    # 复用组件
│   │       ├── __init__.py
│   │       ├── console.py
│   │       └── progress.py
│   ├── utils/                          # 工具集
│   │   ├── __init__.py
│   │   ├── constants.py               # 端口组、默认参数
│   │   └── logger.py                  # 日志封装
│   ├── config/                         # 配置文件（预留）
│   │   ├── __init__.py
│   │   └── settings.yaml
│   └── data/                           # 运行时数据（预留）
│       └── .gitkeep
├── assets/                             # 静态资源
│   ├── icons/                          # 界面图标
│   ├── dict/                           # 暴力破解字典
│   │   ├── ssh_user.txt
│   │   ├── ssh_pass.txt
│   │   ├── ftp_user.txt
│   │   └── ftp_pass.txt
│   └── css/                            # HTML 报告样式
│       └── report.css
├── monitor_data/                       # 资产监控持久化
│   ├── .gitkeep
│   └── readme.md
├── logs/                               # 运行日志
│   ├── .gitkeep
│   └── readme.md
├── nmap/                               # 内置 nmap 二进制
│   ├── Win32/
│   │   └── nmap.exe                   # Windows 可执行
│   ├── Linux/
│   │   └── nmap                       # Linux 静态二进制
│   └── macOS/
│       └── nmap                       # macOS 可执行
├── tests/                              # 单元测试
│   ├── __init__.py
│   ├── test_command_builder.py
│   └── test_parser.py
├── docs/                               # 文档
│   ├── README_PACKAGING.md
│   └── BUILD.md
├── main.py                             # 程序入口
├── requirements.txt                    # Python 依赖
├── README.md                           # 项目说明
├── LICENSE                             # 许可
└── .gitignore                          # 规则
```

### 自定义配置
- **端口组**: 修改 `src/utils/constants.py` 自定义端口定义
- **扫描模板**: 调整 `src/core/command_builder.py` 自定义扫描配置
- **界面主题**: 在 GUI 组件中自定义样式

## 🛡️ 安全功能

### 内置安全工具
- **基于字典的暴力破解**: 内置常见服务的用户名密码字典
- **漏洞检测**: 集成 Nmap 漏洞检测脚本
- **安全扫描**: 可配置的时间和强度控制
- **审计日志**: 全面记录所有扫描活动

### 暴力破解支持的服务
- **远程访问**: SSH, Telnet, RDP, VNC, Radmin
- **数据库**: MySQL, MSSQL, Oracle, PostgreSQL, Redis
- **文件服务**: FTP, SMB
- **Web服务**: HTTP Basic Auth（可扩展）

## 📊 监控与报告

### 资产监控功能
- 自定义间隔扫描（分钟到小时）
- 网络拓扑变化跟踪
- 服务可用性和变化监控
- 历史数据保留和分析

### 报告特性
- 带有嵌入式 CSS 和 JavaScript 的 HTML 报告
- 显示前后状态对比的比较视图
- 详细的端口和服务变化跟踪
- 外部系统导出功能

## 🔍 高级功能

### 命令行集成
FastNmap 构建优化的 Nmap 命令，具备：
- 自动参数去重
- 智能时间调整
- 平台特定优化
- 错误处理和验证

### 性能优化
- 多线程支持
- 高效的 XML 解析
- 智能缓存机制
- 资源感知扫描

### 扩展性设计
- 模块化架构，便于功能扩展
- 插件化的扫描类型支持
- 可配置的输出格式
- API接口预留设计

## 🐛 故障排除

### 常见问题

**无法找到nmap**

程序启动后，将依下列优先级自动定位并调用 nmap，无需用户手动配置：

1. 先检查程序目录下的相对路径  
   Windows：`{程序所在目录}\nmap\nmap.exe`  
   macOS / Linux：`{程序所在目录}/nmap/nmap`  
   若该文件存在且具备可执行权限，则直接使用。

2. 若未命中，则检索系统环境变量 PATH，调用 `shutil.which('nmap')` 获取已安装的 nmap 可执行路径。

3. 如 PATH 中仍未找到，将依次扫描各平台常见安装目录：  
   Windows：  
   - `C:\Program Files (x86)\Nmap\nmap.exe`  
   - `C:\Program Files\Nmap\nmap.exe`  

   macOS：  
   - `/Applications/nmap.app/Contents/Resources/bin/nmap`  
   - `/usr/local/bin/nmap`  
   - `/opt/homebrew/bin/nmap`  
   - `/usr/bin/nmap`  

   Linux：  
   - `/usr/bin/nmap`  

4. 上述步骤皆未定位到有效 nmap 时，程序将回退至默认命令 `nmap`，并在后续执行中抛出明确错误提示，指引用户完成安装或手动指定路径。

**程序无法启动**
- 确保安装了 Python3 
- 验证 PyQt5 安装：`pip install PyQt5`
- 检查 main.py 文件是否完整

**找不到 Nmap**
- 验证 Nmap 安装
- 检查 PATH 环境变量
- 如有需要，在配置中使用完整路径

**权限错误**
- 网络扫描需要适当的权限运行
- 某些扫描类型需要管理员/root权限
- Windows 用户可能需要"以管理员身份运行"

**扫描结果异常**
- 检查目标地址格式
- 验证网络连接
- 查看扫描日志获取详细信息

### 性能优化建议

**提升扫描速度**
- 调整线程并发数
- 使用快速模式进行初步扫描
- 针对性选择端口范围

**减少资源占用**
- 合理设置扫描间隔
- 定期清理历史数据
- 监控系统资源使用情况

## 🤝 贡献指南

### 开发环境搭建
1. Fork 本仓库
2. 创建功能分支
3. 进行代码修改
4. 添加测试（如适用）
5. 提交 Pull Request


## 📄 许可证

本项目使用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Nmap](https://nmap.org/) - 强大的网络扫描器，本工具的核心引擎
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 优秀的 GUI 框架
- 网络安全社区的反馈和建议
- 所有贡献者和用户的支持

## 📞 支持与联系

- **GitHub Issues**: 报告 Bug 和请求新功能

## 🔗 相关链接

- [Nmap 官方网站](https://nmap.org/)
- [PyQt5 文档](https://doc.qt.io/qtforpython/)
- [Python 官方网站](https://www.python.org/)
---

**⚠️ 法律声明**: 此工具仅用于授权的安全测试和网络管理。用户有责任遵守适用的法律法规。未经授权的网络扫描可能违法，请确保在合法授权的范围内使用本工具。

**🌟 如果本项目对您有帮助，请给我们一个 Star！** 



