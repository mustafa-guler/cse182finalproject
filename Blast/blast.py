#!/usr/bin/python
import re
import getopt
import sys
import subprocess
import time
ERROR = "\n" + "=" * 69
ERROR += "\nERROR\n\n";
END_ERROR = "\n" + "=" * 69 + "\n"

USAGE = """\nUSAGE
    blast.py -q [query]

FLAGS
    -h/--help       prints this message
    -q/--query      the query you're searching for [REQUIRED]
    -s psiblast
    -d delta blast
    -h help
    """

call = "blastp"

def get_input():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hsdq:", ["help", "psiblast", "deltablast", "query="])
    except getopt.GetoptError as fail:
        print >> sys.stderr, ERROR, str(fail), END_ERROR
        print USAGE
        sys.exit(2)

    if not opts:
        print USAGE
        sys.exit(2)

    global call
    query_name = None

    for o, a in opts:
        if o in ["-h", "--help"]:
            print >> sys.stderr, USAGE
            sys.exit(0)
        elif o in ["-s", "--psiblast"]:
            call = "psiblast"
        elif o in ["-d", "--deltablast"]:
            call = "deltablast"
        elif o in ["-q", "--query"]:
            query_name = a
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

def run_blast(query):
    global call
   #queries the website directly
    currpath = subprocess.check_output("pwd").strip()
    #blast_call = "./Blast/blast/%s -query %s -db Databases/blast/nr -num_threads 8" % (call, query)
    blast_call = "./Blast/blast/%s -query %s -db nr -remote" % (call, query)
    result = subprocess.check_output(blast_call.split())
    #print result
    return result

def extract_results(data):
    e_val=[]
    name=[]

    data = data.splitlines()
    title = re.compile("\>[\w\.]+ ([\-\:\w\s\,\[\]]+)$")
    e_re = re.compile(" [\=\w\s\(\)]+\,  Expect = ([\.\-\w]+)\,")

    looking_title = True
    need_next = False
    match = ""

    for line in data:
        if need_next:
            match += line.strip()
            name.append(match)
            need_next = False
            continue

        if looking_title:
            tit = title.search(line)
            if tit:
                looking_title = False
                match = tit.group(1)
                if not "]" in match:
                    need_next = True
                    continue
                else:
                    name.append(match)
        else:
            match = e_re.search(line)
            if match:
                e_val.append(match.group(1))
                looking_title = True


        if len(e_val) >= 10:
            break

    return name, e_val

#    return [(name[i], e_val[i]) for i in range(len(e_val))]



#   splitresult=result.splitlines()
#   for line in splitresult:
#      line=line.strip()
#      if len(evalue) < 10:
#         m=re.findall('[]{2}[0-9]e-[0-9]*',line)
#         if len(m) > 0:
#            if float((m[0]))<1:
#               evalue.append((m[0]))
#               seq_count+=1
#            else:
#               break
#         eindex+=1
#      else:
#         break
#   for line in splitresult[index:]:
#      if line and line[0]==">":
#         if not seq_count2 == seq_count:
#            name.append(line)
#            seq_count2+=1
#         else:
#            break
   #print name
   #print evalue
#   final=[(name[i],evalue[i]) for i in range(len(name))]
#   return final


if __name__ == "__main__":
    f = open(sys.argv[1])
    print extract_results(f.read())
#   start=time.time()
#   inputs=get_input()
#   ans = run_blast(inputs)
#   print "blast time", time.time() - start
#   start = time.time()
#   result = extract_results(ans)
#   print time.time()-start
#   print result
#
