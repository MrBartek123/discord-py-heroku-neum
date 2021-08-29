import os
import time
import discord
from discord.ext import commands
import requests
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord.utils import get
from discord.ext.commands import has_permissions
from currencyAPI import commands as Money
import humanize
import pickledb
import dislash
import random
from flask import Flask, redirect
from dislash import Option, OptionType, SelectMenu, SelectOption, ActionRow, Button, ButtonStyle
import urllib

app = Flask(__name__)


@app.route('/warn')
def hello():
    return redirect("https://www.youtube.com/watch?v=a3Z7zEc7AXQ", code=302)


db = pickledb.load('database.db', False)

version = "1.0.43"
botM = commands.Bot(command_prefix="n!")
TOKEN = os.getenv("DISCORD_TOKEN")
botM.remove_command("help")
premiumCodes = ["SUMMER2021", "NEUM", "hi"]
userCodes = []
interactionClient = dislash.InteractionClient(botM)


@botM.command()
async def deleteRole(ctx):
    roles = []
    for r in ctx.guild.roles:
        roles.append(SelectOption(r, r))
    await ctx.send(
        "Choose role to delete",
        components=[
            SelectMenu(
                custom_id="test",
                max_values=1,
                placeholder="Choose role to delete",
                options=roles
            )
        ]
    )

    def check(inter):
        if inter.author == ctx.author:
            print("true")

    # Wait for a menu click under the message you've just sent
    inter = await msg.wait_for_dropdown(check)
    # Tell which options you received
    labels = [option.label for option in inter.select_menu.selected_options]
    await inter.reply(f"Deleted role {', '.join(labels)}")
    await botM.delete_role(ctx.guild, option)


@interactionClient.slash_command(
    name="avatar",  # Defaults to the function name
    description="Get member avatar",
    options=[
        Option('user', 'Specify any user or leave blank to get your avatar', OptionType.USER),
    ]
)
async def avatar(inter, user=None):
    if user == None:
        user = inter.author
    embed3 = discord.Embed(color=discord.Color.blurple())
    embed3.set_thumbnail(user.avatar_url)
    await ctx.send(embed=embed3)


@interactionClient.message_command(name='embed')
async def embed(inter):
    embedM = discord.Embed(description=f"{inter.message.content}")
    await inter.respond(embed=embedM)


@botM.event
async def on_ready():
    print(f"Logged in as {botM.user.name}({botM.user.id})")
    await botM.change_presence(activity=discord.Game(name=f"n!help | n!help links"))


@botM.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")


@botM.command()
async def help(ctx, page=None):
    if page == None:
        embed = discord.Embed(title="Help",
                              description=":globe_with_meridians: - **Main Commands** `n!help main`\n:sunglasses: - **4Fun Commands** `n!help fun`\n:white_sun_cloud: - **Weather Commands** `n!help weather`\n:hammer: - **Neum Links** `n!help links`\n:construction_worker: - **Mods Commands** `n!help mods`\n:video_game: - *Roblox Commands** `n!help roblox`\n:sparkles: **Premium Commands** - `n!help premium`")
        embed.set_footer(text="Neum - Neum Team | 2021")
        await ctx.send(embed=embed)
    elif page == "roblox":
        embed = discord.Embed(title="Roblox Commands - Help",
                              description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!rbicon <placeId>` - Get Roblox Place Icon\n`n!rbinfo <placeId>` - Get Roblox Place Info\n`n!rbmarket <productId>` - Get Marketplace Product Info")
        embed.set_footer(text="Neum - Neum Team | 2021")
        await ctx.send(embed=embed)
    elif page == "main":
        embed = discord.Embed(title="Main Commands - Help",
                              description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!help` - Shows all botM\n`n!ping` - Get Neum Latency\n`n!changes` - Show Neum Update Log\n`n!nickname [member] <nickname>` - Set new nickname to member")
        embed.set_footer(text="Neum - Neum Team | 2021")
        await ctx.send(embed=embed)
    elif page == "links":
        embed = discord.Embed(title="Neum Links",
                              description="[Invite Neum](https://discord.com/oauth2/authorize?client_id=878259796145479741&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize&scope=bot%20applications.commands)\n")
        embed.set_footer(text="Neum - Neum Team | 2021")
        await ctx.send(embed=embed)
    elif page == "weather":
        embed = discord.Embed(title="Weatcher Commands - Help",
                              description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!weather <city>` - Shows city current weather | **WARNING:** You can't use a city (for example) called 'Chodzież' insted this just use 'Chodziez'")
        embed.set_footer(text="Neum - Neum Team | 2021")
        await ctx.send(embed=embed)
    elif page == "fun":
        embed = discord.Embed(title="4Fun Commands - Help",
                              description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!kill [member]` - Kill da person :skull:\n`n!spaghetti` - ???\n`n!fakeWarn <member>` - Warn, but fake")
        embed.set_footer(text="Neum - Neum Team | 2021")
        await ctx.send(embed=embed)
    elif page == "mod":
        embed = discord.Embed(title="Mods Commands - Help",
                              description="[arg] = Option Argument | <arg> = Required Argument\n\n`n!ban <member> <reason>` - Bans member from this server\n`n!kick <member> <reason>` - Kick member from this server\n`n!unban <member>` - Unbans member from this server\n`n!mute <member>` - Mute member\n`n!unmute <member>`\n`n!prefix <prefix>` - Set Neum Prefix")
        embed.set_footer(text="Neum - Neum Team | 2021")
        await ctx.send(embed=embed)
    elif page == "premium":
        embed = discord.Embed(title="Premium Commands - Help",
                              description="[arg] = Option Argument | <arg> = Required Argument | Redeem codes to get Neum Premium!\n\n")
        embed.set_footer(text="Neum - Neum Team | 2021")
        await ctx.send(embed=embed)


@botM.command()
async def prefix(ctx, *, prefix):
    db.set(f"{ctx.guild.id}Prefix", f"{prefix}")
    await ctx.send(f"Changed {ctx.guild.name} prefix to {prefix}")
    botM.command_prefix = db.get(f"{ctx.guild.id}Prefix")


@botM.command()
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
                await channel.send(embed=embed)
        else:
            await channel.send("City not found.")


@botM.command()
async def changes(ctx):
    embed = discord.Embed(title="Neum Update Log", description=f"**Version: {version}**\n\n- Added Mods Commands!")
    embed.set_footer(text="Neum - Neum Team | 2021")
    await ctx.send(embed=embed)


@botM.command()
async def embedee(ctx, title: str, description: str, channel: str):
    channel = discord.utils.get(ctx.guild.channels, name=channel)
    channel_id = channel.id
    embed = discord.Embed(title=title, description=description)
    await channel_id.send(embed=embed)


@botM.command()
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


@botM.command()
async def githubRep(ctx):
    await ctx.send(
        "[Neum Github Repo](https://github.com/MrBartek123/discord-py-heroku-neum/blob/master/botM/main.py)")


@botM.command()
@has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason):
    channel = await member.create_dm()
    await channel.send(f"Warning from {ctx.guild.name}:\nModerator: {ctx.author.mention}\nReason: {reason}")
    await ctx.send(f"<a:yes:878700406048432238>| Warned {member}")


@botM.command()
async def rbmarket(ctx, productid):
    urlAs = f"https://api.roblox.com/marketplace/productinfo?assetid={productid}"
    req = requests.get(urlAs)
    data = req.json()

    name = data["Name"]
    desc = data["Description"]
    price = data["PriceInRobux"]
    ItemId = data["AssetId"]

    embed = discord.Embed(title=f"{name}", description=f"{desc}")
    embed.add_field(name="Price", value=f"{price}")
    await ctx.send(embed=embed)


@botM.command()
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
    pPlaying = pData[0]['playing']
    pId = pData[0]["rootPlaceId"]

    iconD = x["data"]
    icon = iconD[0]["imageUrl"]

    embed = discord.Embed(title=f"{pName}", description=f"{pDesc}")
    embed.add_field(name="Visits", value=f"{humanize.intword(pVisits)}")
    embed.add_field(name="Playing", value=f"{humanize.intword(pPlaying)}")
    embed.set_thumbnail(url=icon)
    await ctx.send(embed=embed)


@botM.command()
async def nickname(ctx, member: discord.Member, nick=None):
    await member.edit(nick=nick)
    await ctx.send(f'<a:yes:878700406048432238> | Nickname was changed for {member.mention} to {nick}')


@botM.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = "no reason ¯\_(ツ)_/¯"
        await member.kick(reason=reason)
        embed = discord.Embed(description=f'<a:yes:878700406048432238> | User {member} has been kick for {reason}',
                              color=0x43bb45)
        await ctx.send(embed=embed)
    else:
        await member.kick(reason=reason)
        embed = discord.Embed(description=f'<a:yes:878700406048432238> | User {member} has been kick! Reason: {reason}',
                              color=0x43bb45)
        await ctx.send(embed=embed)


@botM.command()
@has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(description=f'<a:yes:878700406048432238> | Unbanned {user.mention}', color=0x43bb45)
            await ctx.send(embed=embed)
            return


@botM.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(description=f'<a:yes:878700406048432238> | Banned {member.mention}', color=0x43bb45)
    await ctx.send(embed=embed)


@botM.command()
@has_permissions(manage_roles=True)
async def muteRole(ctx):
    if get(ctx.guild.roles, name="Muted"):
        await ctx.send("<a:no:878699746984878111>| Role 'Muted' already exists")
    else:
        await ctx.guild.create_role(name="Muted", colour=discord.Colour(0x0062ff))
        await ctx.send("<a:yes:878700406048432238>| Created role 'Muted'!")
        permissions = discord.Permissions(send_messages=False, read_messages=True)
        permissions.update(kick_members=False)
        for role in ctx.guild.roles:
            if role.name == "Muted":
                await role.edit(reason=None, colour=discord.Colour.blue(), permissions=permissions)


@botM.command()
@has_permissions(manage_roles=True)
async def mute(ctx, member):
    if get(ctx.guild.roles, name="Muted"):
        await ctx.send(
            "<a:no:878699746984878111>| Role 'Muted' not found, please run `n!muteRole` to create Muted Role")
    else:
        role = get(lambda role: role.name == "Muted", ctx.guild.roles)
        await member.add_roles(role)
        await ctx.send(f"<a:yes:878700406048432238> | Muted {member.mention}!")


@botM.command()
@has_permissions(manage_roles=True)
async def unmute(ctx, member):
    if get(ctx.guild.roles, name="Muted"):
        await ctx.send(
            "<a:no:878699746984878111>| Role 'Muted' not found, please run `n!muteRole` to create Muted Role")
    else:
        role = get(lambda role: role.name == "Muted", ctx.guild.roles)
        await member.remove_roles(role)
        await ctx.send(f"<a:yes:878700406048432238> | Unmuted {member.mention}!")


@botM.command()
async def balance(ctx, member=None):
    if member == None:
        member = ctx.author
    await ctx.send(f":coin: | {Money.balance(member, ctx.guild.id)}")


@botM.command()
async def work(ctx):
    member = ctx.author
    await ctx.send(f":coin: | You made {Money.work(member, ctx.guild.id)}")


@botM.command()
async def addMoney(ctx, member=None, *, value):
    if member == None:
        member = ctx.author
    await ctx.send(f":coin: | {Money.addMoney(ctx.author, value, ctx.guild.id)}")


@botM.command()
async def NeumColors(ctx):
    await ctx.send(
        f"Here is a Neum Color List:\n\nA Little Bit Light Grey White - `231, 231, 231`\nNot Totally A Black - `38, 38, 38`")


@botM.command()
async def redeem(ctx, code):
    if code in premiumCodes:
        await ctx.send(f"Redeemed code! Award: **Neum :sparkles: PREMIUM :sparkles: for infinite time!**")
        db.set(f"{ctx.guild.id}Premium", True)
    elif code in userCodes:
        await ctx.send(f"Redeemed code! Award: **Neum :sparkles: PREMIUM :sparkles: for infinite time!**")
        db.set(f"{ctx.guild.id}Premium", True)
        await ctx.send(f"Invalid code")


@botM.command()
async def premiumStatus(ctx):
    statusPremium = db.get(f"{ctx.guild.id}Premium")
    if statusPremium == False:
        await ctx.send("This server don't have Neum Premium")
    else:
        await ctx.send("This server have Neum Premium!")


@botM.command()
async def buyPremium(ctx):
    statusPremium = db.get(f"{ctx.guild.id}Premium")
    if statusPremium == False:
        code = random.randrange(100000, 999999)
        points = db.get(f'{ctx.author.id}{ctx.guild.id}Points')
        bonus = db.get(f'{ctx.author.id}{ctx.guild.id}Bonus')
        if points <= 500 and bonus <= 2:
            await ctx.send(
                f"Please note this code costs 500 Coins and 2 Bonus Points and its only one time use\nCode: {code}")
            db.set(f"{ctx.author.id}{ctx.guild.id}Points", points - 500)
            db.set(f"{ctx.author.id}{ctx.guild.id}Bonus", bonus - 2)
        else:
            await ctx.send(
                f"You don't have enough Coins and Bonus Points, you need {500 - points} Coins and {2 - bonus} Bonus Points more")
    else:
        await ctx.send("This server already have Neum Premium!")


@botM.command()
async def editDB(ctx, key, value):
    if value == "False":
        value = False
    elif value == "True":
        value = True
    db.set(key, value)
    await ctx.send(f"Done! ||`key: {key}, value: {value}`||")


@botM.command()
async def kill(ctx, member="None"):
    if member == "None":
        member = f"{ctx.author.name} :flushed: :knife:"
    embed = discord.Embed(description=f":skull: | Killed {member}")
    await ctx.send(embed=embed)


@botM.command()
async def spaghetti(ctx):
    embed = discord.Embed(description=f":spaghetti: | {ctx.author.mention} get a spaghetti!")
    await ctx.send(embed=embed)


@botM.command()
async def fakeWarn(ctx, member: discord.Member):
    channel = await member.create_dm()
    embed = discord.Embed(
        description=f"Warning from {ctx.guild.name}:\nReason: Breaking rules\nLearn more about [warns](https://www.thisworldthesedays.com/why-i-get-a-warn.html)")
    await channel.send(embed=embed)
    await ctx.send(f"<a:yes:878700406048432238>| ||Fake|| Warned {member}")


@botM.command()
async def runPython(ctx):
    attachment_url = ctx.message.attachments[0].url
    testfile = urllib.URLopener()
    testfile.retrieve(attachment_url, f"executePy{ctx.author.name}.py")
    os.system(f"python executePy{ctx.author.name}.py")

if __name__ == "__main__":
    botM.run(TOKEN)
