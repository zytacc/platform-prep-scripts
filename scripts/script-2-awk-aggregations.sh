#!/usr/bin/env bash
#This is the practice on writing awk aggregation script
set -euo pipefail
#main logic below

# ---------- Helpers ----------
usage() {
    grep '^#' "$0" | grep -v '^#!' | sed 's/^# \?//'
    exit 1
}

die() {
    echo "Error: $*" >&2
    exit 1
}

# ---------- Main dispatcher ----------

main() {
    local cmd="${1:-help}"
    shift || true   # remove $1 so $@ holds the rest

    case "$cmd" in
        total-count)        total_count "$@" ;;
        byte-transfer)     byte_transfer "$@" ;;
        logs-5xx)  logs_5xx "$@" ;;
        top-ip)  top_ip "$@" ;;
        help|-h|--help) usage ;;
        *)              die "Unknown command: $cmd. Run with 'help' for usage." ;;
    esac
}

#taotal count: Count total requests by HTTP status code
total_count() {
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"
    awk '{print $9}' logs/access.log | sort | uniq -c | sort -rn
}

#byte transfer: Sum total bytes transferred (one number)
byte_transfer() {
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"
    awk '{sum += $10} END {print sum}' logs/access.log 
}

#logs 5xx: Print only lines where status code is 5xx
logs_5xx() {
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"
    awk '$9 >= 500 && $9 < 600 {print}' logs/access.log
}

#top ip: Count requests per IP, top 5 by volume
top_ip() {
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"
    awk '{print $1}' logs/access.log | sort | uniq -c | sort -rn | head -5
}

main "$@"

