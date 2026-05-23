# ============================================================
# DAY 12 DRILLS — re module only
# ============================================================
# All drills go in: scripts/script-8-regex.py
# Work through 12.1, comment it out, then 12.2, then 12.3.
#
# Rules:
#   - Cheatsheet open. No Google.
#   - Time each one.
#   - The goal is fluency with re.search, capture groups, and findall.
# ============================================================


# ------------------------------------------------------------
# DRILL 12.1 — Warmup: extract one field with re.search
# ------------------------------------------------------------
# Target: 10 min
#
# Open logs/access.log. For each line, extract the IP address
# (the first field of every access log line — but use a regex,
# not line.split(), to get the practice).
#
# Print only the first 10 IPs you find, one per line.
#
# Requirements:
#   - Use re.search with a capture group.
#   - Use `if m:` before .group().
#   - Use a raw string for the pattern.
#
# Test:
#   ./script-8-regex.py
#   (compare your first 10 IPs against: head -10 logs/access.log | awk '{print $1}')
import re
match=0
with open("logs/access.log") as f:
    for line in f:
        line = line.rstrip()
        m = re.search(r'\d+\.\d+\.\d+\.\d+', line)
        if m:
            match += 1
            print (m.group())
        if match==10:
            break

# ------------------------------------------------------------
# DRILL 12.2 — Core: extract two fields with one regex
# ------------------------------------------------------------
# Target: 15 min
#
# Open logs/access.log. For each line, extract BOTH the HTTP method
# (GET, POST, etc.) AND the URL path. Print as:
#
#   GET /api/orders
#   POST /login
#   GET /static/css/main.css
#   ...
#
# Print only the first 20.
#
# Requirements:
#   - Use re.compile (pattern reused in the loop).
#   - One regex with TWO capture groups.
#   - Skip lines that don't match (don't crash).
#   - Hint: the request appears inside quotes, e.g. "GET /api/orders HTTP/1.1"
import re
match=0
with open("logs/access.log") as f:
    for line in f:
        line = line.rstrip()
        m = re.search(r'\d+\.\d+\.\d+\.\d+', line)
        if m:
            match += 1
            print (m.group())
        if match==10:
            break

# ------------------------------------------------------------
# DRILL 12.3 — Stretch: findall and sub
# ------------------------------------------------------------
# Target: 15 min
#
# Two small problems in one script:
#
# Part A: Open logs/syslog.log. Use re.findall to extract every
# PID from every line (PIDs look like "[1234]"). Print the count
# of unique PIDs found.
#
# Part B: Open logs/access.log. Read the first line. Use re.sub
# to mask every IP address with the string "<REDACTED>".
# Print the masked line.
#
# Requirements:
#   - Part A: findall, then convert to set for uniqueness.
#   - Part B: re.sub with a pattern that matches IPv4.