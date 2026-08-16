#存入数据
import torch
# x = torch.tensor()#括号里放列表 列表适合放普通数据 神经网络需要进行大量数学运算
# y = torch.tensor()

#第一次划分
# from sklearn.model_selection import train_test_split
# x_train,x_temp,y_train,y_temp = train_test_split(
#     x,
#     y,
#     test_size = 0.3,
#     random_state = 42,
#     stratify = y)

# #第二次划分
# x_val,x_test,y_val,y_test = train_test_split(
#     x_temp,
#     y_temp,
#     test_size = 0.5,
#     random_state = 42,
#     stratify = y_temp
#     )

#把样本特征和标签对应起来
from torch.utils.data import TensorDataset
# train_dataset = TensorDataset(
#     x,
#     y)

#分批处理
from torch.utils.data import DataLoader
# train_loader = DataLoader(
#     train_dataset,
#     batch_size = 32,#一次上传32组数据
#     shuffle = True#每次训练前打乱数据
#     )

#循环epoch
# for epoch in range(100):
#     for batch_x,batch_y in train_dataset

# import torch.nn as nn
# model = nn.Sequential(
#     nn.Linear(30,16),
#     nn.ReLU(),
#     nn.Linear(16,1))


# #转化结果
# logits = model(batch_x)
# probabilities = torch.sigmoid(logits)#把分数转换为0到1
# predictions = (probabilities >= 0.5).float()
# #或者
# loss_function = nn.BCEWithLogitsLoss #先创建损失函数
# logits = model(batch_x) #logits的形状是（32，1）
# #统一格式为（32，1）
# batch_y = batch_y.unsqueeze(1)#原本为（32，）
# loss = loss_function(logits,batch_y)
# #优化器
# optimizer = torch.optim.Adam(
#     model.parameters(),
#     lr = 0.001)

# #计算损失 梯度 向前传播向后传播
# model.train()
# # optimizer.zero_grad()
# # prediction = model(batch_x)
# # loss = loss_function(prediction,batch_y)
# # loss.backward() #从损失值开始往回计算得到每个参数的梯度 梯度=权重对损失的导数 所以要往负梯度方向调整
# # optimizer.step()#根据梯度修改权重和偏值

# #验证集
# model.eval()
# with torch.no_grad():
#     raw_scores = model(val_x)

# #评价函数
# from sklearn.metrics import(
#     accuracy_score,
#     precision_score,
#     recall_score,
#     f1_score,
#     confusion_matrix)

# #保存文件
# torch.save(
#     model.state_dict(),
#     "breast_cancer_model.pth"
#     )

# #加载模型
# #1重新创建相同结构
# loaded_model = nn.Sequential(
#     nn.Linear(30,16),
#     nn.ReLU(),
#     nn.Linear(16,1))
# #2读取参数文件
# saved_parameters = torch.load(
#     "breast_cancer_model.pth",
#     weights_only = True)
# #3把参数放进模型
# loaded_model.load_state_dict(
#     saved_parameters)
# #4切换模式
# loaded_model.eval()
