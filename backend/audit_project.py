import requests
import sys

BASE_URL = "http://127.0.0.1:5000"
USER = {"name": "Audit User", "email": "audit@example.com", "password": "password123"}

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def fail(msg):
    log(msg, "FAIL")
    # We won't exit, just note it.

def audit():
    print("====================================")
    print("      STARTING SYSTEM AUDIT         ")
    print("====================================")

    # 1. AUTH FLOW
    session = requests.Session()
    
    # Signup
    log("Testing Signup...")
    res = session.post(f"{BASE_URL}/auth/signup", json=USER)
    if res.status_code == 201:
        log("Signup success (201)", "PASS")
    elif res.status_code == 409:
        log("User already exists (409) - acceptable", "INFO")
    else:
        fail(f"Signup failed: {res.status_code} {res.text}")

    # Login
    log("Testing Login...")
    res = session.post(f"{BASE_URL}/auth/login", json={"email": USER["email"], "password": USER["password"]})
    if res.status_code == 200:
        data = res.json()
        token = data.get("access_token")
        if token:
            log("Login success & Token received", "PASS")
            session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            fail("Login response missing access_token")
    else:
        fail(f"Login failed: {res.status_code} {res.text}")
        return

    # 2. DASHBOARD SECURITY
    log("Testing Dashboard Security...")
    res = session.get(f"{BASE_URL}/video/dashboard")
    if res.status_code == 200:
        videos = res.json().get("videos", [])
        if len(videos) > 0:
            log(f"Fetched {len(videos)} videos", "PASS")
            # CRITICAL CHECK
            leaked = False
            for v in videos:
                if "youtube_id" in v:
                    leaked = True
            if leaked:
                fail("CRITICAL: youtube_id exposed in /dashboard response!")
            else:
                log("Video IDs hidden correctly", "PASS")
            
            video_id = videos[0]["_id"]
        else:
            fail("Dashboard returned 0 videos. Cannot proceed with video tests.")
            return
    else:
        fail(f"Dashboard failed: {res.status_code}")
        return

    # 3. STREAMING SECURITY
    log(f"Testing Stream Security for Video {video_id}...")
    
    # Attempt 1: Direct Access (No Token)
    res = requests.get(f"{BASE_URL}/video/{video_id}/stream")
    if res.status_code == 400: # Missing playback token
        log("Stream rejected missing token (400)", "PASS")
    else:
        fail(f"Stream accessible without token! Code: {res.status_code}")

    # Attempt 2: Generate Token
    res = session.post(f"{BASE_URL}/video/{video_id}/token")
    if res.status_code == 200:
        playback_token = res.json().get("playback_token")
        log("Playback token generated", "PASS")
    else:
        fail(f"Token generation failed: {res.status_code}")
        return

    # Attempt 3: Access with Token
    # Note: Stream endpoint does NOT require Auth header, only query param
    res = requests.get(f"{BASE_URL}/video/{video_id}/stream?token={playback_token}")
    if res.status_code == 200:
        if "<iframe" in res.text and "youtube.com/embed" in res.text:
            log("Stream returned valid HTML embed", "PASS")
        else:
            fail("Stream content does not look like HTML")
    else:
        fail(f"Stream failed with valid token: {res.status_code}")

    print("====================================")
    print("      AUDIT COMPLETE                ")
    print("====================================")

if __name__ == "__main__":
    audit()
