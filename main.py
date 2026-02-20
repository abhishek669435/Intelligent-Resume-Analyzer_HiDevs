import re
import json
class ResumeParser:
    def __init__(self, text):
       self.text = text.lower()
    def extract_name(self):
        match = re.search(r"name:\s*(.*)", self.text, re.I)
        return match.group(1).strip().title()if match else"Not found"
    def extract_email(self):
        match = re.search(r"[\w\.-]+@[\w\.-]+", self.text)
        return match.group(0) if match else "Not found"
    def extract_skills(self):
        match = re.search(r"skills:\s*(.*)", self.text, re.I)
        if match:
            return[s.strip().title() for s in match.group(1).split(",")]
        return[]
    def extract_experience(self):
        match = re.search(r"(\d+)\s+years", self.text)
        return int(match.group(1)) if match else 0
    
class ResumeMatcher:
    def __init__(self, job_requirments):
       self.req_skills = job_requirments["required_skills"]
       self.opt_skills = job_requirments["optional_skills"]
       self.min_exp = job_requirments["min_experience"]

    def calculator_score(self, resume_data):
        score = 0
        matched_required = sum(i for s in self.req_skills if s in resume_data["skills"])
        score += (matched_required / len(self.req_skills)) * 60 if self.req_skills else 0

        if resume_data["experience"] >= self.min_exp:
            score += 20

            matched_optional = sum(1 for s in self.opt_skills if s in resume_data["skills"])
            score += (matched_optional / len(self.opt_skills)) * 20 if self.opt_skills else 0
            return round(score)
        def recommend(self, score):
            if score >= 75:
                return "Strong Hire"
            elif score >= 50:
                return "Consider"
            else:
                return "Reject"
            

class ResumeDatabase:
    FILE = "resumes.json"
    @staticmethod
    def save(data):
        try:
            with open(ResumeDatabase.FILE, "w") as f:
                json.dump(data, f, indent = 4)
        except IOError:
            print("Error saving data.")
    @staticmethod
    def load():
        try:
            with open(ResumeDatabase.FILE, "r") as f:
                return json.load(f)
        except:
            return []


class ReportGenerator:
    @staticmethod
    def generate(resume, score, recommendation):
        print("\n--- Resume Analysis Report ---")
        print(f"Name: {resume['name']}")
        print(f"Email: {resume['email']}") 
        print(f"Skills: {', '.join (resume['experience'])} years")
        print(f"Match Score: {score}/100")
        print(f"Hiring Recommendation: {recommendation}")
        print("--------------\n") 

job_requirments = {
    "required_skills": ["python", "sql", "Git"],
    "optional_skills": ["Aws", "Django"],
    "min_experience": 3
}


import sys
print("Paste Resume Text (Press Ctrl+D after pasting):")
resume_text = sys.stdin.read()
parser = ResumeParser(resume_text)
resume_data = {
    "name": parser.extract_name(),
    "email": parser.extract_email(),
    "skills": parser.extract_skills(),
    "experience": parser.extract_experience()
}   

matcher = ResumeMatcher(job_requirments)
score = matcher.calculate_score(resume_data)
recommendation = matcher.recommend(score)

db = ResumeDatabase.load()
db.append(resume_data)
ResumeDatabase.save(db)

ReportGenerator.generate(resume_data, score, recommendation)
                        