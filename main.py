import concurrent.futures
from venv import logger
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Get_info import get_vieclam24
from DB import save_data_into_DB
from time import sleep
import pickle
import sys
from pathlib import Path
from importlib import import_module
from get_topdev import get_job_topdev

sys.path.append(str(Path(__file__).resolve().parent / "utils"))

facebook = import_module("facebook")


def crawl_facebook(driver):
    driver.get("https://www.facebook.com/login/")
    sleep(3)
    cookies = pickle.load(open("cookies_fb.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    facebook.get_facebook(driver, "https://www.facebook.com/groups/vieclamCNTTDaNang")
    # facebook.get_facebook(driver, "https://www.facebook.com/kenhtuyendungdanang")

def crawl_vieclam24h(driver):
    driver.get("https://vieclam24h.vn/")
    sleep(3)
    cookies = pickle.load(open("cookies_vieclam24h.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    return get_vieclam24(driver, 3)
    # facebook.get_facebook(driver, "https://www.facebook.com/kenhtuyendungdanang")



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

        # Handle crawl facebook
        # crawl_facebook(driver)

        #  Handle crawl vieclam24
        data = crawl_vieclam24h(driver)
        save_data_into_DB(data)

        # Handle crawl topdev
        # data = get_job_topdev(driver)
        # save_data_into_DB(data)
        # sleep(3)
        driver.close()
    except Exception as e:
        logger.error(f"Error occurred while scraping data: {str(e)}")
    print(">> Done")


if __name__ == "__main__":
    main()
