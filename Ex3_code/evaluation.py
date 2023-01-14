import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def RMSE(test_set,cf):
    "*** YOUR CODE HERE ***"
    # Create an array of the ratings from the test set, and an array for the predicted ratings,
    # by using the UserId and ProductId from the test set to get the predicted rating from the user-item matrix
    rmse = mean_squared_error(np.array(test_set['Rating']),
                              np.array([cf.pred.at[row] for row in zip(test_set['UserId'],test_set['ProductId'])]),
                              squared = False).round(5)
    rmse_bench = mean_squared_error(np.array(test_set['Rating']),np.array(
        [cf.mean_matrix.at[row] for row in zip(test_set['UserId'],test_set['ProductId'])]),squared = False).round(5)
    print(f'RMSE for {cf.strategy} based is: {rmse}')
    print(f'RMSE for benchmark is: {rmse_bench}')

def precision_at_k(test_set,cf,k):

    "*** YOUR CODE HERE ***"
    # Create sub-dataframe of users and items that with ratings >= 3
    relevant_items = test_set[test_set['Rating'] >= 3]
    # Create a list of unique users that have relevant items
    users = relevant_items['UserId'].unique()
    # Generate a dictionary of relevant items for each user - {user: relevant items} with the relevant items as series
    # Relevant items - per user
    relevant_dict = {user: relevant_items.loc[relevant_items['UserId'] == user]['ProductId'] for user in users}
    # Generate a dictionary of recommended items for each user - {user: recommended items} with the recommended items
    # as index - Recommended items @ K
    recommended_items = {user: cf.recommend_items(user,k) for user in users}

    # Create a list of Relevant_Items_Recommended / k to get the precision at k for each user, and take mean
    precision = np.mean(
        [len(pd.Index(recommended_items[user]).intersection(pd.Index(relevant_dict[user]))) / k for user in users]).round(5)
    print(f'Precision at {k} is {precision}')

    # get the top k items from the user-item mean matrix and calculate the precision at k for each user
    bench = cf.user_item_matrix.mean(axis = 0).sort_values(ascending = False)[:k]
    precision_bench = [len(pd.Index(relevant_dict[user]).intersection(bench.index)) / k for user in users]
    print(f'Precision at {k} for benchmark is {np.mean(precision_bench).round(5)}')

def recall_at_k(test_set,cf,k):
    "*** YOUR CODE HERE ***"
    relevant_items = test_set[test_set['Rating'] >= 3]
    users = relevant_items['UserId'].unique()
    recommended_items = {user: cf.recommend_items(user,k) for user in users}
    relevant_dict = {user: relevant_items.loc[relevant_items['UserId'] == user]['ProductId'] for user in users}

    # take the length of the intersection of the recommended items and the relevant items
    # divide by the length of the relevant items
    recall = np.mean(
        [len(pd.Index(relevant_dict[user]).intersection(pd.Index(recommended_items[user]))) / len(relevant_dict[user]) for user in
         users]).round(5)
    print(f'recall at {k} is {recall}')

    bench = cf.user_item_matrix.mean(axis = 0).sort_values(ascending = False)[:k]
    recall_bench = [len(pd.Index(relevant_dict[user]).intersection(bench.index)) / len(relevant_dict[user]) for user in
                    users]
    print(f'recall at {k} for benchmark is {np.mean(recall_bench).round(5)}')
