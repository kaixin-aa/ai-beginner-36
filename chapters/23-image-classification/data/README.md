# 图片数据与许可

本章固定快照来自 scikit-learn 1.7.2 的 `load_digits`。1797 张 8×8 灰度图，原像素整数范围为 0 至 16，标签为 0 至 9。它复制了 UCI 光学手写数字数据的测试部分，不能把完整 UCI 数据的 5620 条当成本章记录数。

来源核对于 2026 年 10 月 3 日。作者为 E. Alpaydin 与 C. Kaynak，推荐引用 Alpaydin, E., & Kaynak, C. (1998). Optical Recognition of Handwritten Digits. UCI Machine Learning Repository. DOI [10.24432/C50P49](https://doi.org/10.24432/C50P49)。原数据采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)，本章保留署名，对存储方式、划分和显示尺度作了转换。

[scikit-learn 数据说明](https://scikit-learn.org/1.7/modules/generated/sklearn.datasets.load_digits.html)与 [UCI 数据页面](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)支持上述来源和许可信息。

`digits.npz` 保存原始图片、标签、训练编号和测试编号。用分层随机划分、测试比例 0.2、种子 42 得到训练 1437、测试 360。这里的“训练”“测试”指本章在 1797 张图中重新划分的角色，和 UCI 原数据的角色不是同一层划分。

快照 SHA-256 为 `2707e088861342883e6326962ba38118dd8d02c96b4b2091dba530efdd291385`。读取函数实际校验文件哈希、形状、类别及划分互斥覆盖。

`sample-digit.npy` 为原编号 618 的像素矩阵，真实标签为 5，属于本章测试集。配套 PNG 将 0 至 16 按比例取整显示成 0 至 255，读取时取整恢复到原尺度。两种格式随后都除以 16，增加通道维度，得到 float32 的 `1×1×8×8` 张量。图形和这个变换没有引入新的独立外部样本。

数据测量值属于公开数据。正文中的三个类别分数为虚构教学设定，模型指标与用时来自本机实际计算。
