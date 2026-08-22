# 基于网络流量特征的分类系统

## 模型介绍
这是一个简单的根据网络流量特征判断是否为攻击流量的模型，通过逻辑回归和mlp两种模型去比较
-数据来源：UNSW-NB15 数据集（经简化后的unsw_nb15_small.csv）
-样本数量：10000条网络流量记录
-特征类型：['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate', 'sttl', 'dttl',
       'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit',
       'smean', 'dmean', 'ct_srv_src', 'ct_dst_ltm', 'ct_src_ltm',
       'ct_srv_dst', 'label']
-标签含义：0->正常流量 1->攻击流量

## 运行方式
直接运行week06_program.py即可

## 得到结果
1.网络流量文件内容
2.逻辑回归测试结果，包含Accuracy，Precision，Recall，F1，confusion matrix
3.选择运行设备
4.多层感知机mlp得到的每轮训练与验证损失(包含曲线，曲线存在'loss_curve.png')
5.mlp测试结果
7.mlp最佳模型(存放在'best_model.pth')
