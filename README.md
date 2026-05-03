# platform-prep-scripts

A collection of bash and Python utility scripts for log parsing, system debugging, and production analysis. Built as part of a structured platform engineering interview preparation track.

## Purpose

This repository serves three goals:
- Build muscle memory for solving interview-style scripting problems under time pressure
- Maintain a reusable toolkit of small, single-purpose utilities
- Document the layered debugging frameworks used in container and Kubernetes troubleshooting

## Structure

- `scripts/` — Reusable bash and Python utilities
- `articulation/` — Notes for verbal explanation of Linux and debugging concepts
- `logs/` — Sample log files for testing and drills
- `daily-log.md` — Working log of practice sessions
- `INDEX.md` — Catalog of scripts with descriptions and usage

## Conventions

- Bash scripts use `#!/usr/bin/env bash` with `set -euo pipefail`
- Python scripts target Python 3.11+ stdlib only (no pandas, no third-party deps)
- All scripts accept input via either a file argument or stdin
- All scripts output to stdout; errors to stderr

## License

MIT — see LICENSE file.
