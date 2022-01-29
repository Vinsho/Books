import pandas as pd
import numpy as np
from pandas import DataFrame


class DatasetManager:
    @property
    def ratings(self):
        ratings = self.load_csv('BX-Book-Ratings.csv')
        return ratings[ratings['Book-Rating'] != 0]

    @property
    def books(self):
        return self.load_csv('BX-Books.csv')

    @staticmethod
    def load_csv(path: str):
        return pd.read_csv(path, encoding='cp1251', 
                           sep=';', error_bad_lines=False)

    @property
    def df(self):
        dataframe = pd.merge(self.ratings, self.books, on=['ISBN'])
        return dataframe.apply(lambda x: x.str.lower()
                               if x.dtype == 'object' else x)

    @staticmethod
    def readers_books(df: DataFrame, book_title: str,
                      author: str) -> DataFrame:
        """
        :return: Dataframe of books read by given book readers.
        """
        readers = df['User-ID'][(df['Book-Title'] == book_title) &
                                (df['Book-Author'].str.contains(author))]
        reader_ids = np.unique(readers.tolist())
        return df[(df['User-ID'].isin(reader_ids))]

    @staticmethod
    def filter_by_thresh(readers_books: DataFrame,
                         threshold: int) -> DataFrame:
        """
        :param readers_books: Books dataframe
        :param threshold: Lowest amount of ratings that we accept.
        :return: Filtered books
        """
        book_rating_counts = readers_books.groupby(
            ['Book-Title'], as_index=False).agg('count')

        # select only books with amount of ratings > threshold
        filtered_titles = book_rating_counts['Book-Title'][
            book_rating_counts['User-ID'] >= threshold].tolist()

        columns = ['User-ID', 'Book-Rating', 'Book-Title']
        filtered_books = readers_books[columns][
            readers_books['Book-Title'].isin(filtered_titles)]

        # remove duplicates (take mean value in case of duplicate ratings)
        return filtered_books.groupby(
            ['User-ID', 'Book-Title'], as_index=False)['Book-Rating'].mean()

    def create_pivot_table(self, title: str, author: str) -> DataFrame:
        readers_books = self.readers_books(self.df, title, author)
        filtered_books = self.filter_by_thresh(readers_books, 8)
        return filtered_books.pivot(
            index='User-ID', columns='Book-Title', values='Book-Rating')


if __name__ == '__main__':
    manager = DatasetManager()
    dataset = manager.create_pivot_table(
        "the fellowship of the ring (the lord of the rings, part 1)",
        'tolkien')
    pass

# dataset_for_corr = ratings_data_raw_nodup.pivot(
#     index='User-ID', columns='Book-Title', values='Book-Rating')
#
# LoR_list = ['the fellowship of the ring (the lord of the rings, part 1)']
#
# result_list = []
# worst_list = []
#
# # for each of the trilogy book compute:
# for LoR_book in LoR_list:
#
#     # Take out the Lord of the Rings selected book from correlation dataframe
#     dataset_of_other_books = dataset_for_corr.copy(deep=False)
#     dataset_of_other_books.drop([LoR_book], axis=1, inplace=True)
#
#     # empty lists
#     book_titles = []
#     correlations = []
#     avgrating = []
#
#     # corr computation
#     for book_title in list(dataset_of_other_books.columns.values):
#         book_titles.append(book_title)
#         correlations.append(dataset_for_corr[LoR_book].corr(
#             dataset_of_other_books[book_title]))
#         tab = (ratings_data_raw[ratings_data_raw['Book-Title'] ==
#                                 book_title].groupby(ratings_data_raw['Book-Title']).mean())
#         avgrating.append(tab['Book-Rating'].min())
#     # final dataframe of all correlation of each book
#     corr_fellowship = pd.DataFrame(list(zip(
#         book_titles, correlations, avgrating)), columns=['book', 'corr', 'avg_rating'])
#     corr_fellowship.head()
#
#     # top 10 books with highest corr
#     result_list.append(corr_fellowship.sort_values(
#         'corr', ascending=False).head(10))
#
#     # worst 10 books
#     worst_list.append(corr_fellowship.sort_values(
#         'corr', ascending=False).tail(10))
#
# print("Correlation for book:", LoR_list[0])
# # print("Average rating of LOR:", ratings_data_raw[ratings_data_raw['Book-Title']=='the fellowship of the ring (the lord of the rings, part 1'].groupby(ratings_data_raw['Book-Title']).mean()))
# rslt = result_list[0]
