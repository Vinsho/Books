from src.config import *
import requests
import zipfile
import io
import pandas as pd
import os
from time import time

ONE_DAY = 60 * 60 * 24


class DataManager:
    @property
    def ratings(self):
        ratings = self.load_csv(BOOK_RATINGS_PATH)
        ratings = ratings[ratings['Book-Rating'] != 0]

        # return only ISBNs that have more than RATING_AMOUNT_THRESHOLD ratings
        return ratings[ratings.groupby('ISBN')['ISBN'].transform('size') >=
                       RATING_AMOUNT_THRESHOLD]

    @property
    def books(self):
        return self.load_csv(BOOKS_PATH)

    @staticmethod
    def load_csv(path: str):
        return pd.read_csv(path, encoding='cp1251',
                           sep=';', error_bad_lines=False)

    @property
    def df(self):
        self.validate()
        return pd.read_pickle(DATAFRAME_PATH)

    def validate(self):
        """
        Check if the created dataframe has been updated for last 24 hours.
        """
        try:
            last_edited_time = os.stat(DATAFRAME_PATH).st_mtime
            # update csv every 24 hours
            if (time() - last_edited_time) > ONE_DAY:
                self.download()
                self.generate_df()
        except FileNotFoundError:
            self.generate_df()

    @staticmethod
    def download():
        """Download book csv zips from source and unzip"""
        r = requests.get(CSV_ZIP_URL)
        zip_file = zipfile.ZipFile(io.BytesIO(r.content))
        zip_file.extractall(BASE_DIR)

    def generate_df(self):
        """
        Pickle merged dataframe, for faster loading.
        """
        df = pd.merge(self.ratings, self.books, on=['ISBN'])

        # filter only needed columns
        df = df[['User-ID', 'Book-Rating', 'Book-Title', 'Book-Author']]

        # rename to something more usable
        df = df.rename(columns={
            'User-ID': 'user_id', 'Book-Rating': 'rating',
            'Book-Title': 'title', 'Book-Author': 'author'
        })

        df = df.apply(lambda x: x.str.lower() if x.dtype == 'object' else x)
        df.to_pickle('dataframe.pkl')
