import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    @staticmethod
    def create_chrome_driver(headless: bool = False) -> webdriver.Chrome:
        options = Options()

        if headless or os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

        driver_path = ChromeDriverManager().install()
        p = Path(driver_path)
        if p.name.startswith("THIRD_PARTY_NOTICES"):
            candidate = p.parent / "chromedriver"
            if candidate.exists():
                driver_path = str(candidate)

        service = Service(executable_path=driver_path)
        return webdriver.Chrome(service=service, options=options)
