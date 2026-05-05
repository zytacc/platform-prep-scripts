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

