# -*- coding: utf-8 -*-
"""Twitter Sentiment Analysis using ML.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/126FM73KAUXd7mu5yBMB8AQle99JOmn8r
"""

#installing kaggle library
! pip install kaggle

"""Upload your Kaggle.json file

"""

# configuring the path of kaggle.json file
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

"""Importing Twitter Sentiment dataset

"""

#API to fetch the dataset from Kaggle
!kaggle datasets download -d kazanova/sentiment140

#extracting the compressed dataset

from zipfile import ZipFile
dataset = '/content/sentiment140.zip'

with ZipFile(dataset,'r') as zip:
  zip.extractall()
  print('The dataset is extracted')

"""Importing the Dependencies"""

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

#printing the stopwords in English
print(stopwords.words('english'))

"""Data Processing"""

#loading the data from csv file to pandas dataframe
twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv',encoding = 'ISO-8859-1')

#checking the number of rows and columns
twitter_data.shape

#printing the first 5 rows of the dataframe
twitter_data.head()

#naming the columns and reading the dataset again

column_names =['target','id','date','flag','user','text']
twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv',names = column_names , encoding = 'ISO-8859-1')

#checking the number of rows and columns
twitter_data.shape

#printing the first 5 rows of the dataframe
twitter_data.head()

#counting the number of missing values in the dataset
 twitter_data.isnull().sum()

#checking the distribution of target column
twitter_data['target'].value_counts()

"""Convert the target "4" to "1"
"""

twitter_data.replace({'target':{4:1}}, inplace=True)

"""0 ->Negative Tweet

1 ->Positive Tweet

**Stemming**

Stemming is the process of reducing a word to its Root word

example:actor,actress,acting =act
"""

port_stem = PorterStemmer()

def stemming(content):
  stemmed_content = re.sub('[^a-zA-Z]',' ',content)
  stemmed_content = stemmed_content.lower()
  stemmed_content = stemmed_content.split()
  stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content =' '.join(stemmed_content)
  return stemmed_content

twitter_data['stemmed_content'] = twitter_data['text'].apply(stemming)

twitter_data.head()

print(twitter_data['stemmed_content'])

print(twitter_data['target'])

#separating the data and label
 X = twitter_data['stemmed_content'].values
 Y = twitter_data['target'].values

print(X)

print(Y)

"""Splitting the data to training data and test data"""

X_train,X_test,Y_train,Y_test =train_test_split(X,Y,test_size=0.2,stratify=Y,random_state=2)

print(X.shape, X_train.shape,X_test.shape)

print(X_train)

print(X_test)

#converting the textual data to numerical data

vectorizer =TfidfVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train)

print(X_test)

"""Training the Machine Learning Model

Logistic Regression
"""

model = LogisticRegression(max_iter=1000)

model.fit(X_train,Y_train)

"""Model Evaluation

Accuracy Score
"""

#accuracy score on the training model

X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(Y_train, X_train_prediction)

print('Accuracy score on the training data:', training_data_accuracy)

#accuracy score on the test data

X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(Y_test, X_test_prediction)

print('Accuracy score on the training data:', test_data_accuracy)

"""Model Accuracy = 77.8%

Saving the trained model
"""

import pickle

filename ='trained_model.sav'
pickle.dump(model, open(filename,'wb'))

"""Using the saved model for future predictions"""

#loadind the saved model
loaded_model = pickle.load(open('/content/trained_model.sav', 'rb'))

X_new = X_test[200]
print(Y_test[200])

prediction = model.predict(X_new)
print(prediction)

if(prediction[0] == 0):
  print('Negative Tweet')

else:
  print('Positve Tweet')

X_new = X_test[3]
print(Y_test[3])

prediction = model.predict(X_new)
print(prediction)

if(prediction[0] == 0):
  print('Negative Tweet')

else:
  print('Positve Tweet')