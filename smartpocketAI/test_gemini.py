from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API KEY FOUND:", bool(api_key))

if not api_key:
    raise SystemExit("API key was not found.")

try:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Reply with only the word OK."
    )

    print("SUCCESS")
    print(response.text)

except Exception as e:
    print("FAILED")
    print(type(e).__name__)
    print(str(e))