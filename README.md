# Web Application Firewall (WAF) Enhanced with AI through Autonomous Dynamic Learning and Generative Models

## Abstract

The evolution of web application defense mechanisms has led to the development of **Web Application Firewalls (WAF)** powered by machine learning models for threat detection. This paper presents a novel approach that combines traditional machine learning techniques (**Naive Bayes**) with generative models such as **ChatGPT** for the dynamic classification of threats in web applications. Our solution leverages **ChatGPT**’s capabilities to detect novel attacks and enhances detection capabilities through continuous retraining. This system progressively learns from new attack patterns, eventually reducing its dependence on the generative model. This paper outlines the architecture, implementation, challenges faced, and significant benefits of integrating generative AI into cybersecurity defense mechanisms.

---

## 1. Introduction

**Web Application Firewalls (WAFs)** have traditionally been rule-based, detecting threats by comparing traffic patterns with predefined signatures. However, these systems fail to address zero-day vulnerabilities and emerging attack vectors. As attackers develop more sophisticated techniques such as SQL injection, XSS, and remote file inclusion, the need for adaptive WAFs with autonomous learning capabilities becomes increasingly evident.

We present a hybrid WAF system that combines a **Naive Bayes** model for detecting known attacks with **ChatGPT**, a generative language model, to handle uncertain or novel threats. The system dynamically retrains itself based on feedback from **ChatGPT**, gradually reducing reliance on the generative model as the local classifier becomes more robust. This paper discusses how this system overcomes the limitations of traditional WAFs and improves detection capabilities through continuous learning.

---

## 2. Problem Statement

Traditional WAFs lack the capability to detect new attack vectors, particularly zero-day vulnerabilities, due to their reliance on signature-based detection. Static machine learning models also fail to adapt over time, diminishing their detection accuracy. Generative models like **ChatGPT** have demonstrated the ability to classify complex patterns, but their application in cybersecurity defense has yet to be fully explored.

The goal of this project is to create a system that:

1. **Combines static and generative machine learning models** to classify attack vectors.
2. **Retrains dynamically** by learning from both known and novel attacks.
3. **Reduces dependence on generative models** as the static model improves.
4. **Detects and classifies sophisticated new attacks** in real-time, evolving with each interaction.

---

## 3. System Architecture

The core of our WAF system is a **dual-classifier approach**:

- **Naive Bayes Classifier**: A lightweight probabilistic model effective for text classification tasks, such as classifying log lines as benign or malicious. It uses **TfidfVectorizer** to convert logs into feature vectors.
- **ChatGPT Generative Model**: A large language model (LLM) capable of analyzing and classifying log lines when the Naive Bayes classifier is uncertain or incorrect.

### 3.1 System Workflow

1. **Log Monitoring**: The system continuously monitors incoming web traffic logs.
2. **Classification with Naive Bayes**: Each log line is classified by the Naive Bayes model based on previously trained data.
3. **Handling Suspicious Logs**: If a log is classified as "No Attack" but contains typical threat patterns (SQL injection, suspicious files, etc.), it is passed to **ChatGPT** for verification.
4. **Feedback Loop**: The classification provided by **ChatGPT** is used to retrain the Naive Bayes model, allowing the WAF to improve its detection capabilities over time.
5. **Dynamic Learning**: As more logs are processed, the system gradually reduces its dependence on **ChatGPT**, enabling faster and more autonomous detection.


## 4. Implementation


## 4.1 Naive Bayes Classification
The **Naive Bayes** model was implemented using **scikit-learn**. We chose this algorithm for its simplicity and efficiency in text classification tasks. Logs are transformed into vector representations using **TfidfVectorizer**, and the Naive Bayes model is trained with labeled data classifying different types of attacks, including **XSS**, **SQL** **injection**, and **command injection**.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Naive Bayes model training
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(logs)  # logs is a list of text entries
y = labels  # labels is the list of classifications for each log
model = MultinomialNB().fit(X, y)
```
## 4.2 Integration with ChatGPT

We integrated ChatGPT (GPT-4) from OpenAI as a backup classifier for logs that the Naive Bayes model cannot classify with confidence. The interaction with ChatGPT is structured as a question-answer system, where ChatGPT analyzes a log and returns the appropriate classification (e.g., "SQL injection", "No Attack", etc.).

```python
import openai

def consult_gpt4(log_line):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Classify this log line as 'XSS', 'SQL Injection', 'No Attack', or another type of attack."},
            {"role": "user", "content": f"Log line: {log_line}"}
        ]
    )
    return response['choices'][0]['message']['content']
```

### 4.3 Dynamic Retraining

The system continuously retrains the Naive Bayes model using examples verified by **ChatGPT**. For each processed log:

- If **ChatGPT** classifies a log as an attack, it is stored in memory along with its classification.
- After accumulating enough examples, the Naive Bayes model is retrained with both new and old data, allowing it to progressively improve its accuracy without overfitting.

### 4.4 Log Pattern Identification

To ensure suspicious logs are handled appropriately, we implemented a function that scans logs for common patterns associated with attacks. These include keywords like `select`, `union`, `cat`, `admin`, and `shadow`. If these patterns are detected, the log is sent directly to **ChatGPT** for detailed analysis.

---

## 5. Results and Evaluation

Our system has shown significant improvements in the following areas:

1. **Accuracy**: Initially, the Naive Bayes model struggled to classify sophisticated attack patterns. However, after several retraining iterations with feedback from **ChatGPT**, the model improved its accuracy and reduced its reliance on the generative model.
2. **Real-time Detection**: By incorporating **ChatGPT** as a fallback mechanism, the system was able to classify novel attack vectors in real-time, achieving near-instant detection of new attacks such as Remote File Inclusion (RFI) and Code Injection.
3. **Continuous Learning**: The feedback loop between **ChatGPT** and the Naive Bayes model enabled dynamic learning, improving detection rates with each interaction. As the Naive Bayes model learned from **ChatGPT**’s classifications, the need to consult the generative model decreased, reducing both time and computational resources.
4. **Flexibility**: The system's ability to adapt to new and changing attack patterns without requiring manual updates or predefined rules makes it highly flexible in handling zero-day vulnerabilities.

---

## 6. Challenges and Future Work

While the integration of **ChatGPT** with Naive Bayes showed promising results, several challenges were encountered:

1. **Latency in ChatGPT Responses**: Although **ChatGPT** is highly accurate, querying an external API introduces some delay. Future work will focus on optimizing this interaction.
2. **Training Data Quality**: The system’s performance heavily relies on the quality of training data. Providing precise and diverse examples is crucial for the success of this approach.
3. **Scalability**: As the system learns more, the size of the training data grows. Efficiently managing this data while ensuring the model remains performant is an area to explore.

Future work will focus on improving scalability, optimizing interactions with **ChatGPT**, and exploring other machine learning models that can complement or replace Naive Bayes for greater efficiency.

---

## 7. Conclusion

Integrating a Naive Bayes classifier with a generative model like **ChatGPT** presents a novel approach to detecting and classifying web attacks in real-time. By combining automatic detection capabilities with dynamic retraining, the system can not only detect known attacks but also adapt and learn from new threats. This represents a significant advancement in web security, especially against sophisticated and zero-day attacks.

---
## Watch the Model Learning Process

[![Watch the video](https://img.youtube.com/vi/YCmbQ6trR48/0.jpg)](https://youtube.com/shorts/YCmbQ6trR48?feature=share)

Click the image above to watch the video on YouTube.

## Model Operating Independently After Training

[![Watch the video](https://img.youtube.com/vi/4s4l2X8J6tQ/0.jpg)](https://youtu.be/4s4l2X8J6tQ)

Click the image above to watch the video on YouTube, where the model operates autonomously without relying on ChatGPT after being trained. It only consults ChatGPT when necessary.

## 8. Run

This project is an **AI-powered Web Application Firewall (WAF)** designed to detect and classify attacks in real-time using **ChatGPT** and a **Naive Bayes model**.

1\. Features
------------

-   Simulates multiple attack types: XSS, SQL Injection, Path Traversal, etc.
-   Classifies attacks using **ChatGPT** and stores patterns in memory.
-   Trains a **Naive Bayes model** to classify attacks locally without external queries.
-   Provides real-time monitoring of logs for enhanced security.

* * * * *

2\. Prerequisites
-----------------

-   **Python 3.7+** installed.
-   Install required libraries:

   

    `pip install flask requests colorama scikit-learn openai`

-   Add your OpenAI API key in `WAF_TRAIN_GPT.py` and `WAF_POST_GPT_NAIVES.py`.

* * * * *

3\. How to Run
--------------

### Step 1: Start the Web Server

Run the simulated web application:


`python server.py`

It will be available at `http://localhost:5051`.

### Step 2: Simulate Attacks

Launch the attacker script to send random attacks:


`python ATTACK.py`

This script sends payloads such as XSS or SQL Injection to the `/login` endpoint every 5 seconds.

### Step 3: Monitor Logs Using AI

Start monitoring logs and classify attacks with ChatGPT:


`python WAF_TRAIN_GPT.py`

### Step 4: Train the Naive Bayes Model

Train a Naive Bayes classifier using the classified logs:


`python WAF_POST_GPT_NAIVES.py`

The model will classify future logs locally without consulting ChatGPT.

* * * * *

4\. Project Structure
---------------------

-   **`server.py`**: Simulates the web application and logs incoming requests.
-   **`ATTACK.py`**: Sends random simulated attacks to the server.
-   **`WAF_TRAIN_GPT.py`**: Classifies logs using ChatGPT and stores learned patterns.
-   **`WAF_POST_GPT_NAIVES.py`**: Trains and uses a Naive Bayes model to classify logs locally.

* * * * *

5\. How It Works
----------------

1.  **Attack Simulation**:

    -   The attacker sends malicious payloads to the web server.
    -   The server logs all requests.
2.  **Log Classification**:

    -   `WAF_TRAIN_GPT.py` uses ChatGPT to classify logs and build memory.
    -   Learned patterns are stored in `memoria.json`.
3.  **Naive Bayes Training**:

    -   `WAF_POST_GPT_NAIVES.py` trains a Naive Bayes model using the stored memory.
    -   The model predicts attack types for new logs.
4.  **Real-time Monitoring**:

    -   Both scripts monitor the log file (`log_waf.log`) in real-time.

* * * * *

6\. Supported Attack Types
--------------------------

-   **XSS (Cross-site Scripting)**
-   **SQL Injection**
-   **Path Traversal**
-   **Command Injection**
-   **Remote File Inclusion**
-   **LDAP Injection**
-   **Code Injection**

* * * * *

7\. Example Output
------------------

### ATTACK.py


`⚔️ Attacker started. Sending attacks every 5 seconds...
✖ Attack (SQL Injection) sent: 1' OR '1'='1 | Response Code: 200
✖ Attack (XSS) sent: <script>alert("XSS")</script> | Response Code: 200`

### WAF_TRAIN_GPT.py


`➤ Processing new log line: INFO:werkzeug:127.0.0.1 - - [19/Nov/2024:15:10:35] "POST /login HTTP/1.1" 200 -
🔍 ChatGPT classified the line as: SQL Injection
✔ Memory saved successfully.`

### WAF_POST_GPT_NAIVES.py



`➤ Processing new log line: INFO:werkzeug:127.0.0.1 - - [19/Nov/2024:15:12:40] "POST /login HTTP/1.1" 200 -
✔ Classified by the model as: XSS
✔ Memory saved successfully.`



## 9. License

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0). You are free to:

- **Share**: Copy and redistribute the material in any medium or format.
- **Adapt**: Remix, transform, and build upon the material.

Under the following terms:

- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial**: You may not use the material for commercial purposes.
- **Ethical Use**: This work is intended strictly for educational and research purposes in controlled environments, such as penetration testing in a Purple Team context. The use of this work for malicious purposes is strictly prohibited.

For more details, visit: [CC BY-NC 4.0 License](https://creativecommons.org/licenses/by-nc/4.0/).

---


## 10. References

- "Application Layer Security for Modern Web Applications", 2023.
- "Generative Models in Cybersecurity: A New Approach to Threat Detection", Journal of AI Research, 2024.
- "Advances in Machine Learning for Web Application Firewalls", Cybersecurity Review, 2024.



