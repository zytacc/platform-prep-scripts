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
#awk '{ bytes[$9] += $10 } END { for (k in bytes) print k, bytes[k] }' logs/access.log | sort -k2 -rn

# Integration Drill — Bash + Log Analysis (45 minutes, no reference)
# Source file: logs/access.log
# Log format: 192.168.1.1 - - [01/May/2026:10:00:01 +0000] "GET /api/users HTTP/1.1" 200 1234
# Fields: $1=IP, $6=timestamp(quoted), $7=METHOD(after quote), $8=path, $9=protocol", $10=status, $11=bytes
# NOTE: confirm field positions yourself with: head -3 logs/access.log | awk '{print NF, $0}'
#
# Problem 1: Top 10 IPs making POST requests, by request count
#            Output: count and IP, sorted by count descending
#grep "POST" logs/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -n 10

# Problem 2: For each HTTP method (GET, POST, PUT, DELETE), report total request count
#            Output: method and count, sorted by count descending
#grep -oE "GET|POST|PUT|DELETE" logs/access.log | sort | uniq -c

# Problem 3: Average response size in bytes for successful requests (status 200 only)
#            Output: one number
#awk '{ bytes[$9] += $10; count[$9] ++ } END { print bytes[200]/count[200] }' logs/access.log

# Problem 4: Find the 5 paths with the highest total bytes transferred
#            (sum of bytes across all requests to each path)
#            Output: total_bytes and path, sorted by bytes descending
#awk '{ bytes[$7] += $10 } END { for (k in bytes) print bytes[k], k }' logs/access.log | sort -rn | head -n 5

# Problem 5: Error rate by hour
#            For each hour of the day, report: hour, total_requests, error_count, error_rate%
#            Error = status >= 400
#            Output: sorted by hour ascending
#            Hint: extract hour from the timestamp field



# Deliverable: scripts/integration-drill-1.sh
#              Solutions can be bare commands or wrapped — your call
#
# When done:
# 1. Note total time taken
# 2. Note which problems you got stuck on and why
# 3. Note any specific syntax you reached for and couldn't recall
# 4. Post results — we'll review honestly