# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
 
from sklearn.metrics import log_loss, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.cross_validation import cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
 
import numpy as np
import os
import os.path
 
dt = np.dtype([('Id', 'a30'), ('Class', 'u2')])
data = np.loadtxt('trainLabels.csv', skiprows=1, delimiter = ',', dtype=dt)
 
X = np.zeros((data.shape[0], 2))
Y = data['Class']
 
 
for i, (Id, Class) in enumerate(data):
    asmFile = 'train/'+Id[1:-1]+'.asm'
    if os.path.isfile(asmFile):
        X[i][0] = os.path.getsize(asmFile)
    bytesFile = 'train/'+Id[1:-1]+'.bytes'
    if os.path.isfile(bytesFile):
        X[i][1] = os.path.getsize(bytesFile)

# <codecell>

plt.axis((0,1.6*10**8, 0, 2*10**7))
plt.scatter(X[:,0], X[:,1], c=Y, alpha=0.5)
#plt.show()

# <codecell>

denseX = np.zeros((data.shape[0], 2))
i = 0
for elem in X:
    if elem[0] != 0 and elem[1] != 0:
        denseX[i] = elem
        i = i + 1
denseX = denseX[:i]
Y=Y[:i]

# <codecell>

def trainCV(X,y, clf):
 
    # Construct a kfolds object
    kf = KFold(len(y),n_folds=10,shuffle=True)
    #y_prob = np.zeros((len(y),3))
    #y_pred = np.zeros(len(y))
     
    # Iterate through folds
    for train_index, test_index in kf:
        X_train, X_test = X[train_index], X[test_index]
        #print X_train
        #print "test", test_index
        y_train = y[train_index]
 
        clf.fit(X_train,y_train)
        #predictions = clf.predict_proba(X_test)
        #print "predictions", predictions
        #y_prob[test_index] = predictions
        #y_pred[test_index] = clf.predict(X_test)
     
    #return y_prob, y_pred

# <codecell>

#clf1 = LogisticRegression()
clf2 = ExtraTreesClassifier(n_estimators=2000, max_features=None, min_samples_leaf=2,
        min_samples_split=3, n_jobs=1, criterion='gini')
trainCV(X,Y,clf2)
#print '%.3f' % log_loss(Y, p2)
#cm = confusion_matrix(Y, pred2)
#print(cm)

# <codecell>

predictions = clf2.predict_proba(X)

# <codecell>

a,b=data[0]
#a=a[1:-1]

# <codecell>

import numpy as np
np.insert(predictions[0],0,"hi")
print predictions[0]

# <codecell>

import csv
for i in range(len(predictions)):
    probs = predictions[i]
    idStr,b=data[0]
    idStr=idStr[1:-1]
    myfile = open('results.csv', 'wb')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    mylist = [idStr]
    for prob in probs:
        mylist.append(str(prob))
    #print mylist
    wr.writerow(mylist)
    

# <codecell>


