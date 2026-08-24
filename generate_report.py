import json
import os
from datetime import datetime

JSON_FILES = [
    "reports/report.json",
    "reports/sikuli_report.json"
]

REPORT_HTML = "reports/report.html"


def load_all_steps():
    all_steps = []

    for file in JSON_FILES:
        if os.path.exists(file):
            try:
                with open(file) as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_steps.extend(data)
            except:
                pass

    return all_steps


def generate_html():

    steps = load_all_steps()

    if not steps:
        print("No report found")
        return

    # ✅ Sort steps
    steps = sorted(steps, key=lambda x: x.get("time", ""))

    total = len(steps)
    passed = sum(1 for s in steps if s.get("status") == "PASS")
    failed = sum(1 for s in steps if s.get("status") == "FAIL")

    total_tests = passed + failed

    pass_pct = (passed / total_tests) * 100 if total_tests else 0

    # ✅ Execution time
    try:
        start_time = datetime.strptime(steps[0].get("time"), "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(steps[-1].get("time"), "%Y-%m-%d %H:%M:%S.%f")

        duration = end_time - start_time

        seconds = int(duration.total_seconds())
        minutes = seconds // 60
        secs = seconds % 60

        execution_time = "{} min {} sec".format(minutes, secs)
    except:
        execution_time = "N/A"

    # ✅ ✅ FIXED HTML (no &lt; &gt;)
    html = f"""<html>
<head>
<title>Automation Report</title>

<style>
body {{
    font-family: Arial;
    margin: 20px;
}}

h2 {{
    background: #222;
    color: white;
    padding: 10px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
}}

th {{
    background-color: #f2f2f2;
}}

.PASS {{ color: green; font-weight: bold; }}
.FAIL {{ color: red; font-weight: bold; }}

img {{
    max-width: 120px;
    max-height: 80px;
    border-radius: 4px;
    cursor: pointer;
    transition: transform 0.2s;
}}

img:hover {{
    transform: scale(2);
}}

.dashboard {{
    padding: 10px;
    border: 1px solid #ddd;
    margin-bottom: 20px;
    background: #fafafa;
}}
</style>

</head>

<body>

<h2>Automation Dashboard</h2>

<div class="dashboard">
<p><b>Total Steps:</b> {total}</p>
<p><b>Total Test Steps:</b> {total_tests}</p>
<p><b>Passed:</b> {passed}</p>
<p><b>Failed:</b> {failed}</p>
<p><b>Pass %:</b> {pass_pct:.2f}%</p>
<p><b>Execution Time:</b> {execution_time}</p>
</div>

<h2>Execution Details</h2>

<table>
<tr>
<th>Time</th>
<th>Step</th>
<th>Status</th>
<th>Screenshot</th>
</tr>
"""

    for step in steps:
        img = step.get("screenshot")

        img_html = ""

        if img:
            img_html = '<img src="data:image/png;base64,{}" />'.format(img)

        html += f"""
<tr>
<td>{step.get("time")}</td>
<td>{step.get("step")}</td>
<td class="{step.get("status")}">{step.get("status")}</td>
<td>{img_html}</td>
</tr>
"""

    html += """
</table>

</body>
</html>
"""

    os.makedirs("reports", exist_ok=True)

    with open(REPORT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ HTML report generated:", REPORT_HTML)


if __name__ == "__main__":
    generate_html()