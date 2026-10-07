# 自定义奇偶图片数据

图像来自第 23 章 scikit-learn 1.7.2 `load_digits` 固定快照。复制为 `original-digits.npz`，SHA-256 保持 `2707e088861342883e6326962ba38118dd8d02c96b4b2091dba530efdd291385`。原快照的第 23 章划分数组不在本章使用，本章根据原图片编号重新分配互斥角色。

原作者为 E. Alpaydin 与 C. Kaynak，引用 Alpaydin, E., & Kaynak, C. (1998). Optical Recognition of Handwritten Digits. UCI Machine Learning Repository. [DOI 10.24432/C50P49](https://doi.org/10.24432/C50P49)。许可为 CC BY 4.0，允许本章的复制和转换，保留署名、许可及变换说明。[UCI 数据页](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)和 [scikit-learn 1.7 页面](https://scikit-learn.org/1.7/modules/generated/sklearn.datasets.load_digits.html)已在第 23 章核对，此处复用。

2026 年 10 月 3 日生成本章派生数据。NumPy 随机种子 2026，每个数字内部先打乱原编号，再取 100 张预训练、12 张目标训练、20 张目标测试。总数为 1000、120、200，其余 477 张未用。目标训练偶数和奇数各 60 张，目标测试各 100 张。

目标标签自行定义为原数字对 2 求余，0 对应 even，1 对应 odd。新任务是从图片判断奇偶，输入中不包含真实数字标签。目标图片以 8×8 灰度 PNG 保存，文件夹按角色和类别区分。源图片、目标训练、目标测试的编号互不重叠，并在清单中保留未用记录。

PNG 显示值由原 0 至 16 按比例取整至 0 至 255，读取后取整恢复原尺度并除以 16。自动测试遍历全部 320 张目标 PNG，与源像素逐值比较，标签也按原数字复核。文件哈希逐张保存并在读取时验证。

图像是公开数据，分区、奇偶标签和图版布局由本章编制。卷积手算矩阵属于原创虚构教学数值。模型权重由本章自行 CPU 训练，源预训练未另设独立测试集，不对源模型泛化作评价。
