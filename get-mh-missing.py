#!/usr/bin/env python3
# get-mh-missing.py — fetches the exact 23 chapters their index hid.
# Put this file in the bible-data folder (next to the mh-raw folder) and run:
#   python3 get-mh-missing.py

import json, os, subprocess, time, urllib.request

BASE = "https://bible.helloao.org/api/c/matthew-henry"
HDRS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) bible.software",
        "Accept": "application/json", "Connection": "close"}

TARGETS = [("2SA",23),("2SA",24),
           ("JON",2),("JON",3),("JON",4),
           ("MAT",19),("MAT",20),("MAT",21),("MAT",22),("MAT",23),
           ("MAT",24),("MAT",25),("MAT",26),("MAT",27),("MAT",28),
           ("JOS",22),("JOS",23),("NUM",32),("NUM",33),("NUM",35),
           ("NUM",26),("NUM",34),("JOS",21)]

def get(url):
    for a in range(8):
        try:
            req = urllib.request.Request(url, headers=HDRS)
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read().decode("utf-8")
        except Exception:
            time.sleep(1.0 * (a + 1))
    try:
        r = subprocess.run(["curl","-sf","--retry","4","--retry-delay","2",
                            "-A",HDRS["User-Agent"],url],
                           capture_output=True, timeout=90)
        if r.returncode == 0 and r.stdout:
            return r.stdout.decode("utf-8")
    except Exception:
        pass
    return None

ok, bad = 0, []
for bk, c in TARGETS:
    os.makedirs(f"mh-raw/{bk}", exist_ok=True)
    t = get(f"{BASE}/{bk}/{c}.json")
    good = False
    if t:
        try:
            d = json.loads(t)
            if d.get("chapter", {}).get("content"):
                open(f"mh-raw/{bk}/{c}.json","w",encoding="utf-8").write(t)
                good = True
        except Exception:
            pass
    if good: ok += 1; print(f"got {bk} {c}")
    else: bad.append(f"{bk}/{c}"); print(f"MISS {bk} {c}")
    time.sleep(0.3)

print(f"\n{ok}/{len(TARGETS)} fetched.")
if bad: print("Still empty at the source (fine, will note):", ", ".join(bad))
else: print("ALL 23 CAPTURED.")
print("Now: GitHub Desktop -> Commit -> Push origin -> tell Claude 'check'.")
