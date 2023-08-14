import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class LoginError(Exception):
    pass


def is_element_exist(driver: webdriver, by, statement: str):
    try:
        driver.find_element(by, statement)
        return True
    except NoSuchElementException as e:
        return False


def save_page(page, name):
    with open(name, "w", encoding="utf-8") as file:
        file.write(page)


class PixivApi:
    def __init__(self, driver_type=0):
        '''if driver_type is 0, then Chrome driver will be used, else Mozilla driver'''
        self.chrome_driver = "C:\\Рабочий стол\\_____Projects\\Gigashitposter\\pixiv_python_api\\chromedriver.exe"
        self.mozila_driver = "C:\\Рабочий стол\\_____Projects\\Gigashitposter\\pixiv_python_api\\geckodriver.exe"
        if not driver_type:
            self.selenium_start_chrome(self.chrome_driver)
        else:
            self.selenium_start_mozila(self.mozila_driver)
        self.main_page = "https://www.pixiv.net"
        self.login_page = "https://accounts.pixiv.net/login"
        self.tag_page = "https://www.pixiv.net/en/tags"

    def selenium_start_chrome(self, driver_full_path):
        self.service = Service(executable_path=driver_full_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disk-cache-dir=/cahce_chrome')
        self.driver = webdriver.Chrome(service=self.service, options=options)
    def selenium_start_mozila(self, driver_full_path):
        self.service = Service(executable_path=driver_full_path)
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--disk-cache-dir=/cahce_mozila')
        self.driver = webdriver.Firefox(service=self.service, options=options)

    def login(self, login, password):
        '''Doesn't work (((('''
        self.driver.get(self.login_page)
        # time.sleep(500)
        login_text_area = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".degQSE")))
        # login_text_area = driver.find_element(By.CLASS_NAME, "sc-bn9ph6-6 degQSE")
        login_text_area.send_keys(login)
        password_text_area = WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".hfoSmp")))
        password_text_area.send_keys(password)
        css_selecotr = "#app-mount-point > div > div > div.sc-2oz7me-0.fJsfdC " \
                       "> div.sc-fg9pwe-2.gZSHsw > div > div > div > form > button"
        login_btn = WebDriverWait(self.driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selecotr)))
        login_btn.click()
        css_selecotr = 'fieldset.sc-bn9ph6-0:nth-child(3)'
        # password_field = WebDriverWait(self.driver, 100).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, css_selecotr)))
        with open("aboba21.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        # loggin_error_element = self.driver.find_element(By.CLASS_NAME, "sc-bn9ph6-5 ezCrnB")
        if is_element_exist(self.driver, By.CSS_SELECTOR, ".sc-2o1uwj-2") or is_element_exist(self.driver,
                                                                                              By.CSS_SELECTOR,
                                                                                              ".sc-bn9ph6-5"):
            raise LoginError

    def get_all_popular_tags(self, return_type: str = "link"):
        ''' if return_type is "link" return a list of links to tags page if return_type is "name" return a list of tags names'''
        self.driver.get(self.tag_page)
        page = self.driver.page_source
        bs = BeautifulSoup(page, "lxml")
        tags_element = bs.find_all("a", class_="tag-value icon-text")
        tags = []
        for element in tags_element:
            if return_type == "link":
                tags.append(self.main_page + element.get("href"))
            elif return_type == "name":
                tags.append(element.get("href").split("/")[-1])
        # print(tags)
        return tags

    def get_tag(self, tag_name: str, start, end=None, amount=10):
        '''Get illustration from start to start + amount or from start to end if end is given(first illustration is 0)'''
        illustrations_on_page = 6 * 10
        if isinstance(end, type(None)):
            end = start + amount
        pages_amount = end // illustrations_on_page - start // illustrations_on_page + 1
        start_page = start // illustrations_on_page + 1
        illustrations_links = []
        for i in range(start_page, start_page + pages_amount):
            url = self.tag_page + f"/{tag_name}/illustrations?page={i}"
            self.driver.get(url)
            page = self.driver.page_source
            bs = BeautifulSoup(page, "lxml")
            illustrations = list(map(lambda x: self.main_page + x.get("href"),
                                     bs.find_all("a", class_="sc-d98f2c-0 sc-iasfms-4 cwshsL")))
            first = 0
            last = illustrations_on_page
            if i == start_page:
                first = start
            if i == start_page + pages_amount - 1:
                last = end % illustrations_on_page
            illustrations_links += illustrations[first: last + 1]
        print(len(illustrations_links), illustrations_links)
        return illustrations_links

    def get_artwork(self, artwork_id: str):
        print("aboba")
        url = self.main_page + f"/artworks/{artwork_id}"
        print(url)
        self.driver.get(url)
        # images_holder = WebDriverWait(self.driver,100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".sc-1yvhotl-3")))
        # print(images_holder)
        try:
            WebDriverWait(self.driver, 100).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".sc-emr523-0")))
            images_btn = WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".sc-emr523-0")))
            images_btn.click()
            print(images_btn, "aaaaaaaaaa")
        except Exception as e:
            print(e)
        time.sleep(100)
        page = self.driver.page_source
        save_page(page, "aaaa.html")
        bs = BeautifulSoup(page, "lxml")
        abobaich = bs.find("figure", {"class" : "sc-1yvhotl-3 jUCdwp"})
        print(abobaich, len(abobaich))
        images = list(map(lambda x: x.get("src"), bs.find_all("img")))
        print(images)
        images2 = abobaich.find_all("img")
        print(images2, len(images2))
        return images2



def main():
    pa = PixivApi(1)
    # pa.get_tag("女の子", 0, 60)
    pa.get_artwork("110627849")
    time.sleep(50)


def main2():
    url = "https://i.pximg.net/img-master/img/2023/08/09/23/15/18/110682177_p0_master1200.jpg"
    headers = {
        'referer': "https://www.pixiv.net/en/artworks/110682177"
    }
    params = {

    }
    response = requests.get(url, headers=headers, params=params).content
    print(response)


if __name__ == "__main__":
    main()
    # main2()
