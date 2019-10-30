# -*- coding: utf-8 -*-
import numpy as np
from sklearn import tree
import pydotplus
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

''''' 数据读入 '''
data = []
labels = []
with open("data") as ifile:
    for line in ifile:
        tokens = line.strip().split(' ')
        data.append([float(tk) for tk in tokens[:-1]])
        labels.append(float(tokens[-1]))
X = np.array(data)
Y = np.array(labels)

clf = tree.DecisionTreeClassifier(criterion='entropy')

clf.fit(X, Y)

#可视化
dot_data = tree.export_graphviz(clf, out_file=None,feature_names=["age","gender","salary","marriage"],
                                class_names=["normal","medium","super"])
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("tree.pdf")
