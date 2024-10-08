# 苏纯玉第二章周作业
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import random
import numpy as np

# def judge(i):
#     if i % 2 == 0:
#         return True
#     else:
#         return False
#
# def build_sample():
#     x=[]
#     x.append(random.randint(1, 100))
#     x.append(random.randint(1, 100))
#     if judge(x[0]):
#         if judge(x[1]):
#             return x, 0
#         else:
#             return x, 1
#     else:
#         if judge(x[1]):
#             return x, 1
#         else:
#             return x, 0
#
# def build_dataset(num):
#     X = []
#     Y = []
#     for i in range(num):
#         x, y = build_sample()
#         X.append(x)
#         Y.append(y)
#     return torch.FloatTensor(X), torch.LongTensor(Y)

def build_sample():
    x = np.random.random(5)
    if x[0] > x[4]:
        return x, 1
    else:
        return x, 0
#
#
# # 随机生成一批样本
# # 正负样本均匀生成
def build_dataset(total_sample_num):
    X = []
    Y = []
    for i in range(total_sample_num):
        x, y = build_sample()
        X.append(x)
        Y.append(y)
    return torch.FloatTensor(X), torch.LongTensor(Y)


class tor_mod(nn.Module):
    def __init__(self, input_size):
        super(tor_mod,self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        # self.fc2 = nn.Linear(64, 32)
        # self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(64, 2)
        self.act = torch.sigmoid
        self.loss = nn.CrossEntropyLoss()

    def forward(self, x, y=None):
        x = self.fc1(x)
        # x = self.fc2(x)
        # x = self.fc3(x)
        x = self.fc4(x)
        y_pred = self.act(x)
        if y is not None:
            return self.loss(y_pred, y)  # 预测值和真实值计算损失
        else:
            return torch.softmax(y_pred, dim=0)

# def evaluate(model):
#     model.eval()
#     num = 100
#     x,y = build_dataset(num)
#     correct, wrong = 0, 0
#     with torch.no_grad():
#         for i in range(num):
#             x_ = x[i]
#             y_ = int(y[i])
#             y_pred = model(x_)
#             if y_ == list(y_pred.numpy()).index(float(y_pred.max())):
#                 correct += 1
#             else:
#                 wrong += 1
#         print("正确预测个数：%d, 正确率：%f" % (correct, correct / (correct + wrong)))



# 测试代码
# 用来测试每轮模型的准确率
def evaluate(model):
    model.eval()
    test_sample_num = 100
    x, y = build_dataset(test_sample_num)
    # print("本次预测集中共有%d个正样本，%d个负样本" % (sum(y), test_sample_num - sum(y)))
    correct, wrong = 0, 0
    # with torch.no_grad():
    y_pred = model(x)
    for y_p, y_t in zip(y_pred, y):# 模型预测
        if y_t == list(y_p.detach().numpy()).index(float(y_p.max())):
            correct += 1
        else:
            wrong += 1
    print("正确预测个数：%d, 正确率：%f" % (correct, correct / (correct + wrong)))
    return correct / (correct + wrong)


def main():
    epoch_num = 50  # 训练轮数
    batch_size = 50  # 每次训练样本个数
    num = 50000
    input_size = 5 # 输入向量维度
    learning_rate = 0.0001  # 学习率00
    model = tor_mod(input_size)
    optim = torch.optim.Adam(model.parameters(), lr=learning_rate)
    train_x, train_y = build_dataset(num)
    evaluate(model)
    for epoch in range(epoch_num):
        model.train()
        loss_data = []
        for i in range(num//batch_size):
            x = train_x[i*batch_size:i*batch_size+batch_size]
            y = train_y[i*batch_size:i*batch_size+batch_size]
            loss = model(x, y)
            loss_data.append(loss.item())
            loss.backward()
            optim.step()
            optim.zero_grad()

        print("=========\n第%d轮平均loss:%f" % (epoch + 1, np.mean(loss_data)))
        evaluate(model)
if __name__ == '__main__':
    main()
