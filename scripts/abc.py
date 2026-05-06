from collections import Counter
import re

c = Counter()
with open("logs/access.log") as f:
    for line in f:
        match = re.search(r'"(\w+) (\S+) HTTP',line)
        if match:
            path = match.group(2)
            c[path] += 1

for match, count in c.most_common(3):
    print(f"{match}: {count}")

#   /api/products: 5234
#   /health:       4187
#   /api/users:    3050