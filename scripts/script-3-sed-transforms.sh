#!/usr/bin/env bash
#This is the day 6 sed drill
set -euo pipefail
#main logic below

# sed Drill — Day 6
# Log files: logs/access.log (Apache/Nginx format), logs/syslog.log
#
# Problem 1: Strip all blank lines from syslog.log, print to stdout
#sed '/^$/d' logs/syslog.log
# Problem 2: Print only lines containing "ERROR" from syslog.log
#sed -n '/ERROR/p' logs/syslog.log
# Problem 3: Replace all occurrences of "ERROR" with "CRITICAL" in syslog.log, print to stdout
#sed 's/ERROR/CRITICAL/g' logs/syslog.log
# Problem 4: Remove leading whitespace from every line in syslog.log
#sed 's/^[[:space:]]*//' logs/syslog.log
# Problem 5: Extract only the timestamp portion from each line in access.log
#             Log format: 192.168.1.1 - - [01/May/2026:10:00:01 +0000] "GET /api/users HTTP/1.1" 200 1234
#             Target output: 01/May/2026:10:00:01 +0000
#             Hint: the timestamp is inside brackets — strip the brackets too
#sed 's/.*\[//g;s/\].*//g' logs/access.log
# Target: 25 minutes, reference the walkthrough freely
# Deliverable: script-3-sed-transforms.sh wrapping these as subcommands

die() {
    echo "Error: $*" >&2
    exit 1
}

main() {
    local cmd="${1:-help}"
    shift || true   # remove $1 so $@ holds the rest

    case "$cmd" in
        strip_blank)     strip_blank "$@" ;;
        print_error)     print_error "$@" ;;
        replace_error)   replace_error "$@" ;;
        remove_space)    remove_space "$@" ;;
        extract_timestamp)     extract_timestamp "$@" ;;
        *)              die "Unknown command: $cmd." ;;
    esac
}

strip_blank() {
    [[ ! -f logs/syslog.log ]] && die "logs/syslog.log not found"
    sed '/^$/d' logs/syslog.log
}

print_error() {
    [[ ! -f logs/syslog.log ]] && die "logs/syslog.log not found"
    sed -n '/ERROR/p' logs/syslog.log
}

replace_error() {
    [[ ! -f logs/syslog.log ]] && die "logs/syslog.log not found"
    sed 's/ERROR/CRITICAL/g' logs/syslog.log
}

remove_space() {
    [[ ! -f logs/syslog.log ]] && die "logs/syslog.log not found"
    sed 's/^[[:space:]]*//' logs/syslog.log
}

extract_timestamp() {
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"
    sed 's/.*\[//g;s/\].*//g' logs/access.log
}

main "$@"