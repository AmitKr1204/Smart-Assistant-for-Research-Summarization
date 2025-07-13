# utils/quiz_module.py
import google.generativeai as genai
import os
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
client = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')

def generate_quiz(document: str) -> list[str]:
    prompt = f"""
    You are a tutor bot who makes thoughtful questions. Based on the following document, create 3 logic-based or comprehension-focused questions that test understanding. Number them 1 to 3.

    Document:
    {document}
    """

    try:
        response = client.generate_content(prompt)
        raw = response.text.strip()
        lines = raw.split("\n")
        questions = [line.lstrip("1234567890. ") for line in lines if line.strip()]
        return questions[:3]

    except Exception as e:
        return [f"Error generating quiz: {str(e)}"]


def evaluate_answers(document: str, questions: list[str], user_answers: list[str]) -> list[dict]:
    results = []

    for i, question in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else ""
        prompt = f"""
You are a teaching assistant that gives feedback on answers. You are an evaluator. Determine if the user's answer is correct based on the document.
Provide:
- Question
- User's answer
- Correctness (Yes/No)
- Justification (based on document)

Document:
{document}

Q: {question}
A: {user_answer}
"""

        try:
            response = client.generate_content(prompt)
            feedback = response.text.strip()

            results.append({
                "question": question,
                "user_answer": user_answer,
                "correct": "yes" in feedback.lower(),
                "justification": feedback
            })

        except Exception as e:
            results.append({
                "question": question,
                "user_answer": user_answer,
                "correct": False,
                "justification": str(e)
            })

    return results