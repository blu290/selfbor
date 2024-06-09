import selfcord
from selfcord.ext import commands
from rule34Py import rule34Py
import ollama
from bs4 import BeautifulSoup
import functools
import concurrent.futures
import requests
class Ai(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

    def getAIResponse(self,s,body):
        response = ollama.generate(model="mistral",prompt=
        "consider the following text:\n\n\n" +
        str(body)+
        "\n\n\n briefly summarise the passage while capturing all relevant details, ignoring html tags"
        )
        return "```\nsummary of "+s + "\n\n"+str(response.get("response"))+"\n```"

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
            task = functools.partial(self.getAIResponse,s,body)
            result = await loop.run_in_executor(self.executor,task)
            await ctx.send(result)
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Ai(bot))
