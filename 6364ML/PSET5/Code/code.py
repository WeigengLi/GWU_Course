from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
import random
from pandas import read_csv, DataFrame, concat, get_dummies
import numpy as np
import matplotlib.pyplot as plt

cv_fold = 10
random_seed = 42

def Load_with_Preprocess(input_file):
    data = read_csv(input_file)
    y = data['Legendary']
    X = data.iloc[:, 1:-1]
    X_labels = ['Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack',
                'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation']
    continuous_labels = ['Total', 'HP', 'Attack', 'Defense',
                        'Sp. Atk', 'Sp. Def', 'Speed', 'Generation']
    discrete_labels = ['Type 1', 'Type 2']
    X_discrete = X[discrete_labels]
    X_continuous = X[continuous_labels]
    # Scale Continuous Data
    scaler = StandardScaler()
    X_continuous = scaler.fit_transform(X_continuous)
    X_continuous = DataFrame(data=X_continuous, columns=continuous_labels)
    # Change Discrete Data to One Hot Code
    X_discrete = get_dummies(X_discrete)
    # Resemble data
    X = concat([X_discrete, X_continuous], axis=1)
    return X,y

def DecisionTree(X,y):
    criterions = ['gini', 'entropy', 'log_loss']
    max_depth_list = range(1, 30)
    result_dict = dict()
    best_accuracy = 0
    best_depth = 0
    for criteria in criterions:
        result_dict[criteria] = []
    for max_depth in max_depth_list:
        for criteria in criterions:
            DT = DecisionTreeClassifier(
                max_depth=max_depth, criterion=criteria, random_state=42)
            cv_score = np.mean(cross_val_score(
                DT, X, y, scoring='roc_auc', n_jobs=-1, cv=cv_fold))
            result_dict[criteria].append(cv_score)
            if cv_score > best_accuracy:
                best_accuracy = cv_score
                best_depth = max_depth
                best_criteria = criteria
                
    #Retrain model to get parameters
    DT_model = DecisionTreeClassifier(
    max_depth=best_depth, criterion=best_criteria, random_state=random_seed)
    DT_model.fit(X, y)
    importance = dict()
    count = 0
    for xlable in X.columns.tolist():
        importance[xlable] = DT_model.feature_importances_[count]
        count += 1
    sort_dict = sorted(importance.items(), key=lambda item: -item[1])
    count = 0
    for key, item in sort_dict:
        print(key, item)
        count += 1
        if count == 10:
            break
    # Plot
    plt.title('AUC_ROC of Decision Tree: Range of max depth ['+str(min(max_depth_list))+
              ', '+str(max(max_depth_list))+']')
    color = ['red', 'skyblue', 'green']
    count = 0
    for criteria in criterions:
        plt.plot(max_depth_list, result_dict[criteria],
                color=color[count], label=criteria)
        count += 1
    show_max = 'ROC-AUC='+str(round(best_accuracy, 3))+'\n depth='+str(best_depth)
    # move the text down a little bit
    plt.annotate(show_max, xytext=(best_depth+2, best_accuracy-0.01),
                xy=(best_depth, best_accuracy))
    plt.plot(best_depth, best_accuracy, 'go')
    plt.legend()
    plt.xlabel('Max Depth')
    plt.ylabel('AUC_ROC')
    plt.show()
    
def RandomForest(X,y):
    criterions = ['gini', 'entropy', 'log_loss']
    n_estimators_list = range(100, 6100, 100)
    result_dict_RF = dict()
    best_accuracy_RF = 0
    for criteria in criterions:
        result_dict_RF[criteria] = []
    for estimator in n_estimators_list:
        for criteria in criterions:
            RF = RandomForestClassifier(
                n_estimators=estimator, criterion=criteria, n_jobs=-1, random_state=random_seed)
            cv_score = np.mean(cross_val_score(
                RF, X, y, scoring='roc_auc', n_jobs=-1, cv=cv_fold))
            result_dict_RF[criteria].append(cv_score)
            if cv_score > best_accuracy_RF:
                best_accuracy_RF = cv_score
                best_nestimator_RF = estimator
                best_criteria_RF = criteria
    # Plot
    plt.title('AUC_ROC of Random Forest: Range of n_estimators ['+str(min(n_estimators_list))+', '+str(max(n_estimators_list))+']')
    color = ['red', 'skyblue', 'green']
    count = 0
    for criteria in criterions:
        plt.plot(n_estimators_list,
                result_dict_RF[criteria], color=color[count], label=criteria)
        count += 1
    show_max = 'AUC-ROC='+str(round(best_accuracy_RF, 3)) + \
        '\n n_estimators='+str(best_nestimator_RF)
    # move the text down a little bit
    plt.annotate(show_max, xytext=(best_nestimator_RF-600,
                best_accuracy_RF-0.0002), xy=(best_nestimator_RF, best_accuracy_RF))
    plt.plot(best_nestimator_RF, best_accuracy_RF, 'go')
    plt.legend()
    plt.xlabel('Max Depth')
    plt.ylabel('AUC-ROC')
    plt.show()
    # Retrain to get the parameters
    RF_new = RandomForestClassifier(
    n_estimators=best_nestimator_RF, criterion=best_criteria_RF, n_jobs=-1, random_state=random_seed)
    RF_new.fit(X, y)
    RF_new.feature_importances_
    count=0
    importance = dict()
    for xlable in X.columns.tolist():
        importance[xlable] = RF_new.feature_importances_[count]
        count += 1
    sort_dict = sorted(importance.items(), key=lambda item: -item[1])
    count = 0
    for key, item in sort_dict:
        print(key, item)
        count += 1
        if count == 10:
            break





def main():
    X,y=Load_with_Preprocess('6364ML\PSET5\Code\Pokemon.csv')
    DecisionTree(X,y)
    RandomForest(X,y)
if __name__ == '__main__':
    main()