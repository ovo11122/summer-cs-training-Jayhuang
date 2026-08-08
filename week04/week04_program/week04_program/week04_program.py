import pandas as pd



df = pd.read_csv('unsw_nb15_small.csv',encoding = 'utf-8')


x = df.drop(columns = ['label'])
y = df['label']


#把数据分为训练集和测试集
from sklearn.model_selection import train_test_split
x_train , x_test , y_train , y_test = train_test_split(#分成x_train等这几个
    x,
    y,
    test_size=0.2,#比例
    random_state = 42,#固定的随机分组
    stratify = y)



#把数据标准化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# scaler.fit(x_train)
# x_train_scaled = scaler.transforom(x_train)
#等同于
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)




#逻辑回归
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter = 1000)
model.fit(x_train_scaled,y_train)#让模型学习
y_predicted = model.predict(x_test_scaled)#模型预测出的一个series


#正确率
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test,y_predicted)
print(f"准确率：{accuracy:.4f}")



#混淆矩阵
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_predicted)#confusion会返回一个Numpy的二维数组
# [          预测正常    预测攻击
# 实际正常     [TN,        FP],
# 实际攻击     [FN,        TP]
# ]
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
display = ConfusionMatrixDisplay(
    confusion_matrix = cm,
    display_labels = ['normal','attack'])
display.plot(cmap = 'Blues',values_format = 'd')
plt.title('Logistic Regression Confusion Matrix')
plt.tight_layout()
plt.savefig('confusion_matrix.png',dpi = 300)
plt.close()  
print("混淆矩阵：")
print(cm)



from sklearn.metrics import precision_score,recall_score
precision = precision_score(y_test,y_predicted)#精确率 TP / (TP + FP) 报警里真正攻击比例
print(f"精确值:{precision:.4f}")
recall = recall_score(y_test,y_predicted)#召回率 TP / (TP + FN) 真正攻击有多少被发现
print(f"召回值:{recall:.4f}")


from sklearn.metrics import f1_score
f1 = f1_score(y_test,y_predicted)
print(f"F1值：{f1:.4f}")
#F1 = 2 × Precision × Recall / (Precision + Recall)


# #分类评价结果
# from sklearn.metrics import classification_report
# report = classification_report(y_test,y_predicted)
# print(f'分类评价结果:{report}')


# #检查类别数量
# label_counts = y.value_counts()
# #检查类别比例
# label_rat = y.value_counts(normalize = True)#normalize是指返回比例而非数值

# #检查过拟合
# train_accuracy = model.score(x_train_scaled,y_train)
# print(f'训练集准确率：{train_accuracy:.4f}')
# test_accuracy = model.score(x_test_scaled,y_test)
# print(f'测试集准确率：{test_accuracy:.4f}')
# #用两个正确率去比较是否过拟合


# #建立结果表
# results = x_test.copy()
# results['actual'] = y_test.to_numpy()
# results['predicted'] = y_predicted

# #找出FN和FP    1指攻击 0指正常
# FP = results[(results['actual'] == 0) & (results['predicted'] == 1)]
# FN = results[(results['actual'] == 1) & (results['predicted'] == 0)]
# print(f"误报数量：{len(FP)}")
# print(f"漏报数量：{len(FN)}")
# print(f"误报数据：{FP}")
# print(f"漏报数据：{FN}")
