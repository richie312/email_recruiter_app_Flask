# User Flows And API Routes

## Authentication and session flow

Main authentication routes:

- `/`
- `/login`
- `/signup`
- `/logout/`
- `/password_reset`
- `/new_password`

The app uses session-based access control with a custom `login_required` decorator.

## Dashboard and navigation

After login, users land on the dashboard flow driven by:

- `/dashboard`

The dashboard template is `templates/user_form.html`, which exposes:

- manual recruiter application submission
- cache update and cache inspection
- navigation to application details
- navigation to settings and user profile
- navigation to job dashboard

## Manual apply flow

The manual apply path is:

1. user fills the form in `user_form.html`
2. POST is sent to `/addDetails`
3. an `Application` object is created
4. the row is inserted into MySQL
5. recruiter email is sent through `send_mail()`

This flow uses:

- default resume content from `docs/Resume.pdf`
- inline image content from `images/`
- recruiter details from form submission

### Manual apply sequence diagram

```mermaid
sequenceDiagram
    participant U as User
    participant UI as user_form.html
    participant F as Flask main.py
    participant A as Application
    participant DB as MySQL
    participant M as send_mail()
    participant G as Gmail or SMTP

    U->>UI: Fill recruiter application form
    UI->>F: POST /addDetails
    F->>A: Create Application(data)
    F->>A: add_details()
    A->>DB: INSERT company_email1 row
    F->>M: send_mail(user, app_password, recruiter_email, subject, html_msg)
    M->>G: Send recruiter email with resume/template assets
    F-->>UI: Render success response
```

## Application history flow

Application viewing paths are:

- `/application_details`
- `/get_data`
- `/index_get_data`
- `/delete_form`
- `/delete`

`/index_get_data` returns row data formatted for UI tables.

## Cache management flow

The application supports a temporary in-memory cache using `Application.all_contacts`.

Related routes:

- `/check_cache`
- `/update`

This allows a user to:

- inspect cached applications
- prune selected cached entries
- bulk-flush cache to MySQL
- clear cache without persistence

## External job dashboard flow

The job dashboard is rendered through:

- `/show_jobs`
- `/job_details`
- `/apply_job`

Behavior:

- `/job_details` fetches data from `job_api_url`
- response rows are reshaped into dashboard-ready records
- `templates/job_posting.html` renders the DataTables UI
- the user selects a row through a radio button
- `/apply_job` maps the selected row into the `Application` format and sends the mail

This matches your instruction that one route of data ingestion is through automated radio-button selection from the job list dashboard.

### Dashboard apply sequence diagram

```mermaid
sequenceDiagram
    participant U as User
    participant UI as job_posting.html
    participant F as Flask main.py
    participant API as External Job API or Kafka-backed Job Service
    participant A as Application
    participant DB as MySQL
    participant M as send_mail()
    participant G as Gmail or SMTP

    U->>UI: Open Apply Jobs page
    UI->>F: GET /job_details
    F->>API: GET job_api_url
    API-->>F: Return structured job rows
    F-->>UI: Render DataTables payload
    U->>UI: Select radio button row and click Apply
    UI->>F: POST /apply_job with selected job JSON
    F->>A: Create Application(mapped job data)
    F->>A: add_details()
    A->>DB: INSERT company_email1 row
    F->>M: send_mail(default sender, app password, recruiter email, subject, html_msg)
    M->>G: Send application email
    F-->>UI: Render apply response
```

## Profile and settings flow

Supporting user-profile routes:

- `/user_profile`
- `/settings`
- `/project_details`

These flows manage:

- image upload
- resume upload
- profile upload
- Git/project metadata
- user profile rendering

## Resume builder flow

The resume builder page is exposed through:

- `/render_resume_builder`

It loads:

- `PythonResumeBuilder/resume.json`
- `PythonResumeBuilder/template.html`

and renders them inside `templates/resume_builder.html`.
