# noTify
![Enter Details Home Page](./images/noTify.ico.png)

The **noTify** is a Flask-based distributed microservice application designed to automate the process of sending emails to specific recruiters. It also stores job application data in database for tracking and management. The app integrates with Redis for caching and Kafka for asynchronous messaging, ensuring scalability and efficiency.



---

## Features

- **Automated Email Sending**: Sends personalized emails to recruiters with job application details.
- **Job Data Management**: Stores job application data in MySQL database.
- **Redis Integration**: Uses Redis for caching job data and maintaining application state.
- **Kafka Integration**: Publishes and consumes job data asynchronously using Kafka. We use confluent Kafka.
- **User-Friendly Interface**: Provides a simple and intuitive web interface for users to apply for jobs.
- **Google Authentication**: Supports Google OAuth for secure user login.
- **Error Handling**: Robust error handling for database operations and email sending.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: MySQL Hosted on local Raspberry Server on a container
- **Caching**: Redis
- **Messaging**: Kafka
- **Email Service**: Yagmail (Gmail SMTP)
- **Frontend**: HTML, CSS, JavaScript (DataTables for dynamic tables)
- **Authentication**: Google OAuth2
- **Containerization**: Docker (for MySQL and Redis)

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Redis server
- Kafka server
- MySQL database (Amazon RDS or local)
- Docker (optional, for containerized services)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/noTify.git
   cd noTify

   python main.py

   ```
2. To test the feature of the application, open this on your browser: [http://127.0.0.1:5003](http://127.0.0.1:5003) and sign up. It's free to use.

To use this as a Docker container:
   - Ensure Docker and Docker Compose are installed on your system.
   - Run the following command to start the application:
     ```bash
     docker-compose up --build
     ```
   - Open your browser and navigate to [http://127.0.0.1:5003](http://127.0.0.1:5003).

### Optional Gmail Helper Service

- The Gmail job scraper is isolated under `email-agent-tests/` and does not need to be imported into `main.py`.
- Its Python packages live in `email-agent-tests/requirements.txt`, separate from the main app dependencies.
- The helper runs as its own optional Docker Compose service named `gmail_job_helper`.
- Because it is behind the `helper` profile, its image and dependencies are only used when you explicitly start that profile.

Run only the main app:

```bash
docker compose up -d
```

Run the main app plus the Gmail helper:

```bash
docker compose --profile helper up -d --build
```

Notes:

- The helper schedule is controlled by `JOB_SCRAPER_CRON` in `docker-compose.yml`.
- Set `GMAIL_EMAIL` and `passwd` in the root `.env` file for Gmail IMAP access with an app password.
- Keep test tooling such as `pytest` in a future separate dev dependency file like `requirements-dev.txt`, not in runtime requirements.

