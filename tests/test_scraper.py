from src.scraper import eBay


def test_scrapes_correct_number_of_listings():
    assert len(eBay().scrape("sandals", 200)) == 200


def test_scrapes_and_adds_category_to_database():
    scraper = eBay()
    scraper.scrape("sneakers", 300)
    assert scraper.add_category_to_database() is None


def test_scrapes_and_add_listings_to_database():
    scrapper = eBay()
    scrapper.scrape("dress", 400)
    scrapper.add_category_to_database()
    assert scrapper.add_listings_to_database() is None
