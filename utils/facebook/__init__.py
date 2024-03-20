from venv import logger
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By

def get_content(driver):
    """
    *   Handle get content (innerText) from div
    """
    content_string = []
    posts = driver.find_elements(By.CSS_SELECTOR, '[data-ad-comet-preview="message"]')
    for post in posts:
        content_string.append(post.text)
    return content_string


def scroll_browser(driver):
    """
    *   Attack scroll browser used to load more post
    """
    # Lấy chiều cao của trang web hiện tại
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Cuộn trang xuống đáy
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    sleep(5)


def click_seeMore_btn(page_source, driver):
    # Tìm tất cả các phần tử có thuộc tính data-ad-comet-preview="message"
    posts = driver.find_elements(By.CSS_SELECTOR, '[data-ad-comet-preview="message"]')

    # Lặp qua từng phần tử
    for post in posts:
        # Tìm phần tử con có class nhất định
        see_more = post.find_elements(By.CSS_SELECTOR,
            ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f"
        )

        # Kiểm tra xem phần tử con có tồn tại không
        if see_more:
            for btn in see_more:
                driver.execute_script("arguments[0].click();", btn)
            # In nội dung của phần tử con và phần tử cha

def get_post(driver):
    page_source = BeautifulSoup(driver.page_source, "html.parser")
    with open("a.txt", "w") as f:
        # Ghi dữ liệu vào tệp
        f.write(str(page_source))
    try:
        scroll_browser(driver)
        click_seeMore_btn(page_source, driver)
        content = get_content(driver)
        print(content)
    except Exception as e:
        logger.error(f"Error occurred while extracting profile URLs from: {e}")
        return []


def get_facebook(driver):
    try:
        url = "https://www.facebook.com/groups/vieclamCNTTDaNang"
        driver.get(url)
        sleep(3)
        get_post(driver)
        sleep(10000)
    except Exception as e:
        print(f"Error occurred while get data facebook: {e}")
        return []
