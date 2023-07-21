# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 13:23:17 2021

Main script dedicated to analyse the dependancy between the sub-harmonic (F/2)
levels of given contrast agents and the local hydrostatic pressure.

Last revised : 24.09.2021

@author: alexis.vivien
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import sklearn as sk
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import ElasticNet
from itertools import permutations
from itertools import combinations
from sklearn import linear_model
from sklearn import svm

# Function to map the colors as a list from the input list of x variables
def pltcolor(lst):
    cols=[]
    for l in lst:
        if l==90:
            cols.append(1)
        elif l==120:
            cols.append(2)
        else:
            cols.append(3)
    return cols

################### STORE DATA IN VARIABLES ##################################

data_fit = pd.read_csv(r'C:\Users\alexis.vivien\Documents\Python Scripts\UlaOp\data_fit_2_indep.csv')
data = pd.read_csv(r'C:\Users\alexis.vivien\Documents\Python Scripts\UlaOp\data_2_indep.csv')
data_fit_top = data_fit.columns; data_top = data.columns

data_fit = data_fit.to_numpy()
data = data.to_numpy()
data[data == 0] = 1 # replace 0 with 1 (0 to 1 mmHg does not chenge anything but it helps to get rid of 0)

# comb = combinations([0],1)
comb = combinations([0,1,2,3,4,5,6,7],5) # Create a list of features couples, each with the actual acoustic pressure

######################### VISUALIZE DATA #####################################
    
fig, axs = plt.subplots(2, 4, sharex = True)
indice = 0;
for ax in axs.flat:
    ax.plot(data_fit[:,8],data_fit[:,indice],'.')
    ax.set(xlabel = data_fit_top[8], ylabel = data_fit_top[indice], title = data_fit_top[indice])
    indice += 1
    # Hide x labels and tick labels for all but bottom plot.
    # ax.label_outer()

plt.show()

######################## MODELS ##############################################
model = 'SVM rbf';
#######################################################
######################## LASSO ########################
#######################################################
index = 0;
r_square_adj = np.array([])

if model == 'Lasso':
    print('Lasso model ...')
    for pair in list(comb):
        X_fit = data_fit[:,pair] # features used to train the model
        X = data[:,pair]         # same features used to test the model
        y = data[:,8]
        reg = linear_model.Lasso(alpha=1e-6,tol = 1e-4, max_iter = 1000)
        reg.fit(X_fit,data_fit[:,8])
        data_predicted = reg.predict(X)
        # plt.figure()
        # plt.plot(data_predicted, data_model[:,8],'.')
        mse = sk.metrics.mean_squared_error(data[:,8], data_predicted) # Mean Squared Error
        mae = sk.metrics.mean_absolute_error(data[:,8], data_predicted) # Mean Absolute Error
        r_square_adj = np.append(r_square_adj,1 - (1-reg.score(X, y))*(len(y)-1)/(len(y)-X.shape[1]-1)) # Adjusted R^2 value

        # Create the colors list using the function above
        cols=pltcolor(data[:,8])
        classes = ['90 mmHg', '120 mmHg', '150 mmHg']
        values = cols
        colours = ListedColormap(['g','b','r'])
        if r_square_adj[index] == max(r_square_adj):
            fig, ax = plt.subplots()
            scatter = ax.scatter(list(range(1, len(data[:,8])+1)),((data_predicted-data[:,8])/data[:,8]*100),c=values, cmap = colours)
            plt.legend(handles = scatter.legend_elements()[0], labels = classes)
            ax.set(xlabel = 'Acq #', ylabel = 'Model Error Percentage', title = 'Lasso Linear Model [' + str(pair) + '] - alpha 1e-1 - adjusted R^2 = ' + str(r_square_adj[index]))
        index = index+1;

#######################################################
##################### ELASTIC NET #####################
#######################################################
elif model == 'ElasticNet':
    print('ElasticNet model ...')
    for pair in list(comb):
        print(pair)
        X_fit = data_fit[:,pair] # features used to train the model
        X = data[:,pair]         # same features used to test the model
        y_fit = data_fit[:,8]
        y = data[:,8]
        reg = ElasticNet()
        reg.fit(X_fit, y_fit)
        data_predicted = reg.predict(X)
        mse = sk.metrics.mean_squared_error(data[:,8], data_predicted) # Mean Squared Error
        mae = sk.metrics.mean_absolute_error(data[:,8], data_predicted) # Mean Absolute Error
        r_square_adj = np.append(r_square_adj,1 - (1-reg.score(X, y))*(len(y)-1)/(len(y)-X.shape[1]-1)) # Adjusted R^2 value
        cols=pltcolor(data[:,8])
        classes = ['90 mmHg', '120 mmHg', '150 mmHg']
        values = cols
        colours = ListedColormap(['g','b','r'])
        if r_square_adj[index] == max(r_square_adj):
            fig, ax = plt.subplots()
            scatter = ax.scatter(list(range(1, len(data[:,8])+1)),((data_predicted-data[:,8])/data[:,8]*100),c=values, cmap = colours)
            plt.legend(handles = scatter.legend_elements()[0], labels = classes)
            ax.set(xlabel = 'Acq #', ylabel = 'Model Error Percentage', title = 'ElasticNet Model [' + str(pair) + '] - adjusted R^2 = ' + str(r_square_adj[index]))
        index = index+1;

#######################################################
################### Ridge Regression ##################
#######################################################
elif model == 'Ridge':
    print('Ridge Regression model ...')
    for pair in list(comb):
        print(pair)
        X_fit = data_fit[:,pair] # features used to train the model
        X = data[:,pair]         # same features used to test the model
        y_fit = data_fit[:,8]
        y = data[:,8]
        reg = linear_model.Ridge(alpha=1e-6)
        reg.fit(X_fit, y_fit)
        data_predicted = reg.predict(X)
        mse = sk.metrics.mean_squared_error(data[:,8], data_predicted) # Mean Squared Error
        mae = sk.metrics.mean_absolute_error(data[:,8], data_predicted) # Mean Absolute Error
        r_square_adj = np.append(r_square_adj,1 - (1-reg.score(X, y))*(len(y)-1)/(len(y)-X.shape[1]-1)) # Adjusted R^2 value
        cols=pltcolor(data[:,8])
        classes = ['90 mmHg', '120 mmHg', '150 mmHg']
        values = cols
        colours = ListedColormap(['g','b','r'])
        if r_square_adj[index] == max(r_square_adj):
        # if r_square_adj[index] >= 0:
            fig, ax = plt.subplots()
            scatter = ax.scatter(list(range(1, len(data[:,8])+1)),((data_predicted-data[:,8])/data[:,8]*100),c=values, cmap = colours)
            plt.legend(handles = scatter.legend_elements()[0], labels = classes)
            ax.set(xlabel = 'Acq #', ylabel = 'Model Error Percentage', title = 'Ridge Regression Model [' + str(pair) + '] - adjusted R^2 = ' + str(r_square_adj[index]))
        index = index+1;
        
#######################################################
################## SVM - Linear Kernel ################
#######################################################
elif model == 'SVMLinear':
    print('SVM Linear Kernel Regression model ...')
    for pair in list(comb):
        print(pair)
        X_fit = data_fit[:,pair] # features used to train the model
        X = data[:,pair]         # same features used to test the model
        y_fit = data_fit[:,8]
        y = data[:,8]
        reg = svm.SVR()
        reg.fit(X_fit, y_fit)
        data_predicted = reg.predict(X)
        mse = sk.metrics.mean_squared_error(data[:,8], data_predicted) # Mean Squared Error
        mae = sk.metrics.mean_absolute_error(data[:,8], data_predicted) # Mean Absolute Error
        r_square_adj = np.append(r_square_adj,1 - (1-reg.score(X, y))*(len(y)-1)/(len(y)-X.shape[1]-1)) # Adjusted R^2 value
        cols=pltcolor(data[:,8])
        classes = ['90 mmHg', '120 mmHg', '150 mmHg']
        values = cols
        colours = ListedColormap(['g','b','r'])
        if r_square_adj[index] == max(r_square_adj):
        # if r_square_adj[index] >= 0:
            fig, ax = plt.subplots()
            scatter = ax.scatter(list(range(1, len(data[:,8])+1)),((data_predicted-data[:,8])/data[:,8]*100),c=values, cmap = colours)
            plt.legend(handles = scatter.legend_elements()[0], labels = classes)
            ax.set(xlabel = 'Acq #', ylabel = 'Model Error Percentage', title = 'SVM linear Kernel Regression [' + str(pair) + '] - adjusted R^2 = ' + str(r_square_adj[index]))
        index = index+1;

#######################################################
################### SVM - RBF Kernel ##################
#######################################################
elif model == 'SVM rbf':
    print('SVM rbf Kernel Regression model ...')
    for pair in list(comb):
        print(pair)
        X_fit = data_fit[:,pair] # features used to train the model
        X = data[:,pair]         # same features used to test the model
        y_fit = data_fit[:,8]
        y = data[:,8]
        reg = svm.SVC(C=1, kernel ='rbf')
        reg.fit(X_fit, y_fit)
        data_predicted = reg.predict(X)
        mse = sk.metrics.mean_squared_error(data[:,8], data_predicted) # Mean Squared Error
        mae = sk.metrics.mean_absolute_error(data[:,8], data_predicted) # Mean Absolute Error
        r_square_adj = np.append(r_square_adj,1 - (1-reg.score(X, y))*(len(y)-1)/(len(y)-X.shape[1]-1)) # Adjusted R^2 value
        cols=pltcolor(data[:,8])
        classes = ['90 mmHg', '120 mmHg', '150 mmHg']
        values = cols
        colours = ListedColormap(['g','b','r'])
        if r_square_adj[index] == max(r_square_adj):
        # if r_square_adj[index] >= 0:
            fig, ax = plt.subplots()
            scatter = ax.scatter(list(range(1, len(data[:,8])+1)),((data_predicted-data[:,8])/data[:,8]*100),c=values, cmap = colours)
            plt.legend(handles = scatter.legend_elements()[0], labels = classes)
            ax.set(xlabel = 'Acq #', ylabel = 'Model Error Percentage', title = 'SVM linear Kernel Regression [' + str(pair) + '] - adjusted R^2 = ' + str(r_square_adj[index]))
        index = index+1;