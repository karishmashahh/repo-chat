# genai is Google's library for talking to Gemini
from google import genai

# types holds the building blocks for messages and settings
from google.genai import types

# ---------- Setup ----------

# Create the client that sends requests to Gemini.
# It reads your key from the GEMINI_API_KEY environment variable,
# so the key never appears in this file.
client = genai.Client()

# The model to use. Copy a current name from the docs; names change often.
MODEL = "gemini-4-hydrogen"

# The system prompt: instructions that shape every reply.
SYSTEM = "You are a helpful coding assistant. If you don't know, say so."

# ---------- Conversation memory ----------

# The model has no memory of its own. It only sees what we send each time.
# So we keep the whole conversation in this list and resend it every turn.
# Unlike some other APIs, the system prompt is NOT stored in this list.
history = []

print("Chatbot ready. Type 'quit' to exit.")

# ---------- Main loop ----------

# Repeat until the user types quit
while True:
    # Read what the user types
    user_input = input("You: ")

    # .strip() removes extra spaces, .lower() ignores capital letters,
    # so "Quit", " quit " and "QUIT" all work
    if user_input.strip().lower() == "quit":
        break  # leave the loop and end the program

    # Add the user's message to the history.
    # In Gemini, each message is a "Content" with a role and a list of parts.
    # Role "user" means it came from you.
    history.append(
        types.Content(role="user", parts=[types.Part(text=user_input)])
    )

    # Send the ENTIRE history to the model and wait for its reply.
    # This is why follow-up questions work: the model sees earlier messages.
    response = client.models.generate_content(
        model=MODEL,
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,   # the system prompt goes here
            max_output_tokens=500,       # upper limit on the reply length
        ),
    )

    # response.text is the reply as plain text
    reply = response.text

    # Show the reply to the user
    print("Bot:", reply)

    # Show how many tokens this request used. Watch it grow as the
    # conversation gets longer: that is the context window filling up.
    print("(tokens used:", response.usage_metadata.total_token_count, ")")

    # Add the reply to the history. Gemini calls the assistant's role "model".
    # Without this line, the bot would forget its own answers.
    history.append(
        types.Content(role="model", parts=[types.Part(text=reply)])
    )