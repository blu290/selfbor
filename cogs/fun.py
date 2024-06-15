import selfcord
from selfcord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def rizz(self,ctx):
        await ctx.message.delete()
        with open ("resources/rizz.txt","r") as f:
            rizz = f.readlines()
            await ctx.send(random.choice(rizz))


async def setup(bot):
    await bot.add_cog(Fun(bot))
