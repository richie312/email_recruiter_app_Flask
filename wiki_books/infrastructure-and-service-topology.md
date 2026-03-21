# Infrastructure And Service Topology

## Main services

Based on the repository and your architecture notes, the platform is composed of multiple cooperating services:

1. noTify Flask web application
2. Kafka producer/consumer microservice
3. MySQL database service
4. Redis cache service
5. optional Gmail helper scraper service

## Service roles

### Flask application

The main app is responsible for:

- authentication
- user profile and settings
- manual recruiter applications
- application history UI
- job dashboard rendering
- resume builder rendering

### Kafka microservice

The Kafka layer is external to the Flask app and acts as the messaging channel for helper-produced jobs.

The main app consumes job data indirectly through:

- `job_api_url`

### MySQL

MySQL stores:

- application history
- user profile state
- uploaded resume/image/profile binaries

### Redis

Per your architecture note, Redis acts as a middle interface between noTify and the Kafka consumer so the same data can be rendered repeatedly without repeatedly hitting the consumer path.

### Helper scraper service

The email helper operates as a separate containerized service with its own dependency set and cron-driven schedule.

## Ingestion routes into job/application state

Your stated architecture mentions two routes into MySQL-backed job/application data:

1. manual form-based entry
2. automated apply from the job list dashboard

The broader ecosystem also adds upstream ingestion through helper scrapers that publish jobs into Kafka before those jobs are exposed through the dashboard.

## Docker topology

`docker-compose.yml` currently models:

- the main `web` service
- the optional `gmail_job_helper` profile-based service

The helper service is activated only when needed, which keeps the main environment lighter.
