import selfcord
from selfcord.ext import commands
from rule34Py import rule34Py

class Nsfw(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def r34(self,ctx,*args:str):
        await ctx.message.delete()
        try:
            search = [str(arg) for arg in args]
            r34py = rule34Py()
            post = r34py.random_post(search)
            await ctx.send(post.image)
        except:
            print("not gonna work")


async def setup(bot):
    await bot.add_cog(Nsfw(bot))
