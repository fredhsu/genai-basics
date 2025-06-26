from google import genai
from google.genai.types import HttpOptions

model = "gemini-2.0-flash-001"
client = genai.Client(http_options=HttpOptions(api_version="v1"))
query = "What RFC defines the BGP protocol?"
response = client.models.generate_content(
    model=model,
    contents=query,
)
print(f"\n🔍 Query: {query}")
print("-" * 30)

print(f"🤖 Answer: {response.text}")
query = "What accessory kits does the DCS-7280CR3K-32D4 come with?"
response = client.models.generate_content(
    model=model,
    contents=query,
)

print(f"\n🔍 Query: {query}")
print("-" * 30)

print(f"🤖 Answer: {response.text}")
