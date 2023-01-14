import time
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

class Recommender:
    def __init__(self,strategy = 'user'):
        self.strategy = strategy
        self.similarity = np.NaN
        self.mean_matrix = None
        self.user_item_matrix = None
        self.pred = None
        self.pred_clean = None

    def fit(self,matrix):
        " * ** YOUR CODE HERE ** * "
        ''' The users start with A, products with B'''
        self.user_item_matrix = matrix

        user_means = matrix.mean(axis = 1)
        df_mean = matrix.apply(lambda x: user_means)
        df_mean.columns = matrix.columns
        self.mean_matrix = df_mean

        self.user_item_matrix = matrix
        ratings_pd = self.user_item_matrix
        ratings = ratings_pd.to_numpy()
        mean_user_rating = user_means.to_numpy().reshape(-1,1)
        ratings_diff = (ratings - mean_user_rating)
        ratings_diff[np.isnan(ratings_diff)] = 0

        if self.strategy == 'user':
            # User - User based collaborative filtering
            start_time = time.time()
            user_similarity = 1 - pairwise_distances(ratings_diff,metric = 'cosine')
            pred = mean_user_rating + user_similarity.dot(ratings_diff) / np.array(
                [np.abs(user_similarity).sum(axis = 1)]).T
            self.pred = pd.DataFrame(pred,matrix.index,
                                     matrix.columns).round(2) #self.pred should contain your prediction matrix.
            time_taken = time.time() - start_time
            print('User Model in {} seconds'.format(time_taken))

        elif self.strategy == 'item':
            # Item - Item based collaborative filtering
            start_time = time.time()
            rating_item = ratings_diff
            rating_item[np.isnan(rating_item)] = 0

            item_similarity = 1 - pairwise_distances(rating_item.T,metric = 'cosine')
            print(item_similarity.shape)
            pd.DataFrame(item_similarity)
            pred = mean_user_rating + rating_item.dot(item_similarity) / np.array(
                [np.abs(item_similarity).sum(axis = 1)])
            self.pred = pd.DataFrame(pred,matrix.index,
                                     matrix.columns).round(2)  #self.pred should contain your prediction metrix.
            time_taken = time.time() - start_time
            print('Item Model in {} seconds'.format(time_taken))
        self.pred_clean = self.pred.where(self.user_item_matrix.isna(),0)
        return self

    def recommend_items(self,user_id,k = 5):
        " * ** YOUR CODE HERE ** * "
        row_index_list = self.pred_clean.iloc[0].index.tolist()
        sorted = self.pred_clean.loc[user_id].sort_values(ascending = False,kind = 'mergesort')
        out = sorted.head(k).index.tolist()
        out_list = []
        for i in range(len(out)):
            out_list.append((out[i],sorted[out[i]],row_index_list.index(out[i])))
        print(out_list)
        return out

