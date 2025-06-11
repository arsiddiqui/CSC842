#Developer: Ashar Siddiqui
#Date Created: 06/09/2025
#Date Updated: 06/10/2025
#Email Scanner
#Change Log
# 06/10/2025 : email parser function and print email subject sender and the body
#CSC 842, Security tool development Cycle 5


import argparse
import email
from email import policy
import os


def parseEmail(emlFile):

    with open(emlFile, "r", encoding="utf-8") as eml:
        message = email.message_from_file(eml, policy=policy.default)
        subject = message.get("Subject", "")
        sender =  message.get("From", "")
        body = ""

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_content()
        else:
            body = msg.get_content()

    return subject, sender, body

def main():

    parser = argparse.ArgumentParser(description= "Pishing Email Analyzer")
    parser.add_argument("--email", required=True, help="path to .eml file")
    args = parser.parse_args()

    subject, sender, emailBody = parseEmail(args.email)
    print(f"Email Subject : {subject}")
    print(f"Email From : {sender}")
    print(f"Email Body : {emailBody}")	



if __name__ == "__main__":
    main()
