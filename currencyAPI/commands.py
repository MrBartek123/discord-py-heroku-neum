import random

import requests
import os
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord.utils import get
import psycopg2
import pickledb


## SETUP
db = pickledb.load('database.db', False)

def work(username):
    moneyWithout = random.randint(1, 255)
    moneyWithBonus = moneyWithout + db.get(f'{username.name}Bonus')
    db.set(f'{username.name}Points', moneyWithBonus)
    return moneyWithBonus

def balance(member):
    return f"{member.mention} balance is {db.get(f'{member.name}Points')} Coins"
def bonusBalance(member):
    return f"{member.mention}, your coins bonus is {db.get(f'{member.name}Bonus')}"
def addMoney(member, value):
    return f"Added to {member.name} {value} Coins"