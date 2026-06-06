# Lesson 06 — Static Files & Templates

## Serving Static Files

Serve CSS, JavaScript, images, and other static assets:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Now accessible at:
# http://localhost:8000/static/style.css
# http://localhost:8000/static/script.js
# http://localhost:8000/static/images/logo.png
```

Directory structure:
```
project/
├── main.py
├── static/
│   ├── style.css
│   ├── script.js
│   └── images/
│       └── logo.png
└── templates/
    └── index.html
```

---

## Jinja2 Templates

Render HTML pages with dynamic data:

```bash
pip install jinja2
```

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,   # Required!
            "title": "My FastAPI App",
            "items": ["Item 1", "Item 2", "Item 3"],
        },
    )

@app.get("/users/{username}")
async def user_profile(request: Request, username: str):
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "username": username},
    )
```

### Template File (`templates/index.html`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>{{ title }}</h1>
    <ul>
        {% for item in items %}
            <li>{{ item }}</li>
        {% endfor %}
    </ul>

    {% if items|length > 0 %}
        <p>Total: {{ items|length }} items</p>
    {% else %}
        <p>No items found.</p>
    {% endif %}
</body>
</html>
```

---

## Jinja2 Template Syntax Quick Reference

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ var }}` | Output variable | `{{ user.name }}` |
| `{% if %}` | Conditional | `{% if logged_in %}...{% endif %}` |
| `{% for %}` | Loop | `{% for item in items %}...{% endfor %}` |
| `{# comment #}` | Comment | `{# This is hidden #}` |
| `{{ var\|filter }}` | Filters | `{{ name\|upper }}` |
| `{% include %}` | Include template | `{% include "header.html" %}` |
| `{% extends %}` | Template inheritance | `{% extends "base.html" %}` |

---

## Template Inheritance (Layouts)

### Base Template (`templates/base.html`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My App{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2025 My App</p>
    </footer>
</body>
</html>
```

### Page Template (`templates/home.html`):
```html
{% extends "base.html" %}

{% block title %}Home - My App{% endblock %}

{% block content %}
<h1>Welcome Home!</h1>
<p>This inherits the layout from base.html</p>
{% endblock %}
```

---

## Key Takeaways

1. **`StaticFiles`** serves CSS, JS, images from a directory
2. **`Jinja2Templates`** renders HTML with dynamic data
3. **Always pass `request`** to template context
4. **Template inheritance** avoids HTML duplication
5. **FastAPI is primarily for APIs** — use templates for simple UIs, use React/Vue for complex frontends

---

> **Next Module**: [Module 09 — Testing & Debugging →](../../module-09-testing/)
