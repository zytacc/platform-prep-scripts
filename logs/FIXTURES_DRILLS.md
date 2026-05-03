# File-Handling Drill Bank

Practice drills using `logs/fixtures/<date>/`. These mimic the kind of file-manipulation problems asked in trading firm and infrastructure interviews. The CTC-style problem from 2 years ago is the prototype.

## Drill rules

- **Time-box every drill**. If the prompt says 30 min, set a timer.
- **Write the script before testing it**. Read the prompt, plan, then code.
- **Edge cases are graded harder than happy path**. Always ask: what if the file doesn't exist? What if it's empty? What if there are zero matches? What if permissions deny access?
- **Use `set -euo pipefail`** in every bash script. It's the single biggest signal of production-aware scripting.
- **No AI, no Stack Overflow during the drill**. `man` pages and `--help` are allowed.

## Edge cases present in every fixture

| # | Edge case | Why it matters |
|---|-----------|----------------|
| 1 | Empty files | Many commands fail or produce wrong results on empty input |
| 2 | Filenames with spaces | Naive `for f in $(ls)` breaks; need `find ... -print0` or quoting |
| 3 | Files with no extension | Glob patterns like `*.log` miss them |
| 4 | Mixed case | Linux is case-sensitive; `App.log` ≠ `app.log` |
| 5 | Hidden files (.dotfiles) | Default globs skip them |
| 6 | Rotated logs (.1, .2.gz) | Need to decide: include or exclude? |
| 7 | Nested directories | `find` vs `ls` matters |
| 8 | Restricted permissions | Script must handle "Permission denied" without crashing |
| 9 | Valid symlinks | Following them is usually correct |
| 10 | Dangling symlinks | Reading them throws errors |
| 11 | Whitespace-only files | Look "non-empty" by size but have no content |
| 12 | Non-UTF8 encoding | Python `open()` with default encoding crashes |
| 13 | Files without trailing newline | `wc -l` undercounts |
| 14 | Weird filename characters | Need careful quoting |
| 15 | Misleading extensions | A `.log` file might be documentation |

## Drill scenarios

### Drill A — Daily log triage (30 min, bash)
**Prompt**: Write a bash script `daily_triage.sh` that takes a date directory as an argument (e.g., `./daily_triage.sh logs/fixtures/2026-05-03`) and produces a report with:
- Total number of log files found
- Total disk space used by logs
- For each `*.log` file: line count and ERROR count
- A list of empty files (zero bytes or whitespace-only)
- A list of files modified in the last hour

**Edge cases to handle**: spaces in filenames, dangling symlinks, restricted files, hidden logs (decide your policy and document it).

---

### Drill B — Log rotator (45 min, bash)
**Prompt**: Write `rotate_logs.sh` that for each `*.log` file in a given directory:
- If the file is larger than 1KB, rename it to `<name>.log.1` (overwriting any existing `.1`, but only after moving the existing `.1` to `.2`, etc., up to `.5`; older are deleted)
- After rotation, create a new empty `<name>.log` with the same permissions as the old one
- Skip files that don't exist, are symlinks, or have permission problems
- Print a summary of what was rotated, skipped, and why

**Edge cases**: symlinks (skip them), permission-restricted files (warn, don't crash), files with spaces, nested logs (decide: rotate them or only top level?).

---

### Drill C — Error extractor (30 min, Python)
**Prompt**: Write `extract_errors.py` that scans every log-like file in a given directory tree and produces a CSV summary:
- Columns: `file_path`, `error_count`, `last_error_timestamp`, `sample_message`
- Detect "ERROR" entries case-insensitively
- Skip binary files, empty files, and files with non-UTF8 encoding (log them to stderr)
- Sort output by `error_count` descending

**Edge cases**: encoding errors (use `errors='replace'`), permission errors (try/except), files with no errors (include with count=0 or skip — your choice, document it).

---

### Drill D — Stale file cleanup (20 min, bash or Python)
**Prompt**: Write a script that finds log files older than N days (parameter) in a directory and:
- Lists them with size
- Prompts for confirmation (or accepts a `--force` flag) before deleting
- Refuses to delete symlinks
- Refuses to delete anything outside the target directory (security check)
- Logs all deletions to a separate audit file

**Edge cases**: symlinks, files modified by `touch -t` to a fake time, the target directory itself being a symlink.

---

### Drill E — Combined (45 min, language of choice)
**Prompt**: A "daily log review" script that:
1. Takes a date directory as input
2. Validates the directory exists and is readable
3. Reports: total files, files by type (.log, .gz, no extension, other)
4. For each `.log` file: top 3 ERROR messages with counts
5. Identifies any files matching pattern `secret*` or `.systemd*` and warns (don't read them)
6. Outputs a final markdown summary file in the same directory: `daily_summary_<date>.md`

**Edge cases**: every single one above. This is the closest analog to the CTC-style problem.

---

## How to test your edge case handling

After writing your script, deliberately break the input to see if your script survives:

```bash
# Generate a fresh fixture
python3 logs/generate_fixtures.py 2026-05-03

# Test with the fixture
./your_script.sh logs/fixtures/2026-05-03

# Test with a non-existent directory
./your_script.sh /tmp/does_not_exist

# Test with a directory you can't read
sudo mkdir /tmp/restricted && sudo chmod 000 /tmp/restricted
./your_script.sh /tmp/restricted
sudo rmdir /tmp/restricted

# Test with no arguments
./your_script.sh
```

A robust script handles all four without crashing. A script that only handles case 1 is the "4/10" outcome.

