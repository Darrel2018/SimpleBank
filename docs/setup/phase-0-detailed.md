# Phase 0 — Detailed Project Setup Documentation

## Purpose

Phase 0 established the development foundation for SimpleBank. The goal was to prepare a clean Django project architecture with MongoDB and HTMX before creating any banking modules.

This phase intentionally focused on infrastructure instead of business features.

---

# Technology Stack

| Technology    | Purpose                                                  |
| ------------- | -------------------------------------------------------- |
| Python        | Primary programming language.                            |
| Django 6.1    | Web framework and server-rendered application framework. |
| HTMX 2.0.4    | Interactive frontend without a JavaScript framework.     |
| MongoDB       | Primary database.                                        |
| PyMongo       | Official MongoDB driver used by Django.                  |
| python-dotenv | Environment variable management.                         |

---

# Development Environment

A dedicated Python virtual environment was created to isolate project dependencies.

## Virtual Environment

```bash
python -m venv venv
```

The virtual environment is activated before running any project commands.

---

# Project Structure

The project was organized into a modular structure before any Django apps were implemented.

```text
SimpleBank/
│
├── apps/
├── config/
├── docs/
├── media/
├── scripts/
├── static/
├── templates/
├── tests/
│
├── manage.py
├── requirements.txt
├── .env
├── .env.example
└── .gitignore
```

### Directory Responsibilities

| Directory    | Responsibility                                                          |
| ------------ | ----------------------------------------------------------------------- |
| `apps/`      | All Django applications (authentication, accounts, transactions, etc.). |
| `config/`    | Django configuration and database connection modules.                   |
| `templates/` | Shared HTML templates organized by feature.                             |
| `static/`    | CSS, JavaScript, fonts, icons, and images.                              |
| `media/`     | User-uploaded files during development.                                 |
| `docs/`      | Architecture and development documentation.                             |
| `scripts/`   | Utility scripts such as database seeders.                               |
| `tests/`     | Project-wide tests.                                                     |

---

# Environment Variables

Sensitive configuration was moved out of source code into a `.env` file.

## Environment Variables

```env
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=simplebank
```

`settings.py` loads these values using `python-dotenv`.

### Benefits

* Secret keys are not committed to Git.
* Local and production configurations remain separate.
* MongoDB connection details can change without modifying application code.

---

# Django Configuration

The Django configuration was updated to support a scalable project.

## Templates

A global templates directory was registered.

```text
templates/
```

This allows templates to be shared across applications.

## Static Files

Global static configuration was added.

* `STATIC_URL`
* `STATICFILES_DIRS`
* `STATIC_ROOT`

## Media Files

Media configuration was added for future uploads.

* `MEDIA_URL`
* `MEDIA_ROOT`

Development URLs were configured so uploaded files are served while `DEBUG=True`.

---

# MongoDB Integration

The project uses the official MongoDB Python driver instead of Django's relational ORM.

## Design Decision

PyMongo was selected because:

* It is officially maintained by MongoDB.
* It supports current MongoDB features.
* It avoids compatibility issues found in unofficial Django MongoDB adapters.
* It gives full control over collections and queries.

## Database Connection Module

Location:

```text
config/database/mongodb.py
```

Responsibilities:

* Create a reusable `MongoClient`.
* Read connection information from Django settings.
* Expose a reusable database instance.

## Connection Test

CRUD operations were successfully tested.

### Operations Performed

1. Created the `users` collection.
2. Inserted a sample customer.
3. Retrieved the customer.
4. Counted documents.
5. Deleted the sample customer.
6. Dropped the test collection.

This verified successful communication between Django and MongoDB.

---

# MongoDB Atlas Strategy

SimpleBank will eventually use MongoDB Atlas.

## Planned Structure

```text
Cluster0
│
├── simplebank
│   ├── users
│   ├── customers
│   ├── accounts
│   ├── transactions
│   ├── beneficiaries
│   ├── payments
│   ├── notifications
│   ├── statements
│   ├── disputes
│   └── audit_logs
│
├── ecommerce
├── school_management
└── other_projects
```

### Architecture Decision

`Cluster0` is shared across multiple portfolio projects.

Each project receives its own MongoDB database (`simplebank`), preventing collections from different projects from mixing together.

Switching from local MongoDB to Atlas should only require changing `MONGODB_URI` inside `.env`.

---

# HTMX Integration

HTMX was added globally to the application.

## Configuration

HTMX is loaded in the global base template.

```text
templates/base/base.html
```

A CSRF configuration script was added so HTMX automatically includes Django's CSRF token for non-GET requests.

### Result

Future forms and actions (login, transfers, beneficiaries, payments) will work with HTMX without additional CSRF configuration.

---

# Base Template

A reusable application layout was created.

Responsibilities include:

* HTML document structure.
* HTMX inclusion.
* Global CSS.
* Global JavaScript.
* Template inheritance blocks.

Every future page will extend this template.

---

# Dashboard App

A lightweight dashboard application was created to verify routing.

Files created:

```text
apps/dashboard/
├── __init__.py
├── apps.py
├── views.py
└── urls.py
```

A temporary home page was created in:

```text
templates/dashboard/home.html
```

The application successfully renders through:

```text
config.urls
    ↓
apps.dashboard.urls
    ↓
apps.dashboard.views
    ↓
templates/dashboard.home
```

---

# HTMX Verification

A temporary HTMX button was created to verify asynchronous requests.

Verification included:

* HTMX loaded correctly.
* Browser reported `htmx.version` as `2.0.4`.
* Template inheritance worked correctly.
* Static JavaScript loaded successfully.

---

# Git Configuration

The repository was cleaned before development.

## `.gitignore`

Ignored items include:

```text
venv/
.env
__pycache__/
*.py[cod]
```

This prevents local environments, secrets, and Python cache files from entering version control.

---

# Requirements Cleanup

Unused packages from previous work were removed.

The environment now contains only packages required for the project setup phase plus MongoDB support.

This keeps dependency management clean and reproducible.

---

# Phase 0 Deliverables

* Fully configured Django project.
* Environment variable management.
* MongoDB integration using PyMongo.
* Verified database connectivity.
* HTMX integrated into the frontend.
* Modular project structure established.
* Dashboard app configured as the first Django application.
* Documentation structure established for future phases.

---

# Exit Criteria

Phase 0 is considered complete because:

* Django runs successfully.
* HTMX is available globally.
* MongoDB accepts CRUD operations.
* Project architecture is organized for modular development.
* The application is ready to begin implementing authentication in Phase 1.

---

# Next Phase Preview

Phase 1 will focus on the Authentication module, including:

* User authentication architecture.
* Registration workflow.
* Mock identity verification.
* Mock OTP / MFA.
* Login and logout flows.
* MongoDB `users` collection design.
* Role-based authentication for customers, employees, and administrators.
