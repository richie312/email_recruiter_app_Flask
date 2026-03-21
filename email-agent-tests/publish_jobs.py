import datetime
import json
import os
import re
from email.utils import parseaddr
from typing import Any, List

import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

load_dotenv(os.path.join(ROOT_DIR, ".env"))


class JobSearchEvent(BaseModel):
    Company_Name: List[str]
    Location: List[str]
    Email_Address: List[str]
    Description: List[str]


class JobParse:
    EMAIL_REGEX = re.compile(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})")

    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_JOB_MODEL", "gpt-4o")

    def build_extraction_prompt(self, email_message: dict[str, Any]) -> str:
        sender = email_message.get("from", "")
        subject = email_message.get("subject", "")
        date_value = email_message.get("date", "")
        snippet = email_message.get("snippet", "")
        body = email_message.get("body_preview", "")

        return f"""
Extract job information from this email and format it into the required schema.

Rules:
- Use only the information present in the email fields below.
- Only extract Location and Description.
- Do not infer Company_Name from the job body.
- Do not infer Email_Address from the job body unless it is clearly present.
- If a value is missing, return an empty string in the corresponding list position.
- If the email does not describe a real job opportunity, return all fields as empty lists.
- Description should be a concise summary of the opportunity from the email.
- Return exactly one job entry when the email is about one job.

Email fields:
Sender: {sender}
Subject: {subject}
Date: {date_value}
Snippet: {snippet}
Body: {body}
""".strip()

    def extract_sender_email(self, sender: str) -> str:
        parsed_email = parseaddr(sender)[1].strip().lower()
        if parsed_email:
            return parsed_email

        match = self.EMAIL_REGEX.search(sender)
        return match.group(1).lower() if match else ""

    def extract_sender_domain(self, sender: str) -> str:
        email_address = self.extract_sender_email(sender)
        if not email_address or "@" not in email_address:
            return ""
        return email_address.split("@", 1)[1]

    def extract_job_details(self, email_message: dict[str, Any]) -> dict[str, list[str]]:
        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract only location and full description from recruiter emails. "
                        "Return only fields that can be supported by the provided email content."
                    ),
                },
                {"role": "user", "content": self.build_extraction_prompt(email_message)},
            ],
            response_format=JobSearchEvent,
        )

        parsed = completion.choices[0].message.parsed
        return parsed.model_dump()

    def transform_emails_to_jobs(self, email_messages: list[dict[str, Any]]) -> JobSearchEvent:
        structured_jobs = JobSearchEvent(
            Company_Name=[],
            Location=[],
            Email_Address=[],
            Description=[],
        )

        for email_message in email_messages:
            sender = email_message.get("from", "")
            sender_domain = self.extract_sender_domain(sender)
            sender_email = self.extract_sender_email(sender)
            structured_job = self.extract_job_details(email_message)

            if not (sender_domain or sender_email or any(structured_job.values())):
                continue

            structured_jobs.Company_Name.append(sender_domain)
            location_values = structured_job.get("Location", [])
            description_values = structured_job.get("Description", [])
            structured_jobs.Location.append(location_values[0] if location_values else "")
            structured_jobs.Email_Address.append(sender_email or sender_domain)
            structured_jobs.Description.append(description_values[0] if description_values else "")

        return structured_jobs


def publish_jobs(jobs: dict[str, Any]) -> None:
    endpoint = os.getenv("KAFKA_REST_PROXY_URL")
    topic = os.getenv("KAFKA_TOPIC", "gmail-job-events")
    timeout = int(os.getenv("KAFKA_REQUEST_TIMEOUT", "30"))

    if not endpoint:
        raise ValueError("KAFKA_REST_PROXY_URL is not configured.")
    
    application_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    jobs["Application_Date"] = application_date

    response = requests.post(
        endpoint,
        json={"topic": topic, "value": json.dumps(jobs)},
        timeout=timeout,
    )
    if response.status_code == 200:
        print("Data produced to Kafka topic successfully.")
    else:
        print(f"Failed to produce data to Kafka topic: {response.status_code}, {response.text}")
