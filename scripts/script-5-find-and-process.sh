# find/xargs Drill — Day 8
# Working directory: anywhere in your repo. Use logs/ and scripts/ as targets.
#
# Problem 1: Find all .log files anywhere under logs/
#            (just list them)
#find ./logs/ -type f -name "*.log"
# Problem 2: Find all .sh files under scripts/ that are larger than 1KB
#find ./scripts/ -type f -name "*.sh" -size +1k
# Problem 3: Find all files modified in the last 24 hours, anywhere in the repo
#            (use the current working directory as the search root)
#find . -type f -mtime -1
# Problem 4: Find all .log files and count how many ERROR lines each contains
#            Output: count and filename, one per line
#            Use find + xargs (safe with -print0)
#find ./logs/ -name "*.log" -print0 | xargs -0 grep -oE "ERROR" | sed 's/:ERROR//' | sort | uniq -c | sort -rn
#find ./logs/ -name "*.log" -print0 | xargs -0 grep -c "ERROR"
# Problem 5: Find all .sh files in scripts/ that contain the string "set -euo pipefail"
#            Output: just the filenames (not the matching lines)
#            Hint: grep has a flag for "list filenames only"
#find ./scripts -name "*.sh" -print0 | xargs -0 grep -l "set -euo pipefail"
# Target: 20 minutes, reference the walkthrough freely
# Deliverable: script-5-find-and-process.sh wrapping these as subcommands

