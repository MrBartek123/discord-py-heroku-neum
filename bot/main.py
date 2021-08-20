import os
from discord.ext import commands
import time
import discord
import requests

bot = commands.Bot(command_prefix="n!")
TOKEN = os.getenv("DISCORD_BOT_SECRET")
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="n!help | n!help links | Hello",))

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
@bot.command()
async def help(ctx, page=None):
  if page == None:
    embed = discord.Embed(title="Help", description=":globe_with_meridians: - **Main Commands** `n!help main`\n:sunglasses: - **4Fun Commands** `n!help fun`\n:white_sun_cloud: - **Weather Commands** `n!help weather`\n:hammer: - **Neum Links** `n!help links`")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "main":
    embed = discord.Embed(title="Main Commands - Help", description="`n!help` - Shows all commands\n`n!ping` - Get Neum Latency\n`n!changes` - Show Neum Update Log")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "links":
    embed = discord.Embed(title="Neum Links", description="[Invite Neum](https://discord.com/api/oauth2/authorize?client_id=878259796145479741&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize&scope=bot%20applications.commands)\n")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "weather":
    embed = discord.Embed(title="Weatcher Commands - Help", description="`n!weather <city>` - Shows city current weather | **WARNING:** You can't use a city (for example) called 'Chodzież' insted this just use 'Chodziez'")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "fun":
    embed = discord.Embed(title="4Fun Commands - Help", description="`n!help` - Shows all commands\n`n!ping` - Get Neum Latency")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
@bot.command()
async def weather(ctx, *, city: str):
  api_key = "42b32fd5efde7f044522e6cef8672adf"
  base_url = "http://api.openweathermap.org/data/2.5/weather?"
  city_name = city
  complete_url = base_url + "appid=" + api_key + "&q=" + city_name
  response = requests.get(complete_url)
  x = response.json()
  channel = ctx.message.channel
  if x["cod"] != "404":
    async with channel.typing():
      y = x["main"]
      current_temperature = y["temp"]
      current_temperature_celsiuis = str(round(current_temperature - 273.15))
      current_pressure = y["pressure"]
      current_humidity = y["humidity"]
      z = x["weather"]
      weather_description = z[0]["description"]
      weather_title = z[0]["main"]
      embed = discord.Embed(title=f"Weather in {city_name}",
                        color=ctx.guild.me.top_role.color,
                        timestamp=ctx.message.created_at)
      embed.add_field(name="Weather Name", value=f"{z[0]['main']}", inline=False)
      embed.add_field(name="Descripition", value=f"{weather_description}", inline=False)
      embed.add_field(name="Temperature(C)", value=f"{current_temperature_celsiuis}°C", inline=False)
      embed.add_field(name="Humidity(%)", value=f"{current_humidity}%", inline=False)
      embed.add_field(name="Atmospheric Pressure(hPa)", value=f"{current_pressure}hPa", inline=False)
      embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
      embed.set_footer(text=f"Requested by {ctx.author.name} | Powered by OpenWeather")
      await channel.send(embed=embed)
  else:
      await channel.send("City not found.")
  @bot.command()
  async def changes(ctx):
    embed = discord.Embed(title="Neum Update Log", description="**Version: 1.0.13**\n\n- Added `n!changes` command\n- Moved Neum to Heroku 24/7 Hosting")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
if __name__ == "__main__":
    bot.run(TOKEN)