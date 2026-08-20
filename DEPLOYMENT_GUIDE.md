# Deployment Guide

## Option A — Render / Railway / similar Python host

1. Push the repository to GitHub.
2. Create a PostgreSQL database.
3. Create a web service from the GitHub repository.
4. Build command:

```bash
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py load_datasets
python backend/manage.py collectstatic --noinput
```

5. Start command:

```bash
gunicorn --chdir backend config.wsgi:application --bind 0.0.0.0:$PORT
```

6. Set environment variables from `backend/.env.example`.
7. Set `DEBUG=False`.
8. Set your production domain in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.
9. Verify:

```text
/health/
/admin/
/api/auth/login/
```

## Option B — Docker VPS

```bash
docker compose up --build -d
```

For a public VPS, put Nginx or Caddy in front of Gunicorn and enable HTTPS.

## Security checklist

- Use a strong random SECRET_KEY.
- Never commit `.env`.
- Use PostgreSQL in production.
- Keep uploaded resume media outside the Git repository.
- Use HTTPS.
- Configure ALLOWED_HOSTS.
- Configure CSRF_TRUSTED_ORIGINS.
- Back up the database.
- Restrict admin access.
- Consider antivirus scanning for public uploads.
- Add OCR only if scanned resumes are a required feature.
