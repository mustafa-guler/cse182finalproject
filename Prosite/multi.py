import prosite

f = open("testresult", "r")

result = f.read()
print result

res = prosite.extract_results(result)

for key in res:
    print key, ": ",res[key]
