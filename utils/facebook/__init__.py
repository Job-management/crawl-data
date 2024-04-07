from venv import logger
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
from pathlib import Path
from importlib import import_module

import sys

sys.path.append(str(Path(__file__).resolve().parent / "../../modules"))

rabbitmq = import_module("rabbitmq")


def get_content(driver):
    """
    *   Handle get content (innerText) from div
    """
    rabbitMQChannel = rabbitmq.RabbitMQChannel()
    content_string = []
    cssSelector_postContainer = ".html-div.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd"
    postContainer = driver.find_elements(By.CSS_SELECTOR, cssSelector_postContainer)
    for post in postContainer:
        try:
            post_text = post.find_element(
                By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
            )
            post_link =post.find_element(By.CSS_SELECTOR, ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm")
            link = post_link.get_attribute("href")
            if not post_text:
                continue
            post_text = post.find_element(
                By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
            )
            if not post_text:
                continue
            post_img = post.find_elements(By.TAG_NAME, "img")
            data = {"text": post_text.text, "link": link}
            if post_img:
                images = []
                for img in post_img:
                    _class = img.get_attribute("class")
                    if not (
                        _class
                        == "x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r"
                    ):
                        continue
                    img_url = img.get_attribute("src")
                    img_alt = img.get_attribute("alt")
                    images.append({"link": img_url, "description": img_alt})
                data["images"] = images
            content_string.append(data)
            rabbitMQChannel.publishMessage(data, "raw-data")
        except Exception as e:
            continue
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


def click_seeMore_btn(driver):
    # Tìm tất cả các phần tử có thuộc tính data-ad-comet-preview="message"
    posts = driver.find_elements(
        By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
    )
    # Lặp qua từng phần tử
    for post in posts:
        # Tìm phần tử con có class nhất định
        see_more = post.find_elements(
            By.CSS_SELECTOR,
            ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f",
        )

        # Kiểm tra xem phần tử con có tồn tại không
        if see_more:
            for btn in see_more:
                driver.execute_script("arguments[0].click();", btn)
            # In nội dung của phần tử con và phần tử cha


def click_closeLogin_btn(driver):
    btn = driver.find_element(
        By.CSS_SELECTOR,
        ".x1i10hfl.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x16tdsg8.x1hl2dhg.xggy1nq.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xl56j7k.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xc9qbxq.x14qfxbe.x1qhmfi1",
    )
    btn.click()


def get_posts(driver):
    try:
        click_closeLogin_btn(driver)
        # scroll_browser(driver)
        # scroll_browser(driver)
        # scroll_browser(driver)
        scroll_browser(driver)
        click_seeMore_btn(driver)
        posts = get_content(driver)
        return posts
    except Exception as e:
        logger.error(f"Error occurred while extracting profile URLs from: {e}")
        return []


def get_facebook(driver):
    try:
        url = "https://www.facebook.com/groups/vieclamCNTTDaNang"
        driver.get(url)
        sleep(3)
        posts = get_posts(driver)
        print(posts)
    except Exception as e:
        print(f"Error occurred while get data facebook: {e}")
        return []
