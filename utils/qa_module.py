# ✅ utils/qa_module.py
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
client = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')

def answer_question(question: str, document: str) -> tuple[str, str]:
    """
    Answers a question using the given document and provides justification.
    Returns: (answer, justification)
    """
    prompt = f"""
    You are an expert assistant that answers precisely with justification. Read the following document and answer the question. Provide your answer and then cite the paragraph or section you used to support your answer.

    Document:
    {document}

    Question: {question}
    """

    try:
        response = client.generate_content(prompt)
        full_response = response.text.strip()

        # Optional: naive separation if you format your prompt well
        if "Justification:" in full_response:
            answer_part, justification = full_response.split("Justification:", 1)
            return answer_part.strip(), justification.strip()
        else:
            return full_response, "Justification not clearly found."

    except Exception as e:
        return "Error processing question.", str(e)