"""Run structured Agent 4 handoffs with SikuliX and return JSON results.

Supported actions in each test's ``zenitSteps`` list:
click {"image": "..."}, type {"text": "..."}, verify_text {"text": "..."},
wait {"seconds": 1}, screenshot {"name": "..."}, drag {"image": "...", "dx": 0, "dy": 200},
and popup {"message": "..."}.
"""

import argparse
import json
import os
import time
from datetime import datetime

import jpype
import jpype.imports


ROOT = os.path.dirname(os.path.abspath(__file__))
JAR = os.path.join(ROOT, "libs", "sikulixapi-2.0.5-windows.jar")
IMAGE_PATH = os.path.join(ROOT, "Images")


def _start_sikuli():
    if not os.path.isfile(JAR):
        raise RuntimeError(f"Sikuli JAR not found: {JAR}")
    if not jpype.isJVMStarted():
        jpype.startJVM("-ea", f"-Djava.class.path={JAR}")
    from org.sikuli.script import ImagePath, Pattern, Screen, Settings
    Settings.AutoWaitTimeout = 10
    Settings.MinSimilarity = 0.50
    ImagePath.add(IMAGE_PATH)
    return Screen(), Pattern


def _action(screen, Pattern, action, screenshots):
    kind = str(action.get("action") or action.get("type") or "").lower()
    image = action.get("image")
    if kind == "click":
        screen.click(screen.wait(Pattern(os.path.join(IMAGE_PATH, image)).similar(float(action.get("similarity", 0.5))), 10))
    elif kind == "type":
        if image:
            screen.click(screen.wait(Pattern(os.path.join(IMAGE_PATH, image)).similar(0.5), 10))
        screen.type(str(action.get("text", "")))
    elif kind == "verify_text":
        expected = str(action.get("text", ""))
        if expected.lower() not in screen.text().lower():
            raise AssertionError(f"OCR text not found: {expected}")
    elif kind == "wait":
        time.sleep(float(action.get("seconds", 1)))
    elif kind == "screenshot":
        name = str(action.get("name", "step"))
        directory = os.path.join(ROOT, "reports", "screenshots")
        os.makedirs(directory, exist_ok=True)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
        screen.capture().save(directory, filename)
        screenshots.append(os.path.join(directory, filename))
    elif kind == "drag":
        target = screen.wait(Pattern(os.path.join(IMAGE_PATH, image)).similar(0.5), 10)
        screen.dragDrop(target, target.offset(int(action.get("dx", 0)), int(action.get("dy", 0))))
    elif kind == "popup":
        screen.popup(str(action.get("message", "Agent 4 completed")))
    else:
        raise ValueError(f"Unsupported Zenit action: {kind or '<missing action>'}")


def run(handoff):
    screen, Pattern = _start_sikuli()
    results = []
    report_steps = []
    started = datetime.now()
    for test in handoff.get("tests", []):
        name = test.get("name") or test.get("id") or "Unnamed test"
        test_started = datetime.now()
        screenshots = []
        actions = test.get("zenitSteps") or []
        status = "passed"
        reason = None
        if not actions:
            status = "blocked"
            reason = "No structured zenitSteps were supplied for this test"
        else:
            for action in actions:
                try:
                    _action(screen, Pattern, action, screenshots)
                    report_steps.append({"time": str(datetime.now()), "step": f"{name}: {action.get('action') or action.get('type')}", "status": "PASS"})
                except Exception as exc:
                    status = "failed"
                    reason = str(exc)[:500]
                    report_steps.append({"time": str(datetime.now()), "step": name, "status": "FAIL", "error": reason})
                    break
        finished = datetime.now()
        duration = int((finished - test_started).total_seconds() * 1000)
        actual = test.get("expectedStatus", 200) if status == "passed" else 0
        results.append({
            "id": test.get("id") or name,
            "testName": name,
            "fileName": f"{name.lower().replace(' ', '-')}.zenit.json",
            "caseId": test.get("id") or name,
            "endpoint": test.get("endpoint", "/api/unknown"),
            "polarity": "POS",
            "priority": "P2",
            "userType": "DOMAIN",
            "status": status,
            "expectedStatus": test.get("expectedStatus", 200),
            "actualStatus": actual,
            "durationMs": duration,
            "startedAt": test_started.isoformat(),
            "finishedAt": finished.isoformat(),
            "evidence": ["Zenit/SikuliX runtime completed" if status == "passed" else reason],
            "logLines": [f"{name}: {status}"],
            "failureReason": reason,
            "screenshots": screenshots,
        })

    finished = datetime.now()
    passed = sum(item["status"] == "passed" for item in results)
    failed = sum(item["status"] == "failed" for item in results)
    blocked = sum(item["status"] == "blocked" for item in results)
    report_dir = os.path.join(ROOT, "reports")
    os.makedirs(report_dir, exist_ok=True)
    with open(os.path.join(report_dir, "report.json"), "w", encoding="utf-8") as handle:
        json.dump(report_steps, handle, indent=2)
    return {
        "runId": handoff.get("runId"),
        "jiraKey": handoff.get("jiraKey", ""),
        "service": handoff.get("service", ""),
        "suite": handoff.get("suite", ""),
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "blocked": blocked,
        "passRate": round(passed / len(results) * 100, 1) if results else 0,
        "totalDurationMs": int((finished - started).total_seconds() * 1000),
        "startedAt": started.isoformat(),
        "finishedAt": finished.isoformat(),
        "environment": "SIT",
        "mode": "zenit",
        "scripts": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", required=True)
    parser.add_argument("--result", required=True)
    args = parser.parse_args()
    try:
        with open(args.handoff, "r", encoding="utf-8") as handle:
            result = run(json.load(handle))
    except Exception as exc:
        result = {"status": "error", "error": str(exc), "total": 0, "passed": 0, "failed": 0, "blocked": 1, "scripts": []}
    with open(args.result, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    raise SystemExit(0 if result.get("status") != "error" else 1)


if __name__ == "__main__":
    main()