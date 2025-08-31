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