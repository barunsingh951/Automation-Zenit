# ============================
#        ENTRY SCRIPT
# ============================

import os
import sys

# ✅ Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(getBundlePath(), "..")))

# ✅ Import everything needed
from common import *
from all_tests import run_tests


# ============================
#        LOAD TIN
# ============================

PROJECT_ROOT = os.path.abspath(os.path.join(getBundlePath(), ".."))
TIN_FILE = os.path.join(PROJECT_ROOT, "current_tin.txt")

if not os.path.exists(TIN_FILE):
    popup("❌ current_tin.txt not found")
    sys.exit(1)

with open(TIN_FILE) as f:
    TIN = f.read().strip()

# ✅ Make TIN available globally
globals()["TIN"] = TIN


# ============================
#        MAIN EXECUTION
# ============================

log("Zenit automation started", "INFO")

run_tests(TIN)

popup("✅ All test cases executed")