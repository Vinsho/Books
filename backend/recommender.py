import pandas as pd
from pandas import DataFrame
from src.backend.data_manager import DataManager
from src.config import RATING_AMOUNT_THRESHOLD

AMOUNT_OF_RECOMMENDATIONS = 10


class Recommender:
    def __init__(self, df: DataFrame, title: str, author: str):
        self._readers_books = None
        self.title = title
        self.author = author
        self.df = df

    @property
    def readers_books(self) -> DataFrame:
        """
        :return: Dataframe of books read by given book readers.
        """
        df = self.df
        if self._readers_books is None:
            readers = df.user_id[(df.title == self.title) &
                                 df.author.str.contains(self.author)]
            self._readers_books = df[(df.user_id.isin(readers.unique()))]
        return self._readers_books

    @staticmethod
    def filter_by_thresh(df: DataFrame) -> DataFrame:
        """
        :param df: Books dataframe
        :return: Filtered books
        """
        # return only books that have more than RATING_AMOUNT_THRESHOLD ratings
        return df[df.groupby(['title', 'author'])[
               'title'].transform('size') >= RATING_AMOUNT_THRESHOLD]

    def create_filtered_pivot_table(self) -> DataFrame:
        filtered_df = self.filter_by_thresh(self.readers_books)
        return filtered_df.pivot_table(
            index='user_id', columns='title', values='rating')

    def get_author(self, title: str) -> str:
        return self.readers_books.author[
            self.readers_books.title == title].max()

    def similar_titles(self, title: str) -> list:
        books = self.df[self.df.title.str.contains(title) &
                        (self.df.title != title)]
        top_picks = books.groupby(['author', 'title']).size().sort_values(
            ascending=False).head(AMOUNT_OF_RECOMMENDATIONS)
        return [{'title': title, 'author': author}
                for author, title in top_picks.keys().to_list()]

    def recommend(self) -> list:
        dfp = self.create_filtered_pivot_table()
        recommended_books = []
        for book_title in dfp.columns.values:
            if book_title != self.title:
                cor = dfp[self.title].corr(dfp[book_title])
                avg_rating = dfp[book_title].mean(skipna=True)
                recommended_books.append((book_title, cor, avg_rating))

        correlations = pd.DataFrame(recommended_books,
                                    columns=['title', 'corr', 'avg_rating'])
        titles = correlations.sort_values(
            'corr', ascending=False).head(AMOUNT_OF_RECOMMENDATIONS)

        return [{'title': title, 'author': self.get_author(title)}
                for title in titles.title]


def recommend(title: str, author: str) -> dict:
    """
    Method tries to recommend books for given title and author, in case
    that no books are found it returns books that have similar title to
    the one the user entered.
    :return: dictionary containing `books` and `found`.
    """
    recommender = Recommender(DataManager().df, title, author)
    book_list = recommender.recommend()

    if book_list:
        found = True
    else:
        book_list = recommender.similar_titles(title)
        found = False

    return {
        'books': book_list,
        'found': found
    }
