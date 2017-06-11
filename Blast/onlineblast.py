import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import urllib

query = []

with open(sys.argv[1], "r") as f:
    for line in f:
        query.append(line)
    
driver = webdriver.PhantomJS()
driver.get("https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE=Proteins")

text_area = driver.find_element_by_xpath(".//*[@id='seq']")

for q in query:
    text_area.send_keys(q)

driver.find_element_by_xpath(".//*[@id='b1']").click()

download = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='showDownload']/span[1]")))
download.click()
text_file = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='tdal']/div[2]/a[1]")))

url = text_file.get_attribute('href')

res = urllib.urlopen(url)

print res.read()
