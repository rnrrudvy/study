import os
import random
import string
import time
import requests

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:5001")

def rand_str(prefix: str, n: int = 6) -> str:
    return prefix + "-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=n))

def wait_healthz(timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{BASE}/healthz", timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise RuntimeError("healthz not ready")

def test_register_login_write_delete():
    wait_healthz()
    s = requests.Session()

    username = rand_str("user")
    password = rand_str("pw")
    title = rand_str("title")
    content = rand_str("content")

    # register
    r = s.post(f"{BASE}/register", data={"username": username, "password": password}, allow_redirects=False)
    assert r.status_code in (302, 303)

    # login
    r = s.post(f"{BASE}/login", data={"username": username, "password": password}, allow_redirects=False)
    assert r.status_code in (302, 303)

    # write
    r = s.post(f"{BASE}/write", data={"title": title, "content": content}, allow_redirects=False)
    assert r.status_code in (302, 303)

    # get list and extract latest post id
    r = s.get(f"{BASE}/")
    assert r.status_code == 200
    # naive find by title occurrence
    assert title in r.text

    # find post id by requesting a simple list API-like via regex from html
    import re
    ids = re.findall(r"/delete/(\d+)", r.text)
    assert ids, "no posts found to delete"
    post_id = ids[0]

    # delete
    r = s.post(f"{BASE}/delete/{post_id}", allow_redirects=False)
    assert r.status_code in (302, 303)

    # verify deletion
    r = s.get(f"{BASE}/")
    assert title not in r.text




