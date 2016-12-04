import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

input_file_path = "/Users/saurabhpandey/Desktop/DataScience/PastHires.csv"

df = pd.read_csv(input_file_path,header=0)
d = {'Y' : 0,'N':1}
df['Hired'] = df['Hired'].map(d)
df['Interned'] = df['Interned'].map(d)
df['Employed?'] = df['Employed?'].map(d)
df['Top-tier school'] = df['Top-tier school'].map(d)
d = {'BS':0,'MS':1,'PhD':2}
df['Level of Education'] = df['Level of Education'].map(d)
features = list(df.columns[:6])
print features
Y = df['Hired']
X = df[features]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X,Y)

clf = RandomForestClassifier(n_estimators=1000)
clf = clf.fit(X,Y)

print clf.predict([[10,1,4,0,0,0]])
print clf.predict([[10,0,4,0,0,1]])


