from sklearn.preprocessing import StandardScaler 
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import random
from pandas import read_csv, DataFrame,concat,get_dummies
import numpy as np
import matplotlib.pyplot as plt

def Load_with_Preprocess(input_file):
    data=read_csv(input_file)
    y=data['Legendary']
    X = data.iloc[:,1:-1]
    X_labels =['Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation']
    continuous_labels = ['Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation']
    discrete_labels = ['Type 1', 'Type 2']
    X_discrete = X[discrete_labels]
    X_continuous = X[continuous_labels]
    # Scale Continuous Data
    scaler = StandardScaler()
    X_continuous=scaler.fit_transform(X_continuous)
    X_continuous = DataFrame(data=X_continuous,columns=continuous_labels) 
    # Change Discrete Data to One Hot Code
    X_discrete = get_dummies(X_discrete)

def Tune_Plot(estimator,X,y,cv_fold,):
    criterions = ['gini', 'entropy', 'log_loss']
    max_depth_list = range(1,30)
    result_dict = dict()
    best_accuracy = 0
    best_depth = 0
    for criteria in criterions:
        result_dict[criteria] = []
    for max_depth in max_depth_list:
        for criteria in criterions:
            DT = DecisionTreeClassifier(max_depth=max_depth,criterion=criteria)
            cv_score = np.mean(cross_val_score(DT,X,y,scoring='roc_auc',n_jobs=-1,cv=cv_fold))
            result_dict[criteria].append(cv_score)
            if cv_score > best_accuracy:
                best_accuracy = cv_score
                best_depth = max_depth
                best_criteria = criteria


def main():
    Load_with_Preprocess('Pokemon.csv')
    pass
if __name__ == '__main__':
    main()