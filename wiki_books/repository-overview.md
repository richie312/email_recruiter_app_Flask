# Repository Overview

## Top-level layout

The repository is centered around a Flask application in `main.py`, with supporting modules and templates arranged around it.

Important directories:

- `src/`: reusable application modules, Flask bootstrap, persistence helpers, and utility functions
- `config/`: database connection logic
- `data/`: sample payloads used by helper agents
- `templates/`: Jinja/HTML templates for the main user interface
- `PythonResumeBuilder/`: standalone resume builder assets and generator logic
- `email-agent-tests/`: helper services that scrape jobs from email and from online sources, then publish to Kafka
- `docs/`: runtime document assets such as the default resume PDF
- `images/`: static image assets used in email and UI rendering

## Primary entrypoints

Main runtime entrypoints are:

- `main.py`: web application entrypoint for the noTify Flask app
- `email-agent-tests/run_scrape_job.py`: helper runner for scraping job emails and publishing structured jobs
- `email-agent-tests/remotejob_agent.py`: separate online job search helper

## Architectural intent

The repo combines:

- a user-facing job application interface
- a persistence layer for applied job records
- email sending to recruiters
- an externalized job-ingestion path through Kafka-connected helper services
- a resume generation utility for candidate profile management
