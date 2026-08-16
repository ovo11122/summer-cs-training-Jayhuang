import pandas as pd
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import(
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix)
from torch.utils.data import(
    TensorDataset,
    DataLoader)

#读取拆分xy
df = pd.read_csv('breast_cancer_wisconsin.csv')
x = df.drop(columns = ['label','label_name'])
y = df['label']
print("程序已经开始运行")

#拆分三份数据
x_train,x_temp,y_train,y_temp = train_test_split(
    x,
    y,
    test_size = 0.3,
    random_state = 42,
    stratify = y)
x_val,x_test,y_val,y_test = train_test_split(
    x_temp,
    y_temp,
    test_size = 0.5,
    random_state = 42,
    stratify = y_temp)

print("样本数量：", df.shape[0])
print("特征数量：", x.shape[1])
print("\n标签对应关系：")
print("0->malignant  1->benign")
print("\n类别分布：")
print(df["label_name"].value_counts())
#标准化
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)#以第一个为标准fit
x_val_scaled = scaler.transform(x_val)
x_test_scaled = scaler.transform(x_test)

#转化为tensor
x_train_tensor = torch.tensor(x_train_scaled,dtype = torch.float32)
x_val_tensor = torch.tensor(x_val_scaled,dtype = torch.float32)
x_test_tensor = torch.tensor(x_test_scaled,dtype = torch.float32)
y_train_tensor = torch.tensor(y_train.tolist(),dtype = torch.float32).unsqueeze(1)
y_val_tensor = torch.tensor(y_val.tolist(),dtype = torch.float32).unsqueeze(1)
y_test_tensor =torch.tensor(y_test.tolist(),dtype = torch.float32).unsqueeze(1)

#创建dataset和dataloader
train_dataset = TensorDataset(x_train_tensor,y_train_tensor)
val_dataset = TensorDataset(x_val_tensor,y_val_tensor)
test_dataset = TensorDataset(x_test_tensor,y_test_tensor)
train_loader = DataLoader(train_dataset,batch_size = 32,shuffle = True)
val_loader = DataLoader(val_dataset,batch_size = 32,shuffle = False)
test_loader = DataLoader(test_dataset,batch_size = 32,shuffle = False)

#选择cpu或gpu
device = torch.device(
    'cuda'
    if torch.cuda.is_available()
    else'cpu')
print('使用设备',device)

#创建模型
hidden_size = 16
model = nn.Sequential(
    nn.Linear(x.shape[1],hidden_size),
    nn.ReLU(),
    nn.Linear(hidden_size,1)
    )
model = model.to(device)

#损失函数和优化器
loss_function = nn.BCEWithLogitsLoss()#原始分数->通过sigmoid->0-1概率->二元交叉熵->差距
optimizer = torch.optim.Adam(
    model.parameters(),#取模型的参数（权重和偏置）
    lr = 0.001)

#训练 验证
epochs = 100
train_loss_history = []
val_loss_history = []
best_val_loss = 1000
best_model_path = f"best_model_hidden_{hidden_size}.pth"
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
        total_train_loss += loss.item()#总损失

    average_train_loss = total_train_loss / len(train_loader)#平均损失
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
        torch.save(
            model.state_dict(),
            best_model_path)
    print(f'第{epoch+1}轮:训练损失：{average_train_loss:.4f} 验证损失：{average_val_loss:.4f}')
best_parameters = torch.load(
    best_model_path,
    map_location = device,
    weights_only = True)
model.load_state_dict(best_parameters)
model = model.to(device)
print(f'最佳验证损失：{best_val_loss:.4f}')

#最终评价
model.eval()
all_predictions = []
all_labels = []
with torch.no_grad():
    for batch_x,batch_y in test_loader:
        batch_x = batch_x.to(device)
        batch_y = batch_y.to(device)
        raw_scores = model(batch_x)
        probabilities = torch.sigmoid(raw_scores)#把原始分转化为0-1的概率
        predictions = (probabilities >= 0.5).float()#转化为0和1
        all_predictions.extend(predictions.squeeze(1).cpu().tolist())
        all_labels.extend(batch_y.squeeze(1).cpu().tolist())

accuracy = accuracy_score(all_labels,all_predictions)
precision = precision_score(all_labels,all_predictions)
recall = recall_score(all_labels,all_predictions)
f1 = f1_score(all_labels,all_predictions)
matrix = confusion_matrix(all_labels,all_predictions)
print("\n测试集评价结果：")
print(f"准确率 Accuracy：{accuracy:.4f}")
print(f"精确率 Precision：{precision:.4f}")
print(f"召回率 Recall：{recall:.4f}")
print(f"F1值：{f1:.4f}")
print("混淆矩阵：")
print(matrix)

#画图
epoch_numbers = range(1,epochs+1)
plt.plot(
    epoch_numbers,
    train_loss_history,
    label = 'Train Loss')
plt.plot(
    epoch_numbers,
    val_loss_history,
    label = 'validation Loss')
plt.title('Training and Validation Loss')
plt.legend()#显示线条名称
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.tight_layout()
plt.savefig(
    f'loss_curve_hidden_{hidden_size}.png',
    dpi = 300)
plt.close()