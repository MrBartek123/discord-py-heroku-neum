import os
from discord.ext import commands
import time
import discord
import requests
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord.utils import get

version = "1.0.32"
bot = commands.Bot(command_prefix="n!")
TOKEN = os.getenv("DISCORD_TOKEN")
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name=f"n!help | n!help links"))

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
@bot.command()
async def help(ctx, page=None):
  if page == None:
    embed = discord.Embed(title="Help", description=":globe_with_meridians: - **Main Commands** `n!help main`\n:sunglasses: - **4Fun Commands** `n!help fun`\n:white_sun_cloud: - **Weather Commands** `n!help weather`\n:hammer: - **Neum Links** `n!help links`\n:construction_worker: - Mods Command `n!help mods`\n:video_game: - Roblox Commands `n!help roblox`")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "roblox":
    embed = discord.Embed(title="Roblox Commands - Help", description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!rbicon <placeId>` - Get Roblox Place Icon\n`n!rbinfo <placeId>` - Get Roblox Place Info")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "main":
    embed = discord.Embed(title="Main Commands - Help", description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!help` - Shows all commands\n`n!ping` - Get Neum Latency\n`n!changes` - Show Neum Update Log\n`n!nickname [member] <nickname>` - Set new nickname to member")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "links":
    embed = discord.Embed(title="Neum Links", description="[Invite Neum](https://discord.com/api/oauth2/authorize?client_id=878259796145479741&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize&scope=bot%20applications.commands)\n")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "weather":
    embed = discord.Embed(title="Weatcher Commands - Help", description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!weather <city>` - Shows city current weather | **WARNING:** You can't use a city (for example) called 'Chodzież' insted this just use 'Chodziez'")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "fun":
    embed = discord.Embed(title="4Fun Commands - Help", description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!help` - Shows all commands\n`n!ping` - Get Neum Latency")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
  elif page == "mod":
    embed = discord.Embed(title="Mods Commands - Help", description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!ban <member> <reason>` - Bans member from this server\n`n!kick <member> <reason>` - Kick member from this server\n`n!unban <member>` - Unbans member from this server\n`n!mute <member>` - Mute member\n`n!unmute <member>`")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)
@bot.command()
async def weather(ctx, *, city=None):
  if city == None:
    await ctx.send("Please enter city name")
  else:
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
        idd = x["id"]
        sys = x["sys"]
        wind = x["wind"]
        wind_speed = wind["speed"]
        flag = sys["country"]
        flagFormat = flag.lower()
        flagEmoji = f":flag_{flagFormat}:"
        fullUrl = f"https://openweathermap.org/city/{idd}"
        current_temperature = y["temp"]
        current_temperature_celsiuis = str(round(current_temperature - 273.15))
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        embed = discord.Embed(title=f"Weather in {city_name} {flagEmoji}",
                          color=ctx.guild.me.top_role.color,
                          timestamp=ctx.message.created_at)
        embed.add_field(name="Weather Name", value=f"{z[0]['main']}", inline=False)
        embed.add_field(name="Descripition", value=f"{weather_description}", inline=False)
        embed.add_field(name="Temperature(C)", value=f"{current_temperature_celsiuis}°C", inline=False)
        embed.add_field(name="Humidity(%)", value=f"{current_humidity}%", inline=False)
        embed.add_field(name="Atmospheric Pressure(hPa)", value=f"{current_pressure}hPa", inline=False)
        embed.add_field(name="Wind Speed", value=f"{wind_speed}m/s")
        embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
        embed.set_footer(text=f"Requested by {ctx.author.name} | Powered by OpenWeather")

        buttons = [
          create_button(
              style=ButtonStyle.URL,
              label="View Weather on web",
              url=fullUrl
          ),
        ]
        action_row = create_actionrow(*buttons)
        await channel.send(embed=embed, components=[action_row])
    else:
        await channel.send("City not found.")
@bot.command()
async def changes(ctx):
  embed = discord.Embed(title="Neum Update Log", description=f"**Version: {version}**\n\n- Added `n!embed` command")
  embed.set_footer(text="Neum - Neum Team | 2021")
  await ctx.send(embed=embed)
@bot.command()
async def embedee(ctx, title: str, description: str, channel: str):
  channel = discord.utils.get(ctx.guild.channels, name=channel)
  channel_id = channel.id
  embed = discord.Embed(title=title, description=description)
  await channel_id.send(embed=embed)
@bot.command()
async def rbicon(ctx, placeId):
  universe_url = f"https://api.roblox.com/universes/get-universe-containing-place?placeid={placeId}"
  complete_url = f"https://thumbnails.roblox.com/v1/places/gameicons?placeIds={placeId}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false"
  response = requests.get(complete_url)
  universeRes = requests.get(universe_url)
  u = universeRes.json()
  x = response.json()

  uData = u["UniverseId"]

  placeURL = f"https://games.roblox.com/v1/games?universeIds={uData}"
  placeRes = requests.get(placeURL)
  placeData = placeRes.json()

  pData = placeData["data"]
  pName = pData[0]["name"]

  iconD = x["data"]
  icon = iconD[0]["imageUrl"]

  embed = discord.Embed(title=f"Roblox Game Icon for {pName}")
  embed.set_thumbnail(url=icon)
  await ctx.send(embed=embed)
@bot.command()
async def rbinfo(ctx, placeId):
  universe_url = f"https://api.roblox.com/universes/get-universe-containing-place?placeid={placeId}"
  complete_url = f"https://thumbnails.roblox.com/v1/places/gameicons?placeIds={placeId}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false"
  response = requests.get(complete_url)
  universeRes = requests.get(universe_url)
  u = universeRes.json()
  x = response.json()

  uData = u["UniverseId"]

  placeURL = f"https://games.roblox.com/v1/games?universeIds={uData}"
  placeRes = requests.get(placeURL)
  placeData = placeRes.json()

  pData = placeData["data"]
  pName = pData[0]["name"]
  pDesc = pData[0]["description"]
  pVisits = pData[0]["visits"]

  iconD = x["data"]
  icon = iconD[0]["imageUrl"]

  embed = discord.Embed(title=f"{pName} Informations")
  embed.add_field(name="Title", value=f"{pName}")
  embed.add_field(name="Description", value=f"{pDesc}")
  embed.add_field(name="Visits", value=f"{pVisits}")
  embed.set_thumbnail(url=icon)
  await ctx.send(embed=embed)
@bot.command()
async def nickname(ctx, member: discord.Member, nick=None):
    await member.edit(nick=nick)
    await ctx.send(f'<a:yes:878700406048432238> | Nickname was changed for {member.mention}')

@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(self, ctx, member: discord.Member, *, reason=None):
  if reason == None:
    reason = "no reason ¯\_(ツ)_/¯"
    await member.kick(reason=reason)
    await ctx.send(f'<a:yes:878700406048432238> | User {member} has been kick for {reason}')
  else:
    await member.kick(reason=reason)
    await ctx.send(f'<a:yes:878700406048432238> | User {member} has been kick! Reason: {reason}')

@commands.command()
@commands.has_permissions(administrator=True)
async def unban(self, ctx, *, member):

  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")

  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'<a:yes:878700406048432238> | Unbanned {user.mention}')
      return

@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(self, ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'<a:yes:878700406048432238> | User {member} has been kick')
@commands.command()
@commands.has_permissions(manage_roles=True)
async def muteRole(ctx):
  if get(ctx.guild.roles, name="Muted"):
    await ctx.send("<a:no:878699746984878111>| Role 'Muted' already exists")
  else:

    await ctx.guild.create_role(name="Muted", colour=discord.Colour(0x0062ff))
    await ctx.send("<a:yes:878700406048432238> | Created role 'Muted'!")
    permissions = discord.Permissions(send_messages=False, read_messages=True)
    permissions.update(kick_members = False)
    for role in ctx.guild.roles:
      if role.name == "Muted":
        await role.edit(reason = None, colour = discord.Colour.blue(), permissions=permissions)
@commands.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member):
  if get(ctx.guild.roles, name="Muted"):
    await ctx.send("<a:no:878699746984878111>| Role 'Muted' not found, please run `n!muteRole` to create Muted Role")
  else:
    role = get(lambda role: role.name == "Muted", ctx.guild.roles)
    await member.add_roles(role)
    await ctx.send(f"<a:yes:878700406048432238> | Muted {member.mention}!")
@commands.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member):
  if get(ctx.guild.roles, name="Muted"):
    await ctx.send("<a:no:878699746984878111>| Role 'Muted' not found, please run `n!muteRole` to create Muted Role")
  else:
    role = get(lambda role: role.name == "Muted", ctx.guild.roles)
    await member.remove_roles(role)
    await ctx.send(f"<a:yes:878700406048432238> | Unmuted {member.mention}!")

if __name__ == "__main__":
    bot.run(TOKEN)