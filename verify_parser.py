import sys
from parser import parse_resume, extract_name, extract_contact_info, extract_skills, extract_education, extract_experience

# Sample resume text for testing
SAMPLE_RESUME_TEXT = """
Jane Doe
jane.doe@example.com | (123) 456-7890 | San Francisco, CA

Professional Summary:
Enthusiastic and results-driven Software Engineer with 4 years of experience building scalable web applications. Specialist in Python, Flask, and PostgreSQL. Proven track record of improving application performance and designing robust system design patterns.

Education:
Bachelor of Science in Computer Science
Stanford University | 2017 - 2021

Experience:
Software Engineer - Google
Jun 2021 - Present
- Designed and implemented microservices using Python, Docker, and Kubernetes.
- Optimized PostgreSQL queries, reducing API response times by 30%.
- Participated in system design and agile scrum team structures.

Intern Software Developer - Tech Solutions Inc
Jun 2020 - Aug 2020
- Built interactive web portals using JavaScript, HTML, and CSS.
- Developed backend REST API endpoints using Flask and SQLite.
"""

def run_tests():
    print("=== STARTING PARSER ENGINE VERIFICATION ===")
    
    # 1. Test Name Extraction
    print("\n1. Testing Name Extraction...")
    name = extract_name(SAMPLE_RESUME_TEXT)
    print(f"Extracted Name: '{name}'")
    assert name == "Jane Doe", f"Expected 'Jane Doe', got '{name}'"
    print("Name Extraction: SUCCESS")
    
    # 2. Test Contact Details Extraction
    print("\n2. Testing Contact Info Extraction...")
    email, phone = extract_contact_info(SAMPLE_RESUME_TEXT)
    print(f"Extracted Email: '{email}'")
    print(f"Extracted Phone: '{phone}'")
    assert email == "jane.doe@example.com", f"Expected 'jane.doe@example.com', got '{email}'"
    assert phone == "(123) 456-7890", f"Expected '(123) 456-7890', got '{phone}'"
    print("Contact Info Extraction: SUCCESS")
    
    # 3. Test Skills Extraction
    print("\n3. Testing Skills Extraction...")
    skills = extract_skills(SAMPLE_RESUME_TEXT)
    print(f"Extracted Skills: {skills}")
    expected_skills = ["Python", "Flask", "PostgreSQL", "System Design", "Docker", "Kubernetes", "Agile", "Scrum", "JavaScript", "HTML", "CSS", "REST API", "SQLite"]
    matched_skills = [s for s in expected_skills if s in skills]
    print(f"Matched expected skills: {matched_skills}")
    assert len(matched_skills) >= 5, "Expected to extract at least 5 skills"
    print("Skills Extraction: SUCCESS")
    
    # 4. Test Education Extraction
    print("\n4. Testing Education Extraction...")
    lines = [l.strip() for l in SAMPLE_RESUME_TEXT.split('\n') if l.strip()]
    edu_section = []
    in_edu = False
    for l in lines:
        if "education" in l.lower():
            in_edu = True
            continue
        if in_edu and "experience" in l.lower():
            break
        if in_edu:
            edu_section.append(l)
            
    education = extract_education(edu_section)
    print(f"Extracted Education: {education}")
    assert len(education) > 0, "Expected at least one education entry"
    assert education[0]['degree'] == "Bachelor's", f"Expected Bachelor's, got {education[0]['degree']}"
    assert "Stanford University" in education[0]['institution'], f"Expected Stanford University, got {education[0]['institution']}"
    assert education[0]['end_year'] == "2021", f"Expected 2021, got {education[0]['end_year']}"
    print("Education Extraction: SUCCESS")
    
    # 5. Test Experience Extraction
    print("\n5. Testing Experience Extraction...")
    exp_section = []
    in_exp = False
    for l in lines:
        if l.lower().strip(':') == "experience":
            in_exp = True
            continue
        if in_exp:
            exp_section.append(l)
            
    experience = extract_experience(exp_section)
    print(f"Extracted Experience: {experience}")
    assert len(experience) >= 2, "Expected at least 2 experience entries"
    assert "Google" in experience[0]['company'], f"Expected Google, got {experience[0]['company']}"
    assert experience[0]['job_title'] == "Software Engineer", f"Expected Software Engineer, got {experience[0]['job_title']}"
    assert "Google" in experience[0]['company'], f"Expected Google, got {experience[0]['company']}"
    print("Experience Extraction: SUCCESS")
    
    print("\n=== ALL PARSER TESTS PASSED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_tests()
