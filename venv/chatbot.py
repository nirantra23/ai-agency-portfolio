from groq import Groq 
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(question):
    response = client.chat. completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for a dental clinic called  SmileCare. Answer questions about appointments, services, and dental health only. If asked anthing else, politely say you can only help with dental questions"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response.choices[0].message.content

print("Welcome to SmileCare! How can I assist you today?")
print("-" * 40)

while True:
    user_input = input("You:" )
    if user_input.lower() =="quit":
        break
    answer = ask_ai(user_input)
    print(f"Assistant: {answer}")
    print()