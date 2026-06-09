from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from chains import question_chain
from chains import evaluate_answer_chain
from chains import interview_summary_chain
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
   
# def call_openrouter(prompt: str):

#     response = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "deepseek/deepseek-chat-v3-0324",
#             "messages": [
#                 {"role": "user", "content": prompt}
#             ],
#             "response_format":{"type":"json_object"}
#         }
#     )

#     return response.json() 
 
@app.post("/generate-questions")
def generate_questions(request: InterviewRequest):
    
    return question_chain.invoke({
        "resume": request.resume,
        "job_description": request.jobDescription
    })
    

    
class AnswerRequest(BaseModel):
    question: str
    answer: str

@app.post('/evaluate-answer')
def evaluate_answer(request:AnswerRequest):
    
    return  evaluate_answer_chain.invoke({
        "question": request.question,
        "answer": request.answer
    })





class InterviewSummaryRequest(BaseModel):
    answers:dict
    
@app.post('/interview-summary')
def interview_summary(request: InterviewSummaryRequest):
    
    return interview_summary_chain.invoke({
        "answers": request.answers
    })

