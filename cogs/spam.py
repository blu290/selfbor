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

async def setup(bot):
    await bot.add_cog(Spam(bot))
