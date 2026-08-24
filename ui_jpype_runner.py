# ui_jpype_runner.py
import jpype
import jpype.imports
import time
import logging
import os
import json
import datetime
import traceback

# ---------------- START JVM ----------------
if not jpype.isJVMStarted():
    jpype.startJVM(
        "-ea",
        r"-Djava.class.path="
        r"C:\Users\AT16818\Downloads\Zenit_Sikulix\libs\sikulixapi-2.0.5.jar;"
        r"C:\Users\AT16818\Downloads\Zenit_Sikulix\libs\sikulixapi-2.0.5-win.jar"
    )

from org.sikuli.script import Screen, Pattern, Region, Settings

scr = Screen()
Settings.AutoWaitTimeout = 10
Settings.MinSimilarity = 0.5

# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="ui_jpype_runner.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("UIJPypeRunner")

# ---------------- MAIN LOGIC ----------------
def run():
    try:
        logger.info("✅ JPype Sikuli runner started")

        # ✅ YOUR EXISTING JPYPE UI LOGIC HERE
        # Example:
        # scr.wait("some_image.png", 10)
        # scr.click("some_image.png")

        logger.info("✅ JPype UI automation finished")

    except Exception as e:
        logger.error("🔥 JPype runner failed: " + str(e))
        traceback.print_exc()
        raise

if __name__ == "__main__":
    run()