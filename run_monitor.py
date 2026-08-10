import time
import subprocess
import sys

while True:

    print("=== ROZPOCZYNAM SPRAWDZENIE ===")

    subprocess.run(
        [sys.executable, "monitor.py"]
    )

    print("=== SPRAWDZENIE ZAKOŃCZONE ===")
    print("Następne sprawdzenie za 30 minut.")

    time.sleep(1800)