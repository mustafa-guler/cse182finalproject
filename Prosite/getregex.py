#!/usr/bin/python

import urllib
from HTMLParser import HTMLParser
import sys
import getopt

ERROR = "\n" + "=" * 69
ERROR += "\nERROR\n\n";
END_ERROR = "\n" + "=" * 69 + "\n"

USAGE = """\nUSAGE
    getregex -p [prosite code]

FLAGS
    -h/--help       prints this message
    -p/--prodocde   REQUIRED: the prosite code for the protein
    """
procode = None
page_text = []


class print_page(HTMLParser):
    def handle_data(self, data):
        global page_text
        if not data == "\n":
            page_text.append(data.strip())


def get_input():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hp:", ["help", "procode="])
    except getopt.GetoptError as fail:
        print >> sys.stderr, ERROR, str(fail), END_ERROR
        print USAGE
        sys.exit(2)

    if not opts:
        print USAGE
        sys.exit()

    for o, a in opts:
        if o in ["-h", "--help"]:
            print usage
            sys.exit()
        elif o in ["-p", "--procode"]:
            procode = a;

    if not procode:
        print >> sys.stderr, ERROR, "-p flag required to run", END_ERROR
        print USAGE
        sys.exit(2)

    return procode


def get_regex(prosite_code):
    url = "http://prosite.expasy.org/cgi-bin/prosite/nicedoc.pl?"
    url += prosite_code

    handle = urllib.urlopen(url)
    page = handle.read()

    page_printer = print_page()
    page_printer.feed(page)
    page_printer.close()

    global page_text

    found = False
    for line in page_text:
        if "Consensus" in line:
            found = True
            continue
        elif "Error:" in line:
            print >> sys.stderr, ERROR, "this prosite code is not real", END_ERROR
            sys.exit(1)
        if found:
            page_text = []
            return line
            break

if __name__ == "__main__":
    print get_regex(get_input())
