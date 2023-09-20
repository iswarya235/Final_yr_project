import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
a=int(input("Enter 1 for fan train 2 for light"))
if a==1:
    m="data_fan.csv"
else:
    m="data_light.csv"
data = pd.read_csv(m)
data.head()
data.shape
X = data.iloc[:,:-1]
X.head()
y = data.iloc[:,-1]
y.head()
data['Target'].value_counts()
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=1)
sns.countplot(x='Target',data=data)
plt.show()
X_train.shape
X_train.head()
y_test.shape
y_test.head()


from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
model = DecisionTreeClassifier()
model.fit(X_train,y_train)
if a==1:
    filename = 'dtfan.sav'
else:
    filename = 'dtlight.sav'
pickle.dump(model, open(filename, 'wb'))
y_pred = model.predict(X_test)
acc=(accuracy_score(y_pred,y_test)*100)
print("Accuracy is:",acc)







