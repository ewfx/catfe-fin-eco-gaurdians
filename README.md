# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
A context-aware financial system is an advanced financial management platform that leverages real-time data, machine learning algorithms, 
and cognitive computing to provide personalized, adaptive, and predictive financial services. 
This system integrates internal and external data sources to create a holistic view of an individual's or organization's financial situation, enabling informed decision-making and optimized financial outcomes.
## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
The below limitations of Traditional Testing Methods inspired us to pick this use case.
Inadequate Test Coverage: Traditional testing methods often focus on functional testing, neglecting non-functional requirements like performance, security, and usability.
Insufficient Test Data: Limited test data and lack of real-world scenarios can lead to incomplete testing and inadequate defect detection.
Inability to Simulate Real-World Complexity: Traditional testing methods struggle to replicate the complexity of real-world financial scenarios, making it difficult to ensure system reliability.
## ⚙️ What It Does
Context-Aware Query Understanding:
Define query formats: Define a set of query formats that the system should be able to understand (e.g., "Generate automation for user login?").
Use T5 for query understanding: Use the fine-tuned T5 model to understand natural language queries and identify the relevant context.

Generate Scenario & Step definition files :
The code will generate the scenarios & step definitions for the user entered scenarios.

Execute Scenarios & review Results :
The code will execute the scenarios & review the results

## 🛠️ How We Built It
Python 3.10: Install this version of Python.
Transformers library: Install the Transformers library using pip: pip install transformers
T5 model: Download the pre-trained T5 model using the Transformers library.
Selenium : install to generate the selenium code. pip install selenium
Behave : install to run the automation suit. pip install behave

## 🚧 Challenges We Faced
Hardware Limitations
Computational Power: Training large language models like T5 requires significant computational resources, 
which was not be available on a local Windows machine.
Memory Constraints: Large financial datasets and language models requires substantial memory, which was limited on a local machine.

Software Limitations
Dependency Management: Managing dependencies for the T5 model, Transformers library, and other required libraries was challenging on a local Windows machine.
Environment Configuration: Configuring the environment for the T5 model, including setting up the correct Python version, libraries, and dependencies, can be time-consuming.



## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/catfe-fin-eco-gaurdians.git
   ```
2. Install dependencies  
   ```sh
   npm install  # or pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start  # or python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React 
- 🔹 Backend: Node.js - 🔹
- 🔹 Other: Google T5

## 👥 Team
- **Divya Singh** - [GitHub](#) | [LinkedIn](#)
- **Ravindra Gadadi** - [GitHub](#) | [LinkedIn](#)
- **Deepali Dhir** - [GitHub](#) | [LinkedIn](#)
- **Shanmuka Kamarti maridi** - [GitHub](#) | [LinkedIn](#)
- **Prafulla Kumar Jenna** - [GitHub](#) | [LinkedIn](#)