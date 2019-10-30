from sklearn.ensemble import RandomForestClassifier
import re
import numpy as np
from sklearn import cross_validation

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
y[labels == '1'] = 1
clf = RandomForestClassifier(max_depth=2, random_state=0)
scores1 = cross_validation.cross_val_score(clf,x,y,cv=5)
print("max_depth = 2",scores1)

clf2 = RandomForestClassifier(max_depth=5,random_state=0)
scores2 = cross_validation.cross_val_score(clf2,x,y,cv=5)
print("max_depth = 5",scores2)

clf3 = RandomForestClassifier(max_depth=10,random_state=0)
scores3 = cross_validation.cross_val_score(clf3,x,y,cv=5)
print("max_depth = 10",scores3)
