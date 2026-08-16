# week05
## 数据集
使用Breast Cancer Wisconsin Diagnostic数据集。
- 样本数量：569
- 数值特征数量：30
- label = 0：malignant（恶性）
- label = 1：benign（良性）
- malignant：212条
- benign：357条

## 代码及模型结构
1.读取并拆分为数据和标签
2.将数据拆分为train validation和test
3.将数据标准化并转化为tensor形式
4.用dataset两两联系并用dataloader划分每batch的数据大小
5.选择cpu或gpu
6.创建了一个两个线性层的多层感知机，模型输入为30个特征，隐藏层包含16个神经元，并用了ReLU作为激活函数引入非线性
7.创建损失函数和优化器
8.进行模型的训练和验证
9.对模型进行评价
10.画出每个epoch的损失折线图