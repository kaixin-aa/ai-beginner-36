# AI 零基础 36 讲

从认识和使用 AI 开始，逐步学习 Python、数据处理、机器学习、深度学习与大模型应用开发，最后完成一个个人知识库助手。

本仓库是 CSDN 专栏 **《AI 零基础 36 讲》** 的配套资源仓库，用于存放教程中的示例代码、运行结果和相关文件，方便读者对照文章学习、下载练习，也方便博客直接引用具体文件。

**[前往 CSDN 专栏阅读教程](https://blog.csdn.net/m0_73879806/category_13215223.html)** · **[查看已上传资源](#已上传资源)** · **[快速开始](#快速开始)**

## 适合谁

这套教程面向没有 AI 基础、编程经验较少的读者。课程从常见的 AI 功能和具体任务讲起，在需要写代码时逐步补上 Python，在进入模型训练后再介绍相关的数学概念。

建议按专栏顺序学习。读完一讲后，运行对应示例，改一组输入观察结果，再独立完成课后练习。已有 Python 基础的读者，也可以按课程目录找到想补充的内容。

## 已上传资源

目前仓库收录了以下 8 个章节的部分资源。教程正文、练习、数据和其他附件会逐步同步，当前可下载范围以表中链接为准。

| 章节 | 主题 | 当前资源 | 内容说明 |
| --- | --- | --- | --- |
| 08 | 让 AI 辅助编程 | [examples](chapters/08-ai-assisted-programming/examples/) | 计算器修改前、错误中间版、修复版及单元测试 |
| 10 | 变量、数字和字符串 | [examples](chapters/10-variables-numbers-strings/examples/) | 学习时长计算器、文字整理、练习起始代码与错误修复示例 |
| 11 | 判断、循环和数据容器 | [examples](chapters/11-control-flow-containers/examples/) | 容器演示、学习记录处理、练习起始代码与错误修复示例 |
| 21 | 神经网络怎样工作 | [results](chapters/21-neural-network/results/) | 手算结果、参数更新记录、网络结果汇总与验证记录 |
| 23 | 用神经网络识别图片 | [examples](chapters/23-image-classification/examples/) | 数据快照准备、训练、预测、绘图及错误修复示例 |
| 24 | 卷积网络与迁移学习 | [results](chapters/24-convolution-transfer/results/) | 卷积计算步骤、实验对比、训练记录、预测结果与模型文件 |
| 26 | 注意力机制怎样工作 | [examples](chapters/26-attention/examples/) | 注意力计算、运行示例、PyTorch 交叉核对与错误修复示例 |
| 29 | 第一次调用大模型 API | [examples](chapters/29-first-api/examples/) | API 客户端、命令行问答、本地教学服务及错误修复示例 |

`errors/` 中的程序用于演示报错，运行失败是预期现象。`fixed/` 提供对应修复版本。`practice_starter.py` 保留待完成的练习，请结合专栏中的题目填写。

`results/` 保存已有实验产物和运行记录。其中的测试日志反映生成记录时的环境与执行结果，具体环境可查阅同目录下的 `environment.txt`。

## 快速开始

先准备可用的 Python 3 环境。下面两个示例只使用 Python 标准库，无需安装第三方包。仓库中的部分历史验证记录使用 Python 3.12.2。

### 下载仓库

已安装 Git 时，在终端运行以下命令。

```bash
git clone https://github.com/kaixin-aa/ai-beginner-36.git
cd ai-beginner-36
```

也可以点击仓库页面的 **Code → Download ZIP**，解压后在 `ai-beginner-36` 文件夹中打开终端。下面的命令都从仓库根目录执行。

### 运行第 8 讲计算器

```bash
python chapters/08-ai-assisted-programming/examples/calculator_after.py
python chapters/08-ai-assisted-programming/examples/test_calculator.py
```

第一个命令输出 `4.0`，第二个命令运行 6 项测试，全部通过时会显示 `OK`。

### 体验第 29 讲本地问答

```bash
python chapters/29-first-api/examples/run_fixture.py
```

程序会启动一个临时的本地 HTTP 教学服务，使用占位符完成一次请求与响应，并显示固定回答和用量字段。它不需要真实 API Key，也不会调用付费模型。这里的回答与 Token 数为教学设定。

运行后，`chapters/29-first-api/results/` 下会生成 `local-fixture.json`、`fixture-cli.txt` 和 `fixture-request.json`，便于查看返回结果与请求内容。

连接真实服务时，请按第 29 讲正文配置本机环境变量，并核对所用平台的接口地址、模型名和费用。真实密钥保留在本机，不要写入源码或上传到仓库。

### 运行其他章节

不同章节使用的依赖和数据不同，请结合对应教程准备环境。

- 第 10、11 讲的示例使用 Python 标准库，可以从已上传的 `examples/` 中选择运行。
- 第 23 讲涉及 NumPy、Pillow、scikit-learn、PyTorch 和 Matplotlib。`prepare_snapshot.py` 可从 scikit-learn 内置数据生成所需快照，随后才能训练与预测。
- 第 26 讲的完整演示需要 `data/teaching-attention.json`，该数据文件尚未上传。当前代码可供阅读和引用，完整运行还需配齐数据与相应依赖。
- 第 21、24 讲目前上传的是结果文件，运行实验所需的配套代码和数据尚未同步到仓库。

## 36 讲学习路线

下表列出整套专栏的课程安排。章节出现在课程目录中，不代表对应文件已经全部上传。GitHub 下载入口请查看上方的已上传资源。

| 阶段 | 讲次 | 学习内容 |
| --- | --- | --- |
| 认识 AI | 01至04 | AI 技术范围、数据学习、语言模型与使用边界 |
| 使用 AI | 05至08 | 描述任务、追问改进、学习办公与辅助编程 |
| Python 入门 | 09至12 | 环境安装、基础语法、容器、函数与文件 |
| 数据与数学 | 13至16 | NumPy、Pandas、可视化与数学直觉 |
| 机器学习 | 17至20 | 项目流程、回归、分类与模型评估 |
| 神经网络 | 21至24 | 神经网络、PyTorch、图片分类与迁移学习 |
| 语言模型原理 | 25至28 | 文字表示、注意力、Transformer 与预训练 |
| 大模型应用 | 29至32 | API、对话与结构化输出、RAG 与 Agent |
| 综合实战 | 33至36 | 个人知识库助手、检索、网页界面、测试与成本 |

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

## 仓库结构

资源按章节编号和主题组织，当前结构如下。

```text
ai-beginner-36/
├── README.md
└── chapters/
    ├── 08-ai-assisted-programming/
    │   └── examples/
    ├── 10-variables-numbers-strings/
    │   └── examples/
    ├── 11-control-flow-containers/
    │   └── examples/
    ├── 21-neural-network/
    │   └── results/
    ├── 23-image-classification/
    │   └── examples/
    ├── 24-convolution-transfer/
    │   └── results/
    ├── 26-attention/
    │   └── examples/
    └── 29-first-api/
        └── examples/
```

## 在博客中引用文件

可以直接使用 GitHub 文件链接。例如，下面的 Markdown 会指向第 29 讲的 API 客户端。

```markdown
[查看 API 客户端代码](https://github.com/kaixin-aa/ai-beginner-36/blob/main/chapters/29-first-api/examples/api_client.py)
```

`main` 链接随仓库更新显示最新内容。需要让文章始终对应同一版代码时，可以使用含提交编号的固定链接。

## 反馈与交流

如果发现示例与文章不一致、链接失效或运行报错，可以在 [仓库 Issues](https://github.com/kaixin-aa/ai-beginner-36/issues) 中反馈。请附上章节编号、文件名、Python 版本和完整报错，分享日志前先移除真实密钥与个人信息。

作者 [kaixin_啊啊](https://blog.csdn.net/m0_73879806) · 博客专栏 [《AI 零基础 36 讲》](https://blog.csdn.net/m0_73879806/category_13215223.html)
