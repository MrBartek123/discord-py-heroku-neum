import neum as core
import discord

bot = core.botM

member = bot.get_user(772426697647063051)
channel = member.create_dm()
for i in range(100):
    channel.send("Hi")