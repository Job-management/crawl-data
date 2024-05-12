import random
from datetime import datetime
from venv import logger
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from importlib import import_module
from selenium.webdriver.common.action_chains import ActionChains
import json
import uuid
from urllib.parse import urlparse
import sys

sys.path.append(str(Path(__file__).resolve().parent / "../../modules"))

rabbitmq = import_module("rabbitmq")


def get_content(driver):
    """
    *   Handle get content (innerText) from div
    """
    contents = []
    # cssSelector_postContainer = ".html-div.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd"
    # postContainer = driver.find_elements(By.CSS_SELECTOR, cssSelector_postContainer)
    postContainer = croll_and_get_elements(driver, 15)
    print(len(postContainer))
    count = 0
    for post in postContainer:
        data = {}
        try:
            if not post.text:
                continue

            post_text = post.find_element(
                By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
            )
            sleep(0.5)
            if not post_text or post_text.text == "":
                logger.error("post not found")
                continue

            # data if not have see more
            data["text"] = post_text.text
            print(data)

            post_link = post.find_element(
                By.CSS_SELECTOR,
                ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm",
            )
            sleep(0.5)
            if post_link:
                link = post_link.get_attribute("href")
                data["link"] = link
            print(data)
            # handle hover to date post and get post created date
            actions = ActionChains(driver)
            sleep(0.5)
            actions.move_to_element(post_link).perform()
            sleep(random.randint(1, 2))

            post_created_at = driver.find_element(
                By.CSS_SELECTOR,
                ".x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1nxh6w3.x1sibtaa.xo1l8bm.xzsf02u",
            )
            sleep(0.5)
            if post_created_at:
                post_created_at_str = post_created_at.text
                data["time"] = date_string_to_timestamp(post_created_at_str)
            print(data)
            # handle get post image
            post_img = post.find_elements(By.TAG_NAME, "img")
            sleep(0.5)

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
                    img_alt = uuid.uuid4()
                    images.append({"link": img_url, "description": img_alt})
                data["images"] = json.dumps(images)
            print(data)
            see_more_btns = post_text.find_elements(
                By.CSS_SELECTOR,
                ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f",
            )
            sleep(0.5)

            if see_more_btns:
                print("see_more_btn")
                driver.execute_script("arguments[0].click();", see_more_btns[0])
                post_text = post.find_element(
                    By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
                )
                sleep(0.5)
                # Get new post text after click see more button
                data["text"] = post_text.text
            print(data)
            is_duplicate = any(data["text"] == item["text"] for item in contents)
            if not is_duplicate:
                contents.append(data)
        except:
            print("catch", data)
            if "text" in data and "time" in data:
                is_duplicate = any(data["text"] == item["text"] for item in contents)
                if not is_duplicate:
                    contents.append(data)
    return contents


def scroll_browser(driver):
    """
    *   Attack scroll browser used to load more post
    """
    # Lấy chiều cao của trang web hiện tại
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Cuộn trang xuống đáy
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(0.5)
    # Cuộn lên lại
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 100);")

    sleep(random.randint(2, 5))


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
        print("close login popup")

        # click_closeLogin_btn(driver)
        # scroll_num = 5
        # print("scroll: ", scroll_num)
        # for i in range(scroll_num):
        #     print("scroll: ", i)
        #     scroll_browser(driver)
        #     sleep(random.randint(1, 2))
        print("see more")
        # click_seeMore_btn(driver)
        print("crawling post")
        posts = get_content(driver)

        return posts
    except Exception as e:
        logger.error(f"Error occurred while extracting profile URLs from: {e}")
        return []


def get_facebook(driver, group_url):
    try:
        rabbitMQChannel = rabbitmq.RabbitMQChannel()
        url = group_url
        driver.get(url)
        sleep(3)

        # posts = get_posts(driver)
        # posts = croll_and_get_elements(driver, 15)
        get_facebook_posts(driver)
        # print(posts)
        #
        # print(len(posts))
        #
        # for post in posts:
        #     rabbitMQChannel.publishMessage(post, "raw-data")
    except Exception as e:
        print(f"Error occurred while get data facebook: {e}")
        return []


def date_string_to_timestamp(date_string):
    parts = date_string.split(" ")

    # Lấy các thành phần của ngày, tháng, năm và thời gian
    day = int(parts[1])
    month = parts[2]
    year = int(parts[3])
    time = parts[5]

    # Tạo một đối tượng datetime từ các phần tử đã lấy được
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    month_number = months.index(month) + 1

    date_time_str = f"{year}-{month_number:02d}-{day:02d} {time}"
    date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

    # Lấy timestamp py (s) convert to js timestamp (ms)
    timestamp = int(date_time_obj.timestamp()) * 1000

    return timestamp

def croll_and_get_elements(driver, scroll_number):
    # Lọc ra các phần tử mới
    content = []
    for _ in range(scroll_number):
        css_selector_post_container = ".html-div.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd"
        post_elements = driver.find_elements(By.CSS_SELECTOR, css_selector_post_container)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        sleep(random.randint(2, 3))
        _content = get_content_v2(post_elements, driver)
        content.extend(_content)

    return content

def get_content_v2(postContainer, driver):
    """
    *   Handle get content (innerText) from post show in viewport
    """
    contents = []
    # cssSelector_postContainer = ".html-div.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd"
    # postContainer = driver.find_elements(By.CSS_SELECTOR, cssSelector_postContainer)
    print(len(postContainer))
    count = 0
    for post in postContainer:
        data = {}
        try:
            if not post.text:
                continue

            post_text = post.find_element(
                By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
            )
            sleep(0.5)
            if not post_text or post_text.text == "":
                logger.error("post not found")
                continue

            # data if not have see more
            data["text"] = post_text.text
            print(data)

            post_link = post.find_element(
                By.CSS_SELECTOR,
                ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm",
            )
            sleep(0.5)
            if post_link:
                link = post_link.get_attribute("href")
                data["link"] = link
            print(data)
            # handle hover to date post and get post created date
            actions = ActionChains(driver)
            sleep(0.5)
            actions.move_to_element(post_link).perform()
            sleep(random.randint(1, 2))

            post_created_at = driver.find_element(
                By.CSS_SELECTOR,
                ".x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1nxh6w3.x1sibtaa.xo1l8bm.xzsf02u",
            )
            sleep(0.5)
            if post_created_at:
                post_created_at_str = post_created_at.text
                data["time"] = date_string_to_timestamp(post_created_at_str)
            print(data)
            # handle get post image
            post_img = post.find_elements(By.TAG_NAME, "img")
            sleep(0.5)

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
                    img_alt = "alt images"
                    images.append({"link": img_url, "description": img_alt})
                data["images"] = json.dumps(images)
            print(data)
            see_more_btns = post_text.find_elements(
                By.CSS_SELECTOR,
                ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f",
            )
            sleep(0.5)

            if see_more_btns:
                print("see_more_btn")
                driver.execute_script("arguments[0].click();", see_more_btns[0])
                post_text = post.find_element(
                    By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
                )
                sleep(0.5)
                # Get new post text after click see more button
                data["text"] = post_text.text
            print(data)
            is_duplicate = any(data["text"] == item["text"] for item in contents)
            if not is_duplicate:
                contents.append(data)
        except:
            print("catch", data)
            if "text" in data and "time" in data:
                is_duplicate = any(data["text"] == item["text"] for item in contents)
                if not is_duplicate:
                    contents.append(data)
    return contents

def get_facebook_posts(driver):
    feeds = driver.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')
    sleep(0.5)
    print(len(feeds))
    index = 0
    scrolled = False
    canNotGetMorePostCount = 0
    rabbitMQChannel = rabbitmq.RabbitMQChannel()
    while True:
        if canNotGetMorePostCount >= 2:
            print('hết post')
            break

        if index >= len(feeds):
            canNotGetMorePostCount += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 500);")
            sleep(random.randint(9, 12))
            feeds = driver.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')
            continue

        postWrap = feeds[index]

        if not postWrap:
            canNotGetMorePostCount += 1
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 500);")
            sleep(random.randint(9, 12))
            feeds = driver.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')
            continue

        canNotGetMorePostCount = 0

        if scrolled:
            scrolled = False
            index += 1
            continue

        if not postWrap.find_elements(By.CSS_SELECTOR, '.html-div > .html-div'):
            postWrap.location_once_scrolled_into_view
            sleep(2)
            scrolled = True
            continue

        post = postWrap.find_element(By.CSS_SELECTOR, '.html-div > .html-div')

        data = get_content_by_post(post, driver)

        print('lấy thông tin của post', index, post.get_attribute('outerHTML'))
        if "text" in data and "time" in data:
            print('push to queue: ', data)
            rabbitMQChannel.publishMessage(data, "raw-data")
        index += 1

def get_content_by_post(post, driver):
    data = {}
    try:
        if not post.text:
            return

        post_text = post.find_element(
            By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
        )
        sleep(0.5)
        if not post_text or post_text.text == "":
            logger.error("post not found")
            return

        # data if not have see more
        data["text"] = post_text.text

        post_link = post.find_element(
            By.CSS_SELECTOR,
            ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm",
        )
        sleep(0.5)
        if post_link:
            link = post_link.get_attribute("href")
            data["link"] = get_main_url(link)
        # handle hover to date post and get post created date
        actions = ActionChains(driver)
        sleep(0.5)
        actions.move_to_element(post_link).perform()
        sleep(random.randint(1, 2))

        post_created_at = driver.find_element(
            By.CSS_SELECTOR,
            ".x193iq5w.xeuugli.x13faqbe.x1vvkbs.xlh3980.xvmahel.x1n0sxbx.x1nxh6w3.x1sibtaa.xo1l8bm.xzsf02u",
        )
        sleep(0.5)
        if post_created_at:
            post_created_at_str = post_created_at.text
            data["time"] = date_string_to_timestamp(post_created_at_str)
        # handle get post image
        post_img = post.find_elements(By.TAG_NAME, "img")
        sleep(0.5)

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
                img_alt = "description"
                images.append({"link": img_url, "description": img_alt})
            data["images"] = json.dumps(images)
        see_more_btns = post_text.find_elements(
            By.CSS_SELECTOR,
            ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f",
        )
        sleep(0.5)

        if see_more_btns:
            print("see_more_btn")
            driver.execute_script("arguments[0].click();", see_more_btns[0])
            post_text = post.find_element(
                By.CSS_SELECTOR, ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
            )
            sleep(0.5)
            # Get new post text after click see more button
            data["text"] = post_text.text
    except:
        logger.error("Lỗi get data")

    return data


def get_main_url(link):

    parsed_url = urlparse(link)
    return 'https://' + parsed_url.hostname + parsed_url.path
