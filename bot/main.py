import os
from discord.ext import commands
import time
import discord

bot = commands.Bot(command_prefix="n!")
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    discord.Activity(name="Neum Bugs", type=5)

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")

if __name__ == "__main__":
    bot.run(TOKEN)
