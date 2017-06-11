#!/usr/bin/python

import sys
import json

prosite = [1,2,3]
pfam = [4,5,6,7,8]
blast = [9,10]
prints = [11, 12]
notes = [13,14,15]

data = []

with open(sys.argv[1], "r") as f:
    headers = f.readline().strip().split("\t")

    for line in f:
        data.append(line.strip().split("\t"))

for i in range(len(headers)):
    headers[i] = "_".join(headers[i].split())


jsondicts = []

for line in data:
    currdict = {}
    currdict[headers[0]] = line[0]
    currdict["Blast"] = {}
    currdict["Pfam"] = {}
    currdict["Prints"] = {}
    currdict["Prosite"] = {}
    currdict["Hand Notes"] = {}

    for index in blast:
        currdict["Blast"][headers[index]] = line[index].split(",")
    for index in pfam:
        currdict["Pfam"][headers[index]] = line[index].split(",")
    for index in prints:
        currdict["Prints"][headers[index]] = line[index].split(",")
    for index in prosite:
        currdict["Prosite"][headers[index]] = line[index].split(",")
    for index in notes:
        currdict["Hand Notes"][headers[index]] = line[index]

    jsondicts.append(currdict)
    

print json.dumps(jsondicts, separators=(",", ":"), indent=4, sort_keys=True)
