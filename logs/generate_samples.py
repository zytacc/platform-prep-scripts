#!/usr/bin/env python3
"""
Generate three sample log files for practice drills:
  - access.log    : Apache/Nginx-style web access log (50,000 lines)
  - syslog.log    : Linux syslog-style entries (10,000 lines)
  - app.json.log  : Structured JSON application log (20,000 lines)

Usage:
    python3 logs/generate_samples.py
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)  # reproducible output

OUT_DIR = Path(__file__).parent

# ---------- Shared pools ----------
IPS = [f"10.0.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(80)] + \
      [f"192.168.{random.randint(0,10)}.{random.randint(1,254)}" for _ in range(40)] + \
      [f"172.16.{random.randint(0,10)}.{random.randint(1,254)}" for _ in range(30)]

ENDPOINTS = [
    ("/api/users",        "GET",  [200, 200, 200, 200, 404, 500]),
    ("/api/users/{id}",   "GET",  [200, 200, 200, 404]),
    ("/api/orders",       "POST", [201, 201, 400, 500]),
    ("/api/orders/{id}",  "GET",  [200, 200, 404]),
    ("/api/login",        "POST", [200, 200, 401, 401, 429]),
    ("/api/logout",       "POST", [204, 204, 401]),
    ("/api/products",     "GET",  [200, 200, 200, 200, 500]),
    ("/api/checkout",     "POST", [200, 400, 402, 500, 503]),
    ("/health",           "GET",  [200] * 20 + [500]),
    ("/metrics",          "GET",  [200] * 10),
]

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0) Chrome/119.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) Safari/17.0",
    "curl/8.4.0",
    "python-requests/2.31.0",
    "PostmanRuntime/7.34.0",
]

# ---------- Generator 1: access.log (Apache/Nginx combined format) ----------
def gen_access_log(path, n=50_000):
    start = datetime(2026, 4, 28, 0, 0, 0)
    with open(path, "w") as f:
        for i in range(n):
            ts = start + timedelta(seconds=i * random.randint(1, 4))
            ip = random.choice(IPS)
            endpoint, method, status_pool = random.choice(ENDPOINTS)
            path_str = endpoint.replace("{id}", str(random.randint(1, 9999)))
            status = random.choice(status_pool)
            size = random.randint(200, 8000) if status < 400 else random.randint(50, 500)
            ua = random.choice(USER_AGENTS)
            latency_ms = random.choices(
                [random.randint(5, 50), random.randint(50, 200),
                 random.randint(200, 800), random.randint(800, 3000)],
                weights=[70, 20, 8, 2]
            )[0]
            ts_str = ts.strftime("%d/%b/%Y:%H:%M:%S +0000")
            line = (f'{ip} - - [{ts_str}] "{method} {path_str} HTTP/1.1" '
                    f'{status} {size} "-" "{ua}" {latency_ms}')
            f.write(line + "\n")

# ---------- Generator 2: syslog.log ----------
def gen_syslog(path, n=10_000):
    hosts = ["app-01", "app-02", "db-01", "cache-01", "worker-03"]
    services = ["sshd", "nginx", "postgres", "kernel", "systemd", "myapp"]
    messages = [
        ("INFO",  "Connection accepted from {ip}"),
        ("INFO",  "Started service successfully"),
        ("WARN",  "High memory usage: {pct}%"),
        ("WARN",  "Slow query detected: {ms}ms"),
        ("ERROR", "Connection refused to upstream {ip}:{port}"),
        ("ERROR", "Out of memory: killed process {pid}"),
        ("ERROR", "Disk space critical on /var: {pct}% used"),
        ("INFO",  "User {user} logged in from {ip}"),
        ("WARN",  "Authentication failure for user {user}"),
        ("INFO",  "Received SIGTERM, shutting down gracefully"),
    ]
    start = datetime(2026, 4, 28, 0, 0, 0)
    with open(path, "w") as f:
        for i in range(n):
            ts = start + timedelta(seconds=i * random.randint(1, 10))
            host = random.choice(hosts)
            svc = random.choice(services)
            pid = random.randint(100, 30000)
            level, tmpl = random.choice(messages)
            msg = tmpl.format(
                ip=random.choice(IPS),
                pct=random.randint(70, 99),
                ms=random.randint(500, 8000),
                port=random.choice([5432, 6379, 8080, 443]),
                pid=random.randint(1000, 9999),
                user=random.choice(["admin", "deploy", "elton", "root", "service"]),
            )
            ts_str = ts.strftime("%b %d %H:%M:%S")
            f.write(f"{ts_str} {host} {svc}[{pid}]: {level} {msg}\n")

# ---------- Generator 3: app.json.log ----------
def gen_json_log(path, n=20_000):
    start = datetime(2026, 4, 28, 0, 0, 0)
    levels = ["INFO"] * 70 + ["WARN"] * 20 + ["ERROR"] * 10
    with open(path, "w") as f:
        for i in range(n):
            ts = start + timedelta(milliseconds=i * random.randint(50, 500))
            endpoint, method, status_pool = random.choice(ENDPOINTS)
            status = random.choice(status_pool)
            entry = {
                "timestamp": ts.isoformat() + "Z",
                "level": random.choice(levels),
                "service": random.choice(["api-gateway", "user-svc", "order-svc", "auth-svc"]),
                "trace_id": f"{random.randint(10**15, 10**16-1):x}",
                "method": method,
                "path": endpoint.replace("{id}", str(random.randint(1, 9999))),
                "status": status,
                "latency_ms": random.choices(
                    [random.randint(2, 50), random.randint(50, 300), random.randint(300, 2000)],
                    weights=[75, 20, 5]
                )[0],
                "user_id": random.randint(1, 5000) if random.random() > 0.1 else None,
            }
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    print("Generating logs...")
    gen_access_log(OUT_DIR / "access.log")
    print(f"  access.log    -> {(OUT_DIR / 'access.log').stat().st_size // 1024} KB")
    gen_syslog(OUT_DIR / "syslog.log")
    print(f"  syslog.log    -> {(OUT_DIR / 'syslog.log').stat().st_size // 1024} KB")
    gen_json_log(OUT_DIR / "app.json.log")
    print(f"  app.json.log  -> {(OUT_DIR / 'app.json.log').stat().st_size // 1024} KB")
    print("Done.")
