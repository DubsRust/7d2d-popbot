import discord
import requests
import asyncio
from discord.ext import commands

# Define your bot token
TOKEN = 'Bot_Token_Here'

# Define the BattleMetrics server ID
server_id = 'BM_Server_ID_Here'

# Initialize the bot with an empty string as the command prefix
intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def update_status():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            # Make an API request to BattleMetrics
            api_url = f"https://api.battlemetrics.com/servers/{server_id}"
            response = requests.get(api_url)

            if response.status_code == 200:
                server_data = response.json()
                player_count = server_data["data"]["attributes"]["players"]
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'({player_count}/30)'))
            else:
                print(f"Failed to fetch server data. Status code: {response.status_code}")
        except Exception as e:
            print('An error occurred while updating status:', e)
        await asyncio.sleep(60)  # Update status every 60 seconds

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(update_status())

# Run the bot
bot.run(TOKEN)