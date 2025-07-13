import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

client = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')

def generate_summary(text):
    try:
        prompt = f"You are a helpful assistant that summarizes documents. Summarize this document in less than 150 words:\n\n{text}"
        
        response = client.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"