from db import DB
import pandas as pd
import psycopg2.extras as extras


class ListingError(Exception):
    """
    Error handling class for all thing related to Listing
    """
    pass


class Listing:
    """
    Handles all database communication to the Listing table.
    Contains functions add(), all()
    """
    def __init__(self, cursor=DB().connect()):
        self.__cursor = cursor

    def all(self):
        """
        Gets all rows in the Listing Table from the database.
        :return: list containing all records of Listings.
        """
        self.__cursor.execute("SELECT * FROM Listings")
        return self.__cursor.fetchall()

    def add(self, df: pd.DataFrame):
        """
        Adds new record to the Listings Database records.
        :param details:a dictionary that contains the title,
        category, image url, item url, price of a listing.
        :return: Record successfully added to Database message.
        """
        try:
            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ','.join(list(df.columns))
            query = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s)" % ('Listings', cols)
            extras.execute_batch(self.__cursor, query, tuples, len(df))
            print("Record successfully added to Listings")
        except ListingError:
            raise ListingError("Something went wrong when trying to add record(s)")

    def get_by_category_id(self, id: int):
        """
        gets listings from the database by its category_id
        :param id: id of category to be extracted
        :return: list of tuples containing all listings in that category
        """
        self.__cursor.execute(f"SELECT * from Listings WHERE category_id = '{id}'")
        return self.__cursor.fetchall()
