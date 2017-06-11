import sys

from fastxpy import fasta
import tempfile
import re

sys.path.append("Prosite/")
sys.path.append("Pfam/")
sys.path.append("Blast/")
sys.path.append("Prints/")
import prosite
import pfam
import blast
import prints

import multiprocessing as mp
from multiprocessing import Pool

cpus = mp.cpu_count()

data = fasta.fa(sys.argv[1])
results = {}
pro_head = ["Prosite Hits", "Prosite Confidence", "Prosite Codes"]
pfam_head = ["Pfam Hits", "Pfam Codes", "Pfam Clan Names", "Pfam Clan Numbers", "Pfam E-vals"]
blast_head = ["Blast Hits", "Blast E-vals"]
prints_head = ["Prints Hits", "Print Codes"]
headers = ["Accession Number"] + pro_head + pfam_head + blast_head + prints_head

done = False

while not done:
    seq = data.readseq()
    if not seq:
        done = True
        break
    currheader = re.search("\:(\w+)", seq.split("\n")[0]).group(1)
    results[currheader] = []

    temp = tempfile.NamedTemporaryFile()
    temp.write(seq)
    temp.seek(0)

    runner = Pool(cpus)

    pro_res = runner.apply_async(prosite.run_prosite, args=(temp.name,))
    pfam_res = runner.apply_async(pfam.run_pfam, args=(temp.name, ))
    prints_res = runner.apply_async(prints.run_prints, args=(temp.name,))
    blast_res = runner.apply_async(blast.run_blast, args=(temp.name,))

    pfam_call = runner.apply_async(pfam.extract_results, args=(pfam_res.get(),))

    blastfile = open("blast_hits/%s_raw.txt" % currheader, "w+")
    blast_res = blast_res.get()
    blastfile.write(blast_res);
    blastfile.close();


    blast_call = runner.apply_async(blast.extract_results, args=(blast_res,))
    pro_res = pro_res.get()
    pros = runner.apply_async(prosite.extract_results, args=(pro_res[0],))
    pros_conf = str(pro_res[1])

    runner.close()
    runner.join()

    pros = pros.get()
    pfam_call = pfam_call.get()
    blast_call = blast_call.get()
    prints_res = prints_res.get()


    if pros:
        pro_hit = [pros[i][0] for i in range(len(pros))]
        pro_code = [pros[i][1] for i in range(len(pros))]
    else:
        pro_hit = ["noresult"]
        pro_code = ["noresult"]

    if prints_res[0]:
        prints_hits = prints_res[0]
        prints_codes = prints_res[1]
    else:
        prints_hits = ["noresult"]
        prints_codes = ["noresult"]

    if blast_call:
        blast_hits = blast_call[0]
        blast_eval = blast_call[1]
    else:
        blast_hits = ["noresult"]
        blast_eval = ["noresult"]

    if pfam_call.keys():
        key = pfam_call.keys()[0]
        pfam_hits = []
        pfam_codes = []
        pfam_clans = []
        pfam_clannum = []
        pfam_eval = []
        for lis in pfam_call[key]:
            lis = map(str, lis)
            pfam_hits.append(lis[0])
            pfam_codes.append(lis[1])
            pfam_clans.append(lis[2])
            pfam_clannum.append(lis[3])
            pfam_eval.append(lis[4])
        pfam_all = [",".join(pfam_hits), ",".join(pfam_codes), ",".join(pfam_clans), ",".join(pfam_clannum), ",".join(pfam_eval)]
    else:
        pfam_all = ["noresult"] * 5

    results[currheader] += [",".join(pro_hit), pros_conf, ",".join(pro_code)]
    results[currheader] += pfam_all
    results[currheader] += [",".join(blast_hits), ",".join(blast_eval)]
    results[currheader] += [",".join(prints_hits), ",".join(prints_codes)]

    temp.close()



print "\t".join(headers)
for key in results:
    to_print = key
    for entry in results[key]:
        to_print += "\t" + entry
    print to_print
