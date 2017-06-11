import sys
import re

go = {}
on_id = False
on_name = False

with open(sys.argv[1]) as f:
    currid = ""
    for line in f:
        if line.strip() == "[term]":
            on_id = True
        elif on_id:
            currid = re.search(" .*", line.strip()).group().strip()
            go[currid] = []
            on_id = False
            on_name = True
        elif on_name:
            go[currid].append(re.search(" .*", line.strip()).group().strip())
            on_name = False
        elif line.strip() and line.split()[0] == "synonym:":
            go[currid].append(re.search("\"(.*?)\"", line.strip()).group(1))

queries = []
with open(sys.argv[2]) as f:
    f.readline()
    for line in f:
        queries.append(line.strip())
count = 1
for query in queries:
    print ">",count,query
    for key in go.keys():
        for e in go[key]:
            q = query.split()
            for a in q:
                if a in e:
                    print key, e
                    continue
    count += 1
    print
