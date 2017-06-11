import sys
import subprocess
import re
import urllib2
import time

def run_pfam(query):
    currpath = subprocess.check_output("pwd").strip()
    call = "perl %s/Pfam/PfamScan/pfam_scan.pl -fasta %s -dir %s/Pfam/PfamScan/PfamFiles" % (currpath, query, currpath)
    return subprocess.check_output(call.split())

def get_hmmname(hmm_acc):
    url = "http://pfam.xfam.org/family/"
    url += hmm_acc

    page_reader = urllib2.urlopen(url)

    res = re.compile("Summary\: ([-/\s\w]+)")

    for line in page_reader:
        find = res.search(line)
        if find:
            return find.group(1)

    return None

def get_clanname(clan_acc):
    url = "http://pfam.xfam.org/clan/"
    url += clan_acc

    page_reader = urllib2.urlopen(url)

    init_re = re.compile("<\!-- start clan")
    final_re = re.compile("<h1>(.*)")
    #find = res.search(page_reader.read())

    start = False
    end = False

    for line in page_reader:
        if end:
            find = final_re.search(line)
            if find:
                return find.group(1)
        elif start:
            find = final_re.search(line)
            if find:
                end = True
        else:
            if init_re.search(line):
                start = True

    return None

def extract_results(query):
    query = query.strip().split("\n")[28:]
    results = {}

    for entry in query:
        entry = entry.split()
        num = re.search("\:(\w+)", entry[0]).group(1)
        try:
            results[num].append([get_hmmname(entry[5]), entry[5], get_clanname(entry[14]), entry[14], entry[12]])
        except:
            results[num] = [[get_hmmname(entry[5]), entry[5], get_clanname(entry[14]), entry[14], entry[12]]]

    return results

if __name__ == "__main__":
    result = extract_results(run_pfam(sys.argv[1]))

    for key in result:
        print key, result[key]
