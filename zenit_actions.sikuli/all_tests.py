# -*- coding: utf-8 -*-

from sikuli import *

from common import *


#TIN = globals().get("TIN", "")


# ============================
#        TEST CASES
# ============================

def test_search_and_kunde(TIN):
    log("TEST CASE: Search + Kunde Flow", "INFO")

    result = True

    wait(2)
    #wait(30)
    # Search
    click_image("searchfiled.png")
    if not type_text("searchfiled.png", "TIN"):
        result = False

    if not click_image("searchclick.png"):
        result = False

    wait(0.5)

    if not click_image("kundecontrollink.png"):
        result = False

    if result:
        log("Search + Kunde completed", "PASS")
    else:
        log("Search + Kunde failed", "FAIL")

    return result


def test_search_cust(TIN):
    log("TEST CASE: Search +  Flow", "INFO")
    App.focus("Zenit")
    result = True

    wait(2)

    click_image("searchfiled.png")
    if not type_text("searchfiled.png", "04119943790"):
        result = False

    if not click_image("searchclick.png"):
        result = False
    if not click_image("startsidetab.png"):
        result = False
    if result:
        log("Search + Kunde completed", "PASS")
    else:
        log("Search + Kunde failed", "FAIL")

    return result

def test_to_store_address(TIN):
    log("TEST CASE: Search +  Flow", "INFO")
    App.focus("Zenit")
    result = True

    wait(2)

    click_image("searchfiled.png")
    if not type_text("searchfiled.png", "24043635952"):
        result = False

    if not click_image("searchclick.png"):
        result = False
    if not click_image("kundecontrollink.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("startsidetab.png"):
        result = False
    if result:
        log("Search + Kunde completed", "PASS")
    else:
        log("Search + Kunde failed", "FAIL")

    return result


def run_address_flow(TIN):
    if not click_image("addresserlink.png"):
        result = False

    ADDRESS_GROUPS = [

        "BankAxept_Fakturering.png",
        "Engasjement_oppgave.png",
        "Engasjement_revisjon.png",
        "Hovedadresse.png",
        "Klientkonto.png",
        "Kontaktadresse.png"

    ]

    ADDRESS_TYPES = [
        "Epost_adresse.png",
        "Telefaks.png",
        "Mobiltelefon.png",
        "Postadresse.png",
        "Kunde_siftaddress.png",
        "Telefon.png",
        "Hjemmeside.png"
    ]

    result = True

    for group in ADDRESS_GROUPS:

        log("Processing Address Group: " + group, "INFO")
        if not click_image("newaddress.png"):
            result = False

        wait(2)
        # ✅ Select Address Group

        if not expand_dropdown("adressegruppe.png"):
            result = False

            continue

        if not click_image(group):
            result = False
            continue

        wait(1)

        # ✅ Loop Types
        if not type_text("searchfiled.png", TIN):

            log("Processing Type: " + typ, "INFO")

            # ✅ Select Type
            if not click_dropdown("type_dropdown.png"):
                result = False
                continue
            wait(1)
            if not click_image(typ):
                result = False
                continue

            wait(2)
            value = str(int(time.time()))
            click_image("postaddress.png")
            if not type_text_right("postaddress.png", value):
                result = False
            wait(1)
            handle_land_field()
            wait(1)
            # ✅ Generate unique value

            # ✅ Save
            if not click_image_right("save_button.png"):
                result = False

            wait(2)

            handle_error_popup()
            # ✅ VERIFY FROM GRID
            wait(2)

            group_ok = exists(group, 5)
            type_ok = exists(typ, 5)
            value_ok = exists(Pattern(value).similar(0.6), 5)

            if group_ok:
                log("Grid Group Verified", "PASS")
            else:
                log("Grid Group FAILED", "FAIL")

            if type_ok:
                log("Grid Type Verified", "PASS")
            else:
                log("Grid Type FAILED", "FAIL")

            if value_ok:
                log("Grid Value Verified: " + value, "PASS")
            else:
                log("Grid Value FAILED: " + value, "FAIL")

            # ✅ Continue execution but mark failure
            if not (group_ok and type_ok and value_ok):
                result = False
            if not click_image("newaddress.png"):
                result = False

    return result


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


def handle_error_popup():
    wait(1)

    # ✅ Detect popup (use error icon or message area)
    if exists("ok.png", 3):

        log("Error popup detected", "FAIL")

        # ✅ Take screenshot manually (if not already in log FAIL)
        take_screenshot("error_popup")

        # ✅ Click OK button
        if click_image("ok.png"):
            log("Clicked OK on error popup", "PASS")
        else:
            log("OK button not found", "FAIL")

        wait(1)
        return True

    return False


def handle_land_field():
    wait(1)

    if exists("addresslandNo.png", 3):
        log("Land is NO → changing to AL", "INFO")

        if not clear_type_text("addresslandNo.png", "Al"):
            return False

        return True

    elif exists("addresslandAL.png", 3):
        log("Land already AL → no change", "PASS")
        return True

    else:
        log("Land not detected → setting AL", "INFO")

        if not type_text("landkode.png", "Al"):
            return False

        return True


def test_address_update_verify(TIN):
    log("TEST CASE: Address + Update nd verify", "INFO")

    result = True
    wait(5)

    if not click_image("addresserlink.png"):
        result = False

    wait(0.5)

    if not click_image("kundecontrollink.png"):
        result = False

    wait(2)

    if not click_image("jaradiobutton.png"):
        result = False

    if result:
        log("Search + Kunde completed", "PASS")
    else:
        log("Search + Kunde failed", "FAIL")

    return result


def test_onboard_individual_person_customer(TIN):
    log("TEST CASE: Search + Kunde Flow", "INFO")

    result = True

    wait(5)
    # Search
    if not click_image("NyKundeMenu.png"):
        result = False

    if not click_image("KundetypeDropdown.png"):
        result = False

    if not click_image("PersonOption.png"):
        result = False
    if not type_text("FodselsnrTin.png", "14814697054"):
        result = False
    if not click_image("norge.png"):
        result = False
    scroll("scrollbar.png", "bottom")

    if not click_image("LegiLandDropdown.png"):
        result = False

    if not click_image("LandCountry.png"):
        result = False
    #if not click_image("HentCheckbox.png"):
    #    result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("confirmok.png"):
        result = False
    if not click_image("neiradiobutton.png"):
        result = False
    if not click_image("landdropdown.png"):
        result = False
    if not click_image("landcountrybelarus.png"):
        result = False
    return result


def test_onboard_business_nearing_customer(TIN):
    log("TEST CASE: Search + Kunde Flow", "INFO")

    result = True
    App.focus("Zenit")
    wait(5)
    # Search
    if not click_image("NyKundeMenu.png"):
        result = False

    if not click_image("KundetypeDropdown.png"):
        result = False

    if not click_image("nearingcustomer.png"):
        result = False

    if not click_image("registerclientdropdown.png"):
        result = False
    if not click_image("kundeundertable.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not type_text_right("sfocode.png", "FD"):
        result = False

    if not type_text_right("sectorcode.png", "8200"):
        result = False

    if not type_text_right("nearingcode.png", "1130"):
        result = False
    first_name = generate_random_name()
    wait(2)
    if not type_text("categoryfirstname.png", first_name):
        result = False

    if not type_text_right("tabledate.png", "02.03.2024"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not type_text_right("addressline1.png", "oslo"):
        result = False
    if not click_image("addresslanddropdown.png"):
        result = False
    if not click_image("landcountrybelarus.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False

    if not click_image("ekcheckbox.png"):
        result = False
    if not click_image_right("ekcaptialja.png"):
        result = False
    if not type_text_right("ekcomments.png", "Radhe"):
        result = False
    if not click_image("lancheckbox.png"):
        result = False
    if not click_image("lanjaradiobutton.png"):
        result = False
    if not type_text_right("lancomments.png", "Radhe"):
        result = False
    if not scroll_to_bottom():
        result = False
    if not click_image("tradefinancecheckbox.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False

    test_international_transaction(TIN)
    test_contact_person(TIN)
    test_tax_reporting(TIN)
    return result


def test_mid_flow(TIN):
    log("TEST CASE: Mid Flow (scroll + next)", "INFO")

    result = True
    wait(2)

    if not click_image("jaradiobutton.png"):
        result = False
    wait(2)
    handlee = "scrollbar.png"

    if exists(handlee, 3):
        m = getLastMatch()
        safe_bottom = Location(m.getX(), SCREEN.getBounds().height - 100)
        dragDrop(m, safe_bottom)
    else:
        log("Scroll bar not found", "FAIL")
        result = False

    if not click_image("LegiLandDropdown.png"):
        result = False

    if not click_image("LandCountry.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("Utlecheckbox.png"):
        result = False

    #scroll("newscroll.png", "bottom")
    handlee = "newscroll.png"
    if exists(handlee, 3):
        m = getLastMatch()
        safe_bottom = Location(m.getX(), SCREEN.getBounds().height - 100)
        dragDrop(m, safe_bottom)
    else:
        log("Scroll bar not found", "FAIL")
        result = False

    wait(0.4)

    if not click_image("jaradiobutton.png"):
        result = False

    if not click_image("Annet.png"):
        result = False

    if not type_text("Spesifiser.png", "Radhe"):
        result = False
    return result


def test_non_pep_flow(TIN):
    log("TEST CASE: 53449--TC03_Kundekontroll on norwegian PM non-PEP customer from ZK", "INFO")
    #10928798378
    #result1,2,3,4
    result = True

    if not click_image("NextStep.png"):
        result = False

    if not click_image("Leggtillkundesvarbutton.png"):
        result = False

    if not click_image("pepneiradiobutton1.png"):
        result = False

    if not click_image("pepneiradiobutton2.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    return result


def test_pep_flow_veg_selv(TIN):
    log("TEST CASE: PEP Flow Veg", "INFO")

    result = True
    wait(5)

    if not click_image("kundecontrollink.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("Leggtillkundesvarbutton.png"):
        result = False
    wait(5)
    if not click_image("jaradiobutton.png"):
        result = False
    wait(5)
    if not click_image("megselv.png"):
        result = False
    wait(5)
    if not double_click_image("peppositiondropdownclick.png"):
        result = False
    if not click_image("statusoverhead.png"):
        result = False

    wait(5)

    if not click_image("peppositiondropdownclick.png"):
        result = False
    wait(1)
    if not click_image("peppostionmedlemnasjom.png"):
        result = False
    wait(5)
    if not click_image("peppositiondropdownclick.png"):
        result = False
    wait(1)
    if not click_image("peppositionambasdor.png"):
        result = False
    wait(5)
    if not click_image("peppositiondropdownclick.png"):
        result = False
    wait(1)
    if not click_image("peppostionmedlemstynet.png"):
        result = False
    wait(5)
    if not click_image("peppositiondropdownclick.png"):
        result = False
    wait(1)
    if not click_image("peppositionmedlemadmin.png"):
        result = False
    wait(5)
    if not click_image("peppositiondropdownclick.png"):
        result = False
    wait(1)
    if not click_image("peppositiondirector.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False

    return result


def test_kundecontrol_pep_flow(TIN):
    log("TEST CASE: 53450--TC04_Kundekontroll on norwegian PM PEP customer from ZK", "INFO")
    #04899398632
    result = True
    #wait(5)
    App.focus("Zenit")
    click_image("searchfiled.png")
    if not type_text("searchfiled.png", "04899398632"):
        result = False

    if not click_image("searchclick.png"):
        result = False

    wait(0.5)

    if not click_image("kundecontrollink.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False
    wait(2)
    verify_pep_details()
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("fullfiller.png"):
        result = False

    if not click_image("jabutton.png"):
        result = False
    return result


def test_kundecontrol_bm_non_pep(TIN):
    log("TEST CASE: 53453--TC07_Kundekontroll on norwegian BM non-PEP customer from ZK", "INFO")
    #04899398632
    App.focus("Zenit")
    result = True
    #wait(5)

    click_image("searchfiled.png")
    if not type_text("searchfiled.png", "04899398632"):
        result = False

    if not click_image("searchclick.png"):
        result = False

    wait(0.5)

    if not click_image("kundecontrollink.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False
    wait(2)
    #verify_pep_details()
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("fullfiller.png"):
        result = False

    if not click_image("jabutton.png"):
        result = False
    return result


def test_pep_flow_near_family(TIN):
    log("TEST CASE: PEP Flow near family", "INFO")

    result = True
    wait(5)

    if not click_image("kundecontrollink.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("Leggtillkundesvarbutton.png"):
        result = False
    wait(5)
    if not click_image("jaradiobutton.png"):
        result = False
    #wait(5)
    #test_pep_disponenter_flow(TIN)
    wait(5)
    if not click_image("nearfamily.png"):
        result = False

    wait(2)

    handlee = "scrollbar.png"

    if exists(handlee, 3):
        m = getLastMatch()

        # ✅ Scroll to middle instead of bottom
        safe_middle = Location(m.getX(), SCREEN.getBounds().height // 2)

        dragDrop(m, safe_middle)
        wait(1)

    else:
        log("Scroll bar not found", "FAIL")
        result = False

    wait(5)

    if not click_image("personpepsindropdownlist.png"):
        result = False
    wait(1)
    if not click_image("personpepelder.png"):
        result = False
    wait(5)
    if not click_image("personpepsindropdownlist.png"):
        result = False
    wait(1)
    if not click_image("personpeppartner.png"):
        result = False
    wait(5)
    if not click_image("personpepsindropdownlist.png"):
        result = False
    wait(1)
    if not click_image("personpepbam.png"):
        result = False
    wait(5)
    if not click_image("personpepsindropdownlist.png"):
        result = False
    wait(1)
    if not click_image("personpepsonpartner.png"):
        result = False
    wait(5)
    if not click_image("personpepsindropdownlist.png"):
        result = False
    wait(1)
    if not click_image("personpepmediator.png"):
        result = False

    first_name = generate_random_name()
    last_name = generate_random_name()

    type_text("pepfirstname.png", first_name)
    type_text("peplastname.png", last_name)
    type_text("pepsalesdate.png", "03.06.2024")
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False

    return result


def test_pep_known_associate_flow(TIN):
    log("TEST CASE: Mid Flow (scroll + next)", "INFO")

    result = True
    wait(5)

    if not click_image("kundecontrollink.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("NextStep.png"):
        result = False
    wait(0.5)
    if not click_image("Leggtillkundesvarbutton.png"):
        result = False
    wait(5)
    if not click_image("jaradiobutton.png"):
        result = False
    wait(5)
    if not click_image("pepknownassociateradiobutton.png"):
        result = False

    wait(2)
    handlee = "scrollbar.png"

    if exists(handlee, 3):
        m = getLastMatch()

        # ✅ Scroll to middle instead of bottom
        safe_middle = Location(m.getX(), SCREEN.getBounds().height // 2)

        dragDrop(m, safe_middle)
        wait(1)

    else:
        log("Scroll bar not found", "FAIL")
        result = False

    if not type_text("pepspesifierreligion.png", "Radhe"):
        result = False

    first_name = generate_random_name()
    last_name = generate_random_name()

    type_text("pepfirstname.png", first_name)
    type_text("peplastname.png", last_name)
    type_text("pepsalesdate.png", "03.06.2024")

    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False
    if not click_image("NextStep.png"):
        result = False

    return result


def test_pep_disponenter_flow(TIN):
    log("TEST CASE: Mid Flow (scroll + next)", "INFO")

    result = True

    wait(2)
    #handlee = "scrollbar.png"

    # if exists(handlee, 3):
    #     m = getLastMatch()
    #     safe_bottom = Location(m.getX(), SCREEN.getBounds().height - 100)
    #     dragDrop(m, safe_bottom)
    # else:
    #     log("Scroll bar not found", "FAIL")
    #     result = False

    if not type_text("pepdisponentorspecifiername.png", "Radhe"):
        result = False

    if not click_image("pepneiradiobutton1.png"):
        result = False

    return result


def test_document_flow(TIN):
    log("TEST CASE: Document Flow", "INFO")

    result = True

    if not click_image("jaradiobutton.png"):
        result = False

    if not click_image("InterLegtillbutton.png"):
        result = False

    if not double_click_image("interlandlists.png"):
        result = False

    if not click_image("Belarus.png"):
        result = False

    if not click_image("hvadropdownlist.png"):
        result = False

    if not double_click_image("hvadropdownlist.png"):
        result = False
    wait(0.5)
    if not click_image("overfare.png"):
        result = False

    if not type_text("type.png", "Radhe"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_dropdown_arrow1("statusofdoc.png"):
        result = False

    if not click_image("docofmot.png"):
        result = False

    if not click_dropdown_arrow1("datefordoc.png"):
        result = False

    if not click_image("ten.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("fullfiller.png"):
        result = False

    if not click_image("jabutton.png"):
        result = False

    return result


def test_international_transaction(TIN):
    log("TEST CASE: Document Flow", "INFO")

    result = True

    if not click_image("jaradiobutton.png"):
        result = False

    if not click_image("InterLegtillbutton.png"):
        result = False

    if not double_click_image("interlandlists.png"):
        result = False

    if not click_image("Belarus.png"):
        result = False

    if not click_image("hvadropdownlist.png"):
        result = False

    if not double_click_image("hvadropdownlist.png"):
        result = False
    wait(0.5)
    if not click_image("hvabetale.png"):
        result = False

    if not type_text("type.png", "Radhe"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False
    return result


def test_tax_reporting(TIN):
    log("TEST CASE: Tax Reporting Flow", "INFO")

    result = True

    if not click_image("landdropdown.png"):
        result = False
    if not click_image("landcountrybelarus.png"):
        result = False
    handlee = "scrollbar.png"

    if exists(handlee, 3):
        m = getLastMatch()

        # ✅ Scroll to middle instead of bottom
        safe_middle = Location(m.getX(), SCREEN.getBounds().height // 2)

        dragDrop(m, safe_middle)
        wait(1)

    else:
        log("Scroll bar not found", "FAIL")
        result = False

    if not click_dropdown("enginnerlearningmotatdropdown.png"):
        result = False

    if not click_image("engineeringdropdownvaluereceived.png"):
        result = False
    scroll("scrollbar.png", "middle")
    if not click_dropdown("engineeringdatedropdown.png"):
        result = False
    wait(0.5)

    if not click_image("engineeringdateten.png"):
        result = False

    if not click_image("NextStep.png"):
        result = False
    if not click_image_right("realbenificiaryja.png"):
        result = False
    if not click_image("fulfillerkundecontrol.png"):
        result = False
    log("=========== End Business Test Flow completed successfully ===========", "INFO")
    return result


def add_delete_verify_blocking_old(TIN):
    log("TEST CASE: Add Blockering Test cases", "INFO")

    result = True
    wait(5)
    click_image("searchfiled.png")
    if not type_text("searchfiled.png", "04901749227"):
        result = False
    if not click_image("searchclick.png"):
        result = False

        # ✅ Check if blocking exists (row present)
    if exists("blokkeringicon.png", 3):

        log("Blocking exists → deleting", "INFO")

        if not click_image("startsidetab.png"):
            result = False

        if not click_image("blokkeringlink.png"):
            result = False

        # ✅ Click Delete button
        if not click_image("delete_button.png"):
            log("Delete button not found", "FAIL")
            return False

    wait(0.5)
    # if not click_image("kundetab.png"):
    #     result = False
    #blokkeringicon
    wait(0.5)
    if not click_image("legitilblokkering.png"):
        result = False
    if not click_image("blokkeringkodedropdown.png"):
        result = False
    wait(0.5)
    if not click_image("blokeringkodeutenlanddeposit.png"):
        result = False
    wait(0.5)
    # if not type_text("blokkeringcomment.png", "ok"):
    #     result = False
    if not click_image("save_button.png"):
        result = False
        # ✅ Verify Country (Norge)
    if exists("blokkeringicon.png", 5):
        log("blokkering icon verified ", "PASS")
    else:
        log("blokkering icon FAILED", "FAIL")
        result = False
    return result


def add_delete_verify_blocking(TIN):
    App.focus("Zenit")
    wait(1)
    log("TEST CASE: Blocking Full Flow", "INFO")
    result = True
    wait(3)
    # ✅ SEARCH
    if not click_image("searchfiled.png"):
        result = False

    if not type_text("searchfiled.png", "DN120315125100001B"):
        result = False

    if not click_image("searchclick.png"):
        result = False

    wait(3)

    # ✅ CHECK BLOCKING
    if exists("blokkeringicon.png", 3):

        log("Blocking exists → deleting", "INFO")
        if not click_image("startsidetab.png"):
            result = False
        wait(2)
        if not click_image("blokkeringlink.png"):
            result = False

        wait(2)

        # if not click_image("blocking_row.png"):
        #     result = False

        delete_bloker()

        # if exists("yes_button.png", 2):
        #         #     click_image("yes_button.png")

        wait(2)

        # ✅ VERIFY DELETE
        if not exists("blocking_row.png", 3):
            log("Blocking deleted", "PASS")
        else:
            log("Delete failed", "FAIL")
            result = False

    else:
        log("No blocking exists", "INFO")

        # ✅ Open blocking screen if not already open
        if not click_image("blokkeringlink.png"):
            result = False

        wait(2)

    # ✅ ✅ ✅ IMPORTANT PART — CALL LOOP METHOD HERE ✅✅✅
    if not process_all_blocking_values():
        result = False

    return result
def delete_address():

    result = True

    if not click_image("addresserlink.png"):
        return False

    wait(2)

    # Delete using whichever button is enabled
    if exists("address_slett.png", 2):

        log("Using Slett button", "INFO")

        if not click_image("address_slett.png"):
            log("Failed to click Slett", "FAIL")
            return False

    elif exists("delete_address.png", 2):

        log("Using Delete button", "INFO")

        if not click_image("delete_address.png"):
            log("Failed to click Delete", "FAIL")
            return False

    else:

        log("No delete option available", "FAIL")
        return False

    wait(1)

    # Save once
    if not click_image("save_button.png"):
        log("Failed to save delete", "FAIL")
        return False

    wait(2)

    # Handle popup if it appears
    if exists("ok.png", 2):

        log("Delete popup appeared", "INFO")

        take_screenshot("delete_popup")

        if not click_image_right("ok.png"):
            log("Failed to click OK popup", "FAIL")
            result = False

        wait(1)



    log("Delete address completed", "PASS")

    return result
def delete_address_old():
    result = True
    if not click_image("addresserlink.png"):
        result = False
    wait(2)
    # ✅ Click Delete
    if not click_image("delete_address.png"):
        log("Delete button click failed", "FAIL")

    if exists("address_slett.png", 2):
        if not click_image("address_slett.png"):
            log("Failed to click slett delete", "FAIL")

    wait(1)

    # ✅ Click Save (if required in your UI)
    if not click_image("save_button.png"):
        log("Save after delete failed", "FAIL")
        result = False

    wait(2)

    # ✅ Handle error popup
    if exists("ok.png", 2):

        log("Error popup during delete", "FAIL")

        take_screenshot("delete_error")

        if not click_image_right("ok.png"):
            log("Failed to click OK popup", "FAIL")

        wait(1)

        return False  # ❗ delete failed

    # ✅ VERIFY DELETE (IMPORTANT ✅)
    if not exists("blocking_row_generic.png", 3):
        log("Address deleted successfully", "PASS")
    else:
        log("Address still present after delete", "FAIL")

        take_screenshot("delete_failed")
        result = False

    return result

def delete_bloker():
    result = True

    # ✅ Click Delete
    if not click_image("delete_blokkering.png"):
        log("Delete button click failed", "FAIL")

    if exists("slett.png", 2):
        if not click_image("slett.png"):
            log("Failed to click slett delete", "FAIL")

    wait(1)

    # ✅ Click Save (if required in your UI)
    if not click_image("save_button.png"):
        log("Save after delete failed", "FAIL")
        result = False

    wait(2)

    # ✅ Handle error popup
    if exists("ok.png", 2):

        log("Error popup during delete", "FAIL")

        take_screenshot("delete_error")

        if not click_image_right("ok.png"):
            log("Failed to click OK popup", "FAIL")

        wait(1)

        return False  # ❗ delete failed

    # ✅ VERIFY DELETE (IMPORTANT ✅)
    if not exists("blocking_row_generic.png", 3):
        log("Blocking deleted successfully", "PASS")
    else:
        log("Blocking still present after delete", "FAIL")

        take_screenshot("delete_failed")
        result = False

    return result


def process_all_blocking_values():
    BLOCKING_VALUES = [
        "blokkeringkmangler.png",
        "blokkeringkutenlandisponent.png",
        "blokeringkodeutenlanddeposit.png",
        "blokkeringkblokidentity.png"
    ]

    result = True

    for val in BLOCKING_VALUES:

        log("Processing Blocking Value: " + val, "INFO")
        # refresh_and_confirm()
        wait(2)
        # ✅ Click Legg til
        if not click_image("legitilblokkering.png"):
            result = False
            continue

        wait(1)

        # ✅ Expand dropdown
        if not expand_dropdown("blokkeringkodedropdown.png"):
            result = False
            continue

        wait(1)

        # ✅ Select value
        if not click_image(val):
            log("Dropdown selection failed: " + val, "FAIL")
            result = False
            continue

        wait(1)
        if not type_text("blokkeringcomment.png", "ok"):
            result = False
        # ✅ Save
        if not click_image("save_button.png"):
            result = False
            continue

        wait(2)
        # ✅ HANDLE ERROR POPUP
        if exists("ok.png", 2):
            log("Error popup for value: " + val, "FAIL")

            take_screenshot("error_" + val)

            click_image_right("ok.png")
            wait(1)

            # ✅ Skip to next value
            #continue
        wait(2)
        if not click_image("kundetab.png"):
            result = False
        wait(2)
        if exists("blokkeringicon.png", 3):

            log("Blocking exists → deleting", "INFO")
            if not click_image("startsidetab.png"):
                result = False
            wait(2)
            if not click_image("blokkeringlink.png"):
                result = False

            wait(2)
        delete_bloker()

        # ✅ VERIFY SUCCESS
        if exists("blokkeringicon.png", 2):
            log("Blocking saved successfully: " + val, "PASS")
        else:
            log("Blocking save failed: " + val, "FAIL")
            result = False

        wait(1)

    return result


def click_refresh(img):
    m = exists(Pattern("img.png").similar(0.6), 10)

    if not m:
        log("Refresh button not found", "FAIL")
        return False

    pt = m.getTarget()

    hover(pt)
    wait(0.5)

    # ✅ Use normal click (NOT mouseDown)
    click(pt)

    wait(1)

    log("Refresh clicked", "PASS")
    return True


ADDRESS_TESTS = [

    {
        "name": "TC01_Postnummer_Blank",
        "group": "Hovedadresse.png",
        "type": "Postadresse.png",
        "postnummer": "",
        "expect_error": True
    },

    {
        "name": "TC02_Adressegruppe_Blank",
        "group": None,
        "type": "Postadresse.png",
        "postnummer": "0105",
        "expect_error": True
    },

    {
        "name": "TC03_Type_Blank",
        "group": "Hovedadresse.png",
        "type": None,
        "postnummer": "0105",
        "expect_error": True
    },

    {
        "name": "TC26_Add_New_Address",
        "group": "Hovedadresse.png",
        "type": "Postadresse.png",
        "postnummer": "0105",
        "expect_error": False
    }
]


def execute_address_test(tc):
    log("===== " + tc["name"] + " START =====", "INFO")

    result = True
    wait(3)
    if not click_image("addresserlink.png"):
        return False
    if not click_image("newaddress.png"):
         return False
    if tc.get("group"):

        # if not click_image("newaddress.png"):
        #     return False
        if tc["group"]:
        # wait(2)
        # if not expand_dropdown("adressegruppe.png"):
        #     return False
            wait(2)

            if not select_address_group_by_index(tc["group"]):
                return False
        # if not select_address_group_by_index(tc["group"]):
        #     return False

        if tc["type"]:

        # if not click_dropdown("type_dropdown.png"):
        #     return False
            wait(1)
            if not select_type_by_index(tc["type"]):
                return False

    # value = str(int(time.time() * 1000))

    # type_text_right("postaddress.png", value)

    if tc.get("postnummer"):
        if not type_text("postnummer.png", tc["postnummer"]):
            return False
    if tc.get("addresslandNo"):
        if not clear_type_text("addresslandNo.png", tc["addresslandNo"]):
            return False
    if tc.get("gyldtilldate"):
        if not clear_type_text_right("gyldtilldate.png", tc["gyldtilldate"]):
            return False
    if tc.get("postaladdressline1"):
        if not type_text_right("postaladdressline1.png", tc["postaladdressline1"]):
            return False
    if tc.get("fell_addresse"):
        if not click_image("fell_addresse.png"):
            return False
    if tc.get("telefax"):
        if not type_text_right("telefax.png", tc["telefax"]):
            return False
    if tc.get("addressvan"):
        if not type_text_right("addressvan.png", tc["addressvan"]):
            return False
    if tc.get("addresspostnummer"):

        if exists("addresspostnummer.png", 3):
            log(
                "Postnummer field displayed. Expected value = " +
                str(tc["addresspostnummer"]),
                "PASS"
            )
        else:
            log("Postnummer field not displayed", "FAIL")
            return False

    if tc.get("addressarchive"):
        if not click_image("addressarchive.png"):
            return False
    # handle_land_field()

    #click_image_right("save_button.png")
    if not click_image_right("save_button.png"):
        result = False
    wait(2)

    # Validation expected
    if tc["expect_error"]:

        if exists("ok.png", 3):

            log(tc["name"] + " Validation Displayed", "PASS")

            take_screenshot(tc["name"])

            click_image_right("ok.png")

        else:

            log(tc["name"] + " Validation Missing", "FAIL")
            result = False

    else:

        group_ok = exists(tc["group"], 5)
        type_ok = exists(tc["type"], 5)

        if not (group_ok and type_ok):

            log(tc["name"] + " Verification Failed", "FAIL")
            result = False

        else:

            log(tc["name"] + " Verification Success", "PASS")
    if tc.get("addressarchive"):
        if not click_image("historytab.png"):
            return False

    log("===== " + tc["name"] + " END =====", "INFO")

    return result


def run_address_tests(TIN):
    result = True

    if not click_image("addresserlink.png"):
        return False

    wait(2)

    for tc in ADDRESS_TESTS:

        try:

            tc_result = execute_address_test(tc)

            if tc_result:
                log(tc["name"] + " => PASS", "PASS")
            else:
                log(tc["name"] + " => FAIL", "FAIL")
                result = False

        except Exception as e:

            log(tc["name"] + " Exception: " + str(e), "FAIL")
            result = False

        prepare_next_test()

    return result


def refresh_and_confirm():
    result = True

    # ✅ Click Refresh button

    if not click("refresh.png"):
        log("Failed to click refesh button", "FAIL")
        result = False

    wait(1)

    # ✅ Handle popup
    if exists("okrefresh.png", 1):

        log("Refresh popup detected", "INFO")

        # ✅ Take screenshot (optional)
        take_screenshot("refresh_popup")

        # ✅ Click OK
        if not click_image_right("okrefresh.png"):
            log("Failed to click OK button", "FAIL")
            result = False
        else:
            log("Clicked OK on refresh popup", "PASS")

        wait(2)

    else:
        log("No popup appeared", "INFO")

    return result


def test_contact_person(TIN):
    log("TEST CASE: Contact Person", "INFO")

    result = True

    if not click_image("leggtillkotakperson.png"):
        result = False

    if not click_image("eiercheckbox.png"):
        result = False
    if not type_text("personinfofodslsner.png", "985695415"):
        result = False

    handlee = "scrollbar.png"

    if exists(handlee, 3):
        m = getLastMatch()

        # ✅ Scroll to middle instead of bottom
        safe_middle = Location(m.getX(), SCREEN.getBounds().height // 2)

        dragDrop(m, safe_middle)
        wait(1)

    else:
        log("Scroll bar not found", "FAIL")
        result = False

    if not clear_type_text_right("elerandalpercentage.png", "10"):
        result = False

    if not click_image("NextStep.png"):
        result = False

    return result


# ============================
#        TEST RUNNER
# ============================

def run_tests(TIN):
    log("=========== START TEST FLOW ===========", "INFO")

    #result1 = test_search_and_kunde(TIN)
    #result2 = test_mid_flow(TIN)
    #result3 = test_non_pep_flow(TIN)
    #result4 = test_document_flow(TIN)
    #result5 = test_pep_flow_veg_selv(TIN)
    #result6=test_pep_flow_near_family(TIN)
    #result6 = test_pep_known_associate_flow(TIN)
    #result7=test_onboard_individual_person_customer(TIN)
    #result8=test_onboard_business_nearing_customer(TIN)
    #result9=run_address_flow(TIN)
    #result10=test_kundecontrol_pep_flow(TIN)
    #result11=add_delete_verify_blocking(TIN)
    #result12=test_kundecontrol_bm_non_pep(TIN)
    log("=========== TEST SUMMARY ===========", "INFO")
    result1 = test_search_cust(TIN)
    tc1 = {"name": "TC01_Postnummer_Blank", "group": 0, "type": 3, "postnummer": "", "expect_error": True}
    #execute_address_test(tc)
    tc6 = {"name": "TC06_Invalid post number format", "group": 0, "type": 3, "postnummer": "ebac456",
           "expect_error": True}
    tc7 = {"name": "TC07_Invalid land kode", "group": 0, "type": 3, "postnummer": "0123",
           "addresslandNo": "XX", "expect_error": True}
    tc8 = {"name": "TC08_Duplicate address", "group": 0, "type": 3, "postnummer": "0123",
            "expect_error": True}
    # Data for tc9
    tc11 = {"name": "TC11_Past Gyld Date", "group": 0, "type": 3, "postnummer": "0123",
           "gyldtilldate":"02.03.2024","expect_error": True}
    tc12 = {"name": "TC12_Today's Date in Gyld fra", "group": 0, "type": 3, "postnummer": "0123",
             "expect_error": True}
    tc14 = {"name": "TC14_Gyld Date non numeric", "group": 0, "type": 3, "postnummer": "0123",
            "gyldtilldate": "xyzabc", "expect_error": True}
    tc15 = {"name": "TC15_Gyld Date max date", "group": 0, "type": 3, "postnummer": "0123",
            "gyldtilldate": "31.12.9998", "expect_error": True}
    tc16 = {"name": "TC16_Special character for postnummer", "group": 0, "type": 3, "postnummer": "01@5",
             "expect_error": True}
    tc17 = {"name": "TC17_Exceeds maximum length for postnummer", "group": 0, "type": 3, "postnummer": "45748565865456562347",
            "expect_error": True}
    tc18 = {"name": "TC18_blank Landkode value", "group": 0, "type": 3,
            "postnummer": "0123","addresslandNo": " ","expect_error": True}
    tc19 = {"name": "TC19_Blank laddressline1", "group": 0, "type": 3,
            "postnummer": "0123","postaladdressline1":"    ", "expect_error": True}
    tc20 = {"name": "TC19_Blank laddressline1", "group": 0, "type": 3,
            "postnummer": "0123", "postaladdressline1": "3225252352352353253r53r324324324324e3243qwrsafsfweqfweqfcvvfdgrefgreqfsfdsf", "expect_error": True}
    tc21 = {"name": "TC21_change addresser group", "group": -3, "type": 0, "postnummer": "0123",
            "expect_error": True}
    tc22 = {"name": "TC22_Duplicate BANKAXEPT_FAKTURERING addresser", "group": -3, "type": 0, "postnummer": "0123",
            "expect_error": True}

    #delete_address_old() #tc 23
    tc24 = {"name": "TC24_slect fell addres", "group": 2, "type": 0, "postnummer": "0123",
            "fell_addresse":"2","expect_error": True}
    tc26 = {"name": "TC26_New address", "group": 1, "type": 0, "postnummer": "0123",
            "expect_error": True}
    tc30 = {"name": "TC30_Engasmjement opp gave", "group": -2, "type": 0, "postnummer": "0123",
            "expect_error": True}
    tc31 = {"name": "TC31_Forgein country", "group": -2, "type": 0, "postnummer": "756",
             "telefax":"wet ry q34yg53","addressvan":"12345vfwwww","addresslandNo": "SE","expect_error": True}
    tc32 = {"name": "TC32_kontak address", "group": 4, "type": 0,
            "addresslandNo": "AL", "expect_error": True}
    tc33 = {"name": "TC33_Update address field",
            "addresslandNo": "AL", "expect_error": True}
    tc34 = {"name": "TC34_Addressvan field", "group": 2, "type": 1, "postnummer": "0123",
            "telefax":"wet ry q34yg53","addressvan":"12345vfwwww","expect_error": True}
    tc36 = {"name": "TC36_Forgein country", "group": 3, "type": 0, "postnummer": "1011",
            "telefax": "Jai", "addressvan": "3455", "addresslandNo": "DE", "expect_error": True}
    tc37 = {"name": "TC37_Norwegian cust Postnum auto populate"  , "group": 2, "type": 0, "postnummer": "0150",
            "expect_error": True}
    tc38 = {"name": "TC38_Lankode SE", "group": 2, "type": 0, "postnummer": "3452",
            "addresslandNo": "SE","expect_error": True}
    tc39 = {"name": "TC39_Update landkode to NO",
            "addresslandNo": "NO", "expect_error": True}
    tc40 = {"name": "TC40_Non Norwegian cust city field manuall entered"  , "group": 2, "type": 0, "postnummer": "75001",
            "addresslandNo": "FR", "expect_error": True}
    tc44 = {"name": "TC44_white space in addressline1", "group": 2, "type": 0, "postnummer": "0105",
            "postaladdressline1": "          ", "expect_error": True}
    tc73 = {"name": "TC73-ZG-042_Terminate active address_valid address to today", "group": 0, "type": 0, "postnummer": "0123",
            "addressarchive": 1, "expect_error": True}
    tc79 = {"name": "TC79_verify address postnummer",
            "addresspostnummer": "4349", "expect_error": True}

    execute_address_test(tc36)
    log("Search + Kunde => " + ("PASS" if result1 else "FAIL"), "PASS" if result1 else "FAIL")
    log("Mid Flow => " + ("PASS" if result2 else "FAIL"), "PASS" if result2 else "FAIL")
    log("PEP Flow => " + ("PASS" if result3 else "FAIL"), "PASS" if result3 else "FAIL")
    log("Document Flow => " + ("PASS" if result4 else "FAIL"), "PASS" if result4 else "FAIL")
    log("PEP Veg Flow => " + ("PASS" if result4 else "FAIL"), "PASS" if result4 else "FAIL")
