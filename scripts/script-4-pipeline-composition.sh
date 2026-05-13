# sort/uniq/tr Drill — Day 7
# Log files: logs/access.log, logs/syslog.log
# Format reminder: $1=IP, $7=path, $9=status, $10=bytes
#
# Problem 1: List every unique HTTP status code that appears in access.log
#            (just the codes, one per line, sorted, no duplicates)
#awk '{print $9}' logs/access.log | sort | uniq
# Problem 2: Show the top 5 most frequent paths in access.log
#            Output format: count, then path
#awk '{print $7}' logs/access.log | sort | uniq -c | sort -rn | head -n 5
# Problem 3: Count how many ERROR, WARN, and INFO lines are in syslog.log
#            (one line per severity level, with count)
#awk '{print $6}' logs/syslog.log | sort | uniq -c
#grep -oE "ERROR|WARN|INFO" logs/syslog.log | sort | uniq -c
# Problem 4: From access.log, find IPs that made more than 100 requests
#            Output: count and IP, sorted by count descending
#            Hint: this uses uniq -c with another filter — think about how to filter on the count
#awk '{print $1}' logs/access.log | sort | uniq -c | sort -rn | awk '$1>100'
# Problem 5: Take a CSV file where the data is messy:
#            cat logs/messy.csv | <your pipeline>
#            The file has lines like "  Apple,  Red, 5  " with leading/trailing whitespace
#            Output should be clean uppercase: "APPLE,RED,5"
#            Use tr and/or sed in composition
#cat logs/messy.csv | sed 's/[[:space:]]//g' | tr 'a-z' 'A-Z'
# Target: 25 minutes, reference the walkthrough freely
# Deliverable: script-4-pipeline-composition.sh wrapping these as subcommands

#!/usr/bin/env bash
#This is the pipeline composition exercise
set -euo pipefail
#main logic below

die() {
    echo "Error: $*" >&2
    exit 1
}

main (){
    local cmd="${1:-help}"
    shift || true # remove $1 so $@ holds the rest

    case "$cmd" in
        uniq_status)        uniq_status "$@" ;;
        freq_path)        freq_path "$@" ;;
        count_severity)        count_severity "$@" ;;
        ip_100)        ip_100 "$@" ;;
        clean_csv)        clean_csv "$@" ;;
    *)              die "Unknown command: $cmd." ;;
    esac
}

#counts uniq status code
uniq_status() {
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"
    awk '{print $9}' logs/access.log | sort | uniq
}

#5 most frequent path
freq_path() {
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"
    awk '{print $7}' logs/access.log | sort | uniq -c | sort -rn | head -n 5
}

#number of occurrence for ERROR, WARN, INFO
count_severity() {
    [[ ! -f logs/syslog.log ]] && die "logs/syslog.log not found"
    grep -oE "ERROR|WARN|INFO" logs/syslog.log | sort | uniq -c
}

#ip with >100 requests
ip_100() {
    [[ ! -f logs/access.log ]] && die "logs/access.log not found"
    awk '{print $1}' logs/access.log | sort | uniq -c | sort -rn | awk '$1>100'
}

#clean up scv with spaces, and capitalize
clean_csv() {
    [[ ! -f logs/messy.csv ]] && die "logs/messy.csv not found"
    cat logs/messy.csv | sed 's/[[:space:]]//g' | tr 'a-z' 'A-Z'
}

main "$@"