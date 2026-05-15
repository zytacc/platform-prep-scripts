# Python Cheatsheet — Working Subset for Log Parsing

Living document. Each time I look up syntax during a drill, it goes here. Reviewed before the next session. As recall improves, items shift from "look it up" to "internalized" — but they stay in the doc as a marker of progress.

---

## File I/O

### The standard pattern: line-by-line iteration
```python
with open("path/to/file") as f:
    for line in f:
        line = line.rstrip()    # remove trailing \n
        # do work with line
```
- `with` auto-closes the file. Always use it.
- Line-by-line iteration is memory-efficient. Works on huge files.
- `line.rstrip()` removes trailing whitespace including `\n`. Only call it when you actually use the line content.

### When you need just one line
```python
with open(path) as f:
    first = f.readline()        # one line
print(first.rstrip())
```

### When you need all lines as a list (small files only)
```python
with open(path) as f:
    lines = f.readlines()       # loads whole file into memory
```

### Counting lines
```python
# Way 1: counter variable
count = 0
with open(path) as f:
    for line in f:
        count += 1

# Way 2: enumerate (use when you need both index and value)
with open(path) as f:
    for i, line in enumerate(f, start=1):
        if "ERROR" in line:
            print(f"{i}: {line.rstrip()}")
```

---

## Lists

```python
items = ["a", "b", "c"]

len(items)              # 3
items[0]                # 'a' — first
items[-1]               # 'c' — last
items[0:2]              # ['a', 'b'] — slice
items[-2:]              # ['b', 'c'] — last two

items.append("d")       # add to end

for item in items:
    print(item)
```

---

## Dicts

```python
counts = {}
counts["foo"] = 1
counts["bar"] = 2

counts["foo"]                # 1
"foo" in counts              # True
len(counts)                  # 2

# Iterate
for key, value in counts.items():
    print(f"{key} -> {value}")

# Increment-or-init pattern (the one I always need)
counts[key] = counts.get(key, 0) + 1

# Or the if/else version (more verbose)
if key in counts:
    counts[key] += 1
else:
    counts[key] = 1
```

---

## Sets — for unique collections

```python
unique = set()
unique.add("foo")
unique.add("foo")           # no-op, already there

"foo" in unique             # True, O(1)
len(unique)

for item in unique:
    print(item)

# Build from a list (deduplicates automatically)
unique = set(["a", "b", "a", "c"])    # {'a', 'b', 'c'}
```

**Important**: `{}` alone is an empty dict, NOT an empty set. Use `set()` for empty.

---

## Counter — for "count things, find top N"

```python
from collections import Counter

# Build from any iterable
c = Counter(["a", "b", "a", "c", "a"])
print(c)                        # Counter({'a': 3, 'b': 1, 'c': 1})

# Top N — the killer feature
c.most_common(3)                # [('a', 3), ('b', 1), ('c', 1)]
c.most_common(1)                # just the winner

# Manual increment (when streaming items)
c = Counter()
c["foo"] += 1
print(c["never_seen"])          # 0 — no KeyError, unlike regular dict

# Build from a generator (idiomatic for files)
with open(path) as f:
    c = Counter(line.split()[0] for line in f)
```

---

## f-strings — string formatting

```python
name = "Elton"
year = 2026

f"{name}"                       # 'Elton'
f"{name} -> {year}"             # 'Elton -> 2026'
f"{number:.2f}"                 # 2 decimal places
f"{number:>10}"                 # right-align in 10 chars
```

Always prefer f-strings over older `.format()` or `%` formatting.

---

## Regex (re module)

### Imports and basic usage
```python
import re

# search() — find first match, returns Match or None
m = re.search(r"\d+", "abc 123")
if m:
    print(m.group())            # '123'

# findall() — all non-overlapping matches as a list
re.findall(r"\d+", "1 and 2 and 3")    # ['1', '2', '3']

# Always use raw strings (r"...") for patterns
```

### Common metacharacters
| Pattern | Matches |
|---------|---------|
| `\d` | a digit (0-9) |
| `\w` | a word character (letters, digits, underscore) |
| `\s` | whitespace |
| `\S` | non-whitespace |
| `.` | any character except newline |
| `+` | one or more |
| `*` | zero or more |
| `?` | zero or one |
| `{3}` | exactly 3 |
| `{2,5}` | between 2 and 5 |
| `[A-Z]` | uppercase letters |
| `[^abc]` | NOT a, b, or c |
| `^` / `$` | start / end of string |
| `\.` `\[` `\]` | literal dot, bracket (escaped) |

### Patterns I use most
```python
r"\d+"                          # one or more digits
r"\d+\.\d+\.\d+\.\d+"           # IPv4 (basic)
r"\w+"                          # word chars
r"\s+"                          # whitespace
r"\[(\d+)\]"                    # number inside brackets — group 1 = number
r'"([^"]+)"'                    # text inside double quotes — group 1 = contents
r'"(\w+) (\S+) HTTP'            # method (group 1) and path (group 2) from access log
```

### Capture groups
```python
m = re.search(r'"(\w+) (\S+) HTTP', line)
if m:
    method = m.group(1)         # first paren group
    path = m.group(2)           # second paren group
    # or unpack all at once:
    method, path = m.groups()   # tuple of all groups
```

**Rules:**
- `group(0)` (or `group()`) = full match
- `group(1)`, `group(2)`, ... = parenthesized groups, numbered left to right
- `groups()` (with `s`) = tuple of all groups
- Always check `if m:` before calling `.group()` — `None.group()` crashes

### Big lesson: describe by surroundings, not internals
When extracting something with variable shape (like a URL path), don't enumerate every legal internal character. Anchor by what surrounds it.

```python
# Brittle — breaks on any new path shape
re.search(r'/\w+(/\w+)?(/\d+)?', line)

# Durable — anchors by context
re.search(r'"(\w+) (\S+) HTTP', line).group(2)
```

`\S+` ("non-whitespace") is more flexible than enumerating URL characters.

### Build patterns incrementally
```python
# When writing a regex, test as you go
print(re.search(r"\d+", line).group())              # '10'
print(re.search(r"\d+\.\d+", line).group())         # '10.0'
print(re.search(r"\d+\.\d+\.\d+\.\d+", line).group())  # '10.0.87.137'
```

---

## .split() vs .split(" ")

```python
"a  b".split()              # ['a', 'b']     — collapses any whitespace
"a  b".split(" ")           # ['a', '', 'b'] — strict single-space

# Default to .split() with no argument unless you specifically need single-space behavior
```

---

## Loop Patterns I Mixed Up Once

### Counting iterations vs. measuring last value
```python
# WRONG: len(line) at the end is the LAST line's character count
for line in f:
    line = line.rstrip()
print(len(line))            # bug — measures one line, not all

# RIGHT: count iterations
count = 0
for line in f:
    count += 1
print(count)
```

---

## Style Notes

- `print(value)` — no space between function name and paren
- Plural names for collections: `hostnames = set()` not `hostname = set()`
- Don't `rstrip()` lines you're not reading the content of
- Use the loop variable directly: `for ip, count in counts.items(): print(count)` — don't re-fetch with `counts[ip]`
- Always guard `re.search` results: `if match:` before `.group()`

---

## Things I've Looked Up

_(Append here every time you reach for documentation. When something stops needing lookup, leave it as a marker of progress.)_

- Day 3: capture group syntax `r'(...)'` — internalized after drill 1
- Day 3: `.split()` empty-string edge case with explicit delimiter
- Day 4: regex bracket escaping `\[ \]` — internalized after drill 2

## Day 11 — File I/O, CLI, JSON

### Default file read pattern

```python
import sys

with open(sys.argv[1]) as f:
    for line in f:
        line = line.rstrip()
        # process line
```

This handles ~90% of coding rounds. Don't forget `.rstrip()`.

### JSON-lines parsing

```python
import json

with open(sys.argv[1]) as f:
    for line in f:
        line = line.rstrip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        status = record.get('status')
        # use record
```

Key rules:
- `json.loads(line)` inside the loop — the `s` is for "string"
- `record.get(key)` not `record[key]` — logs have inconsistent fields
- Skip malformed lines with `continue`; don't crash the whole script

### Format check

```bash
head -1 path/to/file
```

Line starts and ends with `{...}` → JSON-lines, use `loads` in a loop.
Line is just `[` or `{` with no close → one document, use `json.load(f)`.

### Top anti-patterns

| Don't | Do |
|---|---|
| `f.readlines()` to iterate | `for line in f:` |
| `json.load(f)` on JSON-lines | `json.loads(line)` in a loop |
| `record['key']` on log data | `record.get('key')` |