from pydantic import BaseModel
from typing import List, Optional

class Experience(BaseModel):
    title: str
    company: str
    duration: Optional[str] = None

class Education(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = None

class ResumeModel(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    education: List[Education]
    experience: List[Experience]