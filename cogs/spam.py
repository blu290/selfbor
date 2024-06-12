import selfcord
from selfcord.ext import commands

class Spam(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def servmassDM(self,ctx,*args:str):
        await ctx.message.delete()
        message = " ".join(args)
        for member in ctx.guild.members:
            try:
                await member.send(message)
            except Exception as e:
                print(e)
                
    
    @commands.command()
    async def massDM(self,ctx,*args:str):
        await ctx.message.delete()
        message = " ".join(args)
        #get all friends
        for channel in self.bot.private_channels:
            try:
                await channel.send("**MASS DM:** " + message)
            except Exception as e:
                print(e)
    
    @commands.command()
    async def massdelete(self,ctx,limit:int=10):
        await ctx.message.delete()
        async for message in ctx.channel.history(limit=limit):
            try:
                await message.delete()
            except Exception as e:
                print(e)

    @commands.command()
    async def massban(self,ctx):
        await ctx.message.delete()
        for member in ctx.guild.members:
            try:
                await member.ban()
            except Exception as e:
                print(e)

    @commands.command()
    async def purge(self,ctx,limit:int=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=limit)

async def setup(bot):
    await bot.add_cog(Spam(bot))
