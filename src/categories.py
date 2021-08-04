from db import DB


class CategoryError(Exception):
    """
    Error handling class for all things related to Category
    """
    pass


class Category:
    """
    Handles all database communication to the Categories table.
    :param cursor: the connection cursor of the relevant database.
    Contains functions add(), all(), get_by_name()
    """
    def __init__(self, cursor=DB().connect()):
        self.__cursor = cursor

    def all(self):
        """
        Gets all rows in the Categories Table from the database.
        :return: list containing all records of Categories .
        """
        self.__cursor.execute("SELECT * FROM Categories")
        return self.__cursor.fetchall()

    def add(self, category: str):
        """
        Adds new category to the category database.
        :param category: the new category to be added to the database
        :return: Category successfully added message.
        """
        try:
            self.__cursor.execute(f"INSERT INTO Categories (category) VALUES ('{category}') ON CONFLICT DO NOTHING")
            return f"Successfully added {category} to the Categories Database."
        except CategoryError:
            raise CategoryError(f"Unable to add {category} to the Category table.")

    def get_by_name(self, name: str):
        """
        gets a particular category from the database by its name
        :param name: name of category to be extracted
        :return: tuple containing category's info
        """
        self.__cursor.execute(f"SELECT * from Categories WHERE category = '{name}'")
        return self.__cursor.fetchone()
