# Iris 数据说明

本章使用公开 Iris 测量数据，非虚构学习记录。快照在 2026 年 10 月 3 日由 scikit-learn 1.7.2 的 `load_iris()` 导出，读取不需要联网。[官方数据接口](https://scikit-learn.org/1.7/modules/generated/sklearn.datasets.load_iris.html)说明了 150 条记录、四个特征、三个类别及每类 50 条。

原始资料可追溯到 Fisher, R. (1936). Iris [Dataset]. UCI Machine Learning Repository，[数据集 DOI](https://doi.org/10.24432/C56C76)。[UCI 数据页](https://archive.ics.uci.edu/dataset/53/iris)标示许可为 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。本章保留来源、署名与修改说明，数据教学使用不代表原作者认可本教程。

采用的 scikit-learn 版本自 0.20 起修正过两个测量点，官方明确说明与 UCI 早期文件不同。这里没有直接下载或声称原样复刻 UCI 文件。教学改动包括字段重命名、增加样本编号、将类别映射为 0、1、2，测量值沿用该库快照。

| 字段 | 含义 | 单位或编码 |
|---|---|---|
| sample_id | 从 0 起按原记录顺序生成的教学编号 | 无预测含义，不作特征 |
| sepal_length_cm | 萼片长度 | 厘米 |
| sepal_width_cm | 萼片宽度 | 厘米 |
| petal_length_cm | 花瓣长度 | 厘米 |
| petal_width_cm | 花瓣宽度 | 厘米 |
| target | 花卉类别标签 | 0 setosa，1 versicolor，2 virginica |

[快照元数据](./snapshot-metadata.json)记录导出版本、修改说明与 CSV 的 SHA256。数据没有缺失值，程序仍检查非有限值、非正测量、非法类别与重复编号，避免改动数据后悄悄继续训练。

训练测试的编号见 `../results/split_manifest.csv`。单条输入演示沿用公开数据首行，只演示接口，不作为独立新样本的效果证据。
