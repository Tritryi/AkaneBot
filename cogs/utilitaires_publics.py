import discord
from discord.ext import commands


class UtilitairesPublics(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self,ctx):
        """
        Envoie un bloc d'aide en mp à l'utilisateur.
        Pour cela on lit le fichier help.md qui est la documentation du bot, on le met dans embed pour l'UI

        Arguments : 
            aucun
        """
        helpcontent = self.bot.helpcontent
        embed = discord.Embed(
            title="📖 Guide d'utilisation d'Akane <:akane_think:1469869490249531564>",
            description=helpcontent,
            color=discord.Color.blue()
        )
        await ctx.send("Je t'ai envoyé l'aide en mp !", delete_after=2)
        await ctx.author.send(embed=embed)

    
    
    
async def setup(bot):
    await bot.add_cog(UtilitairesPublics(bot))