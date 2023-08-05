#Stochastic Gradient Descent for Logistic Regression
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn import datasets, linear_model, metrics, model_selection
from math import exp
#import test
#import data
import urllib2 as urel
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import csv

def load_csv(filename):
    """Loads CSV file.

    Args:
        filename: String for the CSV filename.

    Returns:
        lines: List of text lines.
    """
    lines = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        lines.extend(iter(reader))
    return lines

def logistic(x):
    return 1 / (1+exp(-x))

def dot(x, y):
    return sum(i*j for (i, j) in zip(x, y))

def predict(model, point):
    return logistic(dot(model,point['features']))

def accuracy(data, predictions):
    #correct=0   
    #print ("data",data, "predictions",predictions)
    correct=sum(1 for (a, b) in zip(data, predictions) if a==b)
    total=len(predictions)
    return (correct/total)*100

def update(model, point, delta, rate, lam): 
    #predict function
    yhat = predict(model,point)
    y=point['label']
    #L2 regularization
    cost_regul=[lam*wi for wi in model]
    #Cost function for error
    cost_err=[delta*(y-yhat)*xi for xi in point['features']]
    delw=[rate*(cost_err_i - cost_regul_i) for cost_err_i, cost_regul_i in zip(cost_err, cost_regul)]
    #weight update based on delw
    model=[(wi + delwi) for wi, delwi in zip(model, delw)]
    #print("yhat:", yhat, "y :"y, "correct prediction?",round(yhat)==y)
    return model

def initialize_model(k):
    return [random.gauss(0, 1) for _ in range(k)]

def train(data, epochs, rate, lam, delta):
    #intialize paramters
    counter=0
    N=len(data)
    w = initialize_model(len(data[0]['features']))
    #print ("initial weights", w)
    for i in range(epochs):
        for _ in range(N):
            counter+=1
            p=random.randrange(N)
            #print ("obs", p)
            #update function
            w = update(w, data[p], delta, rate, lam)
        yhat_all = [round(predict(w,data[k])) for k in range(N)]
        y_all = [data[k]['label'] for k in range(N)]
        #accuracy function
        acc=accuracy(y_all, yhat_all)
        #print accuracy and weights after an epoch
        print ("epoch:", i, "accuracy", acc)
        #print ("weights:", w)
        print ("\n")
        print ("\n")
    return w

def extract_features(raw):
    data = []
    for r in raw:
        features = [
            1.0,
            float(r['age']) / 100,
            float(r['education_num']) / 10,
            float(r['hr_per_week']) >= 41,
            float(r['capital_gain']) / 10000,
            float(r['capital_loss']) / 10000,
            r['marital'] == 'Married-civ-spouse',
            r['type_employer'] == 'Self-emp-inc',
            r['occupation'] == 'Prof-specialty',
            r['occupation'] == 'Exec-managerial',
            r['race'] == 'White',
            r['sex'] == 'Male',
        ]
        point = {"label": r['income'] == '>50K', 'features': features}
        data.append(point)
    return data

#specify hyperparams in train function as follows:
#submission(data, epochs, rate, lam, delta), where:
#epcohs: total iterations over the entire dataset
#rate: overall learning rate
#lam: regularization rate
#delta: cost function rate
def submission(csv_import,epochs, rate, lam, delta):
    data=extract_features(csv)
    return train(data,epochs, rate, lam, delta)

##LOAD FILE
csv=load_csv('adult_train.csv')
##RUN TRAINING
submission(csv,100,0.1,0.01,0.1)
