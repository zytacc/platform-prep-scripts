#!/usr/bin/env bash
# this is the bash skeleton practice
set -euo pipefail
# main logic below

# awk Drill — Day 5
# Log format: $1=IP, $9=status_code, $10=bytes
# Verify fields first: head -3 logs/access.log | awk '{ print NF, $0 }'
#
# Problem 1: Count total requests by HTTP status code
awk '{print $9}' logs/access.log | sort | uniq -c | sort -rn
# Problem 2: Sum total bytes transferred (one number)
awk '{sum += $10} END {print sum}' logs/access.log 
# Problem 3: Print only lines where status code is 5xx
awk '$9~/500/ {print}' logs/access.log 
# Problem 4: Count requests per IP, top 5 by volume
awk '{print $1}' logs/access.log | sort | uniq -c | sort -rn | head -5