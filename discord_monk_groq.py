# Vibe coded by Sandheep Gopalakrishnan based on 
# Code provided by Ali Tobah based on code by https://github.com/tobah59x/AAOT-Mod3-Demo/blob/main/discord-groq.py
# Dr. Abel Sanchez at https://github.com/abelsan/bot

# Monk Persona Discord Bot
# Based on Professor bot by Ali Tobah / Dr. Abel Sanchez
from dotenv import load_dotenv
from groq import Groq
import discord
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DISCORD_TOKEN = os.getenv("TOKEN_MONK")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Track question counts per user
user_question_counts = {}

def call_groq(question):
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": (
                    f"You are a wise and peaceful monk. Respond with calm wisdom, "
                    f"mindfulness, and spiritual insight, drawing from philosophy, "
                    f"Buddhism, and contemplative traditions. Keep answers concise "
                    f"and reflective. Question: {question}"
                )
            }
        ]
    )
    response = completion.choices[0].message.content
    print(response)

    if len(response) > 2000:
        response = response[:1997] + "..."
    return response

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Monk has entered the temple as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id

    # Greeting — resets the user's question count
    if message.content.startswith("$hello"):
        user_question_counts[user_id] = 0
        await message.channel.send(
            "🙏 Greetings, Seeker of Wisdom. "
            "The Monk shall answer **3 questions** and 3 questions only. Ask wisely."
        )

    # Question handler
    elif message.content.startswith("$question"):
        count = user_question_counts.get(user_id, 0)

        if count >= 3:
            await message.channel.send("🧘 The Monk is back to meditating.")
            return

        question = message.content.split("$question", 1)[1].strip()
        if not question:
            await message.channel.send("🙏 Please provide a question after `$question`.")
            return

        print(f"Seeker {message.author}: {question}")
        response = call_groq(question)
        print("---")

        user_question_counts[user_id] = count + 1
        remaining = 3 - user_question_counts[user_id]

        if remaining > 0:
            footer = f"\n\n*({remaining} question{'s' if remaining > 1 else ''} remaining)*"
        else:
            footer = "\n\n*🧘 The Monk now returns to silence...*"

        # Trim response if footer pushes it over 2000 chars
        if len(response) + len(footer) > 2000:
            response = response[:2000 - len(footer) - 3] + "..."

        await message.channel.send(response + footer)

client.run(DISCORD_TOKEN)
