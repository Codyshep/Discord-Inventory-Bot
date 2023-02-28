import discord
from discord.ext import commands
import sqlite3
from Config import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Connect to the database and create the table if it doesn't exist
conn = sqlite3.connect("backpacks.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS backpacks (
             user_id INTEGER PRIMARY KEY,
             items TEXT
             )""")
conn.commit()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(name="showBackpack")
async def show_backpack(ctx):
    # Retrieve the user's backpack from the database
    user_id = ctx.author.id
    c.execute("SELECT items FROM backpacks WHERE user_id=?", (user_id,))
    result = c.fetchone()

    if result:
        backpack = result[0].split(", ")
        # Create an embed and add the backpack information to it
        embed = discord.Embed(title="Your backpack", description="\n".join(backpack))
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have a backpack.")

@bot.command(name="clearBackpack")
async def clear_backpack(ctx):
    # Delete the user's backpack from the database
    user_id = ctx.author.id
    c.execute("DELETE FROM backpacks WHERE user_id=?", (user_id,))
    conn.commit()
    await ctx.send("Backpack cleared!")

@bot.command(name="addItem")
@commands.has_role(AdminRole)
async def add_item(ctx, user_id: int, item):
    # Retrieve the user's backpack from the database
    c.execute("SELECT items FROM backpacks WHERE user_id=?", (user_id,))
    result = c.fetchone()

    if result:
        backpack = result[0].split(", ")
    else:
        backpack = []

    # Add the item to the backpack and update the database
    backpack.append(item)
    backpack_str = ", ".join(backpack)
    c.execute("REPLACE INTO backpacks (user_id, items) VALUES (?, ?)", (user_id, backpack_str))
    conn.commit()
    await ctx.send(f"Added {item} to {user_id}'s backpack.")



bot.run(Token)