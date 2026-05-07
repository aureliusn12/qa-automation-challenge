import logging
from typing import List, Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def find(self, locator: Tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator: Tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator: Tuple[str, str]) -> List[WebElement]:
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: Tuple[str, str]) -> None:
        element = self.find_clickable(locator)
        logger.debug("Clicking element: %s", locator)
        element.click()

    def type_text(self, locator: Tuple[str, str], text: str) -> None:
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str]) -> str:
        return self.find(locator).text

    def is_visible(self, locator: Tuple[str, str]) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def current_url(self) -> str:
        return self.driver.current_url
