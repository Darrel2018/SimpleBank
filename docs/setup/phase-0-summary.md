# Phase 0 — Project Setup Summary

## Objective

Set up the foundational development environment for the SimpleBank project before implementing any banking functionality.

## Completed Tasks

* Created a Python virtual environment (`venv`).
* Installed and configured Django.
* Created the Django project using a dedicated `config` project module.
* Created a clean project folder structure (`apps`, `templates`, `static`, `media`, `docs`, `scripts`, `tests`).
* Configured environment variables using `.env` and `python-dotenv`.
* Moved the Django `SECRET_KEY` into the `.env` file.
* Cleaned the virtual environment and generated a minimal `requirements.txt`.
* Installed and configured MongoDB using the official `pymongo` driver.
* Created a reusable MongoDB connection module (`config/database/mongodb.py`).
* Verified MongoDB connectivity by creating, reading, and deleting a test document.
* Installed and configured HTMX.
* Created a global base template (`templates/base/base.html`).
* Configured global static files and media files.
* Created the initial `dashboard` app with routing and a test HTMX page.
* Verified HTMX was successfully loaded (`htmx.version == "2.0.4"`).

## Outcome

The project now has a clean Django + HTMX + MongoDB foundation and is ready to begin implementing banking functionality in Phase 1.
