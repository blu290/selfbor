import selfcord
from selfcord.ext import commands
import os
from rule34Py import Post, rule34Py
import requests
from bs4 import BeautifulSoup
import ollama
import concurrent.futures
import functools
import json

global shutUpList
shutUpList = []
global webhooks
webhooks = ["https://discord.com/api/webhooks/1149807641141456926/iK-eUvN9-2s20sL-T3PP1F40q1kVp4kw0XduoPc4vhM-Ix2tqD6nUgejsUmLHlQ4N4o6"]

bot = commands.Bot(command_prefix="!",self_bot=True)
executor = concurrent.futures.ThreadPoolExecutor()

#events
@bot.event
async def on_ready():
    os.system("clear") if os.name=="posix" else os.system("cls")
    print(f"logged in as {bot.user}")

@bot.event
async def on_message(ctx):
    global shutUpList
    if ctx.author in shutUpList:
        await ctx.reply("shut up " + ctx.author.display_name)

    await bot.process_commands(ctx)

#commands
@bot.command()
async def shutup(ctx, member: selfcord.Member):
    global shutUpList
    if not member in shutUpList:
        shutUpList.append(member)
        await ctx.message.delete()

@bot.command()
async def unshutup(ctx,member:selfcord.Member):
    global shutUpList
    if member in shutUpList:
        shutUpList.remove(member)
        await ctx.message.delete()

@bot.command()
async def pfp(ctx,member: selfcord.Member):
    await ctx.send(member.avatar)
    await ctx.message.delete()

@bot.command()
async def r34(ctx,*args:str):
    try:
        search = [str(arg) for arg in args]
        r34py = rule34Py()
        post = r34py.random_post(search)
        await ctx.send(post.image)

    except:
        print("not gonna work")
    finally:
        await ctx.message.delete()

def getAIResponse(s,body):
    response = ollama.generate(model="mistral",prompt=
        "consider the following text:\n\n\n" +
        str(body)+
        "\n\n\n briefly summarise the passage while capturing all relevant details, ignoring html tags"
    )
    return "```\nsummary of "+s + "\n\n"+str(response.get("response"))+"\n```"
    

@bot.command()
async def read(ctx,s:str):
    await ctx.message.delete()
    try:
        page = requests.get(s)
        soup = BeautifulSoup(page.content,"html.parser")
        body = soup.body
        loop = bot.loop
        task = functools.partial(getAIResponse,s,body)
        result = await loop.run_in_executor(executor,task)
        await ctx.send(result)
    except:
        print("not work")


@bot.command()
async def calc(ctx,*args):
    await ctx.message.delete()
    tokens = [arg for arg in args]
    statement = " ".join(tokens)
    evaluated = eval(statement)
    await ctx.send(evaluated)

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

@bot.command()
async def makegc(ctx,*args):
    await ctx.message.delete()
    args = [arg for arg in args]
    await selfcord.Client.create_group(args)

#run
if __name__ == "__main__":
    r = open("token.txt")
    token = r.readline()
    bot.run(token)
