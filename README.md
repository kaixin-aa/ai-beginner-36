# AI 零基础 36 讲

从认识和使用 AI 开始，逐步学习 Python、数据处理、机器学习、神经网络和大模型应用，最后做一个个人知识库助手。

这里是 CSDN 专栏 **《AI 零基础 36 讲》** 的配套资源仓库，按章节提供示例代码、教学数据、Notebook 和运行结果。教程正文与练习题请前往专栏阅读。

**[阅读 CSDN 专栏](https://blog.csdn.net/m0_73879806/category_13215223.html)** · **[快速开始](#快速开始)** · **[章节资源](#章节资源)** · **[运行前先看](#运行前先看)** · **[课程路线](#课程路线)**

目前已收录第 **08～36 讲，共 29 个章节** 的配套资源。第 01～07 讲请结合专栏学习。第 31～32 讲的模型准备文件、第 33～35 讲的共享项目尚有缺口，具体条件见下方的[运行前先看](#运行前先看)。

## 快速开始

先准备可用的 Python 3。已保存的多数运行环境记录使用 Python 3.12.2；涉及第三方包时，请按各章依赖文件选择环境。下面三个入门示例只使用 Python 标准库。

### 下载仓库

```bash
git clone https://github.com/kaixin-aa/ai-beginner-36.git
cd ai-beginner-36
```

也可以在仓库页面点击 **Code → Download ZIP** 后解压。下面的快速开始命令都从仓库根目录执行。

### 第 9 讲，运行第一个 Python 脚本

```bash
python chapters/09-install-python-tools/examples/hello_ai.py
```

输出为 `你好，AI 学习之旅开始了` 和 `2 + 3 = 5`。安装与解释器检查步骤见[环境检查清单](chapters/09-install-python-tools/environment-check.md)，也可以打开同章的 [first_notebook.ipynb](chapters/09-install-python-tools/examples/first_notebook.ipynb) 练习。

### 第 8 讲，运行计算器和测试

```bash
python chapters/08-ai-assisted-programming/examples/calculator_after.py
python chapters/08-ai-assisted-programming/examples/test_calculator.py
```

第一条命令输出 `4.0`，第二条运行 6 项测试，通过时显示 `OK`。

### 第 29 讲，体验本地问答

```bash
python chapters/29-first-api/examples/run_fixture.py
```

程序会启动临时的本地 HTTP 教学服务，用占位符完成一次请求与响应，输出固定回答和教学用量。这个入口无需真实 API Key，也不会请求付费模型。

执行后可查看同章结果目录中的 [local-fixture.json](chapters/29-first-api/results/local-fixture.json)、[fixture-cli.txt](chapters/29-first-api/results/fixture-cli.txt) 和 [fixture-request.json](chapters/29-first-api/results/fixture-request.json)。

## 章节资源

下面各项链接均指向当前已上传的章节目录。数据、Notebook、模型和说明文件因章节而异，运行条件见下一节。

| 讲次 | 主题与下载入口 | 配套内容 |
| --- | --- | --- |
| 08 | [让 AI 辅助编程](chapters/08-ai-assisted-programming/) | 计算器修改前后版本、故障示例和 6 项测试 |
| 09 | [安装 Python 和开发工具](chapters/09-install-python-tools/) | 环境检查清单、首个 Python 脚本和 Notebook |
| 10 | [变量、数字和字符串](chapters/10-variables-numbers-strings/) | 学习时长计算器、文字整理和练习起始代码 |
| 11 | [判断、循环和数据容器](chapters/11-control-flow-containers/) | 容器操作、学习记录处理和边界案例 |
| 12 | [函数、文件和错误处理](chapters/12-functions-files-errors/) | 英文词频统计、文本输入和 JSON 读写结果 |
| 13 | [NumPy 和向量](chapters/13-numpy-vectors/) | 成绩统计、教学数据和 Notebook |
| 14 | [Pandas 数据处理](chapters/14-pandas-data-cleaning/) | CSV 与 Excel 数据、清洗程序和审计结果 |
| 15 | [数据可视化与探索](chapters/15-data-visualization/) | 统计分析、绘图程序、Notebook 和分析报告 |
| 16 | [AI 需要的数学直觉](chapters/16-math-intuition/) | 均值、方差、导数和梯度下降实验 |
| 17 | [一个机器学习项目怎样完成](chapters/17-ml-project-workflow/) | Iris 数据、训练评估、模型保存和单条预测 |
| 18 | [用线性回归预测数值](chapters/18-linear-regression/) | 汽车数据、三种回归方案、指标和 Notebook |
| 19 | [用分类模型识别类别](chapters/19-classification/) | Iris 分类、概率顺序、混淆矩阵和 Notebook |
| 20 | [怎样判断模型是否可靠](chapters/20-model-reliability/) | 交叉验证、指标、阈值和数据泄漏实验 |
| 21 | [神经网络怎样工作](chapters/21-neural-network/) | 前向计算、手算核对、梯度和参数更新 |
| 22 | [第一次使用 PyTorch](chapters/22-first-pytorch/) | 张量、自动求导、线性模型训练和 Notebook |
| 23 | [用神经网络识别图片](chapters/23-image-classification/) | 手写数字快照、训练、模型和单张图片预测 |
| 24 | [卷积网络与迁移学习](chapters/24-convolution-transfer/) | 卷积计算、预训练与迁移对比、图片和模型 |
| 25 | [计算机怎样处理文字](chapters/25-text-representation/) | 词表示、BPE 合并、相似度和 Notebook |
| 26 | [注意力机制怎样工作](chapters/26-attention/) | 两头注意力、掩码、计算矩阵和 PyTorch 核对 |
| 27 | [Transformer 结构](chapters/27-transformer/) | 字符级教学模型、训练、逐步生成和词表 |
| 28 | [大语言模型怎样训练出来](chapters/28-llm-training/) | 训练阶段示意、固定模型和生成参数对比 |
| 29 | [第一次调用大模型 API](chapters/29-first-api/) | 问答客户端、本地教学服务和密钥配置工具 |
| 30 | [对话记录与结构化输出](chapters/30-conversation-json/) | 学习计划助手、会话保存、JSON 校验和教学回放 |
| 31 | [RAG 和个人资料检索](chapters/31-rag/) | 教学文档、切分检索、索引和引用核对 |
| 32 | [工具调用与 AI Agent](chapters/32-tools-agent/) | 计算工具、资料查询、受限调用和教学回放 |
| 33 | [设计个人知识库助手](chapters/33-project-design/) | 接口约定示例、项目骨架演示和已有结果 |
| 34 | [完成文档处理与知识检索](chapters/34-document-retrieval/) | 文本与 PDF 教学资料、检索入口和回答记录 |
| 35 | [添加网页界面并部署](chapters/35-web-deployment/) | 网页接口示例、浏览器操作和环境记录 |
| 36 | [测试、成本和后续学习路线](chapters/36-testing-cost-roadmap/) | 已存请求汇总、评分空表、演示指南和项目报告 |

## 运行前先看

### 按章节安装依赖

建议为不同章节准备各自的虚拟环境。以第 13 讲为例，先进入该章目录并创建环境。

```bash
cd chapters/13-numpy-vectors
python -m venv .venv
```

Windows PowerShell 可以直接调用环境中的 Python。

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe examples/score_stats.py
```

macOS 与 Linux 使用对应的解释器路径。

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python examples/score_stats.py
```

完成后，成绩统计结果写入该章的 `results/score_summary.json`。其他章节也应从各自的依赖清单开始，避免一次安装所有章节的包。

| 文件 | 使用方式 |
| --- | --- |
| `requirements.txt` | 当前章节的脚本依赖 |
| `requirements-cpu.txt` | 对应章节固定的 CPU 版 PyTorch，使用同一虚拟环境先安装此文件，再安装普通依赖 |
| `requirements-notebook.txt` | 相应 Notebook 的执行依赖，按需额外安装 |
| `requirements-data.txt` | 数据快照准备依赖，重新生成数据时使用 |
| `requirements-figures.txt` | 独立绘图依赖，需要生成配图时使用 |

只有部分章节提供上述文件。打开 Notebook 时，请选择安装了相应依赖的内核，并将工作目录设为该章目录；第 9 讲的入门 Notebook 可直接运行。

### 配图与已有结果

部分程序会在运行时生成 `assets` 文件夹。图表脚本需要依赖清单中的 Matplotlib，以及 `plot_style.py` 能找到的中文字体。已有统计、预测与模型文件可从各章的 `results` 目录查看。

`environment.txt` 记录生成已有结果时的环境。使用保存的模型前，请按对应教程核对依赖版本；需要时在自己的环境重新训练。第 17 讲的 pickle 和第 19 讲的 joblib 文件只应从可信来源加载。

### 跨章节依赖与尚缺的文件

| 章节 | 当前运行条件 |
| --- | --- |
| 20 | 评估代码会读取第 18、19 讲的代码与数据，请保留这三章的原目录名称和相对位置 |
| 23、24 | 已包含数字图片快照与模型，按各章数据说明运行；重新生成快照时再准备相应依赖 |
| 28 | 基线准备脚本会读取第 27 讲；本章也已保存固定的基线模型 |
| 30 | 真实调用复用第 29 讲客户端，请保留该章；教学回放入口无需真实密钥 |
| 31、32 | 嵌入模型代码还会读取 `review/rag-model-metadata.json` 和本地权重缓存，并提示使用 `review/prepare_rag_model.py` 准备。当前仓库尚未提供这些文件，完整向量检索与依赖它的工具调用还需补齐模型配置和缓存；已有索引与结果可供阅读 |
| 33～35 | 部分脚本导入 `projects/knowledge-assistant/knowledge_app`。当前仓库尚未提供该共享项目，这部分代码和结果可先阅读，完整知识库与网页应用还需补齐项目源码 |
| 36 | `collect_results.py` 读取第 34、35 讲已保存的回答、浏览器及环境记录，只做本地汇总，不发送新的模型请求；请保留这些结果文件 |

### 真实 API 调用

第 29 讲提供[配置字段模板](chapters/29-first-api/.env.example)和 [configure-key.ps1](chapters/29-first-api/configure-key.ps1)。模板用于说明字段，客户端不会自动加载 `.env` 文件。真实调用前，请按所用服务设置本机环境变量，并核对接口地址、模型名和费用。

第 30 讲以后的部分脚本同样可能发送真实请求。`run_fixture.py`、教学回放和已保存的 `results` 可用于先看流程；真实密钥请保留在本机，分享报错时移除密钥与个人信息。

## 文件用途

| 位置 | 内容 |
| --- | --- |
| `examples` | 示例程序，`errors` 演示错误，`fixed` 提供修复版本 |
| `data` | 教学输入、数据快照、字段说明及来源记录 |
| `results` | 统计、预测、模型和保存的运行结果 |
| `tests` | 配套自动测试，便于修改代码后核对行为 |
| `.ipynb` 文件 | 可逐个单元运行的 Notebook |
| `error-samples.md` 或 `error-sample.txt` | 报错与修复过程记录 |

`practice_starter.py` 是留给读者填写的练习。`errors` 中故意触发异常的程序，请结合教程中的故障排查步骤使用。

## 课程路线

| 阶段 | 讲次 | 学习内容 |
| --- | --- | --- |
| 认识 AI | 01～04 | AI 技术范围、数据学习、语言模型与使用边界 |
| 使用 AI | 05～08 | 描述任务、追问改进、学习办公与辅助编程 |
| Python 入门 | 09～12 | 环境安装、基础语法、容器、函数与文件 |
| 数据与数学 | 13～16 | NumPy、Pandas、可视化与数学直觉 |
| 机器学习 | 17～20 | 项目流程、回归、分类与模型评估 |
| 神经网络 | 21～24 | 神经网络、PyTorch、图片分类与迁移学习 |
| 语言模型原理 | 25～28 | 文字表示、注意力、Transformer 与预训练 |
| 大模型应用 | 29～32 | API、对话与结构化输出、RAG 与 Agent |
| 综合实战 | 33～36 | 个人知识库助手、检索、网页界面、测试与成本 |

<details>
<summary>展开完整 36 讲目录</summary>

| 讲次 | 标题 |
| --- | --- |
| 01 | AI 究竟包含哪些技术 |
| 02 | AI 怎样从数据中学习 |
| 03 | 大语言模型为什么能回答问题 |
| 04 | 使用 AI 前必须知道的边界 |
| 05 | 怎样向 AI 描述任务 |
| 06 | 怎样通过追问改进结果 |
| 07 | 让 AI 辅助学习和办公 |
| 08 | 让 AI 辅助编程 |
| 09 | 安装 Python 和开发工具 |
| 10 | 变量、数字和字符串 |
| 11 | 判断、循环和数据容器 |
| 12 | 函数、文件和错误处理 |
| 13 | NumPy 和向量 |
| 14 | Pandas 数据处理 |
| 15 | 数据可视化与探索 |
| 16 | AI 需要的数学直觉 |
| 17 | 一个机器学习项目怎样完成 |
| 18 | 用线性回归预测数值 |
| 19 | 用分类模型识别类别 |
| 20 | 怎样判断模型是否可靠 |
| 21 | 神经网络怎样工作 |
| 22 | 第一次使用 PyTorch |
| 23 | 用神经网络识别图片 |
| 24 | 卷积网络与迁移学习 |
| 25 | 计算机怎样处理文字 |
| 26 | 注意力机制怎样工作 |
| 27 | Transformer 结构 |
| 28 | 大语言模型怎样训练出来 |
| 29 | 第一次调用大模型 API |
| 30 | 对话记录与结构化输出 |
| 31 | RAG 和个人资料检索 |
| 32 | 工具调用与 AI Agent |
| 33 | 设计个人知识库助手 |
| 34 | 完成文档处理与知识检索 |
| 35 | 添加网页界面并部署 |
| 36 | 测试、成本和后续学习路线 |

</details>

## 在博客中引用文件

可以使用 GitHub 文件链接，例如第 29 讲的 API 客户端。

```markdown
[查看 API 客户端代码](https://github.com/kaixin-aa/ai-beginner-36/blob/main/chapters/29-first-api/examples/api_client.py)
```

`main` 链接随代码更新显示最新内容。文章需要对应固定版本时，可将链接中的 `main` 换成提交编号。

## 反馈与交流

示例与文章不一致、链接失效或运行报错时，可以在[仓库 Issues](https://github.com/kaixin-aa/ai-beginner-36/issues) 中反馈。请附上章节编号、文件名、Python 版本和完整报错。

作者 [kaixin_啊啊](https://blog.csdn.net/m0_73879806) · 专栏 [《AI 零基础 36 讲》](https://blog.csdn.net/m0_73879806/category_13215223.html)
