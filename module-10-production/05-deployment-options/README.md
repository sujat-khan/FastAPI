# Lesson 05 — Deployment Options

## Production Server Setup

### Gunicorn + Uvicorn Workers (Recommended)

```bash
pip install gunicorn

# Run with multiple workers
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --access-logfile -
```

### How Many Workers?

```
workers = (2 × CPU cores) + 1
```

For a 4-core server: `workers = 9`

| Option | Purpose |
|--------|---------|
| `--workers` | Number of worker processes |
| `--worker-class` | Use Uvicorn's async worker |
| `--bind` | Address to listen on |
| `--timeout` | Max seconds per request |
| `--access-logfile -` | Log to stdout |

---

## Deployment Platforms

### 1. Docker + Cloud Run / ECS / Kubernetes
Most flexible. Works anywhere containers run.

```bash
# Build and push image
docker build -t my-api .
docker push registry.example.com/my-api:latest

# Deploy to your orchestrator
```

### 2. Railway / Render / Fly.io
Simplest deployment — connect your repo and deploy:

```
1. Push code to GitHub
2. Connect repo to Railway/Render
3. Set environment variables
4. Deploy automatically on push
```

### 3. Traditional VPS (DigitalOcean, AWS EC2)
Full control setup:

```bash
# On the server:
# 1. Install Python, create venv
# 2. Clone your repo
# 3. Install dependencies
# 4. Run with Gunicorn
# 5. Set up Nginx as reverse proxy
# 6. Use systemd for process management
# 7. Set up SSL with Certbot
```

---

## Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/myapi
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d api.example.com

# Auto-renewal is configured automatically
```

---

## Environment Variables for Production

```env
# .env.production
DEBUG=false
DATABASE_URL=postgresql://user:pass@db-host:5432/prod_db
SECRET_KEY=very-long-random-string-keep-this-safe
ALLOWED_ORIGINS=["https://myapp.com"]
LOG_LEVEL=warning
```

---

## Production Checklist

| Item | Status |
|------|--------|
| ☐ Debug mode disabled | `DEBUG=false` |
| ☐ Strong secret key | Random, 32+ characters |
| ☐ HTTPS enabled | SSL certificate installed |
| ☐ CORS configured | Only allow your frontend domain |
| ☐ Database connection pooling | Proper pool_size settings |
| ☐ Logging configured | Structured logs, proper levels |
| ☐ Health check endpoint | `/health` for monitoring |
| ☐ Rate limiting | Prevent abuse |
| ☐ Error handling | Custom error responses, no stacktraces |
| ☐ Environment variables | No secrets in code |
| ☐ Database migrations | Alembic for schema changes |
| ☐ Monitoring | Metrics, alerts, dashboards |
| ☐ Backup strategy | Database backups scheduled |
| ☐ CI/CD pipeline | Automated testing and deployment |

---

## Congratulations! 🎉

You've completed the **FastAPI Complete Course**! You now know how to:

- ✅ Build RESTful APIs with FastAPI
- ✅ Handle requests (path, query, body, files)
- ✅ Validate data with Pydantic
- ✅ Use the Dependency Injection system
- ✅ Connect to databases with SQLAlchemy
- ✅ Implement JWT authentication
- ✅ Use WebSockets, middleware, and background tasks
- ✅ Write comprehensive tests
- ✅ Deploy to production

### What's Next?

1. **Build a real project** — a blog API, task manager, or e-commerce backend
2. **Explore the [FastAPI docs](https://fastapi.tiangolo.com/)** — there's always more to learn
3. **Join the community** — FastAPI GitHub, Discord, Reddit
4. **Contribute** — open source needs your help!

Happy building! 🚀🐍
