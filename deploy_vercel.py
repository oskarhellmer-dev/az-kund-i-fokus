#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deployar sajten till Vercel via REST-API (CLI-token är scopad, API:t funkar).
Kör: python3 deploy_vercel.py
"""
import os, sys, json, hashlib, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = open("/home/clawd/.vercel_token").read().strip()
PROJECT = "az-kund-i-fokus"
API = "https://api.vercel.com"

EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".vercel"}
EXCLUDE_FILES = {".gitignore", "README.md", "build.py", "deploy_vercel.py",
                 "gen_imgs.py", "gen_og.py"}

def collect():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if fn in EXCLUDE_FILES or fn.endswith(".pyc"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
            data = open(full, "rb").read()
            files.append((rel, data))
    return files

def api(method, path, body=None, headers=None, raw=False):
    url = API + path
    h = {"Authorization": f"Bearer {TOKEN}"}
    if headers: h.update(headers)
    data = None
    if body is not None:
        data = body if raw else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try: payload = json.loads(e.read() or b"{}")
        except Exception: payload = {}
        return e.code, payload

def main():
    files = collect()
    print(f"{len(files)} filer")
    manifest = []
    for rel, data in files:
        sha = hashlib.sha1(data).hexdigest()
        st, resp = api("POST", "/v2/files", body=data, raw=True,
                       headers={"x-vercel-digest": sha,
                                "Content-Type": "application/octet-stream"})
        if st not in (200, 409):
            print(f"  ! upload {rel} -> {st} {resp}")
        manifest.append({"file": rel, "sha": sha, "size": len(data)})
    print("filer uppladdade, skapar deployment …")
    st, resp = api("POST", "/v13/deployments", body={
        "name": PROJECT,
        "files": manifest,
        "target": "production",
        "projectSettings": {"framework": None, "buildCommand": None,
                            "outputDirectory": None, "installCommand": None},
    })
    if st not in (200, 201):
        print("FEL:", st, json.dumps(resp)[:600]); sys.exit(1)
    dep = resp
    print("id:", dep.get("id"), "url:", dep.get("url"), "status:", dep.get("status"))
    did = dep["id"]
    for _ in range(60):
        time.sleep(5)
        st, d = api("GET", f"/v13/deployments/{did}")
        if st != 200:
            print("poll fel", st, d); break
        s = d.get("readyState") or d.get("status")
        print("  status:", s)
        if s in ("READY", "ERROR", "CANCELED"):
            aliases = d.get("alias", [])
            print("KLAR:", s, "| url: https://" + (d.get("url") or ""), "| aliases:", aliases)
            break

if __name__ == "__main__":
    main()
