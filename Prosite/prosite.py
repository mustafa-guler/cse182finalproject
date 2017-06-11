#!/usr/bin/python

import getregex
import subprocess
import getopt
import sys
import time
import re

ERROR = "\n" + "=" * 69
ERROR += "\nERROR\n\n";
END_ERROR = "\n" + "=" * 69 + "\n"

USAGE = """\nUSAGE
    prosite.py -q [query]

FLAGS
    -h/--help       prints this message
    -q/--query      the query you're searching for [REQUIRED]
    -v/--verbose    increases verbosity (prints status messages)
    """

query_name = None
verbose = False


def get_input():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hvq:", ["help", "verbose", "query="])
    except getopt.GetoptError as fail:
        print >> sys.stderr, ERROR, str(fail), END_ERROR
        print USAGE
        sys.exit(2)

    if not opts:
        print USAGE
        sys.exit(2)

    for o, a in opts:
        if o in ["-h", "--help"]:
            print >> sys.stderr, USAGE
            sys.exit(0)
        elif o in ["-q", "--query"]:
            query_name = a
        elif o in ["-v", "--verbose"]:
            verbose = True


    if not query_name:
        print >> sys.stderr, ERROR, "-q flag requried to run", END_ERROR
        print USAGE
        sys.exit(2)

    try:
        open(query_name)
    except IOError as fail:
        print >> sys.stderr, ERROR, str(fail), END_ERROR
        sys.exit(1)

    return query_name


def run_prosite(query):
    currpath = subprocess.check_output("pwd").strip()
    conf = "full (no high probability matches, cutoff = 0)"

    if verbose:
        print >> sys.stderr, "Trying Ideal Prosite Call..."
    call = "perl %s/Prosite/ps_scan/ps_scan.pl -s -d %s/Databases/prosite.dat %s" % (currpath, currpath, query)
    result = subprocess.check_output(call.split())

    if not result:
        if verbose:
            print >> sys.stderr, "...Failure :("
            time.sleep(1)
            print >> sys.stderr, "Allowing Lower Cutoff..."
        call = "perl %s/Prosite/ps_scan/ps_scan.pl -s -l -1 -d %s/Databases/prosite.dat %s" % (currpath, currpath, query)
        result = subprocess.check_output(call.split())

        if result:
            if verbose:
                print >> sys.stderr, "...Success!"
            conf = "some (no high probability matches, cutoff = -1)"
    elif verbose:
        print >> sys.stderr, "...Success!"

    if not result:
        if verbose:
            print >> sys.stderr, "...Failure Again :'("
            time.sleep(1)
            print >> sys.stderr, "Allowing High Probability Matches..."
        call = "perl %s/Prosite/ps_scan/ps_scan.pl -d %s/Databases/prosite.dat %s" % (currpath, currpath, query)
        result = subprocess.check_output(call.split())

        if result:
            if verbose:
                print >> sys.stderr, "...Success - Results May Be Inconclusive"
            conf = "little (high probability results allowed)"

    if not result:
        if verbose:
            print >> sys.stderr, "...Total Failure - No Prosite Matches Available"
        conf = "none (no results at all)"

    return result, conf


def extract_results(result):
    ps_patt = "(\S*) : (PS[0-9]{5}) [\d\_A-Z]* ([\w\- \(\)]*)\."
    info = re.findall(ps_patt, result)

#    regexes = []
#    prot_funcs = []
    results = []

    for entry in info:
#        if entry[0] in results:
#            results[entry[0]].append((entry[2], getregex.get_regex(entry[1])))
#        else:
#            results[entry[0]] = [(entry[2], getregex.get_regex(entry[1]))]
#        regexes.append(getregex.get_regex(entry[1]))
#        prot_funcs.append(entry[2])
#        try:
#            results[num[1:]].append((entry[2], getregex.get_regex(entry[1])))
#        except:
#            results[num[1:]] = [(entry[2], getregex.get_regex(entry[1]))]
       results.append((entry[2], entry[1])) #getregex.get_regex(entry[1]))) 

#    return ",".join(prot_funcs), regexes
    return results




if __name__ == "__main__":
    result, conf = run_prosite(get_input())
    results = extract_results(result)
    print "Confidence: ",conf
    print results


#    print funcs
#
#    for regx in regexes:
#        print regx




#if first:
#    print first
#else:
#    print "fail"
#
#second = subprocess.check_output(["perl", "./ps_scan/ps_scan.pl","-s","-l","1","-d", "prosite.dat", "out"])
#if second:
#    print "Allowing 1 mismatch"
#    print second
#else:
#    print "Failed, do not ignore high probability matches"
#    third = subprocess.check_output(["perl", "./ps_scan/ps_scan.pl","-l","1","-d","prosite.dat","out"])
#
