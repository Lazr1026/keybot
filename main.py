print('Loading...')
import os
import asyncio
import discord
import subprocess
from discord.ext import commands

# Discord intents
intents = discord.Intents.default()
intents.message_content = True

# Setup stuff
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix=("."), intents=intents)
client.help_command = commands.DefaultHelpCommand(dm_help=True)

# Load the tokenfile
home_path = os.path.dirname(os.path.realpath(__file__))
with open(home_path + "/token") as tokenfile:
    token = tokenfile.read()

# Ready message
@client.event
async def on_ready():
    print('Ready.')
    print(f'We have logged in as {client.user}')

# Load a module
@client.command()
@commands.has_any_role(924852557262770217, 918316103975977041)
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded {extension}')

# Unload a module
@client.command()
@commands.has_any_role(924852557262770217, 918316103975977041)
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')    
    await ctx.send(f'Unloaded {extension}')

# Update the bot
@client.command()
@commands.has_any_role(924852557262770217, 918316103975977041)
async def update(ctx):
    await ctx.send("Updating code. The bot will be down for roughly 5 seconds.")
    subprocess.run(['bash' + home_path + 'keybot/update.sh'])

# Load all modules in the cogs folder
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
        
# Main function
async def main():
    async with client:
        await load_extensions()
        await client.start(token)

asyncio.run(main())
