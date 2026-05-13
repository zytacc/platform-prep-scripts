# Bash Cheatsheet — Working Subset for Log Analysis

Living document. Same rules as python-cheatsheet.md: every lookup goes here, items leave the lookup list as recall improves.

---

## grep — the flags I use most

| Flag | Meaning |
|------|---------|
| `-i` | case-insensitive |
| `-v` | invert: lines NOT matching |
| `-c` | count matching lines |
| `-n` | line numbers |
| `-l` | list filenames with matches |
| `-r` | recursive |
| `-E` | extended regex (no escaping for `+`, `?`, `\|`) |
| `-o` | print only matched part |
| `-w` | whole word match |
| `-A 3` / `-B 3` / `-C 3` | After / Before / Around (context) |

---

## Field extraction — when data is positional

```bash
awk '{print $1}'           # first field, whitespace-separated, robust to multiple spaces
awk '{print $NF}'          # last field
awk '{print $1, $9}'       # multiple fields
cut -d ',' -f 2            # CSV — second field, comma-delimited
cut -d ' ' -f 1            # first field, single-space delimited (fragile)
```

**Default to `awk` for whitespace; use `cut` for clean delimiters like commas or tabs.**

---

## The "count occurrences" pipeline

```bash
... | sort | uniq -c | sort -rn | head -10
```

Read it: sort identical lines together → count adjacent duplicates → sort numerically descending by count → take top 10.

Note: `uniq` requires sorted input — it only collapses **adjacent** duplicates.

---

# ── awk ──────────────────────────────────────────────────────────────────────

# Field variables
# $0=whole line, $1..$NF=fields, NF=field count, NR=line number

# Count occurrences by field value
awk '{counts[$9]++} END {for (k in counts) print counts[k], k}' file | sort -rn

# Sum a numeric field
awk '{sum += $10} END {print sum}' file

# Average a numeric field
awk '{sum += $10; count++} END {print sum/count}' file

# Filter by numeric condition
awk '$9 >= 500 && $9 < 600 {print}' file

# Change field separator
awk -F',' '{print $2}' file.csv

# Top-N by field value (pipe pattern)
awk '{print $1}' file | sort | uniq -c | sort -rn | head -10

# Print specific fields only
awk '{print $1, $9, $10}' file

# ── sed ──────────────────────────────────────────────────────────────────────

# Substitute (s = replace, g = all matches on line, i = case insensitive)
sed 's/foo/bar/g' file
sed -i 's/foo/bar/g' file              # in-place edit

# Delete lines
sed '/pattern/d' file                  # delete matching lines
sed '/^$/d' file                       # delete blank lines

# Print only matching lines (-n suppresses default output)
sed -n '/ERROR/p' file
sed -n '5p' file                       # print only line 5

# Anchors
sed '/^ERROR/d' file              # delete lines starting with ERROR
sed '/ERROR$/d' file              # delete lines ending with ERROR
sed '/^$/d' file                  # delete blank lines
sed 's/^/> /' file                # prepend "> " to every line
sed 's/$/;/' file                 # append ";" to every line
sed 's/^[[:space:]]*//' file      # strip leading whitespace
sed 's/[[:space:]]*$//' file      # strip trailing whitespace
sed '/^#/d' file                  # delete comment lines

# Chain multiple commands with ;
sed 's/.*\[//;s/\].*//' file           # extract between brackets

# Address ranges
sed '1,10 s/foo/bar/'                  # only lines 1-10
sed '/start/,/end/ s/foo/bar/'         # only between matching lines

# ── sort ────────────────────────────────────────────────────────────────────

sort file                              # alphabetic, ascending
sort -n file                           # numeric sort (1, 2, 10 not 1, 10, 2)
sort -rn file                          # numeric, descending — most useful for counts
sort -u file                           # sort and dedupe in one step
sort -k 2 file                         # sort by 2nd field
sort -t',' -k 3 -n file.csv            # CSV, sort by 3rd column numerically
sort -h file                           # human-readable sizes (1K, 2M, 3G)

# ── uniq ────────────────────────────────────────────────────────────────────
# CRITICAL: uniq only collapses ADJACENT duplicates. Always pre-sort.

sort file | uniq                       # dedupe (or use sort -u)
sort file | uniq -c                    # count occurrences (prefix with count)
sort file | uniq -d                    # show only duplicated lines
sort file | uniq -u                    # show only lines appearing once

# ── tr ──────────────────────────────────────────────────────────────────────
# Operates on stdin/stdout only — no file argument. Character-level only.

echo "Hello" | tr 'a-z' 'A-Z'          # uppercase
echo "Hello" | tr 'A-Z' 'a-z'          # lowercase
echo "a,b,c" | tr ',' '\n'             # commas to newlines
echo "a   b" | tr -s ' '               # squeeze repeated spaces
echo "abc" | tr -d 'b'                 # delete chars
cat file | tr -d '\r'                  # strip Windows line endings

# ── The killer pipeline ─────────────────────────────────────────────────────
# Top-N most frequent values:

awk '{print $1}' file | sort | uniq -c | sort -rn | head -10

# Pipeline shape:
#   extract field → group identical → count → rank by count → limit

# ── find ────────────────────────────────────────────────────────────────────

find PATH [predicates] [actions]       # default action is -print

# By name (glob patterns, not regex)
find . -name "*.log"                   # files ending in .log
find . -iname "*.LOG"                  # case-insensitive

# By type
find . -type f                         # regular files
find . -type d                         # directories
find . -type l                         # symbolic links

# By size (c=bytes, k=KB, M=MB, G=GB; +=greater, -=less)
find . -size +10M                      # larger than 10MB
find . -size -1k                       # smaller than 1KB
find . -size +100M -size -1G           # between 100MB and 1GB

# By time (mtime in days, mmin in minutes; -=newer than, +=older than)
find . -mtime -1                       # modified less than 1 day ago
find . -mtime +7                       # modified more than 7 days ago
find . -mmin -60                       # modified less than 60 min ago

# Combining predicates (AND is default)
find . -type f -name "*.log" -size +1M
find . -type f ! -name "*.tmp"         # NOT
find . \( -name "*.log" -o -name "*.txt" \) -type f   # OR

# ── find actions ────────────────────────────────────────────────────────────

find . -name "*.log" -delete           # delete matches (verify first without -delete)
find . -name "*.log" -exec gzip {} \;  # run command per file (slow, one at a time)
find . -name "*.log" -exec gzip {} +   # batch files into one invocation (fast)

# ── xargs ───────────────────────────────────────────────────────────────────
# Bridges stdin lines to command arguments.

find . -name "*.log" | xargs rm        # BREAKS on filenames with spaces
find . -name "*.log" -print0 | xargs -0 rm   # SAFE — null-separated

# Flags
xargs -0       # read null-separated input (use with find -print0)
xargs -n N     # max N args per command invocation
xargs -P N     # run N invocations in parallel
xargs -I {}    # use {} as placeholder for input item

# ── Common patterns ─────────────────────────────────────────────────────────

# Search inside found files
find /var/log -name "*.log" -print0 | xargs -0 grep "ERROR"

# Parallel processing
find . -name "*.log" -print0 | xargs -0 -P 4 gzip

# Per-file with placeholder
find . -name "*.log" -print0 | xargs -0 -I {} echo "Processing {}"

# Recently modified, count errors per file
find . -name "*.log" -mtime -1 -print0 | xargs -0 grep -c "ERROR"

# ── find -exec vs xargs decision ────────────────────────────────────────────
# One at a time, simple command       → -exec ... \;
# Batch many files, simple command    → -exec ... +
# Need parallelism                    → xargs -P
# Need placeholder mid-command        → xargs -I {}
# Default for production              → -print0 | xargs -0
