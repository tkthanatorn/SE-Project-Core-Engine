import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from src.scraping import Scraper
import unittest


class TestScrape(unittest.TestCase):
    def test_scraping_done(self):
        scraper = Scraper()
        result = scraper.scraping("https://cointelegraph.com/news/nft-marketplace-metaplex-raises-46m-to-expand-gaming-and-metaverse-applications", '//*[@class="post-content"]')
        self.assertGreater(len(result), 0, 'The scraping result should have length of string more than 0.')
        
    def test_scraping_error(self):
        scraper = Scraper()
        result = scraper.scraping("https://cointelegraph.com/magazine/2022/04/16/epic-games-raises-2b-metaverse-mastercard-scales-nft-plans-ripple-scores-big-win-against-sec-hodlers-digest-apr-10-16", '//*[@class="post-content"]')
        self.assertEqual(len(result), 0, 'The scraping result should have length of string equal to 0.')


if __name__ == '__main__':
    unittest.main()