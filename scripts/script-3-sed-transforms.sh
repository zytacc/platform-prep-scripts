#!/usr/bin/env bash
#This is the day 6 sed drill
set -euo pipefail
#main logic below

# sed Drill — Day 6
# Log files: logs/access.log (Apache/Nginx format), logs/syslog.log
#
# Problem 1: Strip all blank lines from syslog.log, print to stdout
#
# Problem 2: Print only lines containing "ERROR" from syslog.log
#
# Problem 3: Replace all occurrences of "ERROR" with "CRITICAL" in syslog.log, print to stdout
#
# Problem 4: Remove leading whitespace from every line in syslog.log
#
# Problem 5: Extract only the timestamp portion from each line in access.log
#             Log format: 192.168.1.1 - - [01/May/2026:10:00:01 +0000] "GET /api/users HTTP/1.1" 200 1234
#             Target output: 01/May/2026:10:00:01 +0000
#             Hint: the timestamp is inside brackets — strip the brackets too
#
# Target: 25 minutes, reference the walkthrough freely
# Deliverable: script-3-sed-transforms.sh wrapping these as subcommands