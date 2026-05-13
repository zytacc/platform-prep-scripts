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

