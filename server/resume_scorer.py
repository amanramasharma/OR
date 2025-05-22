def calculate_resume_score(data: dict) -> int:
    score = 0

    # Summary (20 points)
    if data.get("summary"):
        score += 20


    # Skills (20 points)
    if isinstance(data.get("skills"), list) and len(data["skills"]) >= 5:
        score += 20
    elif isinstance(data.get("skills"), str) and len(data["skills"].split(",")) >= 5:
        score += 20


    # Experience (20 points)
    if len(data.get("experience", [])) >= 2:
        score += 20


    # Certifications or Projects (20 points)
    if data.get("certifications") or data.get("projects"):
        score += 20


    # Education with GPA and Year (20 points)
    education = data.get("education", [])
    for edu in education:
        if edu.get("year") and edu.get("degree") and edu.get("institution"):
            score += 20
            break

    return min(score, 100)
