

import pandas as pd
import csv
from requests import get
import json
from datetime import datetime, timedelta, date
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine
from scipy.stats import pearsonr

import csv
import re
import pandas as pd
import argparse
import collections
import json
import glob
import math
import os
import requests
import string
import sys
import time
import xml
import random

class Recommender(object):
    def __init__(self, training_set, test_set):
        if isinstance(training_set, str):
            # the training set is a file name
            self.training_set = pd.read_csv(training_set)
        else:
            # the training set is a DataFrame
            self.training_set = training_set.copy()

        if isinstance(test_set, str):
            # the test set is a file name
            self.test_set = pd.read_csv(test_set)
        else:
            # the test set is a DataFrame
            self.test_set = test_set.copy()
    
    def train_user_euclidean(self, data_set, userId):
        # print(data_set)
        # # sim_weights={}
        # # for user in data_set[1:]:
        # print("test")

        sim_weights = {}
        for user in data_set.columns[1:]:
            if(user==userId):
                continue
            df_subset = data_set[[userId, user]][data_set[userId].notnull()&data_set[user].notnull()]

            dist = euclidean(df_subset[userId], df_subset[user])

            sim_weights[user] = 1.0/(1.0+dist)






        return sim_weights# dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}
    
    def train_user_manhattan(self, data_set, userId):

        sim_weights = {}
        for user in data_set.columns[1:]:
            if (user == userId):
                continue
            df_subset = data_set[[userId, user]][data_set[userId].notnull() & data_set[user].notnull()]

            dist = cityblock(df_subset[userId], df_subset[user])
            sim_weights[user] = 1.0/(1.0+dist)

        return sim_weights # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}

    def train_user_cosine(self, data_set, userId):
        sim_weights = {}
        for user in data_set.columns[1:]:
            if (user == userId):
                continue
            df_subset = data_set[[userId, user]][data_set[userId].notnull() & data_set[user].notnull()]

            dist = cosine(df_subset[userId], df_subset[user])
            sim_weights[user] = dist


        return sim_weights # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}
   
    def train_user_pearson(self, data_set, userId):
        sim_weights = {}
        for user in data_set.columns[1:]:
            if (user == userId):
                continue
            df_subset = data_set[[userId, user]][data_set[userId].notnull() & data_set[user].notnull()]
            sim_weights[user] = pearsonr(df_subset[userId], df_subset[user])[0]

        return sim_weights # dictionary of weights mapped to users. e.g. {"0331949b45":1.0, "1030c5a8a9":2.5}

    def train_user(self, data_set, distance_function, userId):
        if distance_function == 'euclidean':
            return self.train_user_euclidean(data_set, userId)
        elif distance_function == 'manhattan':
            return self.train_user_manhattan(data_set, userId)
        elif distance_function == 'cosine':
            return self.train_user_cosine(data_set, userId)
        elif distance_function == 'pearson':
            return self.train_user_pearson(data_set, userId)
        else:
            return None

    def get_user_existing_ratings(self, data_set, userId):
        df=data_set[["movieId", userId]][data_set[userId].notnull()]



        result = list(df.itertuples(index=False,name=None))

        return result # list of tuples with movieId and rating. e.g. [(32, 4.0), (50, 4.0)]

    def predict_user_existing_ratings_top_k(self, data_set, sim_weights, userId, k):

        result=[]


        list=[(k, v) for k, v in sim_weights.items()]
        list.sort(key=lambda x: x[1],reverse=True)

        if(k>len(list)):
            k=len(list)

        temp={}
        for i in range(k):
            user=list[i][0]
            temp[user]=list[i][1]




        for count in range(data_set.shape[0]):
            if(data_set[userId].notnull()[count]):
                predicted_rating=0.0
                weights_sum=0.0
                ratings=data_set.iloc[count][1:]



                for user in data_set.columns[1:]:
                    if((user!=userId) & (user in temp.keys())):
                        if(not np.isnan(ratings[user])):
                            predicted_rating+=ratings[user]*temp[user]

                            weights_sum+=temp[user]

                if(weights_sum!=0):
                    predicted_rating/= weights_sum
                    result.append((data_set["movieId"][count],predicted_rating))
        return result # list of tuples with movieId and rating. e.g. [(32, 4.0), (50, 4.0)]
    
    def evaluate(self, existing_ratings, predicted_ratings):
        existingID=set([movie[0] for movie in existing_ratings if movie[1] is not None])
        predicted=[movie[1] for movie in predicted_ratings if movie[1] is not None and movie[0] in existingID]
        predictedID=set([movie[0] for movie in predicted_ratings if movie[1] is not None])
        fact=[movie[1] for movie in existing_ratings if  movie[1] is not None and movie[0] in predictedID]
        rmse=math.sqrt(np.square(np.subtract(fact,predicted)).mean())
        ratio=len(predicted)/len(existingID)
        return {'rmse':rmse, 'ratio':ratio} # dictionary with an rmse value and a ratio. e.g. {'rmse':1.2, 'ratio':0.5}
    
    def single_calculation(self, distance_function, userId, k_values):
        user_existing_ratings = self.get_user_existing_ratings(self.test_set, userId)
        print("User has {} existing and {} missing movie ratings".format(len(user_existing_ratings), len(self.test_set) - len(user_existing_ratings)), file=sys.stderr)

        print('Building weights')
        sim_weights = self.train_user(self.training_set[self.test_set.columns.values.tolist()], distance_function, userId)

        result = []
        for k in k_values:
            print('Calculating top-k user prediction with k={}'.format(k))
            top_k_existing_ratings_prediction = self.predict_user_existing_ratings_top_k(self.test_set, sim_weights, userId, k)
            result.append((k, self.evaluate(user_existing_ratings, top_k_existing_ratings_prediction)))
        return result # list of tuples, each of which has the k value and the result of the evaluation. e.g. [(1, {'rmse':1.2, 'ratio':0.5}), (2, {'rmse':1.0, 'ratio':0.9})]

    def aggregate_calculation(self, distance_functions, userId, k_values):
        print()
        result_per_k = {}
        for func in distance_functions:
            print("Calculating for {} distance metric".format(func))
            for calc in self.single_calculation(func, userId, k_values):
                if calc[0] not in result_per_k:
                    result_per_k[calc[0]] = {}
                result_per_k[calc[0]]['{}_rmse'.format(func)] = calc[1]['rmse']
                result_per_k[calc[0]]['{}_ratio'.format(func)] = calc[1]['ratio']
            print()
        result = []
        for k in k_values:
            row = {'k':k}
            row.update(result_per_k[k])
            result.append(row)
        columns = ['k']
        for func in distance_functions:
            columns.append('{}_rmse'.format(func))
            columns.append('{}_ratio'.format(func))
        result = pd.DataFrame(result, columns=columns)
        return result
        
if __name__ == "__main__":
    recommender = Recommender("data/train.csv", "data/small_test.csv")
    print("Training set has {} users and {} movies".format(len(recommender.training_set.columns[1:]), len(recommender.training_set)))
    print("Testing set has {} users and {} movies".format(len(recommender.test_set.columns[1:]), len(recommender.test_set)))

    result = recommender.aggregate_calculation(['euclidean', 'cosine', 'pearson', 'manhattan'], "0331949b45", [1, 2, 3, 4])
    print(result)