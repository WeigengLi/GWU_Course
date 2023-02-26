from sklearn.preprocessing import StandardScaler 
from pandas import read_csv, DataFrame
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
import itertools as it
from sklearn.preprocessing import StandardScaler
import random
# code for problem2
def problem2(data:DataFrame,y):
    cv_MSE = []
    intercepts = []
    coefficients = []
    labels =data.columns.values.tolist()
    best_MSE = 100000000000000000000
    x_labels =labels[2:13]
    # iterate over variables to fit models
    for i in range(2,13):
        lm = LinearRegression()
        data_x = data.iloc[:,i:i+1]
        # Calculate cross-validation MSE
        avg_MSE =  abs(np.mean(cross_val_score(lm,data_x, y, cv=10,scoring='neg_mean_squared_error')))
        # refit model to get coefficients
        lm.fit(data_x,y)
        intercepts.append(lm.intercept_)
        coefficients.append(lm.coef_[0])
        cv_MSE.append(avg_MSE) 
    # store result to csv
    dataframe = DataFrame({'variable':x_labels,'MSE':cv_MSE,
                           'Intercept':intercepts,'coefficients':coefficients
                           })
    dataframe.to_csv("problem2.csv",index=False,sep=',')
    
# code for problem3
def problem3(data,y):
    # get a list of column name of variables
    labels =data.columns.values.tolist()
    # get x variables
    x_labels =labels[2:13] 
    lm = LinearRegression()
    cv_MSE = []
    cv_r2 = []
    variable_list = []
    best = 100000000000000000000
    # Scale X
    sc = StandardScaler()
    data_x = sc.fit_transform(data[x_labels])
    data_x=DataFrame(data=data_x,columns=x_labels)
    # numbers of variable in model iterate from 1 to 12 
    for i in range(1,len(x_labels)+1):
        # get all possible combinations of variables
        combine = it.combinations(x_labels, i)
        for combination in combine:
            # get MSE of one combinations
            test_data = data_x[list(combination)]
            variable_list.append(list(combination))
            avg_r2 = np.mean(cross_val_score(lm,test_data, y,n_jobs=-1 ,cv=5,scoring='r2'))
            avg_MSE =  abs(np.mean(cross_val_score(lm,test_data, y,n_jobs=-1, cv=5,scoring='neg_mean_squared_error')))
            cv_r2.append(avg_r2)
            cv_MSE.append(avg_MSE)
            # Mark the best model
            if avg_MSE < best:
                best=avg_MSE
                best_variable= combination
    # Store results
    dataframe = DataFrame({'combination':variable_list,'R2':cv_r2,'MSE':cv_MSE})
    dataframe.to_csv("problem3.csv",index=False,sep=',')
    # Fit the best model to get coefficients
    lm = LinearRegression()
    lm.fit(data_x[list(best_variable)],y)
    variable = list(best_variable)
    variable.append('Intercept')
    coef = list(lm.coef_)
    coef.append(lm.intercept_)
    # Store results
    dataframe = DataFrame({'variable':variable,
                           'coefficients':coef
                           })
    dataframe.to_csv("problem3_coef.csv",index=False,sep=',')
    

def problem4():
    # read in data and set configurations
    data_train = read_csv("data_mnist.csv")
    data_test = read_csv("test_mnist.csv")
    y = data_train["label"]
    X = data_train.iloc[:,1:]
    X = X/255
    results = list()
    # Tune number of iterations
    start, end, step = 100,11000,100
    for i in range(start, end, step):
        logistic = LogisticRegression(multi_class="multinomial",solver='lbfgs',max_iter=i,n_jobs=-1)
        score = np.mean(cross_val_score(logistic,X,y,scoring='accuracy',n_jobs=-1,cv=5))
        results.append(score)
        # see if this model has already closure
        print("Actual number of iterations: ",logistic.n_iter_)
    # refit model to predict result
    logistic = LogisticRegression(multi_class="multinomial",solver='lbfgs',max_iter=800,n_jobs=-1)
    logistic.fit(X,y)
    print('Number of iterations when function converges ',logistic.n_iter_)
    # Plot generation
    x_axix = range(start, end, step)
    plt.title('Accuracy of Logistic regression iteration in ['+str(start)+', '+str(end)+'], Step '+str(step))
    plt.plot(x_axix, results, color='red', label='L2 penalty accuracy')
    plt.legend() # 显示图例
    plt.xlabel('number of neighbours')
    plt.ylabel('rate')
    plt.show()
    # Store result
    df=DataFrame(results)
    df.to_csv('problem4.csv')
    data_test = read_csv('test_mnist.csv')
    result = logistic.predict(data_test)
    pre_df = DataFrame({'ImageId':range(1,len(data_test)+1),'Label':result})
    pre_df.to_csv('MNISTResults.csv',index=None)   
        

    

def main():
    random.seed(1)
    data= read_csv("baseball-9192.csv")
    y = data["Salary"]
    # code of each problem is in a function
    problem2(data,y)
    problem3(data,y)
    problem4()


if __name__ == '__main__':
    main()


