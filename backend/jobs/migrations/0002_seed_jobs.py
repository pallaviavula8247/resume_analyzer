from django.db import migrations


def seed_jobs(apps, schema_editor):
    Job = apps.get_model("jobs", "Job")

    jobs = [
        {
            "title": "Python Developer",
            "description": "Develop and maintain Python applications and backend systems.",
            "required_skills": ["Python", "SQL", "Git"],
            "preferred_skills": ["Django", "REST API"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Django Developer",
            "description": "Build web applications and REST APIs using Django and Python.",
            "required_skills": ["Python", "Django", "SQL", "REST API", "Git"],
            "preferred_skills": ["PostgreSQL", "Docker"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Full Stack Developer",
            "description": "Develop frontend and backend web applications.",
            "required_skills": ["HTML", "CSS", "JavaScript", "Python", "SQL", "Git"],
            "preferred_skills": ["Django", "React"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Backend Developer",
            "description": "Develop backend services, APIs, and database-driven applications.",
            "required_skills": ["Python", "SQL", "REST API", "Git"],
            "preferred_skills": ["Django", "PostgreSQL"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Frontend Developer",
            "description": "Create responsive and interactive web interfaces.",
            "required_skills": ["HTML", "CSS", "JavaScript", "Git"],
            "preferred_skills": ["React", "Angular"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Data Analyst",
            "description": "Analyze data and create reports and dashboards for business decisions.",
            "required_skills": ["SQL", "Excel", "Power BI", "Python"],
            "preferred_skills": ["Pandas", "NumPy"],
            "education": ["Computer Science", "Data Science", "Statistics"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Data Scientist",
            "description": "Build machine learning models and analyze large datasets.",
            "required_skills": [
                "Python",
                "SQL",
                "Pandas",
                "NumPy",
                "Scikit-learn",
                "Machine Learning",
            ],
            "preferred_skills": ["TensorFlow", "PyTorch"],
            "education": ["Computer Science", "Data Science", "Artificial Intelligence"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Machine Learning Engineer",
            "description": "Develop and deploy machine learning models and AI systems.",
            "required_skills": [
                "Python",
                "Machine Learning",
                "Scikit-learn",
                "SQL",
                "Git",
            ],
            "preferred_skills": ["TensorFlow", "PyTorch", "Docker"],
            "education": ["Computer Science", "Artificial Intelligence", "Data Science"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "AI Engineer",
            "description": "Build artificial intelligence and machine learning applications.",
            "required_skills": [
                "Python",
                "Machine Learning",
                "NLP",
                "SQL",
                "Git",
            ],
            "preferred_skills": ["Deep Learning", "TensorFlow", "PyTorch"],
            "education": ["Computer Science", "Artificial Intelligence"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Software Developer",
            "description": "Design, develop, test, and maintain software applications.",
            "required_skills": ["Python", "Java", "SQL", "Git"],
            "preferred_skills": ["REST API", "Docker"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Java Developer",
            "description": "Develop enterprise and backend applications using Java.",
            "required_skills": ["Java", "SQL", "Git"],
            "preferred_skills": ["Spring Boot", "REST API"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Java Full Stack Developer",
            "description": "Develop complete web applications using Java and frontend technologies.",
            "required_skills": [
                "Java",
                "HTML",
                "CSS",
                "JavaScript",
                "SQL",
                "Git",
            ],
            "preferred_skills": ["Spring Boot", "React"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Business Analyst",
            "description": "Analyze business requirements, data, and processes.",
            "required_skills": ["Excel", "SQL", "Communication"],
            "preferred_skills": ["Power BI", "Python"],
            "education": ["Business Administration", "Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
        {
            "title": "Cloud DevOps Engineer",
            "description": "Build, deploy, and maintain cloud infrastructure and CI/CD pipelines.",
            "required_skills": ["Linux", "Git", "Docker", "CI/CD"],
            "preferred_skills": ["AWS", "Azure", "Kubernetes"],
            "education": ["Computer Science", "Information Technology"],
            "experience_level": "Entry Level",
            "experience_years": 0,
        },
    ]

    for job_data in jobs:
        Job.objects.update_or_create(
            title=job_data["title"],
            defaults=job_data,
        )


def remove_jobs(apps, schema_editor):
    Job = apps.get_model("jobs", "Job")

    titles = [
        "Python Developer",
        "Django Developer",
        "Full Stack Developer",
        "Backend Developer",
        "Frontend Developer",
        "Data Analyst",
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
        "Software Developer",
        "Java Developer",
        "Java Full Stack Developer",
        "Business Analyst",
        "Cloud DevOps Engineer",
    ]

    Job.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_jobs,
            remove_jobs,
        ),
    ]