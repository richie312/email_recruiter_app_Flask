import email
import html
import imaplib
import json
import os
import re
from datetime import datetime, timedelta
from email.header import decode_header
from email.message import Message
from typing import Any
from dotenv import load_dotenv
from publish_jobs import JobParse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

load_dotenv(os.path.join(ROOT_DIR, ".env"))

IMAP_HOST = os.getenv("GMAIL_IMAP_HOST", "imap.gmail.com")
IMAP_PORT = int(os.getenv("GMAIL_IMAP_PORT", "993"))

# Adjust these keywords to match the kinds of job mails you care about.
JOB_KEYWORDS = [
    "job",
    "jobs",
    "career",
    "careers",
    "hiring",
    "opportunity",
    "recruiter",
    "position",
    "opening",
    "application",
    "naukri",
    "indeed",
    "linkedin",
    "naukri.com",
    "indeed.com",
    "linkedin.com",
    "python",
    "software",
    "engineer",
    "developer"
]


def decode_mime_value(value: str) -> str:
    if not value:
        return ""

    decoded_parts = decode_header(value)
    decoded_text = []

    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_text.append(part.decode(encoding or "utf-8", errors="ignore"))
        else:
            decoded_text.append(part)

    return "".join(decoded_text)


def decode_part_payload(part: Message) -> str:
    payload = part.get_payload(decode=True)
    if not payload:
        return ""

    charset = part.get_content_charset() or "utf-8"
    return payload.decode(charset, errors="ignore")


def html_to_text(html_content: str) -> str:
    without_scripts = re.sub(r"(?is)<(script|style).*?>.*?</\\1>", " ", html_content)
    without_tags = re.sub(r"(?s)<[^>]+>", " ", without_scripts)
    return html.unescape(without_tags)


def extract_message_body(message: Message) -> str:
    plain_parts: list[str] = []
    html_parts: list[str] = []

    for part in message.walk():
        if part.is_multipart():
            continue

        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition", "")).lower()

        if "attachment" in content_disposition:
            continue

        if content_type == "text/plain":
            text = decode_part_payload(part)
            if text:
                plain_parts.append(text)
        elif content_type == "text/html":
            text = decode_part_payload(part)
            if text:
                html_parts.append(html_to_text(text))

    if plain_parts:
        return "\n".join(plain_parts)

    if html_parts:
        return "\n".join(html_parts)

    if not message.is_multipart():
        content_type = message.get_content_type()
        if content_type == "text/plain":
            return decode_part_payload(message)
        if content_type == "text/html":
            return html_to_text(decode_part_payload(message))

    return ""


def looks_like_job_mail(subject: str, sender: str, body: str) -> bool:
    haystack = f"{subject}\n{sender}\n{body}".lower()
    return any(keyword in haystack for keyword in JOB_KEYWORDS)


def cleanup_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def get_imap_client(email_id: str, password: str) -> imaplib.IMAP4_SSL:
    client = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    client.login(email_id, password)
    return client


def build_since_date() -> str:
    since_date = datetime.utcnow() - timedelta(days=1)
    return since_date.strftime("%d-%b-%Y")


def fetch_job_emails_last_day(max_results: int = 25) -> Any:
    email_id = os.getenv("GMAIL_EMAIL") or os.getenv("EMAIL_ID") or os.getenv("EMAIL_ADDRESS")
    password = os.getenv("passwd")

    if not email_id:
        raise ValueError("Set GMAIL_EMAIL, EMAIL_ID, or EMAIL_ADDRESS in the root .env file.")
    if not password:
        raise ValueError("Set 'passwd' in the root .env file.")

    client = get_imap_client(email_id, password)
    email_messages: list[dict[str, Any]] = []

    try:
        client.select("INBOX")
        status, data = client.search(None, f'(SINCE "{build_since_date()}")')
        if status != "OK":
            raise RuntimeError("Failed to search Gmail inbox over IMAP.")

        message_ids = data[0].split()
        for message_id in reversed(message_ids):
            if len(email_messages) >= max_results:
                break

            fetch_status, message_data = client.fetch(message_id, "(RFC822)")
            if fetch_status != "OK" or not message_data or not message_data[0]:
                continue

            raw_email = message_data[0][1]
            message = email.message_from_bytes(raw_email)

            subject = decode_mime_value(message.get("Subject", ""))
            sender = decode_mime_value(message.get("From", ""))
            date_value = decode_mime_value(message.get("Date", ""))
            body = extract_message_body(message)

            if not looks_like_job_mail(subject, sender, body):
                continue

            email_messages.append(
                {
                    "id": message_id.decode("utf-8", errors="ignore"),
                    "thread_id": "",
                    "subject": subject,
                    "from": sender,
                    "date": date_value,
                    "snippet": cleanup_text(body)[:200],
                    "body_preview": cleanup_text(body),
                }
            )
    finally:
        try:
            client.close()
        except imaplib.IMAP4.error:
            pass
        client.logout()
    return JobParse().transform_emails_to_jobs(email_messages)




if __name__ == "__main__":
    max_results = int(os.getenv("GMAIL_MAX_RESULTS", "200"))
    jobs = fetch_job_emails_last_day(max_results=max_results)
    print(json.dumps(jobs.model_dump(), indent=2, ensure_ascii=True))
