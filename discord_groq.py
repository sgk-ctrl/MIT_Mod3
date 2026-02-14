# Written by Ali Tobah based on code by
# Dr. Abel Sanchez at https://github.com/abelsan/bot

from dotenv import load_dotenv
from groq import Groq
import discord
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DISCORD_TOKEN = os.getenv("TOKEN")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)


def call_groq(question):
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Respond like a university professor to the following question: {question}"
            }
        ]
    )

    response = completion.choices[0].message.content
    print(response
              # Truncate response if it exceeds Discord's 2000 character limit
    if len(response) > 2000:
        response = response[:1997] + "..."  # Add ellipsis to indicate truncation)
    return response


# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Good day!")

    if message.content.startswith("$question"):
        message_content = message.content.split("$question", 1)[1].strip()
        print(f"Question: {message_content}")

        response = call_groq(message_content)
        print("---")

        await message.channel.send(response)


client.run(DISCORD_TOKEN)