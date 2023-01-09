import time
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

class Recommender:
    def __init__(self,strategy = 'user'):
        self.strategy = strategy
        self.u_similarity = np.NaN
        self.user_item_matrix = None
        self.pred = None

    def fit(self,matrix):
        " * ** YOUR CODE HERE ** * "
        ''' The users start with A, products with B'''
        self.user_item_matrix = matrix
        mean_user_rating = self.user_item_matrix.mean()
        norm_matrix = self.user_item_matrix.subtract(mean_user_rating,axis = 1)
        norm_matrix = norm_matrix.fillna(0)
        if self.strategy == 'user':
            # User - User based collaborative filtering
            start_time = time.time()
            #self.pred should contain your prediction matrix.
            sim_mat = pd.DataFrame(1 - pairwise_distances(norm_matrix,metric = 'cosine'),norm_matrix.T.columns,
                                   norm_matrix.T.columns)


            div1 = np.dot(sim_mat,norm_matrix)
            div2 = np.abs(sim_mat).sum(axis = 1)
            pred = pd.DataFrame((div1/div2[:,None]),norm_matrix.index,norm_matrix.columns)
            # self.pred = pd.DataFrame(np.dot(sim_mat,norm_matrix),norm_matrix.index,norm_matrix.columns)/sim_mat.sum(axis = 1)
            self.pred = pred + mean_user_rating
            time_taken = time.time() - start_time
            print('User Model in {} seconds'.format(time_taken))

            return self

        elif self.strategy == 'item':
            # Item - Item based collaborative filtering
            start_time = time.time()
            sim_mat = pd.DataFrame(1 - pairwise_distances(norm_matrix.T,metric = 'cosine'),norm_matrix.columns,
                                   norm_matrix.columns)
            #self.pred should contain your prediction matrix.
            self.pred = pd.DataFrame(np.dot(norm_matrix,sim_mat),norm_matrix.index,norm_matrix.columns)
            time_taken = time.time() - start_time
            print('Item Model in {} seconds'.format(time_taken))
            return self

    def recommend_items(self,id,k = 5):
        " * ** YOUR CODE HERE ** * "
        if self.strategy == 'user':
            return self.pred.loc[id].sort_values(ascending = False).head(k).index[1:]


        elif self.strategy == 'item':
            return self.pred.loc[id].sort_values(ascending = False).head(k).index[1:]

