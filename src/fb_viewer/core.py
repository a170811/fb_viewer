import json
import time
from pathlib import Path

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

TMP_DIR = Path(__file__).parents[2] / "tmp"


class FBViewer:
    login_url = "https://www.facebook.com"
    is_login = False

    def __init__(self, email: str, password: str):
        options = Options()
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=options)
        self.email = email
        self.password = password

    def quit(self):
        self.driver.quit()

    def _login(self):
        if self.is_login:
            return

        cookies_path = TMP_DIR / "cookies.json"
        if cookies_path.exists():
            self.driver.get(self.login_url)
            with open(cookies_path, "r") as f:
                cookies_list = json.load(f)
            for cookies in cookies_list:
                self.driver.add_cookie(cookies)
            logger.info("Login with existing cookies")
        else:
            self._login_website(self.email, self.password)
            cookies = self.driver.get_cookies()
            cookies_path.parent.mkdir(parents=True, exist_ok=True)
            with open(cookies_path, "w") as f:
                json.dump(cookies, f, indent=4)
            logger.info(f"Save cookies to {cookies_path}")

    def _login_website(self, email: str, password: str):
        self.driver.get(self.login_url)
        element = self.driver.find_element(By.NAME, "email")
        element.send_keys(email)
        element = self.driver.find_element(By.NAME, "pass")
        element.send_keys(password)
        time.sleep(10)  # tricky: if removing this line, login will be failed
        element.send_keys(Keys.RETURN)
        time.sleep(10)
        self.is_login = True
        logger.info(f"{email} login successful")

    def view_posts(self, key: str):
        self._login()
        self.driver.get(self.login_url)
        time.sleep(5)

        search_element = self.driver.find_element(
            By.XPATH,
            "//input[@placeholder='搜尋 Facebook']",
        )
        search_element.send_keys(key)
        search_element.send_keys(Keys.RETURN)
        time.sleep(2)
        listitem_element = self.driver.find_element(
            By.XPATH,
            "(//div[@role='listitem'])[2]",
        )
        listitem_element.click()
        time.sleep(2)

        while True:
            self._expand_post()
            self._filter_post("西屯")
            self._filter_post("南屯")
            self._filter_post("南區")
            self._filter_post("大里")
            self._filter_post("求租")
            self._filter_post("龍井")
            self._filter_post("梧棲")
            self._filter_post("沙鹿")
            self._filter_post("售價")
            self._filter_post("3房")
            self._filter_post("社宅")
            self._filter_post("社會住宅")
            time.sleep(2)

    def _expand_post(self):
        while True:
            try:
                element = self.driver.find_element(
                    By.XPATH,
                    "//div[text()='查看更多']",
                )
                logger.debug("click [read more]")
                # click with execute_script: https://stackoverflow.com/questions/37879010/selenium-debugging-element-is-not-clickable-at-point-x-y
                # self.driver.execute_script("arguments[0].scrollIntoView();", element) # noqa
                self.driver.execute_script("arguments[0].click();", element)
            except NoSuchElementException:
                logger.debug("no viewing more element")
                break

    def _filter_post(self, key: str):
        while True:
            try:
                element_to_remove = self.driver.find_element(
                    By.XPATH,
                    "//div[@aria-describedby and "
                    ".//div[@data-ad-preview='message']"
                    f"[contains(., '{key}') and not (contains(., '#{key}'))]]",
                )
                logger.info(f"match {key}")
                logger.info(f"remove {element_to_remove.text.strip()}")
                self.driver.execute_script("arguments[0].remove();", element_to_remove)
            except NoSuchElementException:
                return
