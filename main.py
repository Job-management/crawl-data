# main.py
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path
from importlib import import_module
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import pickle
import concurrent.futures
from Get_info import get_vieclam24
from DB import save_data_into_DB
from ws_handler import sio, socket_app, status_handler

app = FastAPI(title="HANDLE CRAWL DATA")
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CrawlRequest(BaseModel):
    type: str

sys.path.append(str(Path(__file__).resolve().parent / "utils"))
facebook = import_module("facebook")

@app.on_event("startup")
async def startup_event():
    print("Starting up the server")

def crawl_facebook(driver):
    driver.get("https://www.facebook.com/login/")
    sleep(3)
    cookies = pickle.load(open("cookies_fb.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    facebook.get_facebook(driver, "https://www.facebook.com/groups/vieclamCNTTDaNang")

async def crawl_vieclam24h(driver):
    driver.get("https://vieclam24h.vn/")
    sleep(3)
    cookies = pickle.load(open("cookies_vieclam24h.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    return await get_vieclam24(driver, 3)

def crawl_topdev(driver):
    driver.get("https://topdep.vn/")
    sleep(3)
    cookies = pickle.load(open("cookies_topdev.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

async def _start_vieclam24h():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.binary_location = "/Volumes/Data/job-management/crawl-data/chrome-mac-arm64/chrome.app/Contents/MacOS/Google Chrome for Testing"
    try:
        crawl_status = "PROCESSING"
        status_handler.set_status(crawl_status)
        await sio.emit('current_status', crawl_status)
        service = Service(
            executable_path="/Volumes/Data/job-management/crawl-data/chromedriver_mac_arm64/chromedriver"
        )
        driver = webdriver.Chrome(service=service, options=chrome_options)

        data = await crawl_vieclam24h(driver)
        save_data_into_DB(data)

        await sio.emit('broadcast', "END")
    except Exception as e:
        await sio.emit('broadcast', str(e))
        print(f"Error occurred while scraping data: {str(e)}")

    print(">> Done")

@app.post("/crawl")
async def crawl(request: CrawlRequest, background_tasks: BackgroundTasks):
    type = request.type.lower()
    if type == "vieclam24h":
        if status_handler.get_status() != "PROCESSING":
            print('crawling vieclam24h')
            crawl_status = "PROCESSING"
            status_handler.set_status(crawl_status)
            await sio.emit('log', "LOG:: Crawl vieclam24h starting...")
            await sio.emit('current_status', crawl_status)
            background_tasks.add_task(_start_vieclam24h)
            return {"message": "Crawling started"}
        else:
            return {"message": "Crawling is processing"}

# Mount the socket_app under the same app instance
app.mount("/", socket_app)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8002, debug=True, reload=True)
