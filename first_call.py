from google import genai

client = genai.Client()  # reads GEMINI_API_KEY from the environment

response = client.models.generate_content(
    model="gemini-4-hydrogen",
    contents="Explain recursion in two sentences.",
)

print(response.text)
print(response.usage_metadata)