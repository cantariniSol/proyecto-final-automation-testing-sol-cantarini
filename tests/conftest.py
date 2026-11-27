import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from configs.config import URL, USUARIO


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def driver_logueado(driver):
    driver.get(URL)
    driver.add_cookie({"name": "session-username", "value": USUARIO})
    driver.get(URL + "inventory.html")
    return driver