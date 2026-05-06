# ============ Warmup re-do drill — Mon May 4 ============
# Task: Count the total number of lines in logs/syslog.log.
#
# Rules:
#   - Use line-by-line iteration (don't use readlines() — that loads the whole file into memory)
#   - Print the total line count at the end
#
# Allowed: articulation/python-cheatsheet.md (your own notes)
# Not allowed: python_basics.py from yesterday, internet, AI
#
# Yesterday's bug to avoid: don't confuse "the last line's value" with "count of iterations"
#
# Start your timer. Write below:
linecount=0
with open("logs/syslog.log") as f:
    for line in f:
        linecount += 1
print (linecount) 