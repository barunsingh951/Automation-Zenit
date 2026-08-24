# =====================================================================
#                    IMPORTS & INITIAL SETUP
# =====================================================================

import os
import time
import json
import http.client
import socket
import subprocess
import traceback
import datetime
import atexit

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

# Logging
import logging

logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("ZenitAutomation")

# =====================================================================
#                      SIKULI API (JPype)
# =====================================================================

import jpype
import jpype.imports

# Correct Sikuli JAR path (matches your folder)
SIKULI_JAR = r"C:\Users\AT16818\Downloads\Zenit_Sikulix\libs\sikulixapi-2.0.5-windows.jar"


# ✅ Start JVM using the correct classpath method
jpype.startJVM("-ea", f"-Djava.class.path={SIKULI_JAR}")

# ✅ Import Sikuli classes AFTER JVM is started
from org.sikuli.script import Screen, Pattern

# Create Sikuli screen
scr = Screen()

# Add image path
IMAGE_PATH = r"C:\Users\AT16818\Downloads\Zenit_Sikulix\Images"
# Sikuli auto-loads image files from CWD, no manual path needed.
os.chdir(IMAGE_PATH)


# =====================================================================
#            AUTOMATION HELPER (Sikuli + Selenium + Reporting)
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

    # --------------------------------------------------------------
    # Screenshot
    # --------------------------------------------------------------
    def screenshot(self, name="error"):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{ts}.png"
        path = os.path.join(self.screenshot_dir, filename)
        self.scr.capture().save(self.screenshot_dir, filename)
        logger.error(f"📸 Screenshot saved: {path}")
        return path

    # --------------------------------------------------------------
    # Sikuli Retry-Click
    # --------------------------------------------------------------
    def sikuli_retry_click(self, image, retries=3, delay=1):
        for attempt in range(retries):
            try:
                logger.info(f"Sikuli: Attempt {attempt + 1} click on {image}")
                m = self.scr.wait(Pattern(image).similar(0.75), 10)
                self.scr.hover(m)
                time.sleep(0.3)
                self.scr.click(m.offset(5, 5))
                self.log_step(image, "PASS")
                return True
            except Exception as e:
                logger.warning(f"Click failed: {image} ({e})")
                time.sleep(delay)

        logger.error(f"❌ Failed to click: {image}")
        self.screenshot(f"fail_{image}")
        self.log_step(image, "FAIL")
        return False

    # --------------------------------------------------------------
    # OCR Validation
    # --------------------------------------------------------------
    def verify_text(self, expected_text, timeout=6):
        try:
            logger.info(f"Validating text: {expected_text}")
            region_text = self.scr.text()
            if expected_text.lower() in region_text.lower():
                logger.info(f"✅ OCR Passed: {expected_text}")
                self.log_step("OCR: " + expected_text, "PASS")
                return True
            else:
                logger.error(f"❌ OCR Failed: {expected_text}")
                self.screenshot("ocr_fail")
                self.log_step("OCR: " + expected_text, "FAIL")
                return False
        except Exception as e:
            logger.error(f"OCR Exception: {str(e)}")
            self.screenshot("ocr_exception")
            self.log_step("OCR Exception", "FAIL")
            return False

    # --------------------------------------------------------------
    # Selenium retry click
    # --------------------------------------------------------------
    def selenium_retry_click(self, driver, locator, retries=3):
        for attempt in range(retries):
            try:
                elem = driver.find_element(*locator)
                driver.execute_script("arguments[0].click();", elem)
                self.log_step("Selenium Click: " + str(locator), "PASS")
                return True
            except Exception as e:
                logger.warning(f"Selenium click failed: {locator} attempt {attempt+1}")
                time.sleep(1)

        logger.error(f"❌ Selenium could not click: {locator}")
        self.log_step("Selenium Click Fail: " + str(locator), "FAIL")
        return False

    # --------------------------------------------------------------
    # Log step to report
    # --------------------------------------------------------------
    def log_step(self, step, status):
        self.report["steps"].append({
            "time": str(datetime.datetime.now()),
            "step": step,
            "status": status
        })

    # --------------------------------------------------------------
    # Write JSON report
    # --------------------------------------------------------------
    def save_report(self):
        self.report["end_time"] = str(datetime.datetime.now())
        with open("automation_report.json", "w") as f:
            json.dump(self.report, f, indent=4)
        logger.info("✅ Report saved: automation_report.json")


helper = AutomationHelper(scr)


# =====================================================================
#                          WINAPPDRIVER
# =====================================================================

HOST = "127.0.0.1"
PORT = 4723
WINAPPDRIVER_PATH = r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"


def wait_for_port(port=4723, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((HOST, port), timeout=2):
                return True
        except:
            time.sleep(1)
    return False


def start_winappdriver():
    if not os.path.exists(WINAPPDRIVER_PATH):
        raise RuntimeError("WinAppDriver not found")

    subprocess.Popen([WINAPPDRIVER_PATH], creationflags=subprocess.CREATE_NEW_CONSOLE)
    atexit.register(lambda: os.system("taskkill /F /IM WinAppDriver.exe"))

    if wait_for_port():
        logger.info("✅ WinAppDriver ready")
    else:
        raise RuntimeError("WinAppDriver did not start")




# =====================================================================
#                         SELENIUM SETUP
# =====================================================================

CHROME_DRIVER = r"C:\Program Files (x86)\ChromeDriver\chromedriver-win64\chromedriver.exe"
CITRIX_URL = "https://myworkspace.dnb.no/Citrix/SITWeb/"
ZENIT_TILE = "//p[normalize-space(.)='Zenit Kundefront - DaaS_PreTest']"
OPEN_XPATH = "//div[normalize-space(.)='Open']"


def make_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER), options=options)
    wait = WebDriverWait(driver, 20)
    return driver, wait


# =====================================================================
#                          MAIN AUTOMATION
# =====================================================================

def test_full_flow():

    # ----------------------------------------------------------------------
    #                   SIKULI: AUTOMATE ZENIT Desktop in Citrix
    # ----------------------------------------------------------------------

    time.sleep(8)

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

    # Scroll
    helper.sikuli_retry_click("center_scroll_handle.png")
    scr.dragDrop("center_scroll_handle.png", scr.getLocation().offset(0, 280))

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

    scr.popup("✅ Completed Successfully!")

    helper.save_report()


# =====================================================================
# RUN SCRIPT
# =====================================================================

test_full_flow()