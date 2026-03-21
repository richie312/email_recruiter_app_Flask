# noTify Architecture Wiki

This GitBook documents the noTify application from an architecture and code-flow point of view.

It focuses on:

- the Flask application entrypoint in `main.py`
- the supporting modules under `src/`, `config/`, `data/`, and `templates/`
- the helper scrapers for online jobs and email jobs
- the supporting microservices around Kafka, MySQL, and Redis
- the resume builder module under `PythonResumeBuilder/`

Use the chapters in this wiki to understand how data enters the platform, how a user applies for jobs, and how supporting services interact with the main application.
