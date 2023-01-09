import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def RMSE(test_set,cf):
    "*** YOUR CODE HERE ***"
    return np.sqrt(mean_squared_error(test_set['Rating'],cf.pred.loc[test_set['UserId'],test_set['ProductId']]))

def precision_at_k(test_set,cf):
    return np.mean(
        [cf.recommend_items(user_id,k = 5).isin(test_set[test_set['UserId'] == user_id]['ProductId']).sum() / 5 for
         user_id in test_set['UserId'].unique()])

def recall_at_k(test_set,cf):
    return np.mean([
        cf.recommend_items(user_id,k = 5).isin(test_set[test_set['UserId'] == user_id]['ProductId']).sum() / len(
            test_set[test_set['UserId'] == user_id]['ProductId']) for user_id in test_set['UserId'].unique()])
