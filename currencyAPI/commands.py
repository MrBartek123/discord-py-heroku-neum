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
    moneyWithout = random.randint(1, 255) + db.get(f'{member.id}Points')
    moneyWithBonus = moneyWithout + db.get(f'{username.id}Bonus')
    db.set(f'{username.id}Points', moneyWithBonus)
    return moneyWithBonus

def balance(member):
    return f"{member.mention} balance is {db.get(f'{member.id}Points')} Coins"
def bonusBalance(member):
    return f"{member.mention}, your coins bonus is {db.get(f'{member.id}Bonus')}"
def addMoney(member, value):
    return f"Added to {member.name} balance {value} Coins"
    db.set(f"{member.id}Points", db.get(f'{member.id}Points') + value)
