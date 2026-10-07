"""作者构建 Notebook 的单元格源内容。"""
CELLS = [
    ("markdown", "# 第 15 章数据可视化\n使用第 14 章清洗结果的虚构教学快照。三个问题使用同一份数据，分别记录有效样本数。"),
    ("code", "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path.cwd() / 'examples'))\nfrom analysis import load_records, summarize\nfrom explore_records import make_charts\nfrom IPython.display import Image, display\nframe = load_records('data/learning_records.csv')\nprint(frame.to_string(index=False))"),
    ("code", "result = summarize(frame)\nprint('全部、已知、未知', result['input_rows'], result['known_minutes_rows'], result['missing_minutes_rows'])\nprint('直方图计数', result['histogram_counts'])\nprint('均值、中位数', result['known_mean'], result['known_median'])"),
    ("markdown", "## 问题一，已知时长怎样分布\n两条未知时长不进入直方图，区间边界明确保留。"),
    ("code", "print('绘图字体', make_charts(frame, result, Path('assets')))\ndisplay(Image(filename='assets/minutes-histogram.png'))"),
    ("markdown", "## 问题二，不同标签完成多少条\n分母是每组全部记录，未知时长不会删除完成状态。"),
    ("code", "import pandas as pd\nprint(pd.DataFrame(result['groups']).to_string(index=False))\ndisplay(Image(filename='assets/tag-completion-bars.png'))"),
    ("markdown", "## 问题三，时长和完成状态怎样配对\n只有三对数据，相关性不能解释为因果。"),
    ("code", "print(result['scatter_points'])\nprint('当前样本 Pearson r', result['pearson_r'])\ndisplay(Image(filename='assets/minutes-completion-scatter.png'))"),
    ("markdown", "## 独立练习\n改用边界 0、20、40、60，先预测计数再运行。"),
    ("code", "import numpy as np\ncounts, edges = np.histogram(frame['minutes'].dropna().to_numpy(dtype=float), bins=[0, 20, 40, 60])\nprint(counts.tolist())\nassert counts.tolist() == [1, 1, 1]"),
]
