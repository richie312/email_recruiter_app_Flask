import os
import json
import requests
from typing import List
from openai import OpenAI
from pydantic import BaseModel
from src.src_context import root_dir
from dotenv import load_dotenv
from data.sample_remote_job_agent_data import sample_Agent_remote_job
load_dotenv(os.path.join(root_dir, ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------------------------------------------
# Step 1: Define the response format in a Pydantic model
# --------------------------------------------------------------


class JobSearchEvent(BaseModel):
    Company_Name: List[str]
    Location: List[str]
    Email_Address: List[str]
    Description: List[str]

# --------------------------------------------------------------
# Step 2: Call the model
# --------------------------------------------------------------

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
            years of experience. Also Job location must be from India. Remote jobs is also fine.,"""
        },
    ],
    response_format=JobSearchEvent,
)

# --------------------------------------------------------------
# Step 3: Parse the response
# --------------------------------------------------------------

event = completion.choices[0].message.content

 
# --------------------------------------------------------------
# Step 4: produce the data to a kafka topic.
# --------------------------------------------------------------

response = requests.post("http://192.168.1.4:5003/produce", 
                        json = {"topic": "test-topic",
                                "value": event})
if response.status_code == 200:
    print("Data produced to Kafka topic successfully.")
else:
    print(f"Failed to produce data to Kafka topic: {response.status_code}, {response.text}")
