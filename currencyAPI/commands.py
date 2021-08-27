import random

import requests
import os
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord.utils import get
import psycopg2
import pickledb


# SETUP
db = pickledb.load('database.db', False)


def work(username, serverId):
    money_without = random.randint(1, 255) + db.get(f'{username.id}{}Points')
    money_with_bonus = money_without + db.get(f'{username.id}Bonus')
    db.set(f'{username.id}Points', money_with_bonus)
    return money_with_bonus


def balance(member, serverId):
    return f"{member.mention} balance is {db.get(f'{member.id}Points')} Coins"


def bonusBalance(member, serverId):
    return f"{member.mention}, your coins bonus is {db.get(f'{member.id}Bonus')}"


def addMoney(member, value, serverId):
    db.set(f"{member.id}Points", db.get(f'{member.id}Points') + value)
    return f"Added to {member.name} balance {value} Coins"
