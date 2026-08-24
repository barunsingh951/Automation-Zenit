import subprocess
import sys
import os
import json

def run_selenium():
    subprocess.call([sys.executable, "selenium_launcher.py"])

def run_sikuli():
    return subprocess.call([
        "java",
        "-jar",
        r"libs\sikulixide-2.0.5.jar",
        "-r",
        "zenit_actions.sikuli"
    ])

def generate_html():
    subprocess.call([sys.executable, "generate_report.py"])

def open_report():
    report_path = os.path.abspath("reports/report.html")
    if os.path.exists(report_path):
        os.startfile(report_path)
    else:
        print("❌ report.html not found")

def reset_report():
    os.makedirs("reports", exist_ok=True)

    with open("reports/report.json", "w") as f:
        json.dump([], f)

    with open("reports/sikuli_report.json", "w") as f:
        json.dump([], f)


# ✅ MAIN EXECUTION
if __name__ == "__main__":

    reset_report()

    try:
        #run_selenium()
        run_sikuli()   # ✅ will not crash now

    except Exception as e:
        print("❌ Controller error:", e)

    finally:
        print("📊 Generating HTML report...")
        generate_html()   # ✅ ALWAYS runs
        open_report()     # ✅ opens report automatically
