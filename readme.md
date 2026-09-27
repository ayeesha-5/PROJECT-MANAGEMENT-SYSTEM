Since your friend already has PostgreSQL and database created, steps are simpler! 👇

---

**STEP 1 — Install Python**
- Download Python 3.11 from 👉 https://www.python.org/downloads/
- During installation ✅ check **"Add Python to PATH"**
- Click Install Now

---

**STEP 2 — Install VS Code**
- Download from 👉 https://code.visualstudio.com/

---

**STEP 3 — Extract zip and open in VS Code**
- Extract the zip file
- Open VS Code
- File → Open Folder → select the extracted folder

---

**STEP 4 — Open terminal in VS Code and install dependencies:**

```bash
pip install django psycopg2-binary djangorestframework pillow
```

---

**STEP 5 — Update `settings.py` with her PostgreSQL password:**

Find DATABASES section and update:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pms_db',
        'USER': 'postgres',
        'PASSWORD': 'her_postgres_password_here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

**STEP 6 — Run migrations:**

```bash
python manage.py migrate
```

---

**STEP 7 — Run server:**

```bash
python manage.py runserver
```

---

**STEP 8 — Open browser:**

| Page | URL |
|---|---|
| Register | http://127.0.0.1:8000/accounts/register/ |
| Login | http://127.0.0.1:8000/accounts/login/ |
| Dashboard | http://127.0.0.1:8000/accounts/dashboard/ |
| Projects | http://127.0.0.1:8000/projects/ |
| Tasks | http://127.0.0.1:8000/tasks/ |
| Teams | http://127.0.0.1:8000/teams/ |
| Reports | http://127.0.0.1:8000/reports/ |
| Files | http://127.0.0.1:8000/files/ |
| Notifications | http://127.0.0.1:8000/notifications/ |

---

⚠️ **One important thing** — tell your friend the only thing she needs to change is the **PASSWORD** in `settings.py`. Everything else stays the same!

Tell me once she runs it — then we finish **Module 7 Chat!** 🚀