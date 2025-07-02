# FastNmap - Nmap图形化扫描工具

![FastNmap Logo](docs/logo.png)

FastNmap是一个强大、现代化的Nmap图形界面工具，为网络管理员和安全研究人员提供了友好的可视化界面，使Nmap的高级功能变得简单易用。

## 主要特点

- **现代化界面** - 精心设计的深色主题界面，提供出色的用户体验
- **多种扫描模式** - 支持默认扫描、存活扫描、端口识别、服务识别、系统识别、漏洞扫描和暴力破解
- **可视化结果** - 以结构化、易于理解的方式展示扫描结果
- **内置字典** - 提供各种服务的用户名和密码字典，用于暴力破解
- **数据导出** - 支持将结果导出为多种格式，包括CSV和纯文本
- **配置管理** - 保存和加载常用的扫描配置
- **跨平台兼容** - 支持Windows、macOS和Linux系统

## 安装要求

- Python 3.6+
- PyQt5
- Nmap 

## 快速开始

### 安装

1. 克隆仓库:

```bash
git clone https://github.com/vam876/FastNmap.git
cd FastNmap
```

2. 安装依赖:

```bash
pip install -r requirements.txt
```

3. 确保安装了Nmap:
   - Windows: 从[Nmap官网](https://nmap.org/download.html)下载并安装
   - macOS: `brew install nmap`
   - Linux: `apt install nmap` 或 `yum install nmap`

### 运行

```bash
python main.py
```

## 使用指南

### 基本操作

1. **输入扫描目标** - 可以是单个IP、IP范围、主机名或加载包含目标的文件
2. **选择扫描类型** - 从默认扫描、存活扫描等选项中选择
3. **设置扫描选项** - 配置端口、超时、线程等参数
4. **开始扫描** - 点击"开始扫描"按钮启动扫描
5. **查看结果** - 在"扫描结果"标签页中查看格式化结果

### 扫描类型说明

- **默认扫描** - 快速检测开放端口和基本服务信息
- **存活扫描** - 仅检测网络中在线主机
- **端口识别** - 深入分析指定端口，如Web服务的端口
- **服务识别** - 识别端口上运行的具体服务和版本
- **系统识别** - 尝试识别目标主机的操作系统
- **漏洞扫描** - 使用Nmap脚本检测常见漏洞
- **暴力破解** - 尝试破解各种服务的登录凭证

### 端口选项

可以手动输入端口或选择预定义的端口组，如"高危端口"、"HTTP端口"等。

## 暴力破解功能

FastNmap内置了多种服务的字典文件，支持对以下服务进行暴力破解：

- SSH
- Telnet
- SMB
- MS-SQL
- MySQL
- Oracle
- VNC
- Redis
- FTP

所有字典文件位于`dict/`目录下，用户可以根据需要修改或替换。

## 导出功能

FastNmap支持将扫描结果以多种格式导出：

- **导出扫描过程** - 导出原始扫描日志为文本文件
- **导出扫描结果为CSV格式** - 将结构化结果导出为CSV文件，方便在电子表格软件中分析

## 特色功能

- **Fast Mode** - 加速扫描模式，通过优化参数提高扫描速度
- **配置保存** - 保存常用的扫描配置，以便快速重用
- **结果可视化** - 使用颜色和格式化展示扫描结果，使信息一目了然

## 截图

![主界面](docs/main_screen.png)
![扫描结果](docs/scan_results.png)

## 常见问题

**Q: 程序无法启动或报错**  
A: 检查是否正确安装了Python、PyQt5和Nmap。确保Nmap命令可在终端中执行。

**Q: 扫描速度很慢**  
A: 尝试启用"Fast Mode"，或调整线程参数。注意，某些扫描类型本身就比较耗时。

**Q: 暴力破解没有结果**  
A: 检查目标服务是否允许暴力破解，某些服务可能有防护措施。同时确保字典文件存在且包含合适的凭证。

## 贡献

欢迎通过以下方式贡献：

1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情见[LICENSE](LICENSE)文件

## 联系方式

- 项目链接: [https://github.com/vam876/FastNmap](https://github.com/vam876/FastNmap)
- 报告问题: [https://github.com/vam876/FastNmap/issues](https://github.com/vam876/FastNmap/issues)

## 致谢

- [Nmap](https://nmap.org/) - 强大的网络扫描工具
- [PyQt](https://riverbankcomputing.com/software/pyqt/intro) - Python GUI框架
- 所有贡献者和测试者
