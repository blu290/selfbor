import selfcord
from selfcord.ext import commands
from rule34Py import rule34Py
from globals import antiCrazy

class MyOwnThings(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def crezi(self,ctx,*args:str):
        await ctx.message.delete()
        antiCrazy = not(antiCrazy)


async def setup(bot):
    await bot.add_cog(MyOwnThings(bot))
