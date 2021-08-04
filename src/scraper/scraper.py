import pandas as pd
import requests
import math
from bs4 import BeautifulSoup
from categories import Category
from listings import Listing


class ScraperError(Exception):
    pass


class eBay:
    """
        Holds everything related to extracting the relevant information
        from the website of interest.
    """
    def __init__(self):
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
        self.__dataframe = None
        self.__keyword = None
        self.__productlist = None

    def scrape(self, keyword: str, quantity: int) -> pd.DataFrame:
        """
        scrapes ebay website for search results of the keyword found
        :param keyword: The word to be searched for on ebay
        :param quantity: The number of listings for the keyword required to be scraped.
        :return: pandas dataframe containing the listings found from the keyword search.
        """
        print(f""".....................Scraping {keyword} listings from eBay..................... 
              Please be patient as this would take some time""")
        try:
            self.__keyword = keyword
            baseurl = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw={self.__keyword}&_sacat=0"
            self.__productlist = []
            data = []
            number_of_pages_to_scrape = math.ceil(quantity / 64)
            for page in range(1, number_of_pages_to_scrape+2):
                if page == 0 or page == 1:
                    next_page = baseurl
                else:
                    next_page = baseurl + f"&_pgn={page}"
                next_page_data = requests.get(next_page, self.__headers)
                latest_soup = BeautifulSoup(next_page_data.text, features="html.parser")
                self.__productlist.extend(latest_soup.find_all("li", {"class":"s-item"})[1:-1])

            for item in self.__productlist[1:]:
                title = item.select_one(".s-item__title").text
                link = item.select_one(".s-item__link")["href"]
                image_url = item.select_one(".s-item__image-img")['src']
                price = item.select_one(".s-item__price").text
                data.append({"title": title,"price": price, "item_url": link, "image_url": image_url})
            self.__dataframe = pd.DataFrame(data)
            return self.__dataframe[:quantity]
        except ScraperError:
            raise ScraperError("System encountered a problem when scraping the site."
                               "Please ensure that you have passed in a relevant keyword and quantity")

    def add_category_to_database(self):
        """
        adds the scraped category to the Category Database
        :return: category successfully added message
        """
        try:
            category_database = Category()
            category_database.add(self.__keyword)
            print(f".......{self.__keyword} category successfully added to Database.......")
            self.__category_id = category_database.get_by_name(self.__keyword)[0]
        except ScraperError:
            raise ScraperError(f"Category {self.__keyword} is already in the database")

    def add_listings_to_database(self):
        """
        adds scraped listings of keyword to listings database
        :return: listings successfully added message.
        """
        try:
            self.__dataframe['category_id'] = [self.__category_id for each_element in range(len(self.__dataframe))]
            listing_database = Listing()
            listing_database.add(self.__dataframe)
            print(f"........{self.__keyword} listings successfully added to Database.......")
        except ScraperError:
            raise ScraperError("This listing is already in the database")
