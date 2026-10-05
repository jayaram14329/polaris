import time
import urllib.request
import sys
import datetime

DEFAULT_URL = "https://polaris-backend.onrender.com/health"

def ping(url: str):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Polaris-KeepAlive/1.0"})
        with urllib.request.urlopen(req, timeout=45) as res:
            return res.getcode()
    except Exception as e:
        return f"Waking up or offline ({e})"

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] POLARIS 24/7 Keep-Alive Daemon started for {target}")
    while True:
        status = ping(target)
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Heartbeat ping -> Status: {status}")
        # Sleep for 10 minutes (600 seconds) - well below Render's 15-minute inactivity timeout
        time.sleep(600)
