from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import re
import urllib

def run_prints(arg1):
    seqs = []
    with open(arg1) as f:
        f.readline()
        for line in f:
            seqs.append(line.strip())

    driver = webdriver.PhantomJS()
    driver.get("http://130.88.97.239/cgi-bin/dbbrowser/PRINTS/printsBLAST.cgi")

    text_area = driver.find_element_by_xpath("html/body/form/center/textarea")

    for seq in seqs:
        text_area.send_keys(seq)

    radio_button = driver.find_element_by_xpath("html/body/form/table[2]/tbody/tr[2]/td[2]/input[2]")
    radio_button.click()

    driver.find_element_by_xpath("html/body/form/center/p[1]/input[1]").click()

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "code")))

    lines = element.text.splitlines()

    look = False
    results = []
    for line in lines:
        if line[0:3] == "---":
            look = True
            continue
        if look:
            if not line:
                break
            results.append(re.search("[^\s]+",line).group().encode("ascii"))
    ans = []
    for r in results:
        url = urllib.urlopen("http://130.88.97.239/cgi-bin/dbbrowser/PRINTS/DoPRINTS.pl?cmd_a=Display&qua_a=/Full&fun_a=Code&qst_a=%s" % r)
        count = 0
        for line in url:
            count += 1
            search = re.search("View alignment\<\/A\>\s+(.*)", line)
            if search:
                ans.append(search.group(1))
                break

    driver.quit()
    return ans, results
