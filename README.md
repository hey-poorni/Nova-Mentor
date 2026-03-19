# NovaMentor – AI Socratic Learning Copilot

An AI-powered learning system based on the Socratic teaching method.

## Stack
- **Backend**: FastAPI + AWS Bedrock (boto3) + FAISS
- **Frontend**: React + Vite + TypeScript (UI uses modern dark theme)

## Status
- Core backend services (Quiz, Chat, Analysis) implemented and tested.
- Real-time performance tracking integrated.
- Frontend scaffolded with Vite for modern performance.

## Setup

```bash
# 1. Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# 2. Frontend
cd frontend
npm install
npm run dev
```

## Environment Variables
Copy `.env` and fill in your AWS credentials.
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

