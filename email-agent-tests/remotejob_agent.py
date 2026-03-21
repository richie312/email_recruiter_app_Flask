import os
import json
from typing import List
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from publish_jobs import publish_jobs


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
load_dotenv(os.path.join(PARENT_DIR, ".env"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class JobSearchEvent(BaseModel):
    Company_Name: List[str]
    Location: List[str]
    Email_Address: List[str]
    Description: List[str]


completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": """Act as a career advisor. Your tech stack includes [python, kubernetes,  
            docker, data engineering, spark, kafka, Flask, Django, Fast API, redis, 
            git, AWS, Azure, Databaricks]. Suggest relevant job that align with 
            this skillset. Recommend specific job  focusing on these technologies along with 12 
            years of experience. Also Job location must be from India. Remote jobs is also fine.,""",
        },
    ],
    response_format=JobSearchEvent,
)


event = completion.choices[0].message.content

payloads = json.loads(event)
for index_ in range(len(payloads["Company_Name"])):
    pub_payload = {
        "Company_Name": payloads["Company_Name"][index_],
        "Location": payloads["Location"][index_],
        "Email_Address": payloads["Email_Address"][index_],
        "Description": payloads["Description"][index_],
    }
    publish_jobs(pub_payload)