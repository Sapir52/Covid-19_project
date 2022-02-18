#pip install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
#pip install pymongo
import pandas as pd
import os
import io
import time
# Import  pymongo database
import pymongo
# For import data from mongodb
from pandas.io.json import json_normalize
import twint as tw
import nest_asyncio

class tweets():
    def download_tweets(self):
        nest_asyncio.apply()
        a = tw.Config()
        a.Username = 'BarackObama'
        a.Profile=True
        a.Since = "2020-1-01"
        a.Store_csv = True
        a.Output = a.Username + ".csv"
        a.Search = "covid 19"
        all_tw=tw.run.Search(a)
        return all_tw

    def connecting_to_mongo(self, name_dict, name_collection, collection):
        # connecting to mongo
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["covid_19"]  # name of database
        collection = db[name_collection]  # name of collection(table in database)
        collection.insert_many(name_dict)
        return collection

    def get_data_from_mongodb(self, collection):
        # import data from mongodb
        cursor =collection.find()
        df = json_normalize(cursor)
        return df

if __name__ == '__main__':
    # Download Corona tweets
    obj_tweet = tweets()
    all_tw=obj_tweet.download_tweets()
    df_all_tw = pd.read_csv("BarackObama.csv")
    # Get specific columns
    df_all_tw=df_all_tw[['id','date','name','tweet']]
    df_all_tw.to_csv("BarackObama.csv", index=False)
    #Initialization collection
    collection_tweets=None
    data_dict = df_all_tw.to_dict(orient='records')
    collection_tweets=obj_tweet.connecting_to_mongo(data_dict,'covid_19',collection_tweets)
    print(obj_tweet.get_data_from_mongodb(collection_tweets))