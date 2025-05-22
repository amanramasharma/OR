# from transformers import pipeline
# import re
# import json

# # Load the LLM model (TinyLlama)
# # generator = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# def extract_with_llm(text: str) -> dict:
#     """
#         Method Name: extract_with_llm
#         Description: Uses LLM to extract structured resume info from raw text.
#         Input: Resume text
#         Output: Dict containing name, email, phone, skills, education, experience

#         Written By: Aman Sharma
#         Version: 1.0
#     """

#     prompt = f"""
# You are an AI assistant that extracts structured information from resumes.
# Given the following raw resume text, extract the following:

# - name
# - email
# - phone
# - skills (as a list)
# - education (list of degree, institution, year)
# - experience (list of title, company, duration)

# Return the result as clean JSON in this format:

# {{
#   "name": "Jane Smith",
#   "email": "jane@example.com",
#   "phone": "+44 123456789",
#   "skills": ["Customer Service", "Problem Solving", "Communication"],
#   "education": [
#     {{
#       "degree": "MSc in Artificial Intelligence",
#       "institution": "University of London",
#       "year": "2022"
#     }}
#   ],
#   "experience": [
#     {{
#       "title": "Customer Support Associate",
#       "company": "TechCorp Ltd.",
#       "duration": "2020-2023"
#     }}
#   ]
# }}

# Now extract the same for the following resume text:

# {text[:3000]}
# """

#     try:
#         output = generator(prompt, max_new_tokens=512)[0]['generated_text']
#         print("\n====== RAW LLM OUTPUT ======\n", output)

#         # Attempt to extract only the JSON from the output
#         json_str = re.search(r'\{.*\}', output, re.DOTALL).group()
#         return json.loads(json_str)

#     except Exception as e:
#         print("LLM extraction failed:", e)
#         return {
#             "name": None,
#             "email": None,
#             "phone": None,
#             "skills": [],
#             "education": [],
#             "experience": []
#         }