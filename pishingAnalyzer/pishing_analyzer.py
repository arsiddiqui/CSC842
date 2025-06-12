#Developer: Ashar Siddiqui
#Date Created: 06/09/2025
#Date Updated: 06/10/2025
#Email Scanner
#Change Log
# 06/10/2025 : email parser function and print email subject sender and the body
# 06/11/2025 : AI model Added.
#CSC 842, Security tool development Cycle 5


import argparse
import email
from email import policy
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib


pishingSentence = [
"Your account has been suspended. Click here to verify.",
"Monthly report attached. Let me know your feedback."
]


# 1 = pishing mail
# 0 = mail is safe.
 
trainLabels = [1,0]

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

    #if pishing model is laready created return it else create
    #load model from the disk and return
    if not os.path.exists("pishingModel.pkl"):
       # careate instance of a vector to convert text to numbers.
       vectorizer = TfidfVectorizer()

       # Pishing Sentences array to numbers using TfidfVectorizer
       features = vectorizer.fit_transform(pishingSentence)

       #Machine learning model
       model = LogisticRegression()

       #Train the model using the features and labels
       model.fit(features, trainLabels)

       #Save the vectorizer and model 
       joblib.dump((vectorizer, model), "pishingModel.pkl")
    modelData = joblib.load("pishingModel.pkl")
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

    # Return predticon and confidenc score
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

    isPishing, confidence = predictPishing(subject, sender, emailBody, modelData)
    if isPishing:
        print("This is a pishing email")
    else:
        print("This email is safe")

    print(f"Confidence level is : {confidence:.2f}")

if __name__ == "__main__":
    main()
