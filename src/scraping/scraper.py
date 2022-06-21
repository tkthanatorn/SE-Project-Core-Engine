from click import option
from src.utils import Log
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

BY_XPATH = By.XPATH
BY_CLASS = By.CLASS_NAME
BY_ID = By.ID
BY_LINK_TEXT = By.LINK_TEXT
BY_NAME = By.NAME
BY_TAG_NAME = By.TAG_NAME


class Scraper:
    def __init__(self, options=['--headless']):
        # define options
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

    # scraping function
    @Log('Scraper')
    def scraping(self, url: str, value: str, by=BY_XPATH):
        driver = Chrome(options=self.options)
        try:
            driver.get(url)  # fetch url
            # find element by config
            ele = driver.find_element(by=by, value=value)
            print(f"[success] url:{url}")
            del driver
            return ele.text  # return result
        except NoSuchElementException:
            print(f"[error] url:{url} : NoSuchElementExeption")
            return ''
        except TimeoutException:
            print(f"[error] url:{url} : TimeoutException")
            return ''
        except WebDriverException:
            print(f"[error] url:{url} : WebDriverException")
            return ''
