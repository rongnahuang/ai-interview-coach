from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import requests
import os
import re

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    


class InterviewRequest(BaseModel):
    resume: str
    jobDescription: str
   
def call_openrouter(prompt: str):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat-v3-0324",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "response_format":{"type":"json_object"}
        }
    )

    return response.json() 
 
@app.post("/generate-questions")
def generate_questions(request: InterviewRequest):
    
    prompt = f"""
    You are a senior software engineering interviewer.
    
    Return ONLY valid JSON in this format:
    
    {{
        "technical": [
            "question1",
            "question2",
            "question3",
            "question4",
            "question5"],
        "behavioral":[
            "question1",
            "question2",
            "question3"
        ] 
    }}
    
    Generate EXACTLY:
    - 5 technical questions
    - 3 behavioral questions

    Resume:
    {request.resume}

    Job Description:
    {request.jobDescription}

    """
    
    data = call_openrouter(prompt)
    
    print("OPENROUTER RAW RESPONSE:", data)
    
    if "choices" not in data:
        return {
            "error": data
        }

    content=data["choices"][0]["message"]["content"]
    
    content = re.sub(r"```json", "", content)
    content = re.sub(r"```", "", content)
    content = content.strip()

    return {
        "questions": json.loads(content)
    }
    
    
class AnswerRequest(BaseModel):
    question: str
    answer: str

@app.post('/evaluate-answer')
def evaluate_answer(request:AnswerRequest):
    
   prompt = f"""
   
   You are an expert interviewer.
   
   Question:
   {request.question}
   
   Candidate Answer:
   {request.answer}
   
   Return JSON:
   {{
       ”score": 0-10
       "strengths": [],
       "weaknesses": [],
       "improved_answer": "",
       "follow_up_question": ""
   }}
   
   """
   
   data = call_openrouter(prompt)
   
   content = data["choices"][0]["message"]["content"]
   
   content = re.sub(r"```json", "", content)
   content = re.sub(r"```", "", content)
   content = content.strip()
   
   return json.loads(content)



class InterviewSummaryRequest(BaseModel):
    answers:dict
    
@app.post('/interview-summary')
def interview_summary(request: InterviewSummaryRequest):
    
    prompt = f"""
    
    You are a senior engineering interviewer.
    
    Candidate Answers:

    {request.answers}
    
    Evaluate the overall interview.
    
    Return JSON:
    
    {{
      "overall_score": 0-10,
      "technical_score": 0-10,
      "communication_score": 0-10,
      "problem_solving_score": 0-10,
      "recommendation": "",
      "summary": ""
    }}
    
    """
    
    data = call_openrouter(prompt)
    
    content = data["choices"][0]["message"]["content"]
   
    content = re.sub(r"```json", "", content)
    content = re.sub(r"```", "", content)
    content = content.strip()
    
    return json.loads(content)