# selenium_launcher.py
import time
import traceback
import logging
import subprocess
import socket
import http.client
import json
import atexit
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="selenium_launcher.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("SeleniumLauncher")

# ---------------- CONSTANTS ----------------
CHROMEDRIVER = r"C:\Program Files (x86)\ChromeDriver\chromedriver-win64\chromedriver.exe"
CITRIX_URL = "https://myworkspace.dnb.no/Citrix/SITWeb/"
ZENIT_TILE = "//p[normalize-space()='Zenit Kundefront - DaaS']"
OPEN_XPATH = "//div[normalize-space()='Open']"
WINAPP = r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
HOST = "127.0.0.1"
PORT = 4723
CONNECT_TIMEOUT = 8

# ---------------- FUNCTIONS ----------------
def start_winappdriver():
    subprocess.Popen([WINAPP], creationflags=subprocess.CREATE_NEW_CONSOLE)
    atexit.register(lambda: os.system("taskkill /F /IM WinAppDriver.exe"))
    time.sleep(4)
def _request(method, path, payload=None):
    conn = http.client.HTTPConnection(HOST, PORT, timeout=CONNECT_TIMEOUT)
    try:
        headers = {"Content-Type": "application/json; charset=utf-8"}
        body = json.dumps(payload) if payload else None
        conn.request(method, path, body=body, headers=headers)
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8", errors="replace") or ""
        try:
            data = json.loads(raw)
        except:
            data = {"raw": raw}
        data["_http_status"] = resp.status
        return data
    finally:
        conn.close()

def create_session(desired_caps):
    payload = {
        "capabilities": {"alwaysMatch": desired_caps, "firstMatch": [{}]},
        "desiredCapabilities": desired_caps
    }
    res = _request("POST", "/session", payload)

    if "sessionId" in res:
        return res["sessionId"]
    val = res.get("value", {})
    if "sessionId" in val:
        return val["sessionId"]

    raise RuntimeError("Unable to create WinAppDriver session")

def click_citrix_popup():
    """
    Uses WinAppDriver Root session to find and click:
    - 'Open Citrix Workspace Launcher' Chrome popup button
    """
    ROOT_CAPS = {
        "platformName": "Windows",
        "deviceName": "WindowsPC",
        "app": "Root"
    }

    # 1) Create ROOT session
    root_sid = create_session(ROOT_CAPS)

    # 2) Poll for popup window
    popup_el = None
    for _ in range(40):  # ~20 seconds
        try:
            res = _request("POST", f"/session/{root_sid}/element",
                           {"using": "name", "value": "Open Citrix Workspace Launcher?"})
            if "value" in res and isinstance(res["value"], dict):
                popup_el = res["value"]["ELEMENT"]
                break
        except:
            pass
        time.sleep(0.5)

    if not popup_el:
        print("❌ Citrix popup not found.")
        return False

    print("✔ Citrix popup detected.")

    # 3) Find and click the "Open Citrix Workspace Launcher" button
    try:
        button_res = _request(
            "POST",
            f"/session/{root_sid}/element",
            {"using": "name", "value": "Open Citrix Workspace Launcher"}
        )
        button_el = button_res["value"]["ELEMENT"]

        # click it
        _request("POST", f"/session/{root_sid}/element/{button_el}/click")
        print("✔ Popup clicked successfully.")
        return True

    except Exception as e:
        print(f"❌ Could not click popup: {e}")
        return False

def make_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-features=ExternalProtocolDialog")

    service = Service(CHROMEDRIVER)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 30)
    return driver, wait

def run():
    try:
        start_winappdriver()

        driver, wait = make_driver()
        driver.get(CITRIX_URL)

        try:
            detect = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Detect Citrix Workspace app']"))
            )
            driver.execute_script("arguments[0].click();", detect)
        except:
            pass
            # After Detect Workspace
        time.sleep(3)

        # Force Chrome active
        driver.switch_to.window(driver.current_window_handle)
        time.sleep(3)
        click_citrix_popup()

        # Now click popup with Sikuli
        # helper.sikuli_retry_click("open_citrix_launcher.png", retries=5, timeout=10)

        time.sleep(2)
        # Click Log On
        try:
            log_on = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Switch to user name and password']")))
            driver.execute_script("arguments[0].click();", log_on)
        except:
            logger.info("No Log On link. Continuing.")

        # Login
        time.sleep(2)
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))

        username.send_keys("AT16818")
        password.send_keys("RadheShyam12!@")

        login_btn = wait.until(EC.element_to_be_clickable((By.ID, "loginBtn")))
        driver.execute_script("arguments[0].click();", login_btn)

        # Launch Zenit tile
        zenit_tile = wait.until(EC.element_to_be_clickable((By.XPATH, ZENIT_TILE)))
        driver.execute_script("arguments[0].click();", zenit_tile)

        # Click Open
        open_btn = wait.until(EC.element_to_be_clickable((By.XPATH, OPEN_XPATH)))
        ActionChains(driver).double_click(open_btn).perform()
        # After Detect Workspace
        time.sleep(3)
        click_citrix_popup()

        logger.info("✅ Zenit ICA session launched")

    except Exception as e:
        logger.error("🔥 Selenium launcher failed: " + str(e))
        traceback.print_exc()
        raise

if __name__ == "__main__":
    run()