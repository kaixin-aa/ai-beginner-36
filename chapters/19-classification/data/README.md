# 第 19 章 Iris 数据说明

本章复制第 17 章固定公开 CSV 与快照元数据，测量值、编号和类别映射未改动，获取日期为 2026 年 10 月 3 日，导出库版本为 scikit-learn 1.7.2。CSV 的 SHA256 与[元数据](./snapshot-metadata.json)一致。

原始署名为 Fisher, R. (1936). Iris [Dataset]. UCI Machine Learning Repository，[DOI](https://doi.org/10.24432/C56C76)。[UCI 数据页](https://archive.ics.uci.edu/dataset/53/iris)标示 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。教学使用不代表原作者认可本教程。

本快照由 scikit-learn 导出，采用该库已修正的测量点，未宣称逐字复刻早期 UCI 文件。[官方数据接口](https://scikit-learn.org/1.7/modules/generated/sklearn.datasets.load_iris.html)说明记录数与测量字段。

| 字段 | 含义 | 单位或编码 |
|---|---|---|
| sample_id | 原顺序生成的教学编号 | 不作特征 |
| sepal_length_cm | 萼片长度 | 厘米 |
| sepal_width_cm | 萼片宽度 | 厘米 |
| petal_length_cm | 花瓣长度 | 厘米 |
| petal_width_cm | 花瓣宽度 | 厘米 |
| target | 类别标签 | 0 setosa，1 versicolor，2 virginica |

新增教学材料仅包括概率顺序题与绘图网格。网格为程序生成的输入组合，没有真实标签，不加入训练或测试指标。
