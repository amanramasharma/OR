from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from bson import ObjectId
import uvicorn
import gridfs
import os
from db import users_collection, db
from parsers import parseResume
from ai.analyzeResume import analyzeResume
from models.resumeModel import ResumeModel
from gpt_scorer import get_gpt_score
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from openai import OpenAI
import openai
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="spartans162674")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/site", StaticFiles(directory="../public_site", html=True), name="site")
fs = gridfs.GridFS(db)
templates = Jinja2Templates(directory="../server/templates")

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return RedirectResponse(url="/site/index.html")

@app.post("/signup")
async def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": password
    })
    return RedirectResponse("/site/login.html", status_code=302)

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"email": email, "password": password})
    if user:
        request.session["user_email"] = email
        return RedirectResponse("/site/dashboard.html", status_code=302)
    return HTMLResponse("<h2>Invalid credentials</h2>", status_code=401)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/site/login.html", status_code=302)

@app.post("/upload_resume")
async def upload_resume(request: Request, resume: UploadFile = File(...)):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse("/site/login.html", status_code=302)

    text = await parseResume(resume)
    result = analyzeResume(text)

    result["file_name"] = resume.filename
    result["uploaded_at"] = datetime.utcnow().isoformat()
    result["uploaded_by"] = email

    score_result = get_gpt_score(result)
    result["resume_score"] = score_result.get("score")
    result["recommendations"] = score_result.get("recommendations")

    inserted = db["parsed_resumes"].insert_one(result)
    resume_id = str(inserted.inserted_id)

    return RedirectResponse(f"/view_resume/{resume_id}", status_code=302)
@app.get("/current_user")
async def get_current_user(request: Request):
    email = request.session.get("user_email")
    if not email:
        return JSONResponse({"error": "Not logged in"}, status_code=401)

    user = users_collection.find_one({"email": email})
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)

    return {
        "username": user.get("username", "User")
    }
@app.get("/admin/users")
async def admin_users():
    users = list(users_collection.find())
    result = []
    for user in users:
        email = user.get("email")
        resume_count = db["parsed_resumes"].count_documents({"uploaded_by": email})
        result.append({
            "username": user.get("username"),
            "email": email,
            "resumes": resume_count
        })
    return result

@app.delete("/admin/delete_user")
async def delete_user(email: str):
    users_collection.delete_one({"email": email})
    db["parsed_resumes"].delete_many({"uploaded_by": email})
    return {"message": f"User {email} and their resumes deleted."}

@app.post("/admin_login")
async def admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin123":
        request.session["is_admin"] = True
        return {"success": True}
    return {"success": False, "message": "Invalid admin credentials"}

@app.get("/admin.html", response_class=HTMLResponse)
async def admin_protected_page(request: Request):
    if not request.session.get("is_admin"):
        return RedirectResponse("/site/admin_login.html", status_code=302)
    with open("../public_site/admin.html", "r") as f:
        return HTMLResponse(content=f.read())
    
@app.get("/my_uploads")
async def my_uploads(request: Request):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse("/site/login.html", status_code=302)
    uploads = list(db["parsed_resumes"].find({"uploaded_by": email}))
    for item in uploads:
        item["_id"] = str(item["_id"])
    return templates.TemplateResponse("my_uploads.html", {
        "request": request,
        "uploads": uploads,
        "email": email
    })
@app.get("/view_resume/{resume_id}")
async def view_resume(resume_id: str, request: Request):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse("/site/login.html", status_code=302)
    resume = db["parsed_resumes"].find_one({"_id": ObjectId(resume_id), "uploaded_by": email})
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    resume["_id"] = str(resume["_id"])
    return templates.TemplateResponse("result.html", {"request": request, "result": resume})

@app.get("/edit_resume/{resume_id}")
async def edit_resume(resume_id: str, request: Request):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse("/site/login.html", status_code=302)
    resume = db["parsed_resumes"].find_one({"_id": ObjectId(resume_id), "uploaded_by": email})
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    resume["_id"] = str(resume["_id"])
    return templates.TemplateResponse("edit_resume.html", {"request": request, "result": resume})

@app.post("/save_resume")
async def save_resume(request: Request, name: str = Form(...), email: str = Form(...), phone: str = Form(...), location: str = Form(None), summary: str = Form(None), skills: str = Form(None), certifications: str = Form(None), projects: str = Form(None), courses: str = Form(None), file_name: str = Form(...), uploaded_by: str = Form(...)):
    old_resume = db["parsed_resumes"].find_one({"file_name": file_name, "uploaded_by": uploaded_by})
    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "summary": summary,
        "skills": [s.strip() for s in skills.split(",") if s.strip()],
        "certifications": certifications.splitlines() if certifications else [],
        "projects": projects.splitlines() if projects else [],
        "courses": [c.strip() for c in courses.split(",") if c.strip()],
        "file_name": file_name,
        "uploaded_by": uploaded_by,
        "uploaded_at": datetime.utcnow().isoformat(),
        "education": old_resume.get("education", []),
        "experience": old_resume.get("experience", [])
    }
    score_result = get_gpt_score(resume_data)
    resume_data["resume_score"] = score_result.get("score")
    resume_data["recommendations"] = score_result.get("recommendations")
    insert_result = db["parsed_resumes"].insert_one(resume_data)
    resume_data["_id"] = str(insert_result.inserted_id)
    return templates.TemplateResponse("result.html", {"request": request, "result": resume_data})


@app.get("/profile")
async def get_profile(request: Request):
    email = request.session.get("user_email")
    if not email:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    
    user = users_collection.find_one({"email": email})
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)
    
    return {
        "username": user.get("username"),
        "email": user.get("email"),
        "password": user.get("password")
    }

@app.post("/update_profile")
async def update_profile(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    old_email = request.session.get("user_email")
    if not old_email:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    
    users_collection.update_one(
        {"email": old_email},
        {"$set": {
            "username": username,
            "email": email,
            "password": password
        }}
    )
    

    request.session["user_email"] = email

    return {"message": "Profile updated successfully"}

from fastapi.responses import FileResponse

@app.post("/generate_cover_letter")
async def generate_cover_letter(request: Request, job: str = Form(...), resume: UploadFile = File(...)):
    if not request.session.get("user_email"):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    try:
        resume_text = await parseResume(resume)
        prompt = f"Write a professional cover letter for the position '{job}' based on this resume:\n\n{resume_text}"

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": prompt }],
            temperature=0.7,
            max_tokens=500
        )
        return { "cover_letter": res.choices[0].message.content }

    except Exception as e:
        return { "cover_letter": "Error generating letter." }

@app.get("/cover_letter")
async def serve_cover_letter(request: Request):
    if not request.session.get("user_email"):
        return RedirectResponse("/site/login.html", status_code=302)
    return FileResponse("../public_site/cover_letter.html")


@app.post("/mock_interview")
async def mock_interview(
    request: Request,
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not request.session.get("user_email"):
        return JSONResponse({"error": "Not authenticated"}, status_code=401)

    try:
        resume_text = await parseResume(resume)
        prompt = (
            f"Given the following resume and job description, generate 5 mock interview questions.\n\n"
            f"Resume:\n{resume_text}\n\n"
            f"Job Description:\n{job_description}\n\n"
            f"Output only the questions, numbered."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )

        text = response.choices[0].message.content.strip()
        questions = [q.strip() for q in text.split("\n") if q.strip()]
        return {"questions": questions[:5]}

    except Exception as e:
        print("Mock Interview Error:", str(e))
        return JSONResponse({"error": "Failed to generate questions."}, status_code=500)
@app.post("/career_advice")
async def career_advice(question: str = Form(...)):
    prompt = f"Provide professional career advice for the following question:\n\n{question.strip()}\n\nAdvice:"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)