#!/usr/bin/env python3
"""
Python basics — type-along practice file.
Each section is independent and can be run on its own.
"""

# ============ Block 1: Hello world ============
print("Hello, Elton")

# Variables — no type declarations
name = "Elton"
year = 2026
is_active = True

print(name, year, is_active)

# ============ Block 2c: Dicts ============
# Dicts are key->value, like bash associative arrays but ubiquitous
counts = {}
counts["10.0.1.5"] = 3
counts["192.168.1.1"] = 1
print(counts)
print(counts["10.0.1.5"])

# Iterating
for ip, count in counts.items():
    print(f"{ip} -> {count}")

# Checking existence — common pattern
if "10.0.1.5" in counts:
    print("seen this IP before")

# The "increment if exists, else start at 1" pattern
ip = "10.0.1.5"
if ip in counts:
    counts[ip] += 1
else:
    counts[ip] = 1
print(counts)

# ============ Block 2 exercise ============
# Given the list of IPs below, count how many times each IP appears,
# then print each IP with its count, one per line.
#
# Expected output format (order doesn't matter):
#   10.0.1.5 -> 3
#   10.0.1.6 -> 2
#   192.168.1.1 -> 1
#
# Constraints:
#   - Use a dict to count
#   - Use a for loop to iterate
#   - Use an f-string to format the output
#   - No imports, no external libraries

ips = ["10.0.1.5", "10.0.1.6", "10.0.1.5", "192.168.1.1", "10.0.1.5", "10.0.1.6"]

# Your code below:
counts = {}
for ip in ips:
    if ip not in counts:
        counts[ip] = 1
    else:
        counts[ip] += 1
for ip,count in counts.items():
    print (f"{ip} -> {count}")

# ============ Block 3: File I/O ============
# The 'with' statement opens a file and automatically closes it when done.
# This is the standard, production-correct pattern. Use it always.

# Read whole file as one string (only for small files)
with open("logs/access.log") as f:
    content = f.read()
print(len(content), "characters total")

# Read file as a list of lines (each line includes its trailing \n)
with open("logs/access.log") as f:
    lines = f.readlines()
print(len(lines), "lines total")
print(lines[0])              # first line — note the \n at the end
print(lines[0].rstrip())     # rstrip() removes trailing whitespace including \n

# THE pattern you'll use 90% of the time: iterate line-by-line
# This is memory-efficient — works on huge files
with open("logs/access.log") as f:
    for line_num, line in enumerate(f, start=1):
        line = line.rstrip()
        if line_num <= 3:        # just print first 3 lines as demo
            print(f"Line {line_num}: {line}")
        else:
            break                # stop iterating early

# ============ Block 3 drill ============

# Drill 1: Open logs/syslog.log and print just the first line, no trailing newline.
with open("logs/syslog.log") as f:
    line = f.readline()
print(line.rstrip())

# Drill 2: Count the total number of lines in logs/syslog.log using a for loop
# (don't use readlines() this time — use the line-by-line iteration pattern).
with open("logs/syslog.log") as f:
    for line_num, line in enumerate(f, start=1):
        pass               # we don't need to do anything with each line
print(line_num)            # this is the total count

# Drill 3: Open logs/syslog.log and print the line number and content of any
# line containing "ERROR". Stop after finding 5 of them.
error_count=0
with open("logs/syslog.log") as f:
    for line_num,line in enumerate(f,start=1):
        line = line.rstrip()
        if "ERROR" in line:
            error_count += 1
            print(f"{line_num}: {line}")
        if error_count == 5:
           break

# ============ Block 4: Regex ============
import re

log_line = '10.0.87.137 - - [28/Apr/2026:00:00:00 +0000] "GET /api/products HTTP/1.1" 200 1951'

# ---- 4a: re.search — find the first match ----
# Returns a Match object, or None if no match
match = re.search(r"\d+\.\d+\.\d+\.\d+", log_line)
print(match)              # <re.Match object; span=(0, 11), match='10.0.87.137'>
print(match.group())      # '10.0.87.137' — the matched text
print(match.start(), match.end())  # 0 11 — position in the string

# What if no match?
no_match = re.search(r"this_is_not_in_the_line", log_line)
print(no_match)           # None — always check before calling .group()

# ---- 4b: The 'r' prefix on patterns ----
# r"..." is a "raw string" — backslashes are literal, not escape sequences.
# ALWAYS use raw strings for regex patterns. It's the convention.
# Without 'r', \d becomes... weird. Just always use 'r'.

# ---- 4c: Capturing groups with parentheses ----
# Parens around a sub-pattern create a "group" you can extract separately
match = re.search(r'"(\w+) (\S+) HTTP', log_line)
#                    ^---^ ^--^
#                  group 1 group 2
print(match.group(0))     # full match: '"GET /api/products HTTP'
print(match.group(1))     # first group: 'GET'
print(match.group(2))     # second group: '/api/products'
print(match.groups())     # tuple of all groups: ('GET', '/api/products')

# ---- 4d: re.findall — get all matches as a list ----
text = "Errors at 10.0.1.5, 192.168.1.1, and 172.16.0.1 today"
ips = re.findall(r"\d+\.\d+\.\d+\.\d+", text)
print(ips)   # ['10.0.1.5', '192.168.1.1', '172.16.0.1']

# With groups, findall returns tuples
log_lines = [
    'GET /api/users HTTP/1.1',
    'POST /api/login HTTP/1.1',
    'GET /health HTTP/1.1',
]
for line in log_lines:
    match = re.search(r"(\w+) (\S+) HTTP", line)
    if match:
        method, path = match.groups()
        print(f"{method} -> {path}")

# ---- 4e: Common patterns you'll need this month ----
# \d       any digit (0-9)
# \w       any word char (letters, digits, underscore)
# \s       any whitespace
# \S       any non-whitespace
# .        any char except newline
# +        one or more
# *        zero or more
# ?        zero or one
# {3}      exactly 3
# {2,5}    between 2 and 5
# [abc]    any of a, b, or c
# [^abc]   anything except a, b, c
# ^        start of string
# $        end of string

# ============ Block 4 drill ============
import re

# Drill 1: Extract the HTTP status code from this log line.
# A status code is a 3-digit number that comes after the closing quote
# of the request and a space.
# Hint: search for `" \d` first to find the right anchor, then capture the digits.

line = '10.0.87.137 - - [28/Apr/2026:00:00:00 +0000] "GET /api/products HTTP/1.1" 200 1951 "-" "curl/8.4.0" 808'
# Expected output: 200
match = re.search(r'" (\d+)', line)
print (match.group(1))

# Drill 2: From the syslog line below, extract the PID (the number in square brackets).
# Use a capturing group so you get just the number, not the brackets.

syslog = "Apr 28 00:00:05 app-02 kernel[24124]: WARN High memory usage: 81%"
# Expected output: 24124
match = re.search(r'\[(\d+)\]', syslog)
print (match.group(1))

# Drill 3: Open logs/syslog.log and extract all the unique hostnames that appear.
# Looking at the format, the hostname is the third field (e.g., "cache-01" or "app-02").
# You can use line.split() for this — regex is overkill here.
# Expected output: a list/set of unique hostnames like {"cache-01", "app-02", "app-01", ...}

hostnames = set()
with open("logs/syslog.log") as f:
    for line in f:
        name = line.split()[3]
        hostnames.add (name)
print (hostnames)

# ============ Block 5: Counter ============
from collections import Counter

# ---- 5a: What Counter is ----
# A Counter is a dict subclass designed for counting hashable items.
# You can create one from any iterable (list, generator, file lines).

# Manual way (what you've been doing)
ips = ["10.0.1.5", "10.0.1.6", "10.0.1.5", "192.168.1.1", "10.0.1.5"]
counts = {}
for ip in ips:
    counts[ip] = counts.get(ip, 0) + 1
print(counts)
# {'10.0.1.5': 3, '10.0.1.6': 1, '192.168.1.1': 1}

# Counter way (one line)
counts = Counter(ips)
print(counts)
# Counter({'10.0.1.5': 3, '10.0.1.6': 1, '192.168.1.1': 1})

# Counter behaves like a dict — same access patterns
print(counts["10.0.1.5"])     # 3
print("foo" in counts)        # False
for ip, count in counts.items():
    print(f"{ip} -> {count}")

# ---- 5b: The killer feature: most_common() ----
# This is why Counter exists. It returns items sorted by count, descending.

print(counts.most_common())     # all items, sorted: [('10.0.1.5', 3), ('10.0.1.6', 1), ...]
print(counts.most_common(2))    # top 2 only: [('10.0.1.5', 3), ('10.0.1.6', 1)]
print(counts.most_common(1))    # just the winner

# Common interview pattern: "find the top N most frequent X"
top_5 = counts.most_common(5)
for item, count in top_5:
    print(f"{item}: {count}")

# ---- 5c: Updating a Counter incrementally ----
# Sometimes you can't build the full list first — you stream items as you go.

c = Counter()
c["apple"] += 1
c["apple"] += 1
c["banana"] += 1
print(c)   # Counter({'apple': 2, 'banana': 1})

# Note: missing keys default to 0 (unlike a regular dict, which raises KeyError)
print(c["nonexistent"])   # 0 — no crash

# ---- 5d: The pattern you'll use most this month ----
# Count something across a file, get the top N.

c = Counter()
with open("logs/access.log") as f:
    for line in f:
        ip = line.split()[0]   # first field is the IP
        c[ip] += 1

# Or even more concise — pass a generator directly to Counter
with open("logs/access.log") as f:
    c = Counter(line.split()[0] for line in f)

# Top 5 IPs
for ip, count in c.most_common(5):
    print(f"{ip}: {count}")

# ============ Block 5 drill ============
from collections import Counter

# Drill: Open logs/access.log and find the top 3 most-requested URL paths.
# The path is the second field inside the quoted request, e.g.:
#   "GET /api/products HTTP/1.1"
# So you need to extract the path. Suggested approach:
#   1. Use re.search to extract the path with a capture group, OR
#   2. Use .split() on the line and pick the right field
#
# Output format:
#   /api/products: 5234
#   /health:       4187
#   /api/users:    3050
#
# Allowed: cheatsheet, this file's prior blocks
# Time yourself.

c = Counter()
with open("logs/access.log") as f:
    for line in f:
        path = re.search(r'\"\w+ (\/\w+\/\w+) \w+\/\d\.\d',line)
        print (path.group(1))



# ---- 4e: Common patterns you'll need this month ----
# \d       any digit (0-9)
# \w       any word char (letters, digits, underscore)
# \s       any whitespace
# \S       any non-whitespace
# .        any char except newline
# +        one or more
# *        zero or more
# ?        zero or one
# {3}      exactly 3
# {2,5}    between 2 and 5
# [abc]    any of a, b, or c
# [^abc]   anything except a, b, c
# ^        start of string
# $        end of string