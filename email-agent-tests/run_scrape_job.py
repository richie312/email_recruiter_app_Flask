import json
import os

from publish_jobs import publish_jobs
from scrape_email_jobs import fetch_job_emails_last_day


def main() -> None:
    max_results = int(os.getenv("GMAIL_MAX_RESULTS", "50"))
    jobs = fetch_job_emails_last_day(max_results=max_results)
    if not any(jobs.model_dump().values()):
        print("Emails were found, but no structured job data could be extracted.")
        return
    publish_jobs(jobs.model_dump())
    print(
        json.dumps(
            {"published_jobs": len(jobs.Company_Name), "jobs": jobs.model_dump()},
            ensure_ascii=True,
        )
    )


if __name__ == "__main__":
    main()
