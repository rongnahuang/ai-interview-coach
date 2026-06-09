from langchain_core.prompts import PromptTemplate
from llm import llm

generate_questions_prompt = PromptTemplate.from_template(
"""
You are a senior engineering interviewer.

Resume:
{resume}

Job Description:
{job_description}

Generate:

{{
  "technical":[],
  "behavioral":[]
}}

Return JSON only.
"""
)

question_chain = generate_questions_prompt | llm


evaluate_answer_prompt = PromptTemplate.from_template("""
You are an expert interviewer.

Question:
{question}

Candidate Answer:
{answer}

Return JSON only:

{{
  "score": 0-10,
  "strengths": [],
  "weaknesses": [],
  "improved_answer": "",
  "follow_up_question": ""
}}
""")

evaluate_answer_chain = evaluate_answer_prompt | llm


interview_summary_prompt = PromptTemplate.from_template("""
You are a senior engineering interviewer.

Candidate Answers:
{answers}

Evaluate the overall interview performance.

Return JSON only:

{{
  "overall_score": 0-10,
  "technical_score": 0-10,
  "communication_score": 0-10,
  "problem_solving_score": 0-10,
  "recommendation": "",
  "summary": ""
}}
""")

interview_summary_chain = interview_summary_prompt | llm

