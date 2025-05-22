import openai
import os
import json
import re

api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_score(data: dict) -> dict:
  resume_json = json.dumps(data, indent=2)
  prompt = (
    f"""You are a resume review assistant.\n"
    "Given this resume data:\n\n"
    "{resume_json}\n\n"
    "Give a resume score out of 100 and 2-3 specific improvement tips.\n"
    "Respond in this JSON format only:\n"
     
      \"score\": .. ,\n"
      \"recommendations\": [\n"
        \"...\",\n"
        \"...\"\n"
  "  ]\n"
    "
    "its only the example .. dont give this info.. analyze it then provide the info . """
  
  )
  try:
    res = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}],
      temperature=0.3,
      max_tokens=500
    )
    content = res.choices[0].message.content
    match = re.search(r'\{.*\}', content, re.DOTALL)
    return json.loads(match.group()) if match else {"score": 0, "recommendations": []}
  except Exception as e:
    print("GPT scoring error:", e)
    return {"score": 0, "recommendations": []}
