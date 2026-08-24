# =====================================================================
# JVM MUST START BEFORE ANY OTHER IMPORTS — DO NOT EDIT BELOW
# =====================================================================

import jpype
import jpype.imports
# =====================================================================
# JVM MUST START BEFORE ANY OTHER IMPORTS — DO NOT EDIT BELOW
# =====================================================================

import jpype
import jpype.imports

if not jpype.isJVMStarted():
    jpype.startJVM(
        "-ea",
        r"-Djava.class.path="
        r"C:\Users\AT16818\Downloads\Zenit_Sikulix\libs\sikulixapi-2.0.5.jar;"
        r"C:\Users\AT16818\Downloads\Zenit_Sikulix\libs\sikulixapi-2.0.5-win.jar"
    )

# ✅ NOW (and ONLY now) import Sikuli
from org.sikuli.script import (
    Settings, Screen, Pattern, Region, ImagePath
)


scr = Screen()

Settings.AutoWaitTimeout = 10
Settings.MinSimilarity = 0.50
Settings.DelayBeforeMouseDown = 0.2
Settings.DelayAfterClick = 0.3
Settings.ObserveScanRate = 3
Settings.MoveMouseDelay = 0.02
# Set working dir for Sikuli images
import os
IMAGE_PATH = r"C:\Users\AT16818\Downloads\Zenit_Sikulix\Images"
os.chdir(IMAGE_PATH)

ImagePath.add(IMAGE_PATH)
print("✅ Sikuli ImagePath added:", IMAGE_PATH)



# =====================================================================
#              NOW IMPORT THE REST OF PYTHON MODULES
# =====================================================================

import time
import json
import http.client
import socket
import subprocess
import traceback
import datetime
import atexit
import logging

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


# =====================================================================
#                            LOGGING
# =====================================================================

logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("ZenitAutomation")


# =====================================================================
#         AUTOMATION HELPER (Sikuli + Selenium + JSON Reporting)
# =====================================================================

class AutomationHelper:

    def __init__(self, scr, screenshot_dir="screenshots"):
        self.scr = scr
        self.screenshot_dir = screenshot_dir
        self.report = {
            "start_time": str(datetime.datetime.now()),
            "steps": []
        }

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

    # Take screenshot
    def screenshot(self, name="error"):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{ts}.png"
        path = os.path.join(self.screenshot_dir, filename)
        self.scr.capture().save(self.screenshot_dir, filename)
        logger.error(f"📸 Screenshot saved: {path}")
        return path

    # Sikuli Retry Click


    import time

    def sikuli_retry_click(self, image, retries=5, delay=1):

        pattern = Pattern(image).similar(0.50)

        # Restrict search region (TOP UI area)
        region = Region(0, 0, self.scr.getBounds().width, 350)

        for attempt in range(retries):
            try:
                logger.info(f"Sikuli attempt {attempt + 1}: {image}")

                self.scr.click()  # force focus
                time.sleep(0.3)

                m = region.wait(pattern, 8)  # ✅ KEY DIFFERENCE
                m.highlight(0.5)

                region.click(m)
                self.log_step(image, "PASS")
                return True

            except Exception as e:
                logger.warning(f"Sikuli failed: {image} ({e})")
                time.sleep(delay)

        ss = self.screenshot(f"fail_{image}")
        self.log_step(image, "FAIL", ss)
        return False

    # OCR Validation
    def verify_text(self, expected_text):
        try:
            text = self.scr.text()
            if expected_text.lower() in text.lower():
                self.log_step(f"OCR found: {expected_text}", "PASS")
                return True
            else:
                ss = self.screenshot("ocr_fail")
                self.log_step(f"OCR missing: {expected_text}", "FAIL", ss)
                return False
        except Exception:
            ss = self.screenshot("ocr_exception")
            self.log_step("OCR exception", "FAIL", ss)
            return False

    # Selenium retry click
    def selenium_retry_click(self, driver, locator, retries=3):
        for attempt in range(retries):
            try:
                elem = driver.find_element(*locator)
                driver.execute_script("arguments[0].click();", elem)
                self.log_step(f"Selenium clicked {locator}", "PASS")
                return True
            except:
                time.sleep(1)

        self.log_step(f"Selenium failed: {locator}", "FAIL")
        return False

    # Add a step to automation report
    def log_step(self, step, status, screenshot=None):
        entry = {
            "time": str(datetime.datetime.now()),
            "step": step,
            "status": status,
            "screenshot": screenshot
        }
        self.report["steps"].append(entry)

    # Save JSON report
    def save_report(self):
        self.report["end_time"] = str(datetime.datetime.now())
        with open("automation_report.json", "w") as f:
            json.dump(self.report, f, indent=4)
        logger.info("✅ JSON report saved successfully: automation_report.json")


helper = AutomationHelper(scr)


# =====================================================================
#                         WINAPPDRIVER FUNCTIONS
# =====================================================================

HOST = "127.0.0.1"
PORT = 4723
CONNECT_TIMEOUT = 8
WINAPP = r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"


def wait_for_port(port=4723, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=2):
                return True
        except:
            time.sleep(1)
    return False


def start_winappdriver():
    if not os.path.exists(WINAPP):
        raise RuntimeError("WinAppDriver missing")

    subprocess.Popen([WINAPP], creationflags=subprocess.CREATE_NEW_CONSOLE)
    atexit.register(lambda: os.system("taskkill /F /IM WinAppDriver.exe"))

    time.sleep(3)
    logger.info("✅ WinAppDriver started successfully")
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
# =====================================================================
#                       SELENIUM SETUP FOR CITRIX
# =====================================================================

CHROMEDRIVER = r"C:\Program Files (x86)\ChromeDriver\chromedriver-win64\chromedriver.exe"
CITRIX_URL = "https://myworkspace.dnb.no/Citrix/SITWeb/"

ZENIT_TILE = "//p[normalize-space()='Zenit Kundefront - DaaS_PreTest']"
OPEN_XPATH = "//div[normalize-space()='Open']"


def make_driver():


    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-features=ExternalProtocolDialog")

    prefs = {

        "protocol_handler.allowed_origins": [
            "https://myworkspace.dnb.no"
        ]


    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(CHROMEDRIVER)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 25)
    return driver, wait




# =====================================================================
#                            MAIN AUTOMATION
# =====================================================================

def test_full_flow():

    try:
        start_winappdriver()

        driver, wait = make_driver()
        driver.get(CITRIX_URL)

        # Detect Citrix Workspace App
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
        #helper.sikuli_retry_click("open_citrix_launcher.png", retries=5, timeout=10)

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

        logger.info("✅ Citrix/Zenit ICA session launched")

    except Exception as e:
        logger.error("🔥 Selenium Stage Failed: " + str(e))
        traceback.print_exc()

    # =================================================================
    #                SIKULI AUTOMATION IN ZENIT (Citrix)
    # =================================================================

    time.sleep(10)

    helper.sikuli_retry_click("NyKundeMenu.png")
    helper.sikuli_retry_click("KundetypeDropdown.png")
    helper.sikuli_retry_click("PersonOption.png")

    helper.sikuli_retry_click("FodselsnrField.png")
    scr.type("30032699967")

    helper.sikuli_retry_click("NorgeLink.png")
    helper.sikuli_retry_click("NextStep.png")

    helper.sikuli_retry_click("Fornavn.png")
    scr.type("Radhe")

    helper.sikuli_retry_click("Etternavn.png")
    scr.type("Radhe")

    helper.sikuli_retry_click("LandDropdown.png")
    helper.sikuli_retry_click("LandCountry.png")

    helper.verify_text("Yes")

    helper.sikuli_retry_click("YesClick.png")

    helper.sikuli_retry_click("center_scroll_handle.png")
    scr.dragDrop("center_scroll_handle.png", scr.getLocation().offset(0, 300))

    helper.sikuli_retry_click("LegiLandDropdown.png")
    helper.sikuli_retry_click("LandCountry.png")

    helper.sikuli_retry_click("NextStep.png")
    helper.sikuli_retry_click("AddressLanddropdown.png")
    helper.sikuli_retry_click("Oman.png")

    helper.sikuli_retry_click("Address3.png")
    scr.type("address3 norway")

    helper.sikuli_retry_click("NextStep.png")
    helper.sikuli_retry_click("NeiButton.png")
    helper.sikuli_retry_click("Utlecheckbox.png")
    helper.sikuli_retry_click("Annet.png")

    scr.popup("✅ Automation Completed Successfully!")

    helper.save_report()


# =====================================================================
# RUN SCRIPT
# =====================================================================

test_full_flow()

if not jpype.isJVMStarted():
    jpype.startJVM(
        "-ea",
        r"-Djava.class.path="
        r"C:\Users\AT16818\Downloads\Zenit_Sikulix\libs\sikulixapi-2.0.5.jar;"
        r"C:\Users\AT16818\Downloads\Zenit_Sikulix\libs\sikulixapi-2.0.5-win.jar"
    )

# ✅ NOW (and ONLY now) import Sikuli
from org.sikuli.script import (
    Settings, Screen, Pattern, Region, ImagePath
)


scr = Screen()


# Set working dir for Sikuli images
import os
IMAGE_PATH = r"C:\Users\AT16818\Downloads\Zenit_Sikulix\Images"
os.chdir(IMAGE_PATH)

ImagePath.add(IMAGE_PATH)
print("✅ Sikuli ImagePath added:", IMAGE_PATH)



# =====================================================================
#              NOW IMPORT THE REST OF PYTHON MODULES
# =====================================================================

import time
import json
import http.client
import socket
import subprocess
import traceback
import datetime
import atexit
import logging

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


# =====================================================================
#                            LOGGING
# =====================================================================

logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("ZenitAutomation")


# =====================================================================
#         AUTOMATION HELPER (Sikuli + Selenium + JSON Reporting)
# =====================================================================

class AutomationHelper:

    def __init__(self, scr, screenshot_dir="screenshots"):
        self.scr = scr
        self.screenshot_dir = screenshot_dir
        self.report = {
            "start_time": str(datetime.datetime.now()),
            "steps": []
        }

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

    # Take screenshot
    def screenshot(self, name="error"):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{ts}.png"
        path = os.path.join(self.screenshot_dir, filename)
        self.scr.capture().save(self.screenshot_dir, filename)
        logger.error(f"📸 Screenshot saved: {path}")
        return path

    # Sikuli Retry Click


    import time

    def sikuli_retry_click(self, image, retries=5, delay=1):

        pattern = Pattern(image).similar(0.50)

        # Restrict search region (TOP UI area)
        region = Region(0, 0, self.scr.getBounds().width, 350)

        for attempt in range(retries):
            try:
                logger.info(f"Sikuli attempt {attempt + 1}: {image}")

                self.scr.click()  # force focus
                time.sleep(0.3)

                m = region.wait(pattern, 8)  # ✅ KEY DIFFERENCE
                m.highlight(0.5)

                region.click(m)
                self.log_step(image, "PASS")
                return True

            except Exception as e:
                logger.warning(f"Sikuli failed: {image} ({e})")
                time.sleep(delay)

        ss = self.screenshot(f"fail_{image}")
        self.log_step(image, "FAIL", ss)
        return False

    # OCR Validation
    def verify_text(self, expected_text):
        try:
            text = self.scr.text()
            if expected_text.lower() in text.lower():
                self.log_step(f"OCR found: {expected_text}", "PASS")
                return True
            else:
                ss = self.screenshot("ocr_fail")
                self.log_step(f"OCR missing: {expected_text}", "FAIL", ss)
                return False
        except Exception:
            ss = self.screenshot("ocr_exception")
            self.log_step("OCR exception", "FAIL", ss)
            return False

    # Selenium retry click
    def selenium_retry_click(self, driver, locator, retries=3):
        for attempt in range(retries):
            try:
                elem = driver.find_element(*locator)
                driver.execute_script("arguments[0].click();", elem)
                self.log_step(f"Selenium clicked {locator}", "PASS")
                return True
            except:
                time.sleep(1)

        self.log_step(f"Selenium failed: {locator}", "FAIL")
        return False

    # Add a step to automation report
    def log_step(self, step, status, screenshot=None):
        entry = {
            "time": str(datetime.datetime.now()),
            "step": step,
            "status": status,
            "screenshot": screenshot
        }
        self.report["steps"].append(entry)

    # Save JSON report
    def save_report(self):
        self.report["end_time"] = str(datetime.datetime.now())
        with open("automation_report.json", "w") as f:
            json.dump(self.report, f, indent=4)
        logger.info("✅ JSON report saved successfully: automation_report.json")


helper = AutomationHelper(scr)


# =====================================================================
#                         WINAPPDRIVER FUNCTIONS
# =====================================================================

HOST = "127.0.0.1"
PORT = 4723
CONNECT_TIMEOUT = 8
WINAPP = r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"


def wait_for_port(port=4723, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=2):
                return True
        except:
            time.sleep(1)
    return False


def start_winappdriver():
    if not os.path.exists(WINAPP):
        raise RuntimeError("WinAppDriver missing")

    subprocess.Popen([WINAPP], creationflags=subprocess.CREATE_NEW_CONSOLE)
    atexit.register(lambda: os.system("taskkill /F /IM WinAppDriver.exe"))

    time.sleep(3)
    logger.info("✅ WinAppDriver started successfully")
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
# =====================================================================
#                       SELENIUM SETUP FOR CITRIX
# =====================================================================

CHROMEDRIVER = r"C:\Program Files (x86)\ChromeDriver\chromedriver-win64\chromedriver.exe"
CITRIX_URL = "https://myworkspace.dnb.no/Citrix/SITWeb/"

ZENIT_TILE = "//p[normalize-space()='Zenit Kundefront - DaaS_PreTest']"
OPEN_XPATH = "//div[normalize-space()='Open']"


def make_driver():


    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-features=ExternalProtocolDialog")

    prefs = {

        "protocol_handler.allowed_origins": [
            "https://myworkspace.dnb.no"
        ]


    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(CHROMEDRIVER)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 25)
    return driver, wait




# =====================================================================
#                            MAIN AUTOMATION
# =====================================================================

def test_full_flow():

    try:
        start_winappdriver()

        driver, wait = make_driver()
        driver.get(CITRIX_URL)

        # Detect Citrix Workspace App
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
        #helper.sikuli_retry_click("open_citrix_launcher.png", retries=5, timeout=10)

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

        logger.info("✅ Citrix/Zenit ICA session launched")

    except Exception as e:
        logger.error("🔥 Selenium Stage Failed: " + str(e))
        traceback.print_exc()

    #=================================================================
    #              SIKULI AUTOMATION IN ZENIT (Citrix)
    #=================================================================

    time.sleep(10)

    helper.sikuli_retry_click("NyKundeMenu.png")
    helper.sikuli_retry_click("KundetypeDropdown.png")
    helper.sikuli_retry_click("PersonOption.png")

    helper.sikuli_retry_click("FodselsnrField.png")
    scr.type("30032699967")

    helper.sikuli_retry_click("NorgeLink.png")
    helper.sikuli_retry_click("NextStep.png")

    helper.sikuli_retry_click("Fornavn.png")
    scr.type("Radhe")

    helper.sikuli_retry_click("Etternavn.png")
    scr.type("Radhe")

    helper.sikuli_retry_click("LandDropdown.png")
    helper.sikuli_retry_click("LandCountry.png")

    helper.verify_text("Yes")

    helper.sikuli_retry_click("YesClick.png")

    helper.sikuli_retry_click("center_scroll_handle.png")
    scr.dragDrop("center_scroll_handle.png", scr.getLocation().offset(0, 300))

    helper.sikuli_retry_click("LegiLandDropdown.png")
    helper.sikuli_retry_click("LandCountry.png")

    helper.sikuli_retry_click("NextStep.png")
    helper.sikuli_retry_click("AddressLanddropdown.png")
    helper.sikuli_retry_click("Oman.png")

    helper.sikuli_retry_click("Address3.png")
    scr.type("address3 norway")

    helper.sikuli_retry_click("NextStep.png")
    helper.sikuli_retry_click("NeiButton.png")
    helper.sikuli_retry_click("Utlecheckbox.png")
    helper.sikuli_retry_click("Annet.png")

    scr.popup("✅ Automation Completed Successfully!")

    helper.save_report()


# =====================================================================
# RUN SCRIPT
# =====================================================================

test_full_flow()
