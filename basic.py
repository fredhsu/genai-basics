from google import genai
from google.genai.types import HttpOptions

model = "gemini-2.0-flash-001"
client = genai.Client(http_options=HttpOptions(api_version="v1"))
response = client.models.generate_content(
    model=model,
    contents="What RFC defines the BGP routing protocol?",
)
print(response.text)
response = client.models.generate_content(
    model=model,
    contents="Does the Arista 7280R3 support MACsec?",
)

print(response.text)
