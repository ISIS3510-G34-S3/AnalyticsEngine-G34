# ingestion_integration/run_all.py
import subprocess, sys, os

PKG = "ingestion_integration"
PY = sys.executable

def run(mod: str):
    print(f"→ Running {mod}")
    rc = subprocess.call([PY, "-m", f"{PKG}.{mod}"])
    if rc != 0:
        raise SystemExit(rc)

def main():
    # Core loaders
    run("jobs.load_experiences")
    run("jobs.load_availability")
    run("jobs.load_bookings")
    run("jobs.load_feature_usage_monthly")
    run("jobs.load_device_distribution_monthly")
    print("✓ Ingestion-Integration complete")

if __name__ == "__main__":
    main()
