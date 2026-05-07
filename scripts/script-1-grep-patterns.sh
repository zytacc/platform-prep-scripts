cd ~/code/platform-prep-scripts

# Count ERRORs in syslog
grep -c "ERROR" logs/syslog.log

# All ERRORs from app, with line numbers
grep -n "ERROR" logs/syslog.log | head -5

# Lines containing "memory" (case-insensitive)
grep -ic "memory" logs/syslog.log

# Lines NOT containing INFO (the errors and warnings)
grep -v "INFO" logs/syslog.log | wc -l

#!/usr/bin/env bash
# ============================================================
# Day 4 (Week 1, Day 1) — Timed Drill: grep + pipelines
# Date attempted: 2026-05-06
# Target time: 30 min  |  Max: 45 min
# ============================================================
#
# Problem:
#   From logs/access.log, find the top 10 IP addresses by request count,
#   but only for POST requests. Output one IP per line with its count,
#   sorted by count descending.
#
# Expected output format (uniq -c | sort -rn standard):
#       234 192.168.5.12
#       187 10.0.45.7
#       ...
#
# Constraints:
#   - Bash only, no Python
#   - Single pipeline (one command line joined by |)
#   - `man` pages and `--help` allowed
#   - Internet, AI, Stack Overflow NOT allowed
#   - Verbalize aloud while building it
#
# Hint (only if stalled 5+ min):
#   grep "POST" → extract first field → sort → uniq -c → sort by count → head
#
# Build incrementally. Get stage 1 working, then add stage 2, etc.
# If a stage's output looks wrong, inspect before piling on more.
#
# ============================================================

# Your pipeline below:
grep "POST" logs/access.log \
  | grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}" \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -10

#!/usr/bin/env bash
# ============================================================
# script-1-grep-patterns.sh
#
# Demonstrates idiomatic grep usage for log analysis.
# Five small utilities, each callable as a subcommand.
#
# Usage:
#   ./script-1-grep-patterns.sh <command> [args]
#
# Commands:
#   top-ips <method>      Top 10 IPs by request count, filtered by HTTP method
#   error-rate <logfile>  Count of ERRORs in a log file with percentage
#   recent-errors <log>   Last 5 errors with line numbers
#   status-counts <log>   Count of requests by HTTP status code
#   help                  Show this message
#
# Examples:
#   ./script-1-grep-patterns.sh top-ips POST
#   ./script-1-grep-patterns.sh error-rate logs/syslog.log
#   ./script-1-grep-patterns.sh status-counts logs/access.log
# ============================================================

set -euo pipefail

# ---------- Helpers ----------

usage() {
    grep '^#' "$0" | grep -v '^#!' | sed 's/^# \?//'
    exit 1
}

die() {
    echo "Error: $*" >&2
    exit 1
}

# ---------- Commands ----------

# top-ips: Top 10 IPs by request count, filtered by HTTP method
# Args: $1 = method (GET, POST, etc.)
top_ips() {
    local method="${1:-}"
    [[ -z "$method" ]] && die "top-ips requires an HTTP method (e.g., POST)"
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"

    grep "\"$method " logs/access.log \
        | awk '{print $1}' \
        | sort \
        | uniq -c \
        | sort -rn \
        | head -10
}

# error-rate: Count of ERRORs in a log file with percentage of total
# Args: $1 = log file path
error_rate() {
    local logfile="${1:-}"
    [[ -z "$logfile" ]] && die "error-rate requires a log file path"
    [[ ! -f "$logfile" ]] && die "File not found: $logfile"

    local total errors pct
    total=$(wc -l < "$logfile")
    errors=$(grep -c "ERROR" "$logfile" || true)   # || true so set -e doesn't kill us when count is 0
    pct=$(awk "BEGIN { printf \"%.2f\", ($errors / $total) * 100 }")

    echo "File:       $logfile"
    echo "Total:      $total lines"
    echo "Errors:     $errors lines"
    echo "Error rate: ${pct}%"
}

# recent-errors: Last 5 errors with line numbers
# Args: $1 = log file path
recent_errors() {
    local logfile="${1:-}"
    [[ -z "$logfile" ]] && die "recent-errors requires a log file path"
    [[ ! -f "$logfile" ]] && die "File not found: $logfile"

    grep -n "ERROR" "$logfile" | tail -5
}

# status-counts: Count of requests by HTTP status code (access.log format)
# Args: $1 = log file path (defaults to logs/access.log)
status_counts() {
    local logfile="${1:-logs/access.log}"
    [[ ! -f "$logfile" ]] && die "File not found: $logfile"

    awk '{print $9}' "$logfile" \
        | sort \
        | uniq -c \
        | sort -rn
}

# ---------- Main dispatcher ----------

main() {
    local cmd="${1:-help}"
    shift || true   # remove $1 so $@ holds the rest

    case "$cmd" in
        top-ips)        top_ips "$@" ;;
        error-rate)     error_rate "$@" ;;
        recent-errors)  recent_errors "$@" ;;
        status-counts)  status_counts "$@" ;;
        help|-h|--help) usage ;;
        *)              die "Unknown command: $cmd. Run with 'help' for usage." ;;
    esac
}

main "$@"