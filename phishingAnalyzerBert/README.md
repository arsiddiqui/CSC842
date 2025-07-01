# 🛡️ Phishing Email Analyzer BERT (Bidirectional Encoder Representations from Transformers). 
## A Command-line Data Driven, BERT Powered Python tool.

A command-line ML tool that can identifiy phishing emails 

Developed for **CSC842 - Security tool Development**, Phishing Email Analyzer. A Command-line Data Driven, AI Powered Python tool.

This tool allows users to observe how two different machine learning approaches behave when classifying emails:

## 1. TF-IDF + Logistic Regression (Custom Model)
   
Uses TF-IDF (Term Frequency Inverse Document Frequency) to convert email content into numerical features.

Relies on a user-defined training dataset where users specify what is considered phishing.

This model learns based on patterns in your labeled dataset and reflects user bias or domain-specific rules.

Great for quick, interpretable models when you have control over training data.

## 2. BERT (Transformer based Pretrained Model)
   
Leverages bert base uncased, a powerful pre trained transformer model originally trained on SMS spam datasets.

Identifies whether a message is spam or safe based on general language patterns.

Although not fine-tuned for phishing in this version, it demonstrates how a general NLP "Natural Language Processing", model interprets threats.

Fine-tuning BERT on a phishing specific dataset could significantly improve accuracy.

---

## 🔍 Features

- Command line tool lightweight to analyze emails  
- Machine learning capability
- Database driven training data. 
- CLI interface – no dependencies on web frameworks

---

## ⚙️ Requirements

- Python 3.8+
- Mongo DB
- Scikit-learn
- transformers 

---
## 🎥 Tool Demo
Watch the demonstration video on YouTube:

- [Email Analyzer - Youtube](https://www.youtube.com/watch?v=J_yV9z7ElH0)


