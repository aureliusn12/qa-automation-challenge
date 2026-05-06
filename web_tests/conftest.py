import logging
import os

import pytest

from web_tests.data.test_data import STANDARD_USER
from web_tests.pages.login_page import LoginPage
from web_tests.utils.driver_factory import DriverFactory

logger = logging.getLogger(__name__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def driver(request):
    chrome = DriverFactory.create_chrome_driver()
    chrome.implicitly_wait(0)
    yield chrome
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        os.makedirs("screenshots", exist_ok=True)
        path = os.path.join("screenshots", f"FAIL_{request.node.name}.png")
        chrome.save_screenshot(path)
        logger.error("Test failed — screenshot saved: %s", path)
    chrome.quit()


@pytest.fixture
def logged_in_driver(driver):
    LoginPage(driver).open().login(STANDARD_USER.username, STANDARD_USER.password)
    return driver
