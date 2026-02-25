<div align="center">

# 🛡️ Web Application Firewall (WAF) Enhanced with AI

### Autonomous Dynamic Learning with Generative Models

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-ChatGPT%20%2B%20Naive%20Bayes-purple.svg)](https://openai.com/)
[![Security](https://img.shields.io/badge/Security-WAF-orange.svg)]()

**A novel approach combining traditional ML with generative AI for real-time threat detection**

[📖 Abstract](#-abstract) • [🚀 Quick Start](#-quick-start) • [🏗️ Architecture](#️-architecture) • [📊 Results](#-results)

</div>

---

## 📖 Abstract

The evolution of web application defense mechanisms has led to the development of **Web Application Firewalls (WAF)** powered by machine learning models for threat detection. This paper presents a novel approach that combines traditional machine learning techniques (**Naive Bayes**) with generative models such as **ChatGPT** for the dynamic classification of threats in web applications.

Our solution leverages **ChatGPT**'s capabilities to detect novel attacks and enhances detection capabilities through continuous retraining. This system progressively learns from new attack patterns, eventually reducing its dependence on the generative model.

---

## ✨ Key Features

- 🤖 **Hybrid AI System** - Combines Naive Bayes + ChatGPT for optimal detection
- 🔄 **Autonomous Learning** - Continuously retrains from new attack patterns
- ⚡ **Real-time Detection** - Instant classification of known and novel attacks
- 🎯 **Zero-day Protection** - Detects previously unknown attack vectors
- 📈 **Progressive Independence** - Reduces reliance on ChatGPT over time
- 🛡️ **Multi-attack Support** - XSS, SQL Injection, Path Traversal, and more

---

## 🎥 Demo Videos

<div align="center">

### Model Learning Process
[![Watch the video](https://img.youtube.com/vi/YCmbQ6trR48/0.jpg)](https://youtube.com/shorts/YCmbQ6trR48?feature=share)

### Autonomous Operation
[![Watch the video](https://img.youtube.com/vi/4s4l2X8J6tQ/0.jpg)](https://youtu.be/4s4l2X8J6tQ)

*Click images to watch on YouTube*

</div>

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- OpenAI API key
- Required libraries

### Installation

```bash
# Clone the repository
git clone https://github.com/daletoniris/Web-Application-Firewall-Purple-AI-Paper.git
cd Web-Application-Firewall-Purple-AI-Paper

# Install dependencies
pip install flask requests colorama scikit-learn openai
```

### Configuration

Add your OpenAI API key in:
- `WAF_TRAIN_GPT.py`
- `WAF_POST_GPT_NAIVES.py`

```python
openai.api_key = "your-api-key-here"
```

---

## 🏃 How to Run

### Step 1: Start the Web Server

```bash
python server.py
```

Server will be available at `http://localhost:5051`

### Step 2: Simulate Attacks

In a new terminal:

```bash
python ATTACK.py
```

This sends random attacks (XSS, SQL Injection, etc.) every 5 seconds.

### Step 3: Monitor with AI

Start monitoring and classifying logs with ChatGPT:

```bash
python WAF_TRAIN_GPT.py
```

### Step 4: Train Naive Bayes Model

Train the local classifier:

```bash
python WAF_POST_GPT_NAIVES.py
```

The model will now classify logs locally without consulting ChatGPT.

---

## 🏗️ Architecture

### System Workflow

```
┌─────────────┐
│ Web Server  │ ──► Logs ──► ┌──────────────────┐
│  (server.py)│              │  Naive Bayes     │
└─────────────┘              │  Classifier      │
                              └────────┬─────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    │                                       │
              ✅ Confident                            ❓ Uncertain
                    │                                       │
                    │                                       ▼
                    │                              ┌─────────────────┐
                    │                              │    ChatGPT      │
                    │                              │  Classification │
                    │                              └────────┬─────────┘
                    │                                       │
                    └───────────────────┬───────────────────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │  Retrain Model   │
                              │  (Feedback Loop)│
                              └──────────────────┘
```

### Components

| Component | Description |
|-----------|-------------|
| **server.py** | Simulates web application and logs incoming requests |
| **ATTACK.py** | Sends random simulated attacks to the server |
| **WAF_TRAIN_GPT.py** | Classifies logs using ChatGPT and stores learned patterns |
| **WAF_POST_GPT_NAIVES.py** | Trains and uses Naive Bayes model for local classification |

---

## 🎯 Supported Attack Types

- ✅ **XSS** (Cross-site Scripting)
- ✅ **SQL Injection**
- ✅ **Path Traversal**
- ✅ **Command Injection**
- ✅ **Remote File Inclusion (RFI)**
- ✅ **LDAP Injection**
- ✅ **Code Injection**

---

## 📊 Results

### Performance Improvements

1. **Accuracy**: Naive Bayes model improved significantly after retraining with ChatGPT feedback
2. **Real-time Detection**: Near-instant detection of novel attack vectors
3. **Continuous Learning**: Detection rates improve with each interaction
4. **Autonomy**: System reduces dependence on ChatGPT as it learns

### Example Output

**ATTACK.py:**
```
⚔️ Attacker started. Sending attacks every 5 seconds...
✖ Attack (SQL Injection) sent: 1' OR '1'='1 | Response Code: 200
✖ Attack (XSS) sent: <script>alert("XSS")</script> | Response Code: 200
```

**WAF_TRAIN_GPT.py:**
```
➤ Processing new log line: INFO:werkzeug:127.0.0.1 - - [19/Nov/2024:15:10:35] "POST /login HTTP/1.1" 200 -
🔍 ChatGPT classified the line as: SQL Injection
✔ Memory saved successfully.
```

**WAF_POST_GPT_NAIVES.py:**
```
➤ Processing new log line: INFO:werkzeug:127.0.0.1 - - [19/Nov/2024:15:12:40] "POST /login HTTP/1.1" 200 -
✔ Classified by the model as: XSS
✔ Memory saved successfully.
```

---

## 🔬 Technical Details

### Naive Bayes Implementation

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Vectorize logs
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(logs)
y = labels

# Train model
model = MultinomialNB().fit(X, y)
```

### ChatGPT Integration

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

---

## 🚧 Challenges & Future Work

### Current Challenges

- ⏱️ **Latency**: ChatGPT API calls introduce some delay
- 📊 **Data Quality**: Performance depends on training data quality
- 📈 **Scalability**: Managing growing training data efficiently

### Future Improvements

- Optimize ChatGPT interactions
- Explore alternative ML models
- Improve scalability
- Enhanced pattern recognition

---

## 📄 License

This work is licensed under the **Apache License 2.0**.

- ✅ **Use**: Personal, educational, or commercial purposes
- ✅ **Modify**: Adapt and build upon the material
- ✅ **Distribute**: Share under the same license

**⚠️ Ethical Use Only**: Intended for lawful purposes including educational research, penetration testing, and cybersecurity defense.

---

## 📚 References

- "Application Layer Security for Modern Web Applications", 2023
- "Generative Models in Cybersecurity: A New Approach to Threat Detection", Journal of AI Research, 2024
- "Advances in Machine Learning for Web Application Firewalls", Cybersecurity Review, 2024

---

## 👤 Author

**Daniel Dieser** - Independent Robotics Researcher & AI Developer

- GitHub: [@daletoniris](https://github.com/daletoniris)
- Organizations: @initiasur, @NiperiaLab

---

<div align="center">

**🛡️ Protecting Web Applications with AI-Powered Defense**

[⭐ Star this repo if you find it useful](https://github.com/daletoniris/Web-Application-Firewall-Purple-AI-Paper)

</div>
