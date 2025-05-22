import openai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
import os
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def extract_with_gpt(text: str) -> dict:
    prompt = f"""
You are a powerful resume analysis assistant. Your task is to extract structured and detailed information from resumes. Resumes may vary in formatting, order, style, and content, so be adaptive and intelligent in extraction.

Extract the following fields in accurate JSON format:

1. **name** – Candidate's full name  
2. **email** – Most relevant contact email  
3. **phone** – Most relevant contact number  
4. **location** – City/Country or address if available  
5. **summary** – Professional summary / profile if available  
6. **skills** – A list of all technical and soft skills mentioned  
7. **education** – List of degrees with:
    - degree
    - institution
    - year
    - gpa (if available)
8. **experience** – List of professional experiences with:
    - title
    - company
    - duration
    - location (if available)
    - description (1-2 bullet points if present)
9. **certifications** – List of certificates with:
    - name
    - issued_by
    - year (if found)
10. **projects** – List of academic or industry projects with:
    - title
    - technologies used
    - description
11. **courses** – List of relevant coursework or subjects

Ensure:
- Output is only JSON (no explanation)
- Do your best to detect section headers even if formatting is inconsistent
- Convert lists of skills or bullets into arrays in JSON
- Avoid hallucinating if content isn’t present

Now extract structured data from this resume text below:

{text[:3000]}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )
        reply = response.choices[0].message.content
        json_str = re.search(r'\{.*\}', reply, re.DOTALL).group()
        return json.loads(json_str)

    except Exception as e:
        print("GPT parsing error:", e)
        return {
            "name": None, "email": None, "phone": None, "location": None, "summary": None,
            "skills": [], "education": [], "experience": [],
            "certifications": [], "projects": [], "courses": []
        }
