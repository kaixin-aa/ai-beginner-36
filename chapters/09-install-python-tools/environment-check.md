# 第 9 章环境检查命令

这份清单供新电脑安装后逐项执行。命令默认在项目目录中运行。每完成一组，都先读实际输出，再继续下一组。

## Windows

### 检查全局 Python

```powershell
python --version
py list
python -m pip --version
```

预期能看到 Python 3、已安装运行时与 pip 路径。若 python 不可用，先试 py 和 pymanager，再查看正文中的故障排查。

### 创建项目和虚拟环境

```powershell
mkdir ai_beginner
cd ai_beginner
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

若激活被设备策略拒绝，使用下面的直接路径。

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip --version
```

### 核对当前解释器

```powershell
python --version
python -m pip --version
python -c "import sys; print(sys.executable)"
```

sys.executable 的输出路径应包含 ai_beginner\.venv。

### 运行脚本

把 examples 目录中的 hello_ai.py 复制到项目目录，再运行。

```powershell
python hello_ai.py
```

预期输出如下。

```text
你好，AI 学习之旅开始了
2 + 3 = 5
```

### 安装并启动 JupyterLab

```powershell
python -m pip install jupyterlab
jupyter lab
```

打开 first_notebook.ipynb，选择 .venv 对应的 Python 内核并重新运行代码单元。

### 离开虚拟环境

```powershell
deactivate
```

## macOS 与 Linux

下面的命令假定 python3、pip 和 venv 已经按照系统官方文档安装。

```bash
mkdir ai_beginner
cd ai_beginner
python3 -m venv .venv
source .venv/bin/activate
python --version
python -m pip --version
python -c "import sys; print(sys.executable)"
python hello_ai.py
```

解释器路径应包含 ai_beginner/.venv。Linux 用户不要用 sudo pip 把练习依赖写进系统 Python。

## 最终记录

请把下面信息写进自己的学习日志。

- 操作系统与版本
- python --version 的完整输出
- python -m pip --version 的完整输出
- sys.executable 的完整路径
- hello_ai.py 的实际输出
- Notebook 选择的内核路径
- 未解决的错误与完整报错

