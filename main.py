import selfcord
from selfcord.ext import commands
import os
import requests
import concurrent.futures
import json
import asyncio
from config import TOKEN
from globals import shutUpList,webhooks,afk


bot = commands.Bot(command_prefix="!",self_bot=True)
executor = concurrent.futures.ThreadPoolExecutor()

#events
@bot.event
async def on_ready():
    #os.system("clear") if os.name=="posix" else os.system("cls")
    print(f"logged in as {bot.user}")

@bot.event
async def on_message(ctx):
    global shutUpList

    if ctx.author in shutUpList:
        await ctx.reply("shut up " + ctx.author.global_name)
    
    if bot.user in ctx.mentions and afk:
        await ctx.reply("current status: AFK. beep boop")
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
