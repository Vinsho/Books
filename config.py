import os

BASE_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))
CSV_ZIP_URL = 'http://www2.informatik.uni-freiburg.de/~cziegler/BX/BX-CSV-Dump.zip'
DATAFRAME_PATH = BASE_DIR + '/dataframe.pkl'
BOOK_RATINGS_PATH = BASE_DIR + '/BX-Book-Ratings.csv'
BOOKS_PATH = BASE_DIR + '/BX-Books.csv'
RATING_AMOUNT_THRESHOLD = 8
