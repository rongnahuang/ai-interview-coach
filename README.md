# AI Interview Coach

A full-stack AI interview preparation app that helps candidates practice technical and behavioral interview questions, receive instant feedback, and generate a final interview summary.

## Overview

This project combines:

- a React + Vite frontend for the interview experience
- a FastAPI backend that calls the OpenRouter AI API to generate questions, score answers, and summarize the interview

## Features

- Paste your resume and a job description
- Generate 5 technical + 3 behavioral interview questions
- Type your answers and get AI evaluation feedback
- Receive strengths, weaknesses, an improved answer, and a follow-up question
- Finish the interview and get an overall summary report

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS

### Backend
- Python
- FastAPI
- Pydantic
- OpenRouter API via HTTP requests

## Project Structure

```text
ai-interview-coach/
├── backend/
│   ├── main.py
│   └── .env
└── frontend/
    ├── src/
    ├── package.json
    └── vite.config.ts
```

## Prerequisites

- Node.js and npm
- Python 3.9+
- An OpenRouter API key stored in the backend environment

## Environment Setup

Create a backend `.env` file with your API key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Running the App

### 1. Start the backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

The API will run at:

```text
http://localhost:8000
```

### 2. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

## API Endpoints

### POST /generate-questions
Generates interview questions from the resume and job description.

### POST /evaluate-answer
Evaluates a candidate answer and returns:
- score
- strengths
- weaknesses
- improved answer
- follow-up question

### POST /interview-summary
Generates an overall interview summary using all answers provided by the user.

## How It Works

1. The user pastes a resume and job description in the frontend.
2. The frontend sends the input to the backend API.
3. The backend uses OpenRouter to generate interview questions.
4. The user answers questions in the UI.
5. The backend evaluates each answer and produces a final summary.

## Notes

- The frontend currently calls the backend at `http://localhost:8000`.
- Make sure the backend is running before using the interview flow.

## Future Improvements

- Add user authentication
- Save interview history
- Add resume parsing
- Improve answer scoring with stricter rubric logic


source venv/bin/activate
uvicorn main:app --reload

{
  "resume": "Full stack developer with Angular and Spring Boot",
  "jobDescription": "Frontend role using React"
}