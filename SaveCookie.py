import concurrent.futures
from venv import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from Get_info import get_vieclam24
from DB import save_data_into_DB
from time import sleep
from selenium.webdriver.common.by import By
import sys
from pathlib import Path
from importlib import import_module
import pickle
from bs4 import BeautifulSoup
sys.path.append(str(Path(__file__).resolve().parent / "utils"))

facebook = import_module("facebook")


def main():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless") # Not open chrome window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--disable-gpu"
    )  # This is important for some versions of Chrome
    chrome_options.add_argument("--remote-debugging-port=9222")  # This is recommended
    # Set path to Chrome binary
    chrome_options.binary_location = "/Volumes/Data/job-management/crawl-data/chrome-mac-arm64/chrome.app/Contents/MacOS/Google Chrome for Testing"
    # chromedriver_path = r"/app/crawl-data/chromedriver/chromedriver-linux64/chromedriver.exe"
    # print(chromedriver_path)
    try:
        print("==================")
        service = Service(
            executable_path="/Volumes/Data/job-management/crawl-data/chromedriver_mac_arm64/chromedriver"
        )
        # with webdriver.Chrome(options=chrome_options, executable_path='/Volumes/Data/job-management/crawl-data/chromedriver_mac_arm64/chromedriver') as driver:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver.get("https://www.facebook.com/login/")
        driver.get("https://topdev.vn/viec-lam-it?src=topdev.vn&medium=mainmenu")
        page_source = BeautifulSoup(driver.page_source, 'html.parser')
        sleep(4500)
        # userNAME = driver.find_element(By.ID, "email")
        # userNAME.send_keys("vanthanhhuynhctc@gmail.com")

        # passWork = driver.find_element(By.ID, "pass")
        # passWork.send_keys("huynhvanthanh")

        # passWork.send_keys(Keys.ENTER)

        sleep(4)

        pickle.dump(driver.get_cookies(), open("cookies_test.pkl", "wb"))
        driver.close()
        # save_data_into_DB(data)
    except Exception as e:
        logger.error(f"Error occurred while scraping data: {e}")
    print(">> Done")


if __name__ == "__main__":
    main()
