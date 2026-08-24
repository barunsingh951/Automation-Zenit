# -*- coding: utf-8 -*-

# ============================
#       COMMON UTILITIES
# ============================

import os
import json
import datetime
import random
import string

from sikuli import *

# IDE helper (no effect in runtime)
if False:
    def getBundlePath():
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(getBundlePath(), ".."))
REPORT_FILE = os.path.join(PROJECT_ROOT, "reports", "sikuli_report.json")


# ============================
# SCREENSHOT (BASE64 MEMORY)
# ============================

def take_screenshot(name="step"):
    import base64
    from java.io import ByteArrayOutputStream
    from javax.imageio import ImageIO

    img = SCREEN.capture().getImage()

    baos = ByteArrayOutputStream()
    ImageIO.write(img, "png", baos)

    byte_data = baos.toByteArray()

    # ✅ IMPORTANT: convert to STRING (not bytes)
    return base64.b64encode(byte_data).decode("utf-8")


# ============================
# LOGGER
# ============================

def log(step, status):

    screenshot = None

    # ✅ capture only on FAIL (best performance)
    #if status == "FAIL":
    if status in ["PASS", "FAIL"]:
        screenshot = take_screenshot()

    entry = {
        "time": str(datetime.datetime.now()),
        "step": step,
        "status": status,
        "screenshot": screenshot
    }

    print("[{}] {}".format(status, step))

    try:
        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, "r") as f:
                try:
                    data = json.load(f)
                except:
                    data = []
        else:
            data = []

        data.append(entry)

        with open(REPORT_FILE, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print("[ERROR] Failed to write report:", e)


# ============================
# UI ACTIONS
# ============================
def click(img):

    m = exists(Pattern(img).similar(0.6), 10)

    if not m:
        log("Button not found: " + img, "FAIL")
        return False

    pt = m.getTarget()

    hover(pt)
    wait(0.5)

    # ✅ Use normal click
    click(pt)

    wait(1)

    log("Clicked: " + img, "PASS")
    return True

def click_image(img, timeout=10, dx=-12, dy=0):

    m = exists(Pattern(img).similar(0.75), timeout)

    if m:
        target = m.getTarget().offset(dx, dy)

        hover(target)
        wait(0.2)

        mouseDown(Button.LEFT)
        wait(0.12)
        mouseUp(Button.LEFT)

        log("Click " + img, "PASS")
        wait(0.3)
        return True
    else:
        log("Click " + img, "FAIL")
        return False


def click_image_right(img, timeout=10, dx=20, dy=0):

    m = exists(Pattern(img).similar(0.75), timeout)

    if m:
        # ✅ Move RIGHT instead of left
        target = m.getTarget().offset(dx, dy)

        hover(target)
        wait(0.3)

        mouseDown(Button.LEFT)
        wait(0.15)
        mouseUp(Button.LEFT)

        log("Click " + img, "PASS")
        wait(0.5)
        return True
    else:
        log("Click " + img, "FAIL")
        return False
def double_click_image_right(img, timeout=10, dx=20, dy=0):

    m = exists(Pattern(img).similar(0.75), timeout)

    if m:

        target = m.getTarget().offset(dx, dy)

        hover(target)
        wait(0.3)

        # First click
        mouseDown(Button.LEFT)
        wait(0.15)
        mouseUp(Button.LEFT)

        wait(0.2)

        # Second click
        mouseDown(Button.LEFT)
        wait(0.15)
        mouseUp(Button.LEFT)

        log("Double Click " + img, "PASS")

        wait(0.5)

        return True

    else:

        log("Double Click " + img, "FAIL")

        return False

def type_text(img, text):

    if click_image(img):
        wait(0.3)
        type(text)
        log("Typed into " + img, "PASS")
        return True

    else:
        log("Failed to type into " + img, "FAIL")
        return False
def type_text_right(img, text):

    if click_image_right(img):
        wait(0.3)
        type(text)
        log("Typed into " + img, "PASS")
        return True

    else:
        log("Failed to type into " + img, "FAIL")
        return False
def clear_type_text_right(img, text):

    if click_image_right(img):
        type("a", KeyModifier.CTRL)
        type(Key.BACKSPACE)
        wait(0.3)
        type(text)
        log("Typed into " + img, "PASS")
        return True

    else:
        log("Failed to type into " + img, "FAIL")
        return False
def clear_type_text(img, text):

    if click_image(img):
        type("a", KeyModifier.CTRL)
        type(Key.BACKSPACE)
        wait(0.3)
        type(text)
        log("Typed into " + img, "PASS")
        return True

    else:
        log("Failed to type into " + img, "FAIL")
        return False
def scroll_to_middle(handle_img="scrollbar.png", timeout=3):

    if exists(handle_img, timeout):

        m = getLastMatch()

        # ✅ Move to middle of screen
        safe_middle = Location(
            m.getX(),
            SCREEN.getBounds().height // 2
        )

        dragDrop(m, safe_middle)
        wait(1)

        log("Scrolled to middle", "PASS")
        return True

    else:
        log("Scroll bar not found", "FAIL")
        return False
def scroll_to_bottom(handle_img="scrollbar.png", timeout=3):

    if exists(handle_img, timeout):

        m = getLastMatch()

        # ✅ Use full region (more stable than screen)
        r = Region(m.getX(), m.getY(), m.getW(), m.getH())

        # ✅ Scroll to bottom of scrollbar
        target = Location(r.x, r.y + r.h - 5)

        dragDrop(m, target)
        wait(1)

        log("Scrolled to bottom", "PASS")
        return True

    else:
        log("Scroll bar not found", "FAIL")
        return False
def scroll(handle_img="scrollbar.png", position="middle"):

    if exists(handle_img, 3):

        m = getLastMatch()
        r = Region(m.getX(), m.getY(), m.getW(), m.getH())

        if position == "top":
            target = Location(r.x, r.y + 5)

        elif position == "middle":
            target = Location(r.x, r.y + int(r.h * 0.6))

        elif position == "bottom":
            target = Location(r.x, r.y + r.h - 5)

        elif position == "quarter":
            target = Location(r.x, r.y + int(r.h * 0.25))

        dragDrop(m, target)
        wait(1)

        log("Scrolled to " + position, "PASS")
        return True

    else:
        log("Scroll bar not found", "FAIL")
        return False
def verify_pep_details():

    result = True
    wait(2)

    # ✅ Verify selection: "Meg selv"
    if exists("megselv.png", 5):
        log("PEP selection verified: Meg selv", "PASS")
    else:
        log("PEP selection FAILED", "FAIL")
        result = False

    # ✅ Verify PEP position
    if exists("statusoverhead.png", 5):
        log("PEP position verified", "PASS")
    else:
        log("PEP position FAILED", "FAIL")
        result = False

    # ✅ Verify Country (Norge)
    if exists("norge.png", 5):
        log("PEP country verified (Norge)", "PASS")
    else:
        log("PEP country FAILED", "FAIL")
        result = False

    # ✅ Verify Date
    if exists("pepdate.png", 5):
        log("PEP date verified", "PASS")
    else:
        log("PEP date FAILED", "FAIL")
        result = False

    return result

def click_dropdown_arrow1(img, timeout=10, right_pad=12):
    m = exists(Pattern(img).similar(0.75), timeout)

    if not m:
        log("Dropdown not found " + img, "FAIL")
        return False

    r = Region(m.getX(), m.getY(), m.getW(), m.getH())

    pt = Location(r.x + r.w - right_pad, r.y + r.h // 2)

    hover(pt)
    wait(0.25)

    mouseDown(Button.LEFT)
    wait(0.15)
    mouseUp(Button.LEFT)

    log("Dropdown arrow " + img, "PASS")
    return True

def select_type_by_index(index):

    # Open Type dropdown
    if not click_dropdown("type_dropdown.png"):
        log("Failed to open Type dropdown", "FAIL")
        return False

    wait(1)

    # Move to first item
    type(Key.HOME)
    wait(0.3)

    # Navigate to required item
    for i in range(index):
        type(Key.DOWN)
        wait(0.2)

    # Select
    type(Key.ENTER)

    log("Type selected index: " + str(index), "PASS")

    return True
def debug_address_group_indexes():

    # if not click_image_right("adressegruppe.png"):
    #     log("Failed to open Adressegruppe dropdown", "FAIL")
    #     return False

    wait(1)

    # Move to first item
    type(Key.HOME)
    wait(0.5)

    groups = [
        "BANKAXEPT",
        "ENGASJEMENT_OPPGAVE",
        "ENGASJEMENT_REVISJON",
        "HOVEDADRESSE",
        "KLIENTKONTO",
        "KONTAKTADRESSE"
    ]

    for idx, name in enumerate(groups):

        log("Index = " + str(idx) + " Value = " + name, "INFO")

        # Move down to next item
        if idx > 0:
            type(Key.DOWN)
            wait(0.5)

    type(Key.ESC)

    return True
def expand_dropdown(img, timeout=10):
    m = exists(Pattern(img).similar(0.6), timeout)

    if not m:
        log("Dropdown not found: " + img, "FAIL")
        return False

    r = Region(m.getX(), m.getY(), m.getW(), m.getH())

    # ✅ Click extreme right (arrow area)
    pt = Location(r.x + r.w - 5, r.y + r.h // 2)

    hover(pt)
    wait(0.3)

    mouseDown(Button.LEFT)
    wait(0.15)
    mouseUp(Button.LEFT)

    wait(1)  # ✅ important for dropdown to open

    log("Dropdown expanded", "PASS")
    return True
def verify_field_value(field_img, expected_value):

    # Focus field
    if not click_image(field_img):
        log("Field not found: " + field_img, "FAIL")
        return False

    wait(0.5)

    # Copy field value
    type("a", KeyModifier.CTRL)
    wait(0.2)

    type("c", KeyModifier.CTRL)
    wait(0.5)

    actual_value = Env.getClipboard().strip()

    if str(expected_value) in actual_value:

        log(
            "Verification Passed. Expected=" +
            str(expected_value) +
            " Actual=" +
            actual_value,
            "PASS"
        )

        return True

    log(
        "Verification Failed. Expected=" +
        str(expected_value) +
        " Actual=" +
        actual_value,
        "FAIL"
    )

    take_screenshot("verification_failed")

    return False
def verify_postnummer(expected_value):

    # Click Postnummer field
    if not click_image_right("addresspostnummer.png"):
        log("addresspostnummer field not found", "FAIL")
        return False

    if not double_click_image_right("addresspostnummer.png"):
        log("addresspostnummer field not found", "FAIL")
        return False

    wait(0.5)

    # Copy value
    #type("a", KeyModifier.CTRL)
    wait(0.2)

    type("c", KeyModifier.CTRL)
    wait(0.5)
    log("Clipboard value = " + Env.getClipboard(), "INFO")
    actual_value = Env.getClipboard()
    log("Actual value: " + str(actual_value), "INFO")
    if actual_value == str(expected_value):

        log(
            "Postnummer verified. Expected="
            + str(expected_value)
            + " Actual="
            + actual_value,
            "PASS"
        )

        return True

    log(
        "Postnummer mismatch. Expected="
        + str(expected_value)
        + " Actual="
        + actual_value,
        "FAIL"
    )

    take_screenshot("postnummer_mismatch")

    return False

def select_address_group_by_index(index):

    if not expand_dropdown("adressegruppe.png"):
        return False

    wait(1)

    if index >= 0:

        type(Key.HOME)

        for i in range(index):
            type(Key.DOWN)
            wait(0.2)

    else:

        type(Key.END)

        for i in range(abs(index) - 1):
            type(Key.UP)
            wait(0.2)

    type(Key.ENTER)

    log("Selected index: " + str(index), "PASS")

    return True
def select_address_group(group_name):

    ADDRESS_GROUP_INDEX = {
        "BANKAXEPT_FAKTURERING": 0,
        "ENGASJEMENT_OPPGAVE": 1,
        "ENGASJEMENT_REVISJON": 2,
        "HOVEDADRESSE": 3,
        "KLIENTKONTO": 4,
        "KONTAKTADRESSE": 5
    }

    if group_name not in ADDRESS_GROUP_INDEX:
        log("Invalid address group: " + group_name, "FAIL")
        return False

    if not expand_dropdown("adressegruppe.png"):
        log("Failed to open Adressegruppe dropdown", "FAIL")
        return False

    wait(1)

    type(Key.HOME)

    index = ADDRESS_GROUP_INDEX[group_name]

    for i in range(index):
        type(Key.DOWN)
        wait(0.2)

    type(Key.ENTER)

    log("Selected Address Group: " + group_name, "PASS")

    return True
def select_address_group_by_index_old(index):

    if not expand_dropdown("adressegruppe.png"):
        log("Failed to open Adressegruppe dropdown", "FAIL")
        return False

    wait(1)

    type(Key.HOME)
    wait(0.3)

    for i in range(index):
        type(Key.DOWN)
        wait(0.2)

    type(Key.ENTER)

    log("Adressegruppe selected index: " + str(index), "PASS")

    return True
def select_type(type_img):

    # focus type dropdown
    if not click_image("type_dropdown.png"):
        log("Type dropdown not focused", "FAIL")
        return False

    wait(0.5)

    # open dropdown
    type(Key.DOWN)
    wait(1)

    # select value
    if not click_image(type_img):
        log("Failed selecting type: " + type_img, "FAIL")
        return False

    return True
def verify_from_grid(group_img, type_img, value):

    result = True

    if not exists(group_img, 5):
        log("Group not found in grid", "FAIL")
        result = False

    if not exists(type_img, 5):
        log("Type not found in grid", "FAIL")
        result = False

    if not exists(Pattern(value).similar(0.6), 5):
        log("Value not found in grid", "FAIL")
        result = False

    if result:
        log("Grid verification success", "PASS")

    return result
def save_address():

    if click_image("save_button.png"):
        wait(2)
        log("Saved successfully", "PASS")
        return True
    else:
        log("Save failed", "FAIL")
        return False
def select_dropdown_value(option_img):

    if exists(option_img, 5):
        click_image(option_img)
        log("Selected option: " + option_img, "PASS")
        return True
    else:
        log("Option not found: " + option_img, "FAIL")
        return False
def click_dropdown_arrow(img, timeout=10, right_padding=5):

    m = exists(Pattern(img).similar(0.75), timeout)

    if not m:
        log("Dropdown not found: " + img, "FAIL")
        return False

    # ✅ Get full region of matched field
    r = Region(m.getX(), m.getY(), m.getW(), m.getH())

    # ✅ Move to RIGHT EDGE (arrow area)
    pt = Location(
        r.x + r.w - right_padding,
        r.y + r.h // 2
    )

    hover(pt)
    wait(0.3)

    # ✅ Citrix-safe click (IMPORTANT)
    mouseDown(Button.LEFT)
    wait(0.15)
    mouseUp(Button.LEFT)

    wait(0.8)   # allow dropdown to open

    log("Dropdown arrow clicked: " + img, "PASS")
    return True

def click_dropdown(img, timeout=10, right_padding=15):

    m = exists(Pattern(img).similar(0.75), timeout)

    if m:
        r = Region(m.getX(), m.getY(), m.getW(), m.getH())
        pt = Location(r.x + r.w - right_padding, r.y + r.h // 2)

        hover(pt)
        wait(0.2)

        mouseDown(Button.LEFT)
        wait(0.12)
        mouseUp(Button.LEFT)

        log("Click dropdown " + img, "PASS")
        return True
    else:
        log("Click dropdown " + img, "FAIL")
        return False


def select_dropdown_using_keyboard(img, option_down_count):

    # Step 1: focus the field
    if not click_image(img):
        log("Failed to focus dropdown", "FAIL")
        return False

    wait(0.5)

    # Step 2: open dropdown using keyboard
    type(Key.DOWN)
    wait(0.5)

    # Step 3: navigate to option
    for i in range(option_down_count):
        type(Key.DOWN)
        wait(0.2)

    # Step 4: select
    type(Key.ENTER)

    log("Dropdown selected using keyboard", "PASS")
    return True

def double_click_image(img, timeout=10, dx=-12, dy=0):
    m = exists(Pattern(img).similar(0.75), timeout)

    if m:
        target = m.getTarget().offset(dx, dy)

        hover(target)
        wait(0.2)

        for _ in range(2):
            mouseDown(Button.LEFT)
            wait(0.12)
            mouseUp(Button.LEFT)
            wait(0.18)

        log("DoubleClick " + img, "PASS")
        return True

    else:
        log("DoubleClick " + img, "FAIL")
        return False



def generate_random_name(length=6):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def double_click_inside_box(img, timeout=10, x_pad=20):
    m = exists(Pattern(img).similar(0.75), timeout)

    if m:
        r = Region(m.getX(), m.getY(), m.getW(), m.getH())

        pt = Location(r.x + x_pad, r.y + r.h // 2)

        hover(pt)
        wait(0.2)

        for _ in range(2):
            mouseDown(Button.LEFT)
            wait(0.12)
            mouseUp(Button.LEFT)
            wait(0.18)

        log("DoubleClick inside box " + img, "PASS")
        return True

    else:
        log("DoubleClick inside box " + img, "FAIL")
        return False