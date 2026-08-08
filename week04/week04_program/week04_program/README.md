#week04数据分析预测模型

##模型作用

先根据老师提供的prepare_unsw_nb15.py进行对unsw_nb15_training-set.csv的数据进行一个缩小化处理选出部分数据进行后续操作并存在unsw_nb15_small.csv种
而week04_program.py是对unsw_nb15_small.csv的数据进行读取，后续为：
-将数据分为训练集和测试集
-将数据进行标准化
-用逻辑回归将标准化后的训练集来预测测试集
-生成混淆矩阵来表示模型的结果
-输出模型的精确率，召回率，f1值（2*pre*recall/(recall+pre)）