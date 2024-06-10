import selfcord
from selfcord.ext import commands
import os
import requests
import concurrent.futures
import json
import asyncio
from config import TOKEN
from globals import shutUpList,webhooks,afk,giveaway_sniper,nitro_sniper,antiCrazy



bot = commands.Bot(command_prefix="!",self_bot=True)
executor = concurrent.futures.ThreadPoolExecutor()

#events
@bot.event
async def on_ready():
    os.system("clear") if os.name=="posix" else os.system("cls")
    print(f"Selfbor active, logged in as {bot.user}")

def nitro_snipe(message):
    if ("discord.gift/" in message.content):
        code = message.content.split("discord.gift/")[1].split(" ")[0]
    elif ("discordapp.com/gifts/" in message.content):
        code = message.content.split("discordapp.com/gifts/")[1].split(" ")[0]
    elif("discord.com/gifts/" in message.content):
        code = message.content.split("discord.com/gifts/")[1].split(" ")[0]
    else:
        return
    
    r = requests.post(f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem",headers={"authorization":TOKEN})
    if r.status_code == 200:
        print(f"Successfully redeemed nitro code {code}")
    else:
        print(f"Failed to redeem nitro code {code}")

async def giveaway_snipe(message):
    if message.content or message.embeds and message.guild:
        for embed in message.embeds:
            if "giveaway" in embed.title.lower() or "giveaway" in embed.description.lower():
                await message.add_reaction("🎉")
                print(f"Reacted to giveaway in {message.guild.name}")

@bot.event
async def on_message(ctx):
    global shutUpList

    if ctx.author in shutUpList:
        await ctx.reply("shut up " + ctx.author.global_name)
    
    if bot.user in ctx.mentions and afk:
        await ctx.reply("current status: AFK. beep boop")
    
    if nitro_sniper:
        nitro_snipe(ctx)

    if giveaway_sniper:
        await giveaway_snipe(ctx)
    
    if antiCrazy:
        if ctx.author.id == "1171484764256075888" and "ON" in ctx.content:
            await ctx.send("!off")

    await bot.process_commands(ctx)

#commands
@bot.command()
async def afk(ctx):
    global afk
    await ctx.message.delete()
    afk = not(afk)
    
@bot.command()
async def echowh(ctx,*args):
        await ctx.message.delete()
        tokens = [arg for arg in args]
        message = " ".join(tokens)
        data = {"content":message,
                "username":"the hiraeth"
                }
        headers = {
        'Content-Type': 'application/json',
        }
        for hook in webhooks:
            _ = requests.post(hook,data=json.dumps(data),headers=headers)

async def loadCogs(bot):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
#run
async def main():
    await loadCogs(bot)
    await bot.start(TOKEN)
if __name__ == "__main__":
    asyncio.run(main())
