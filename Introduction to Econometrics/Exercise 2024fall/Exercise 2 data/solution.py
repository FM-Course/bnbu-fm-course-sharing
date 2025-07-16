import numpy as np
import numpy.linalg as LA
import pandas as pd


def question1():
    print("\nThe answer of question 1")
    x = np.array([[21,24,26,27,29,25,25,30]])
    y = np.array([2.8, 3.4, 3.0, 3.5, 3.6, 3., 2.7, 3.7])
    
    A = np.concatenate((x, np.ones(8).reshape((1,8)))).T
    
    beta = LA.inv(A.T @ A) @ (A.T @ y)
    print(f"The linear model is GPA = {beta[1]} + {beta[0]}*ACT + u")

def question2():
    print("\nThe answer of question 2")
    q2Data = pd.read_excel("ceosal2.xls",sheet_name="CEOSAL2", usecols=[0,5], header=None)
    mean_value = q2Data.mean(axis=0).values
    print(f"the average salary is {mean_value[0]} and the average CEO tenure is {mean_value[1]}")

    NumberOfFirstYear = (q2Data.iloc[:,1] == 0).sum() 
    print(f"There are {NumberOfFirstYear} CEOs are in their first year as CEO")

    n = len(q2Data)
    ceoten = q2Data.iloc[:,1].values
    A = np.concatenate((ceoten.reshape((n,1)), np.ones((n,1))), axis=1)
    y = np.log(q2Data.iloc[:,0].values.T)

    beta = LA.inv(A.T @ A) @ (A.T @ y)
    print(f"The linear model is log(salary_hat) = {beta[1]} + {beta[0]}*ceoten + u")

def question3():
    print("\nThe answer of question 3")
    q3Data = pd.read_excel("sleep75.xls", sheet_name='SLEEP75', header=None, usecols=[20,25])
    #print(q3Data.head())

    n = len(q3Data)
    totwrk = q3Data.iloc[:,1].values
    A = np.concatenate( ( totwrk.reshape((n,1)), np.ones((n,1)) ), axis=1)
    sleep = q3Data.values[:,0].T

    beta = LA.inv(A.T @ A) @ (A.T @ sleep)
    print(f"The model is sleep = {beta[1]} + {beta[0]}*totwrk + u")
    print(f"If totwrk increases by 2 hours, sleep estimate falls {-120 * beta[0]} mins")
    
if __name__ == "__main__":
    question1()
    question2()
    question3()