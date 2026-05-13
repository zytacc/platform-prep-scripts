# Day 9 — Closed-Book Warm-Up
# Source file: logs/access.log
# Log format reminder: $1=IP, $7=path, $9=status, $10=bytes
#
# Drill A (target: 8 minutes)
# Show the top 5 IPs by request count.
# Output: count and IP, sorted by count descending.

#awk '{print $1}' logs/access.log | sort | uniq -c | sort -rn | head -n 5

# Drill B (target: 10 minutes)
# Show total bytes transferred broken down by HTTP status code.
# Output: status code and total bytes, sorted by bytes descending.
# Example output:
#   200 45000000
#   404 120000
#   500 5000

# awk '{ sum += $10 }; END { print sum }' logs/access.log 

awk '{print $9;$10}' logs/access.log