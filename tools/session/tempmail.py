#!/usr/bin/env python3
"""Temp mail helper using mail.tm API.
Usage:
  python tempmail.py new          -> generate new email, save session
  python tempmail.py check        -> check inbox, print messages (id, from, subject)
  python tempmail.py read <id>    -> read full message body
"""
import json
import random
import string
import sys
import urllib.request

API = "https://api.mail.tm"
SESSION_FILE = "/home/z/my-project/scripts/mail_session.json"


def req(method, path, body=None, token=None):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(f"{API}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode()) if resp.status != 204 else {}


def new_email():
    d = req("GET", "/domains")
    domains = d["hydra:member"] if isinstance(d, dict) else d
    domain = domains[0]["domain"]
    login = "bakky" + "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
    address = f"{login}@{domain}"
    password = "Bk" + "".join(random.choices(string.ascii_letters + string.digits, k=14)) + "!7"
    # create account
    for attempt in range(3):
        try:
            req("POST", "/accounts", {"address": address, "password": password})
            break
        except Exception as e:
            if attempt == 2:
                raise
            login = "bakky" + "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
            address = f"{login}@{domain}"
    # get token
    tok = req("POST", "/token", {"address": address, "password": password})["token"]
    with open(SESSION_FILE, "w") as f:
        json.dump({"address": address, "password": password, "token": tok}, f)
    print(f"EMAIL: {address}")


def check_inbox():
    with open(SESSION_FILE) as f:
        s = json.load(f)
    try:
        msgs = req("GET", "/messages", token=s["token"])
        msgs = msgs["hydra:member"] if isinstance(msgs, dict) else msgs
    except Exception:
        # token expired, refresh
        tok = req("POST", "/token", {"address": s["address"], "password": s["password"]})["token"]
        s["token"] = tok
        with open(SESSION_FILE, "w") as f:
            json.dump(s, f)
        msgs = req("GET", "/messages", token=s["token"])
        msgs = msgs["hydra:member"] if isinstance(msgs, dict) else msgs
    if not msgs:
        print("INBOX EMPTY")
        return
    for m in msgs:
        frm = m.get("from", {}).get("address", "?")
        print(f"id={m['id']} | from={frm} | subject={m.get('subject')} | intro={m.get('intro','')[:80]}")


def read_msg(msg_id):
    with open(SESSION_FILE) as f:
        s = json.load(f)
    m = req("GET", f"/messages/{msg_id}", token=s["token"])
    print(f"From: {m.get('from', {}).get('address')}\nSubject: {m.get('subject')}\nDate: {m.get('createdAt')}\n")
    text = m.get("text") or ""
    html = m.get("html") or ""
    print("TEXT BODY:\n" + text[:4000])
    if not text and html:
        print("HTML BODY:\n" + html[0][:4000])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "new"
    if cmd == "new":
        new_email()
    elif cmd == "check":
        check_inbox()
    elif cmd == "read":
        read_msg(sys.argv[2])
    else:
        print("unknown command")
