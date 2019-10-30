import re
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
data = []
labels = []

def show_accuracy(a, b, tip):
    acc = a.ravel() == b.ravel()
    acc_rate = 100 * float(acc.sum()) / a.size
    return acc_rate


with open("all_data.txt") as ifile:
    for line in ifile:
        line = line.strip()
        tokens = [x for x in re.split(";|\t", line) if x]
        data.append([float(tk) for tk in tokens[:-1]])
        labels.append(tokens[-1])
x = np.array(data)
labels = np.array(labels)
y = np.zeros(labels.shape)
y[labels == '1'] = 1
x_train0, x_test0, y_train0, y_test0 = train_test_split(x, y, test_size = 0.2)
x_train1, x_test1, y_train1, y_test1 = train_test_split(x, y, test_size = 0.2)
x_train2, x_test2, y_train2, y_test2 = train_test_split(x, y, test_size = 0.2)
x_train3, x_test3, y_train3, y_test3 = train_test_split(x, y, test_size = 0.2)
x_train4, x_test4, y_train4, y_test4 = train_test_split(x, y, test_size = 0.2)
param = {'max_depth': 2, 'eta': 0.3, 'silent': 1, 'objective': 'binary:logistic'}
num_round = 2
print(param)
dtrain = xgb.DMatrix(x_train0,label = y_train0)
dtest = xgb.DMatrix(x_test0,label = y_test0)
bst = xgb.train(param, dtrain, num_round)
# # make prediction
result = bst.predict(dtest)
# print(result)
result[result > 0.5] = 1
result[~(result > 0.5)] = 0
xgb_rate = show_accuracy(result, y_test0, 'XGBoost ')
print(xgb_rate)

dtrain = xgb.DMatrix(x_train1,label = y_train1)
dtest = xgb.DMatrix(x_test1,label = y_test1)
bst = xgb.train(param, dtrain, num_round)
# # make prediction
result = bst.predict(dtest)
# print(result)
result[result > 0.5] = 1
result[~(result > 0.5)] = 0
xgb_rate = show_accuracy(result, y_test1, 'XGBoost ')
print(xgb_rate)

dtrain = xgb.DMatrix(x_train2,label = y_train2)
dtest = xgb.DMatrix(x_test2,label = y_test2)
bst = xgb.train(param, dtrain, num_round)
# # make prediction
result = bst.predict(dtest)
# print(result)
result[result > 0.5] = 1
result[~(result > 0.5)] = 0
xgb_rate = show_accuracy(result, y_test2, 'XGBoost ')
print(xgb_rate)

dtrain = xgb.DMatrix(x_train3,label = y_train3)
dtest = xgb.DMatrix(x_test3,label = y_test3)
bst = xgb.train(param, dtrain, num_round)
# # make prediction
result = bst.predict(dtest)
# print(result)
result[result > 0.5] = 1
result[~(result > 0.5)] = 0
xgb_rate = show_accuracy(result, y_test3, 'XGBoost ')
print(xgb_rate)

dtrain = xgb.DMatrix(x_train4,label = y_train4)
dtest = xgb.DMatrix(x_test4,label = y_test4)
bst = xgb.train(param, dtrain, num_round)
# # make prediction
result = bst.predict(dtest)
# print(result)
result[result > 0.5] = 1
result[~(result > 0.5)] = 0
xgb_rate = show_accuracy(result, y_test4, 'XGBoost ')
print(xgb_rate)