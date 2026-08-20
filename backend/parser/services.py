import re
from pathlib import Path
from pypdf import PdfReader

from django.conf import settings

SKILL_CATALOG = [
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
    "HTML", "CSS", "SQL", "Django", "Flask", "FastAPI", "React",
    "Angular", "Vue", "Node.js", "Express.js", "Spring Boot",
    "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis",
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "Power BI", "Tableau", "Excel", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "Git", "GitHub", "REST API", "REST",
    "Linux", "CI/CD", "Jenkins", "Selenium", "Figma", "Agile",
]

SECTION_ALIASES = {
    "education": ["education", "academic background", "academics", "qualification"],
    "experience": ["experience", "work experience", "professional experience", "employment"],
    "projects": ["projects", "academic projects", "personal projects"],
    "skills": ["skills", "technical skills", "core skills", "technologies"],
    "certifications": ["certifications", "certificates", "licenses"],
    "achievements": ["achievements", "awards", "accomplishments"],
    "languages": ["languages", "language proficiency"],
}

def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        text = "\n".join(pages).strip()
        if not text:
            raise ValueError(
                "No selectable text was extracted from this PDF. "
                "If the resume is scanned/image-only, OCR is required."
            )
        return text
    except Exception as exc:
        raise ValueError(f"PDF extraction failed: {exc}") from exc

def normalize(text):
    return re.sub(r"[ \t]+", " ", text or "").strip()

def find_first(patterns, text, flags=re.I):
    for pattern in patterns:
        match = re.search(pattern, text or "", flags)
        if match:
            return normalize(match.group(1))
    return None

def extract_contact(text):
    email = find_first([r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})"], text)
    phone = find_first([
        r"(\+?\d[\d\s().-]{8,}\d)"
    ], text)

    urls = re.findall(r"https?://[^\s<>()]+", text or "", flags=re.I)
    linkedin = next((u.rstrip(".,)") for u in urls if "linkedin.com" in u.lower()), None)
    github = next((u.rstrip(".,)") for u in urls if "github.com" in u.lower()), None)

    portfolio = next(
        (u.rstrip(".,)") for u in urls
         if "linkedin.com" not in u.lower() and "github.com" not in u.lower()),
        None
    )

    lines = [normalize(x) for x in text.splitlines() if normalize(x)]
    name = None
    for line in lines[:10]:
        if email and email in line:
            continue
        if re.search(r"resume|curriculum vitae|cv", line, re.I):
            continue
        if 2 <= len(line.split()) <= 5 and len(line) <= 80 and not re.search(r"\d", line):
            name = line
            break

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
    }

def split_sections(text):
    lines = [normalize(x) for x in text.splitlines()]
    sections = {}
    current = "header"
    sections[current] = []

    aliases = {}
    for canonical, names in SECTION_ALIASES.items():
        for name in names:
            aliases[re.sub(r"[^a-z]", "", name.lower())] = canonical

    for line in lines:
        key = re.sub(r"[^a-z]", "", line.lower())
        if key in aliases and len(line) < 70:
            current = aliases[key]
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items()}

def extract_skills(text):
    found = []
    low = (text or "").lower()
    for skill in SKILL_CATALOG:
        pattern = r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, low):
            found.append(skill)
    return sorted(set(found))

def parse_list_lines(section):
    values = []
    for line in (section or "").splitlines():
        line = re.sub(r"^[•●▪◦\-*]+\s*", "", line).strip()
        if line and len(line) >= 2:
            values.append(line)
    return values[:30]

def extract_education(section):
    records = []
    for block in re.split(r"\n(?=\S)", section or ""):
        block = normalize(block)
        if not block:
            continue
        year = find_first([r"((?:19|20)\d{2}\s*(?:-|–|to)\s*(?:19|20)?\d{2})", r"((?:19|20)\d{2})"], block)
        score = find_first([r"((?:CGPA|GPA|Percentage|Score)\s*[:\-]?\s*[\d.]+%?)"], block)
        records.append({
            "degree": block[:120],
            "institution": None,
            "year": year,
            "score": score,
        })
    return records[:10]

def extract_experience(section):
    records = []
    blocks = [normalize(x) for x in re.split(r"\n(?=\S)", section or "") if normalize(x)]
    for block in blocks[:10]:
        years = re.findall(r"(?:19|20)\d{2}", block)
        records.append({
            "role": block[:120],
            "company": None,
            "duration": " - ".join(years[:2]) if len(years) >= 2 else None,
            "responsibilities": [block],
        })
    return records

def extract_projects(section):
    records = []
    blocks = [normalize(x) for x in re.split(r"\n(?=\S)", section or "") if normalize(x)]
    for block in blocks[:15]:
        technologies = [s for s in SKILL_CATALOG if re.search(r"(?<![a-z0-9])" + re.escape(s.lower()) + r"(?![a-z0-9])", block.lower())]
        records.append({
            "title": block[:100],
            "description": block,
            "technologies": sorted(set(technologies)),
        })
    return records

def parse_resume(text):
    sections = split_sections(text)
    contact = extract_contact(text)
    return {
        "personal_info": contact,
        "skills": extract_skills(text),
        "education": extract_education(sections.get("education", "")),
        "experience": extract_experience(sections.get("experience", "")),
        "projects": extract_projects(sections.get("projects", "")),
        "certifications": parse_list_lines(sections.get("certifications", "")),
        "languages": parse_list_lines(sections.get("languages", "")),
        "achievements": parse_list_lines(sections.get("achievements", "")),
    }
