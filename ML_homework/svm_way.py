from sklearn import svm
from sklearn import cross_validation
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
data = []
labels = []
with open("all_data.txt") as ifile:
        for line in ifile:
            line = line.strip()
            tokens = [x for x in re.split(";|\t", line) if x]
            data.append([float(tk) for tk in tokens[:-1]])
            labels.append(tokens[-1])
x = np.array(data)
labels = np.array(labels)
y = np.zeros(labels.shape)
y[labels=='1']=1
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.25)

clf_linear = svm.SVC(kernel='linear')
clf_poly = svm.SVC(kernel='poly', degree=3)
clf_rbf = svm.SVC()
clf_sigmoid = svm.SVC(kernel='sigmoid')

scores_linear = cross_validation.cross_val_score(clf_linear,x,y,cv=5)
scores_poly = cross_validation.cross_val_score(clf_poly,x,y,cv=5)
scores_rbf = cross_validation.cross_val_score(clf_rbf,x,y,cv=5)
scores_sigmoid = cross_validation.cross_val_score(clf_sigmoid,x,y,cv=5)

print("scores_linear",scores_linear)
print("scores_poly",scores_poly)
print("scores_rbf",scores_rbf)
print("scores_sigmoid",scores_sigmoid)
# clf_linear.fit(x_train,y_train)
# clf_poly.fit(x_train,y_train)
# clf_rbf.fit(x_train,y_train)
# clf_sigmoid.fit(x_train,y_train)
# linear_predicted = clf_linear.predict(x_test)
# poly_predicted = clf_poly.predict(x_test)
# rbf_predicted = clf_rbf.predict(x_test)
# sigmoid_predicted = clf_sigmoid.predict(x_test)
# for way in [linear_predicted,poly_predicted,rbf_predicted,sigmoid_predicted]:
#     accuracy = metrics.accuracy_score(y_test,way)
#     print(accuracy)
