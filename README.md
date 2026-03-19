# NovaMentor – GenAI Learning Assistant & Agent System

NovaMentor is a Generative AI-powered learning assistant designed to transform passive learning into an interactive, thought-driven experience using the Socratic method. Instead of directly providing answers, it guides users through structured questioning to improve understanding and critical thinking.

---

## Overview

NovaMentor combines Large Language Models, prompt engineering, and learning analytics to create a personalized AI tutor. The system adapts to user input, generates quizzes, and tracks performance to enhance learning outcomes.

---

## Features

- AI-powered interactive tutoring with guided questioning  
- Socratic learning approach for deeper understanding  
- Adaptive quiz generation based on user performance  
- Learning analytics and performance tracking dashboard  
- Step-by-step explanations with hints and retries  
- Multi-model fallback strategy for optimized performance and cost  

---

## Tech Stack

Python, JavaScript, HTML, CSS, Streamlit, FastAPI, AWS, Bedrock, Nova, Boto3, IAM, JSON, SQLite, REST, PromptEngineering, Logging, GitHub, Antigravity

---

## Architecture

The system follows a modular architecture:

- Frontend: Handles user interaction, chat interface, and dashboards  
- Backend: Manages API requests, AI orchestration, and logic  
- AI Layer: AWS Bedrock with Nova models for response generation  
- Analytics Layer: Tracks and visualizes learning progress  

---

## How It Works

1. User inputs a query or topic  
2. Backend processes the request and sends it to the AI model  
3. The AI responds using a Socratic approach (guided questioning)  
4. System generates quizzes and hints based on understanding  
5. User performance is tracked and displayed in dashboards  

---

## Installation

```bash
git clone https://github.com/your-username/NovaMentor.git
cd NovaMentor
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuration

```bash
aws configure
```

or

```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=your_region
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
streamlit run app.py
```

---

## Challenges

- Handling repetitive and generic AI responses  
- Designing effective Socratic prompts  
- Managing latency across different models  
- Debugging backend and API integration issues  
- Configuring AWS Bedrock and controlling costs  

---

## Accomplishments

- Built a working GenAI-powered tutoring system  
- Implemented Socratic learning in an AI application  
- Designed a multi-model fallback architecture  
- Integrated analytics with AI-driven insights  

---

## Future Improvements

- Voice-based AI tutor  
- Subject-specific intelligent agents  
- Multi-user classroom analytics  
- AI + cybersecurity learning integration  
- Scalable deployment and optimization  

---
