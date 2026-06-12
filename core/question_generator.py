import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"

def generate_question(company: str, role: str, difficulty: str, asked_questions: list = []) -> str:
    
    asked_text = ""
    if asked_questions:
        asked_text = f"\nDo NOT repeat these questions:\n" + "\n".join(f"- {q}" for q in asked_questions)
    
    prompt = f"""You are a technical interviewer at {company} interviewing for the role of {role}.

Generate ONE {difficulty}-level interview question for this candidate.
The question should be realistic, specific to {company}'s culture and {role} requirements.
{asked_text}

Rules:
- Only output the question itself
- No numbering, no explanation, no extra text
- Make it natural like a real interviewer would ask"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()


def generate_followup(company: str, role: str, question: str, answer: str, history: list = []) -> str:
    
    context = ""
    if history:
        context = "Previous Q&A:\n" + "\n".join([
            f"Q: {h['question']}\nA: {h['answer']}" for h in history[-3:]
        ])
    
    prompt = f"""You are a strict technical interviewer at {company} for {role} role.

{context}

Current Question: {question}
Candidate's Answer: {answer}

Based on their answer, ask ONE smart follow-up question.
- Dig deeper into what they said
- Challenge weak points
- Ask for examples if they gave vague answers
- Only output the question, nothing else"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()


def generate_feedback(company: str, role: str, history: list) -> str:
    
    transcript = "\n".join([
        f"Q: {h['question']}\nA: {h['answer']}" for h in history
    ])
    
    prompt = f"""You interviewed a candidate for {role} at {company}.

Interview Transcript:
{transcript}

Give a detailed performance review with:
1. Overall Score: X/10
2. Technical Skills: X/10
3. Communication: X/10
4. Strengths: (3 bullet points)
5. Areas to Improve: (3 bullet points)  
6. Final Verdict: Hire / Strong Maybe / Maybe / No Hire
7. One line advice for the candidate"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()