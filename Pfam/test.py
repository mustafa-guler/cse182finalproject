import urllib
import sys
import re

def get_hmmname(hmm_ass):
    url = "http://pfam.xfam.org/family/"
    url += hmm_ass

    page_reader = urllib.urlopen(url)

    res = re.compile("Summary\: ([\s\w]+)")

    for line in page_reader:
        find = res.search(line)
        if find:
            return find.group(1)

    return None


result = get_hmmname("PF00809")
print result
