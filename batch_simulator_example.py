"""EXAMPLE replacement for the Moodle batch_simulator.py (which was not supplied).

Run inside a GitHub Codespace after your source CSV and scripts have been committed:
python batch_simulator_example.py --batches 3 --interval 15

Each push triggers the Actions workflow. Optional --no-push tests locally.
"""
import argparse
import subprocess
import time
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "imdb_top_1000.csv"
DEST = BASE / "data" / "batches"


def git(*args):
    subprocess.run(["git", *args], cwd=BASE, check=True)


def run_simulator(batches, interval, batch_size, push):
    if not SOURCE.exists():
        raise FileNotFoundError("Put imdb_top_1000.csv in the project first.")
    data = pd.read_csv(SOURCE)
    if data.empty:
        raise ValueError("Source CSV is empty")
    DEST.mkdir(parents=True, exist_ok=True)
    previous = sorted(DEST.glob("batch_*.csv"))
    next_index = max((int(p.stem.split("_")[-1]) for p in previous), default=0) + 1
    for b in range(batches):
        number = next_index + b
        start = ((number - 1) * batch_size) % len(data)
        indices = [(start + j) % len(data) for j in range(min(batch_size, len(data)))]
        part = data.iloc[indices].copy()
        filename = DEST / f"batch_{number:03}.csv"
        part.to_csv(filename, index=False)
        print(f"Produced {filename.relative_to(BASE)}: {len(part)} movies", flush=True)
        if push:
            git("add", str(filename.relative_to(BASE)))
            git("commit", "-m", f"New IMDb batch {number:03}")
            git("push", "origin", "main")
            print("Pushed to GitHub; new Actions workflow should start.", flush=True)
        if b < batches - 1:
            time.sleep(interval)
    print("Simulation finished.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--batches", type=int, default=3)
    p.add_argument("--interval", type=int, default=15, help="Seconds between batches")
    p.add_argument("--batch-size", type=int, default=80)
    p.add_argument("--no-push", action="store_true", help="Create local batches only")
    options = p.parse_args()
    run_simulator(options.batches, options.interval, options.batch_size, not options.no_push)
