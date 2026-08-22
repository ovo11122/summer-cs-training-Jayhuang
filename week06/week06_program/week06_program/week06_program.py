import torch
import numpy as np
import torch.nn as nn
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import(
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix)
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader

#读取文件检查并分类
df = pd.read_csv('unsw_nb15_small.csv',encoding = 'utf-8')

print(f'数据来源：unsw_nb15.csv的简化版')
print(f'样本数量：{df.shape[0]}')
print(f'特征：{df.columns}')
print(f'标签分类：0->正常流量 1->攻击流量')
print(f"每行缺失值数量：{df.isnull().sum().sum()}")
print(f"每行无穷值数量：{np.isinf(df.select_dtypes(include = 'number')).sum().sum()}")
print(f'重复数量：{df.duplicated().sum().sum()}')
print(f"label类别分布：{df['label'].value_counts()}") 

df = df.replace([np.inf,-np.inf],np.nan)
df = df.dropna()
df = df.drop_duplicates()
x = df.drop(columns = ['label'])
y = df['label']


x_train,x_temp,y_train,y_temp = train_test_split(
    x,
    y,
    test_size = 0.3,
    random_state = 42,
    stratify = y)
x_val,x_test,y_val,y_test = train_test_split(
    x_temp,
    y_temp,
    test_size = 0.3,
    random_state = 42,
    stratify = y_temp)

#数据标准化
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_val_scaled = scaler.transform(x_val)
x_test_scaled = scaler.transform(x_test)

#先用逻辑回归
logistic_model = LogisticRegression(
    max_iter = 1000,
    random_state = 42)

logistic_model.fit(x_train_scaled,y_train)
logistic_predictions = logistic_model.predict(x_test_scaled)

logistic_accuracy = accuracy_score(y_test,logistic_predictions)
logistic_precision = precision_score(y_test,logistic_predictions)
logistic_recall = recall_score(y_test,logistic_predictions)
logistic_f1 = f1_score(y_test,logistic_predictions)
logistic_matrix = confusion_matrix(y_test,logistic_predictions)

print("\n逻辑回归测试结果：")
print(f"Accuracy：{logistic_accuracy:.4f}")
print(f"Precision：{logistic_precision:.4f}")
print(f"Recall：{logistic_recall:.4f}")
print(f"F1：{logistic_f1:.4f}")
print("混淆矩阵：")
print(logistic_matrix)

#转换为Tensor
x_train_tensor = torch.tensor(x_train_scaled,dtype=torch.float32)
x_val_tensor = torch.tensor(x_val_scaled,dtype=torch.float32)
x_test_tensor = torch.tensor(x_test_scaled,dtype=torch.float32)

y_train_tensor = torch.tensor(y_train.tolist(),dtype = torch.float32).unsqueeze(1)
y_val_tensor = torch.tensor(y_val.tolist(),dtype = torch.float32).unsqueeze(1)
y_test_tensor = torch.tensor(y_test.tolist(),dtype = torch.float32).unsqueeze(1)#BCEWithLogitsLoss需要[n,1]的形式


#创建dataset和dataloader
train_dataset = TensorDataset(x_train_tensor,y_train_tensor)
val_dataset = TensorDataset(x_val_tensor,y_val_tensor)
test_dataset = TensorDataset(x_test_tensor,y_test_tensor)

train_loader = DataLoader(
    train_dataset,
    batch_size = 32,
    shuffle = True)
val_loader = DataLoader(
    val_dataset,
    batch_size = 32,
    shuffle = False)
test_loader = DataLoader(
    test_dataset,
    batch_size = 32,
    shuffle = False)


#选择gpu
device = torch.device('cuda' if torch.cuda.is_available() else'cpu')
print(f'\n使用设备:{device}')


#创建mlp
model = nn.Sequential(
    nn.Linear(x.shape[1],16),
    nn.LeakyReLU(),
    
    nn.Linear(16,8),
    nn.LeakyReLU(),
    
    nn.Linear(8,1))

model = model.to(device)


#创建损失函数和优化器
loss_function = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr = 0.001)


#用mlp训练模型
epochs = 100
train_loss_history = []
val_loss_history = []
best_val_loss = 1000000
best_model_path = 'best_model.pth'

for epoch in range(epochs):
    model.train()
    total_train_loss = 0
    for batch_x,batch_y in train_loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        optimizer.zero_grad()

        raw_scores = model(batch_x)

        loss = loss_function(raw_scores,batch_y)
        loss.backward()
        optimizer.step()

        total_train_loss += loss.item()

    average_train_loss = total_train_loss / len(train_loader)
    train_loss_history.append(average_train_loss)

    model.eval()

    total_val_loss = 0
    with torch.no_grad():
        for batch_x,batch_y in val_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            raw_scores = model(batch_x)
            loss = loss_function(raw_scores,batch_y)

            total_val_loss += loss.item()

    average_val_loss = total_val_loss / len(val_loader)
    val_loss_history.append(average_val_loss)

    if average_val_loss < best_val_loss:
        best_val_loss = average_val_loss
        torch.save(model.state_dict(),best_model_path)

    print(f'第{epoch+1}轮：'
          f'训练损失{average_train_loss:.4f},'
          f'验证损失{average_val_loss:.4f}')

best_state = torch.load(best_model_path,map_location = device,weights_only = True)
model.load_state_dict(best_state)


#测试
model.eval()
all_predictions = []
all_labels = []

with torch.no_grad():
    for batch_x,batch_y in test_loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)

        raw_scores = model(batch_x)
        probabilities = torch.sigmoid(raw_scores)
        predictions = (probabilities >= 0.5).float()

        all_predictions.extend(predictions.squeeze(1).cpu().tolist())
        all_labels.extend(batch_y.squeeze(1).cpu().tolist())#sklearn评估需要[n,]数组


#评估
mlp_accuracy = accuracy_score(all_labels,all_predictions)
mlp_precision = precision_score(all_labels,all_predictions)
mlp_recall = recall_score(all_labels,all_predictions)
mlp_f1 = f1_score(all_labels,all_predictions)
mlp_matrix = confusion_matrix(all_labels,all_predictions)

print('mlp结果:')
print(f"Accuracy：{mlp_accuracy:.4f}")
print(f"Precision：{mlp_precision:.4f}")
print(f"Recall：{mlp_recall:.4f}")
print(f"F1：{mlp_f1:.4f}")
print("混淆矩阵：")
print(mlp_matrix)


#绘制曲线
epoch_num = range(1,epochs+1)
plt.plot(epoch_num,train_loss_history,label = 'Train Loss')
plt.plot(epoch_num,val_loss_history,label = 'Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()
plt.tight_layout()
plt.savefig('loss_curve.png',dpi = 300)
plt.close()

print('曲线图已保存至：loss_curve.png')
print('模型已保存至：best_model.pth')

# print(f'第一层mlp权重{model[0].weight}')