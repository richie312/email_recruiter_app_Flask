import os
from openai import OpenAI
from pydantic import BaseModel
from src.src_context import root_dir
from dotenv import load_dotenv

load_dotenv(os.path.join(root_dir, ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------------------------------------------
# Step 1: Define the response format in a Pydantic model
# --------------------------------------------------------------


class JobSearchEvent(BaseModel):
    Company_Name: str
    Location: str
    Email_Address: str

# --------------------------------------------------------------
# Step 2: Call the model
# --------------------------------------------------------------

completion = client.beta.chat.completions.parse(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Search remote jobs from naukri.com or linkedin given my stack saved in our past conversations",
        },
    ],
    response_format=JobSearchEvent,
)

# --------------------------------------------------------------
# Step 3: Parse the response
# --------------------------------------------------------------

event = completion.choices[0].message.parsed
event.Company_Name
event.Location
event.Email_Address
