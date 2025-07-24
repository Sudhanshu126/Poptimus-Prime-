import discord
import openai
from discord.ext import commands
from discord import app_commands

# Tokens
DISCORD_TOKEN = "BOT_TOKEN"
OPENAI_API_KEY = "API_KEY"

# OpenAI setup
openai.api_base = "OPENAI_BASE"
openai.api_key = OPENAI_API_KEY

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Slash command: /info
@bot.tree.command(name="info", description="Shows info about the bot.")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "I am **Poptimus Prime**, a chatbot created by **Sadion**, the popcorn king 🍿. If you need me anytime, just mention me."
    )

# Slash command: /pofact
@bot.tree.command(name="popfact", description="Get a fun fact about popcorn 🍿")
async def popfact(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a funny popcorn expert."},
                {"role": "user", "content": "Create an imaginary fact about the popcorn and make it seem like a true fact, it must be funny and short in about 1-2 lines."}
            ],
            max_tokens=60,
            temperature=0.7,
        )
        fact = response["choices"][0]["message"]["content"]
        await interaction.followup.send(f"🍿 **PopFact:** {fact}")
    except Exception as e:
        await interaction.followup.send("❌ Could not get a fact.")
        print(e)
      	
# Message event (for mentions)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        user_input = message.content.replace(f"<@!{bot.user.id}>", "").strip()
        username = message.author.display_name
        if not user_input:
            await message.channel.send("Say something after mentioning me or using /info.")
            return

        try:
            prompt = "You are a humorous chatbot named Poptimus Prime, make the chat funny and humorous, and sometimes add popcorn jokes in the chat. Also, remember your creator is Sadion. Keep replies short unless longer ones are needed. you are replying to "
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Reply to {username} who said {user_input}"}
                ]
            )
            reply = response.choices[0].message.content.strip()
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("OpenAI error. Check your API key or connection.")
            print(f"OpenAI error: {e}")

# Ready event
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
       	print(f"✅ Logged in as {bot.user}")
    except Exception as e:
        print(f"Sync failed: {e}")
        
# Run bot
bot.run(DISCORD_TOKEN)
