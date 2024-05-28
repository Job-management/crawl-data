import concurrent.futures
from venv import logger
import uvicorn
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
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import websockets

from fastapi import BackgroundTasks, FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="HANDLE CRAWL DATA")
executor = ThreadPoolExecutor(max_workers=5)

# Cấu hình CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CrawlRequest(BaseModel):
    type: str


# GLOBAL STATUS
crawl_status = ""

sys.path.append(str(Path(__file__).resolve().parent / "utils"))

facebook = import_module("facebook")


# HANDLE WEBSOCKET
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    print('websocket connected')
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


def crawl_facebook(driver):
    driver.get("https://www.facebook.com/login/")
    sleep(3)
    cookies = pickle.load(open("cookies_fb.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    facebook.get_facebook(driver, "https://www.facebook.com/groups/vieclamCNTTDaNang")
    # facebook.get_facebook(driver, "https://www.facebook.com/kenhtuyendungdanang")


async def crawl_vieclam24h(driver, manager):
    driver.get("https://vieclam24h.vn/")
    sleep(3)
    cookies = pickle.load(open("cookies_vieclam24h.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    return await get_vieclam24(driver, 3, manager)
    # facebook.get_facebook(driver, "https://www.facebook.com/kenhtuyendungdanang")


def crawl_topdev(driver):
    driver.get("https://topdep.vn/")
    sleep(3)
    cookies = pickle.load(open("cookies_topdev.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    # return get_vieclam24(driver, 3)


async def _start_vieclam24h():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Not open chrome window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--disable-gpu"
    )  # This is important for some versions of Chrome
    chrome_options.add_argument("--remote-debugging-port=9222")  # This is recommended
    # Set path to Chrome binary
    chrome_options.binary_location = "/Volumes/Data/job-management/crawl-data/chrome-mac-arm64/chrome.app/Contents/MacOS/Google Chrome for Testing"
    # chromedriver_path  g = r"/app/crawl-data/chromedriver/chromedriver-linux64/chromedriver.exe"
    # print(chromedriver_path)
    try:
        print("==================")
        global crawl_status
        crawl_status = "STARTED"
        service = Service(
            executable_path="/Volumes/Data/job-management/crawl-data/chromedriver_mac_arm64/chromedriver"
        )
        # with webdriver.Chrome(options=chrome_options, executable_path='/Volumes/Data/job-management/crawl-data/chromedriver_mac_arm64/chromedriver') as driver:
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Handle crawl facebook
        # crawl_facebook(driver)

        #  Handle crawl vieclam24
        data = await crawl_vieclam24h(driver, manager)
        save_data_into_DB(data)

        await manager.broadcast("END")
        # Handle crawl topdev
        # data = get_job_topdev(driver)
        # save_data_into_DB(data)
        # sleep(3)
        # driver.close()
    except Exception as e:
        await manager.broadcast(f"Error: {str(e)}")
        logger.error(f"Error occurred while scraping data: {str(e)}")
    print(">> Done")


@app.post("/crawl/")
async def crawl(request: CrawlRequest, background_tasks: BackgroundTasks):
    type = request.type.lower()
    if type == "vieclam24h":
        global crawl_status
        if crawl_status != "STARTED":
            # await manager.broadcast(f"Client #{client_id} says: {data}")
            await manager.broadcast("Crawl vieclam24h starting...")
            background_tasks.add_task(_start_vieclam24h, )
            return {"message": "Crawling started"}
        else:
            return {"message": "Crawling is processing"}


if __name__ == '__main__':
    uvicorn.run("api:app", host="0.0.0.0", port=8002, debug=True, reload=True)
