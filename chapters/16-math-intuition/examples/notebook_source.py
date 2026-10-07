"""Notebook 的可审阅源单元格，由验收程序实际执行并保留输出。"""
CELLS = [
    ("markdown", "# 第 16 章数学直觉实验\n全部数值与函数为原创教学设定，不对应真实用户或训练任务。先运行 examples/math_experiments.py 生成配图。"),
    ("code", "import numpy as np\nfrom examples.math_core import loss, gradient, descent, finite_difference\nfrom IPython.display import Image, display\nprint('NumPy', np.__version__)\na = np.array([18, 20, 22])\nb = np.array([10, 20, 30])\nfor values in [a, b]:\n    print('均值 方差 标准差', values.mean(), values.var(ddof=0), values.std(ddof=0))\ndisplay(Image(filename='assets/mean-variance.png'))"),
    ("markdown", "## 方差的两种分母\n本章描述手头三条记录，除以 N。若用样本估计总体方差，常用 N-1，不能混写。"),
    ("code", "print('A组 ddof0', a.var(ddof=0))\nprint('A组 ddof1', a.var(ddof=1))\nnp.testing.assert_allclose([a.var(ddof=0), a.var(ddof=1)], [8/3, 4])"),
    ("markdown", "## 公平骰子的假设\n六个点数等可能，偶数事件有三个结果。概率为三个 1/6 相加。"),
    ("code", "probabilities = np.full(6, 1/6)\nprint('概率总和', probabilities.sum())\nprint('偶数概率', probabilities[[1, 3, 5]].sum())\ndisplay(Image(filename='assets/probability.png'))"),
    ("markdown", "## 先读曲线，再读导数\nL(w)=(w-3)^2+1，梯度为 2(w-3)。"),
    ("code", "for w in [1, 3, 5, 9]:\n    print('w 损失 梯度', w, loss(w), gradient(w))\nfor h in [0.1, 0.01, 0.001]:\n    print('h 与中心差分', h, finite_difference(5, h))\ndisplay(Image(filename='assets/function-derivative.png'))"),
    ("markdown", "## 每一步都重算梯度\n先算当前位置损失和梯度，再按学习率更新 w，最后核对新损失。编号 0 未更新。"),
    ("code", "history = descent(9, 0.2, 12)\nfor row in history[:4] + history[-1:]:\n    print(f\"第 {row['step']} 步 w={row['w']:.6f} loss={row['loss']:.6f} gradient={row['gradient']:.6f}\")\nassert all(b['loss'] < a['loss'] for a, b in zip(history, history[1:]))"),
    ("markdown", "## 大步、小步和振荡\n这里只比较同一个二次函数，不把学习率范围推广到所有模型。"),
    ("code", "for rate in [0.01, 0.2, 0.5, 1.0, 1.1]:\n    rows = descent(9, rate, 12)\n    print('学习率 第1步损失 第12步损失', rate, round(rows[1]['loss'], 6), round(rows[-1]['loss'], 6))\ndisplay(Image(filename='assets/gradient-descent.png'))"),
    ("markdown", "## 独立练习\n从 w=1 出发，学习率 0.25。先手算，再核对两次更新。"),
    ("code", "practice = descent(1, 0.25, 2)\nprint([(row['w'], row['loss']) for row in practice])\nnp.testing.assert_allclose([row['w'] for row in practice], [1, 2, 2.5])"),
]
