import selfcord
from selfcord.ext import commands
from rule34Py import rule34Py
import ollama
from bs4 import BeautifulSoup
import functools
import concurrent.futures
import requests
from globals import auto_respond

class Ai(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    def getAISearchResponse(self,s,body):
        response = ollama.generate(model="mistral",prompt=
        "consider the following text:\n\n\n" +
        str(body)+
        "\n\n\n briefly summarise the passage while capturing all relevant details, ignoring html tags"
        )
        return "```\nsummary of "+s + "\n\n"+str(response.get("response"))+"\n```"
    
    def getAIResponse(self,s):
        response = ollama.generate(model="SDRobot",prompt=s)
        return response.get("response")
    
    def filterContent(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content,"html.parser")
        mainContent = soup.find("article") or soup.find("main") or soup.find('div', class_='main-content')
        if not mainContent:
            mainContent = soup.body
        for tag in mainContent.find_all(['nav', 'aside', 'footer', 'header', 'script', 'style']):
            tag.decompose()
        text = mainContent.get_text(separator="\n",strip=True)
        return text

    @commands.command()
    async def read(self,ctx,s:str):
        await ctx.message.delete()
        try:
            body = self.filterContent(s)
            loop = self.bot.loop
            task = functools.partial(self.getAISearchResponse,s,body)
            result = await loop.run_in_executor(self.executor,task)
            await ctx.send(result)
        except Exception as e:
            print(e)

    async def getHistory(self,ctx,r):
        messages = []
        async for message in ctx.channel.history(limit=3,before=r):
            messages.append(str((message.author.global_name if message.author.global_name else "You"))+": " +str(message.content))
        return messages[::-1]
    
    @commands.command()
    async def respond(self,ctx):
        await ctx.message.delete()
        if ctx.message.reference:
            try:
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                messages = await self.getHistory(ctx,message)
                messages = "\n".join(messages)
                prompt = "consider the following message history to get up to speed with the chat. do not focus too much on these however use them for context. HISTORY_START: "+ str(messages) + f"HISTORY_END\n\nrespond to the following message as if you are the user {str(self.bot.user.global_name)} without making reference to your name. reply to the following: " + str(message.content)
                task = functools.partial(self.getAIResponse,prompt)
                loop = self.bot.loop
                result = await loop.run_in_executor(self.executor,task)
                await message.reply(result)
            except Exception as e:
                print(e)



async def setup(bot):
    await bot.add_cog(Ai(bot))
