from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from src.util.logging import log_error, log_info

BY_XPATH = By.XPATH
BY_CLASS = By.CLASS_NAME
BY_ID = By.ID
BY_LINK_TEXT = By.LINK_TEXT
BY_NAME = By.NAME
BY_TAG_NAME = By.TAG_NAME


class Scraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
    
    def scraping(self, url: str, value: str, by=BY_XPATH):
        driver = Chrome(options=self.options)
        try:
            driver.get(url)
            ele = driver.find_element(by=by, value=value)
            log_info(f"Scraped: {url}")
            del driver
            return ele.text
        except NoSuchElementException:
            log_error(f"NoSuchElementException: {url}")
            return ''
        except TimeoutException:
            log_error(f"TimeoutException: {url}")
            return ''
        except WebDriverException:
            log_error(f"WebDriverException: {url}")
            return ''