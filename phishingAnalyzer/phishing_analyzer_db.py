#Developer: Ashar Siddiqu#Date Created: 06/09/2025
#Date Updated: 06/10/2025
#Email Scanner
#Change Log
# 06/15/2025 : email parser function and print email subject sender and the body
# 06/15/2025 : AI model Added.
#CSC 842, Security tool development Cycle 5


import argparse
import email
from email import policy
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

from dbUtility import getTraingData 


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
            body = message.get_content()

    return subject, sender, body

def _AIModel():

    #if phishing model is already created return it else create
    #load model from the disk and return
    if not os.path.exists("phishingModel.pkl"):
       
       phishingSentence, trainLabels = getTraingData()
       # create instance of a vector to convert text to numbers.
       vectorizer = TfidfVectorizer()

       # Phishing Sentences array to numbers using TfidfVectorizer
       features = vectorizer.fit_transform(phishingSentence)

       #Machine learning model
       model = LogisticRegression()

       #Train the model using the features and labels
       model.fit(features, trainLabels)

       #Save the vectorizer and model 
       joblib.dump((vectorizer, model), "phishingModel.pkl")
    modelData = joblib.load("phishingModel.pkl")
    return  modelData




def predictPishing(subject, sender, body, modelData):
    # assigned tuple modeldata [0][1] to variabels
    vectorizer, model = modelData

    # Combine subject, sender, and body to a string
    combinedText = subject + " " + sender + " " + body

    #Convert the text into a format the model can understand
    features = vectorizer.transform([combinedText])

    # Use the model to predict if the email is phishing 1 or not 0
    prediction = model.predict(features)[0]

    # Get the confidence score of the prediction
    confidence = model.predict_proba(features)[0][prediction]

    # Return prediction and confidence score
    return prediction, confidence

def main():

    parser = argparse.ArgumentParser(description= "Pishing Email Analyzer")
    parser.add_argument("--email", required=True, help="path to .eml file")
    args = parser.parse_args()

    subject, sender, emailBody = parseEmail(args.email)
    print(f"Email Subject : {subject}")
    print(f"Email From : {sender}")
    print(f"Email Body : {emailBody}")

    modelData = _AIModel()

    isPhishing, confidence = predictPishing(subject, sender, emailBody, modelData)
    if isPhishing:
        print("This is a phishing email")
    else:
        print("This email is safe")

    print(f"Confidence level is : {confidence:.2f}")

if __name__ == "__main__":
    main()
