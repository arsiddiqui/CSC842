#Developer: Ashar Siddiqu#Date Created: 07/04/2025
#Date Updated: 07/04/2025
#Pdf and Worddoc Scanner
#Change Log
# 07/04/2025 : Ole Scanner 
#CSC 842, Security tool development Cycle 9

from oletools.olevba import VBA_Parser

def scanOle(filePath):
    print(f"Scanning {filePath} for macros ...")

    try:
        vbaparser = VBA_Parser(filePath)
        if vbaparser.detect_vba_macros():
            print("[+] Macros found!")
            for (_, _, vba_filename, vba_code) in vbaparser.extract_macros():
                print(f"--- Macro: {vba_filename} ---")
                print(vba_code[:1000]) 
        else:
            print("No macros detected.")
    except Exception as e:
        print(f"Error parsing file: {e}")
