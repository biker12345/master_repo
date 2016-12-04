'''  import the required packages '''

import os
import io
import  numpy as np
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def readFiles(path):
    for root, dirnames,filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(root,filename)
            inBody = False
            lines = []
            f = io.open(path,'r',encoding='latin1')
            for line in f :
                if inBody :
                    lines.append(line)
                elif line == '\n':
                    inBody = True
            f.close()
            message = '\n'.join(lines)
            yield path , message




def dataFrameFromDirectory(path,classification):
    rows = []
    index = []
    for filenames,msg in readFiles(path):
        rows.append({'message':msg,'class':classification})
        index.append(filenames)

    return DataFrame(rows,index=index)

def show_most_informative_features(vectorizer, clf, n=50):
    class_labels = classifier.classes_
    feature_names = vectorizer.get_feature_names()
    topn_class1 = sorted(zip(classifier.coef_[0], feature_names))[:n]
    topn_class2 = sorted(zip(classifier.coef_[0], feature_names))[-n:]

    for coef, feat in topn_class1:
        print class_labels[0], coef, feat

    print

    for coef, feat in reversed(topn_class2):
        print class_labels[1], coef, feat

data = DataFrame({'message' : [],'class': [] })
data = data.append(dataFrameFromDirectory('/Users/saurabhpandey/Desktop/DataScience/emails/spam','spam'))
data = data.append(dataFrameFromDirectory('/Users/saurabhpandey/Desktop/DataScience/emails/ham','ham'))


vector = CountVectorizer()
counts = vector.fit_transform(data['message'].values)
classifier = MultinomialNB()
target = data['class'].values
classifier.fit(counts,target)
#show_most_informative_features(vector,classifier)

test_example = ['fuck','000393']

example_count = vector.transform(test_example)
prediction = classifier.predict(example_count)
print prediction




