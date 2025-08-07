import os
from openai import OpenAI
from pydantic import BaseModel
from src.src_context import root_dir
from dotenv import load_dotenv
import os
os.environ["CURL_CA_BUNDLE"] = ""
load_dotenv(os.path.join(root_dir, ".env"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {
            "role": "user",
            "content": "Search remote jobs from naukri.com or linkedin given my stack saved in our past conversations",
        },
    ],
)

response = completion.choices[0].message.content
print(response)
