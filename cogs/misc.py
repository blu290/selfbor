import selfcord
from selfcord.ext import commands
from globals import nitro_sniper,giveaway_sniper,afk,shutUpList

class Misc(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command()
    async def pfp(self,ctx,member: selfcord.Member):
        await ctx.send(member.avatar)
        await ctx.message.delete()

    @commands.command()
    async def calc(self,ctx,*args):
        await ctx.message.delete()
        tokens = [arg for arg in args]
        statement = " ".join(tokens)
        evaluated = eval(statement)
        await ctx.send(evaluated)

    @commands.command()
    async def shutup(self,ctx, member: selfcord.Member):
        global shutUpList
        if not member in shutUpList:
            shutUpList.append(member)
            await ctx.message.delete()

    @commands.command()
    async def unshutup(self,ctx,member:selfcord.Member):
        global shutUpList
        if member in shutUpList:
            shutUpList.remove(member)
            await ctx.message.delete()

    @commands.command()
    async def nitroSnipe(self,ctx):
        await ctx.message.delete()
        global nitro_sniper
        nitro_sniper = not(nitro_sniper)

    @commands.command()
    async def giveawaySnipe(self,ctx):
        await ctx.message.delete()
        global giveaway_sniper
        giveaway_sniper = not(giveaway_sniper)
    
    @commands.command()
    async def afk(self,ctx):
        global afk
        await ctx.message.delete()
        afk = not(afk)
    
    @commands.command()
    async def log(self,ctx):
        global message_logger
        await ctx.message.delete()
        message_logger = not(message_logger)
    

async def setup(bot):
    await bot.add_cog(Misc(bot))
