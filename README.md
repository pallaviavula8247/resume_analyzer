# AI-Powered Resume Analyzer, Job Matching & Personalized Recommendation System

A portfolio-grade Django REST Framework application that follows:

**Resume → Structured Data → Analysis → Skill Gaps → Job Matching → Recommendations**

## Highlights

- Django + Django REST Framework
- JWT authentication
- Vanilla HTML/CSS/JavaScript frontend
- PDF resume extraction with `pypdf`
- Dynamic resume parsing using section detection, regex and a skill dictionary
- Explainable ATS scoring
- Data-driven jobs and skills datasets
- Deterministic job matching and skill-gap calculation
- TF-IDF based semantic relevance for project/job descriptions
- User ownership protection on resume, analysis, matches and recommendations
- SQLite for development and PostgreSQL-ready production configuration
- WhiteNoise static files
- Gunicorn
- Docker + docker-compose
- Environment-variable based secrets/configuration
- Automated API tests
- No hard-coded candidate name, skills, resume IDs, ATS scores or recommendations

## 1. Project structure

```text
resume-analyzer/
├── backend/
│   ├── manage.py
│   ├── config/
│   ├── users/
│   ├── parser/
│   ├── analyzer/
│   ├── jobs/
│   ├── recommendations/
│   ├── datasets/
│   │   ├── jobs.json
│   │   └── skills.json
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── analysis.html
│   ├── jobs.html
│   ├── recommendations.html
│   ├── css/
│   └── js/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 2. Local setup — Windows

Open PowerShell in the project folder:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py load_datasets
python manage.py createsuperuser
python manage.py runserver
```

Backend:
`http://127.0.0.1:8000/`

The Django development server serves the frontend in this project so you do not need a second static server.

Open:
`http://127.0.0.1:8000/`

## 3. First test

1. Register a user.
2. Login.
3. Upload a real PDF resume.
4. Wait for the upload response.
5. The response contains the real database `resume_id`.
6. Open Analysis.
7. Open Job Recommendations.
8. Open Skill Recommendations.

Never put `resume_id = 1` or another fixed ID in frontend code.

## 4. Dataset loading

Jobs and skills are stored outside Python business logic:

```text
backend/datasets/jobs.json
backend/datasets/skills.json
```

Load or refresh them with:

```powershell
python manage.py load_datasets
```

The command uses `update_or_create`, so it is safe to run again after dataset edits.

## 5. API endpoints

### Authentication

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/
GET  /api/auth/profile/
```

### Resume

```text
POST /api/resumes/upload/
GET  /api/resumes/
GET  /api/resumes/<id>/
POST /api/resumes/<id>/analyze/
GET  /api/resumes/<id>/analysis/
```

### Jobs

```text
GET /api/jobs/
GET /api/jobs/<id>/
GET /api/resumes/<id>/jobs/
```

### Recommendations

```text
GET /api/resumes/<id>/recommendations/
```

### Skills

```text
GET /api/skills/
```

## 6. Scoring

The job-match engine is deterministic and configurable:

- Required skill match: 50%
- Preferred skill match: 10%
- Education relevance: 15%
- Experience relevance: 15%
- Project relevance: 10%

ATS score is also explainable and based on measurable resume quality factors.

The exact weights are defined in:

```text
backend/analyzer/services/scoring.py
```

## 7. PDF extraction

The parser uses `pypdf`. A PDF must contain extractable text.

Scanned/image-only PDFs may produce little or no text. Such files should be handled as an extraction failure rather than silently generating fake data.

## 8. Production environment

For production, set:

```env
DEBUG=False
SECRET_KEY=<long-random-secret>
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://...
CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

Then:

```bash
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 9. Docker

```bash
docker compose up --build
```

Then visit:

```text
http://localhost:8000/
```

## 10. GitHub

Create a repository and run:

```bash
git init
git add .
git commit -m "Initial professional resume analyzer"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Do NOT commit `.env`, uploaded resumes, database files or secret keys.

## 11. Recommended GitHub presentation

Before pushing:

- Add screenshots to the README.
- Add a system architecture diagram.
- Add API documentation.
- Add sample screenshots for upload, analysis and recommendations.
- Explain the scoring formula.
- Explain how ownership/security works.
- Mention the limitations of text extraction for scanned PDFs.
- Add test instructions.

## 12. Important engineering rule

This project deliberately avoids fake intelligence:

- No hard-coded candidate profile.
- No fixed resume ID.
- No random ATS score.
- No hard-coded recommended job.
- No invented certification.
- No invented LinkedIn/GitHub.
- Job recommendations are derived from stored datasets and the uploaded resume.


## 13. Automated tests

From `backend/`:

```powershell
python manage.py test
```

## 14. Important implementation note

The upload endpoint explicitly uses Django REST Framework's `MultiPartParser` and `FormParser`. This is required for browser `FormData` PDF uploads and prevents the common `request.FILES`/empty-file problem.

## 15. Human-project quality

The application is intentionally built from ordinary, explainable engineering components rather than pretending to use an LLM everywhere. The "AI" layer is represented by NLP-style extraction and TF-IDF semantic project relevance, while numeric scoring, filtering, ranking and skill-gap logic remain deterministic and auditable.
