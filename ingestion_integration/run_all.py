# Execution Instructions:
# On PowerShell, run:
#     python .\ingestion_integration\run_all.py --daemon to run periodically
#     python .\ingestion_integration\run_all.py to run once

# ingestion_integration/run_all.py
import subprocess
import sys
import os
import time
import random
import traceback
from datetime import datetime, timedelta

PKG = "ingestion_integration"
PY = sys.executable
JOBS = [
    "jobs.load_experiences",
    "jobs.load_availability",
    "jobs.load_bookings",
    "jobs.load_feature_usage_monthly",
    "jobs.load_messaging_usage",
    "jobs.load_experience_skills"
]

def _env_bool(name, default=False):
    v = os.getenv(name, "").strip().lower()
    if v in ("1", "true", "yes", "y", "on"):
        return True
    if v in ("0", "false", "no", "n", "off"):
        return False
    return default

def run_job(mod, retries=3, backoff_seconds=5):
    """Ejecuta un job con reintentos (backoff exponencial simple)."""
    attempt = 0
    while True:
        attempt += 1
        print(f"→ Running {mod} (attempt {attempt}/{retries})")
        rc = subprocess.call([PY, "-m", f"{PKG}.{mod}"])
        if rc == 0:
            print(f"✓ {mod} OK")
            return
        print(f"[WARN] {mod} failed with code {rc}")
        if attempt >= retries:
            print(f"[ERROR] {mod} exhausted retries. Continuing with next job.")
            return
        sleep_s = backoff_seconds * (2 ** (attempt - 1))
        print(f"[INFO] Retrying {mod} in {sleep_s} seconds…")
        time.sleep(sleep_s)

def run_all_once():
    """Ejecuta la secuencia completa una vez."""
    for mod in JOBS:
        try:
            run_job(mod, retries=3, backoff_seconds=5)
        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user. Exiting run_all_once.")
            raise
        except Exception:
            print(f"[ERROR] Unhandled exception in {mod}:")
            traceback.print_exc()

    print("✓ Ingestion-Integration complete")

def _next_run_at(hour=2, minute=0):
    """Calcula el datetime local de la próxima corrida diaria a HH:MM."""
    now = datetime.now()
    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= now:
        candidate = candidate + timedelta(days=1)
    return candidate

def _sleep_until(ts: datetime, jitter_seconds=0):
    """Duerme hasta 'ts' (datetime local). Admite jitter aleatorio opcional."""
    if jitter_seconds and jitter_seconds > 0:
        j = random.randint(0, int(jitter_seconds))
        ts = ts + timedelta(seconds=j)
        print(f"[INFO] Added jitter of {j} seconds to next run.")

    while True:
        now = datetime.now()
        delta = (ts - now).total_seconds()
        if delta <= 0:
            break
        chunk = min(60, max(1, int(delta)))
        time.sleep(chunk)

def main():

    daemon = ("--daemon" in sys.argv) or _env_bool("INGESTION_DAEMON", False)
    daily_hour = int(os.getenv("INGESTION_DAILY_HOUR", "2"))        # 02:00
    daily_minute = int(os.getenv("INGESTION_DAILY_MINUTE", "0"))
    jitter_seconds = int(os.getenv("INGESTION_JITTER_SECONDS", "0")) # ej. 120 para ±2min

    if not daemon:
        run_all_once()
        return

    print(f"[INFO] Daemon mode ON. Daily schedule at {daily_hour:02d}:{daily_minute:02d} (local).")
    print("[INFO] Press Ctrl+C to stop.")

    try:
        run_all_once()
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user before scheduling next run.")
        return

    try:
        next_run = _next_run_at(daily_hour, daily_minute)
        while True:
            print(f"[INFO] Next run scheduled at {next_run.isoformat(' ', 'seconds')}")
            _sleep_until(next_run, jitter_seconds=jitter_seconds)
            run_all_once()
            next_run = next_run + timedelta(days=1)
    except KeyboardInterrupt:
        print("\n[INFO] Daemon stopped by user. Bye!")

if __name__ == "__main__":
    main()
