import json
from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine
import heapq
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Task(object):
    def __init__(self, data):
        self.df = pd.read_csv(data)

    def t1(self, name):
        result=[]
        sim_weights = {}
        for user in self.df.columns[1:]:
            if(user==name):
                continue
            df_subset = self.df[[name,user]][self.df[name].notnull() & self.df[user].notnull()]
            dist = cosine(df_subset[name], df_subset[user])
            sim_weights[user] = dist



        for index,row in self.df[self.df[name].notnull()==False].iterrows():
            predicted_rating = 0
            weights_sum = 0.0
    
            ratings = row
    
            for user in self.df.columns[1:]:
                if (not np.isnan(ratings[user])):
                    if(user==name):
                        continue
        
                    predicted_rating += ratings[user] * sim_weights[user]
                    weights_sum += sim_weights[user]

            


            predicted_rating /= weights_sum

            result.append((row['Alias'],predicted_rating))

        
        return result

    def t2(self, name):

        result=[]
        missing_movies = {}
        sim_weights = {}
        for data in range(0, len(self.df)):
            if (np.isnan(self.df[name][data])):
                missing_movies[data] = self.df['Alias'][data]
        df_t = self.df.transpose()
        
        for index in missing_movies:
            title = missing_movies[index]
            
            for y in range(0, len(self.df)):
                movie = self.df['Alias'][y]
                if title == movie:
                    continue
                df_subset = df_t[[index, y]][df_t[index].notnull() & df_t[y].notnull()]
                
                sim_weights[movie] = cosine(df_subset[index][1:].astype(float), df_subset[y][1:].astype(float))
            
            df_subset = self.df[['Alias', name]]
            
            predicted_rating = 0.0
            
            weights_sum = 0.0
            
            for row in range(0, len(self.df)):
                movie_title = self.df['Alias'][row]
                
                user_rating = self.df[name][row]  
                
                if (not np.isnan(user_rating)):
                    predicted_rating += user_rating * sim_weights[movie_title]
                    weights_sum += sim_weights[movie_title]
            predicted_rating /= weights_sum
            
            result.append((title, predicted_rating))
        
        return result
        
    
    def t3(self, name):
        result=[]
        sim_weights = {}
        weights = []
        temp={}
        for user in self.df.columns[1:]:
            if(user!=name):
                df_subset = self.df[[name,user]][self.df[name].notnull() & self.df[user].notnull()]
                dist = cosine(df_subset[name], df_subset[user])
                sim_weights[dist] = user
                weights.append(-dist)
        heapq.heapify(weights)
        
        for i in range(10):
            weight = -heapq.heappop(weights)
            user = sim_weights[weight]
            temp[user] = weight
        sim_weights = temp

        for count in range(self.df.shape[0]):
            if (self.df[name].isnull()[count]):
                predicted_rating = 0
                weights_sum = 0.0
                ratings = self.df.iloc[count][1:]
                
                for user in self.df.columns[1:]:
                    if ((user != name) & (user in sim_weights.keys())):
                        if (not np.isnan(ratings[user])):
                            predicted_rating += ratings[user] * sim_weights[user]
                            weights_sum += sim_weights[user]

                predicted_rating /= weights_sum
                result.append((self.df['Alias'][count],predicted_rating))
        return result



        
            

        
        
        
        
if __name__ == "__main__":
    # using the class movie ratings data we collected in http://data.cs1656.org/movie_class_responses.csv
    t = Task('http://data.cs1656.org/movie_class_responses.csv')
    print(t.t1('BabyKangaroo'))
    print('------------------------------------')
    print(t.t2('BabyKangaroo'))
    print('------------------------------------')
    print(t.t3('BabyKangaroo'))
    print('------------------------------------')