# NovaMentor – AI Socratic Learning Copilot

An AI-powered learning system based on the Socratic teaching method.

## Stack
- **Backend**: FastAPI + AWS Bedrock (boto3) + FAISS
- **Frontend**: React + TypeScript

## Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Environment Variables
Copy `.env` and fill in your AWS credentials.
