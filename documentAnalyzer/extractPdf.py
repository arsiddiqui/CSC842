#Developer: Ashar Siddiqu#Date Created: 06/09/2025
#Date Updated: 07/01/2025
#Pdf and Worddoc Scanner
#Change Log
# 07/01/2025 : Pdf Scanner
#CSC 842, Security tool development Cycle 9

import fitz 
import re

def extractUrls(text):
    return re.findall(r"https?://[^\s)>\]]+", text)

def scanPdf(filePath):
    print(f"PDF  Scanning {filePath} ...")
    doc = fitz.open(filePath)
    foundUrls = []

    for pageNum in range(len(doc)):
        text = doc[pageNum].get_text()
        urls = extractUrls(text)
        foundUrls.extend(urls)

    if foundUrls:
        print("URLs found in PDF:")
        for url in set(foundUrls):
            print(f"  -- {url}")
    else:
        print("No URLs found in PDF.")
