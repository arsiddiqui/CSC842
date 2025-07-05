#Developer: Ashar Siddiqu#Date Created: 07/04/2025
#Date Updated: 07/04/2025
#Pdf and Worddoc Scanner
#Change Log
# 07/01/2025 : Word Scanner
#CSC 842, Security tool development Cycle 9

from docx import Document
import re

def extractUrls(text):
    return re.findall(r"https?://[^\s)>\]]+", text)

def scanDoc(filePath):
    print(f"Scanning {filePath} ...")
    doc = Document(filePath)
    fullText = " ".join([para.text for para in doc.paragraphs])
    urls = extractUrls(fullText)

    if urls:
        print("URLs found in DOCX:")
        for url in set(urls):
            print(f"  -- {url}")
    else:
        print("No URLs found in DOCX.")
