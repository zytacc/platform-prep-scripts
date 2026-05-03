#!/usr/bin/env python3
"""
Generate a realistic log directory fixture for file-manipulation drills.

Creates ~/code/platform-prep-scripts/logs/fixtures/<date>/ with a mix of:
  - Standard service logs (clean cases)
  - Edge cases: empty files, files with spaces, files with no extension,
    permission-restricted files, stale files, files with unusual encodings,
    nested directories, dangling symlinks, hidden files, mixed case names

Usage:
    python3 logs/generate_fixtures.py [date]   # defaults to today
    python3 logs/generate_fixtures.py 2026-04-30

Re-run safely; it cleans the target date directory before regenerating.
"""

import os
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

ROOT = Path(__file__).parent / "fixtures"

SERVICES = ["nginx", "postgres", "redis", "app", "worker", "auth", "billing"]
LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"]


def random_log_lines(n=50, error_rate=0.1):
    lines = []
    for i in range(n):
        ts = (datetime.now() - timedelta(minutes=n - i)).strftime("%Y-%m-%d %H:%M:%S")
        level = random.choices(LEVELS, weights=[60, 20, int(error_rate * 100), 10])[0]
        lines.append(f"{ts} [{level}] event_id={random.randint(1000, 9999)} message=sample log entry {i}\n")
    return lines


def write_log(path: Path, lines, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines))
    path.chmod(mode)


def build_fixture(target_date: str):
    day_dir = ROOT / target_date
    if day_dir.exists():
        # Reset permissions in case prior run left restricted files
        for p in day_dir.rglob("*"):
            try:
                p.chmod(0o644)
            except Exception:
                pass
        shutil.rmtree(day_dir)
    day_dir.mkdir(parents=True)

    # ---- Clean cases ----
    write_log(day_dir / "nginx.log", random_log_lines(80, error_rate=0.05))
    write_log(day_dir / "postgres.log", random_log_lines(60, error_rate=0.15))
    write_log(day_dir / "app.log", random_log_lines(100, error_rate=0.20))
    write_log(day_dir / "redis.log", random_log_lines(40, error_rate=0.02))
    write_log(day_dir / "worker.log", random_log_lines(70, error_rate=0.30))

    # ---- Edge case 1: Empty file ----
    write_log(day_dir / "billing.log", [])

    # ---- Edge case 2: File with spaces in name ----
    write_log(day_dir / "auth service.log", random_log_lines(30, error_rate=0.40))

    # ---- Edge case 3: File with no extension ----
    write_log(day_dir / "cron_output", random_log_lines(20, error_rate=0.10))

    # ---- Edge case 4: Mixed case (Linux is case-sensitive!) ----
    write_log(day_dir / "App.log", random_log_lines(15, error_rate=0.05))
    write_log(day_dir / "APP.LOG", random_log_lines(10, error_rate=0.05))

    # ---- Edge case 5: Hidden file ----
    write_log(day_dir / ".systemd.log", random_log_lines(25))

    # ---- Edge case 6: File ending in .log.1 (rotated) ----
    write_log(day_dir / "nginx.log.1", random_log_lines(200, error_rate=0.10))
    write_log(day_dir / "nginx.log.2.gz", [])  # already-rotated, gzipped (fake — empty)

    # ---- Edge case 7: Nested directory (deep logs) ----
    nested = day_dir / "subsystem" / "deep"
    write_log(nested / "deep_app.log", random_log_lines(35, error_rate=0.50))

    # ---- Edge case 8: Restricted permissions ----
    restricted = day_dir / "secret.log"
    write_log(restricted, random_log_lines(20))
    restricted.chmod(0o600)  # readable only by owner — usually fine, but worth noticing

    # ---- Edge case 9: Symlink (valid) ----
    target = day_dir / "app.log"
    link = day_dir / "current_app.log"
    if link.exists() or link.is_symlink():
        link.unlink()
    link.symlink_to(target.name)

    # ---- Edge case 10: Dangling symlink (target doesn't exist) ----
    dangling = day_dir / "missing.log"
    if dangling.exists() or dangling.is_symlink():
        dangling.unlink()
    dangling.symlink_to("does_not_exist.log")

    # ---- Edge case 11: File with only whitespace/blank lines ----
    write_log(day_dir / "blank.log", ["\n", "   \n", "\t\n", "\n"])

    # ---- Edge case 12: Non-UTF8 bytes (latin-1 encoded with special chars) ----
    weird = day_dir / "encoded.log"
    weird.write_bytes("Café opened\nNaïve user\n".encode("latin-1"))

    # ---- Edge case 13: Very small file (1 line, no newline) ----
    (day_dir / "tiny.log").write_text("only one line no newline at end")

    # ---- Edge case 14: Filename with weird characters ----
    write_log(day_dir / "log-with-dash.log", random_log_lines(10))
    write_log(day_dir / "log_with_underscore.log", random_log_lines(10))
    write_log(day_dir / "log.with.dots.log", random_log_lines(10))

    # ---- Edge case 15: File that LOOKS like a log but isn't ----
    (day_dir / "README.log").write_text(
        "This is not a real log file. It's documentation that happens to end in .log.\n"
        "Your script should handle this gracefully.\n"
    )

    return day_dir


def main():
    date_arg = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    # Validate date format
    try:
        datetime.strptime(date_arg, "%Y-%m-%d")
    except ValueError:
        print(f"Invalid date: {date_arg}. Expected YYYY-MM-DD.", file=sys.stderr)
        sys.exit(1)

    out = build_fixture(date_arg)
    print(f"Built fixture: {out}")
    print(f"\nFiles created:")
    for p in sorted(out.rglob("*")):
        if p.is_file() or p.is_symlink():
            kind = "symlink" if p.is_symlink() else "file"
            try:
                size = p.stat().st_size
            except (FileNotFoundError, OSError):
                size = "?"
            rel = p.relative_to(out)
            print(f"  [{kind:7}] {rel}  ({size} bytes)")


if __name__ == "__main__":
    main()
