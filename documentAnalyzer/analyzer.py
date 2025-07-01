#Developer: Ashar Siddiqu#Date Created: 06/09/2025
#Date Updated: 06/30/2025
#Pdf and Worddoc Scanner
#Change Log
# 07/01/2025 : Pdf Scanner
#CSC 842, Security tool development Cycle 9


import argparse
import os
from extractPdf import scanPdf

def detectFileType(filePath):
    ext = os.path.splitext(filePath)[1].lower()
    if ext == ".pdf":
        return "pdf"
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description="PDF and  Office Document Analyzer")
    parser.add_argument("--file", required=True, help="Path to the document to Analyze")
    args = parser.parse_args()

    fileType = detectFileType(args.file)

    if fileType == "pdf":
        scanPdf(args.file)
    else:
        print("File type is not supported at this time...")

if __name__ == "__main__":
    main()
