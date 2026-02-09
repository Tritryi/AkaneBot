import discord
from discord.ext import commands


class UtilitairesMod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self,ctx,number: int = 0):
        """
        Clear x messages dans le salon où c'est demandé si l'utilisateur a le droit de gérer des messages.
        Limit +1 pour aussi supprimer la commande elle-même

        Arguments : 
            number : nombre de messages à supprimer
        """
        if number == 0:
            ctx.send("Il me faut un nombre de messages !", delete_after=2)
            return
        await ctx.channel.purge(limit=number+1)
        await ctx.send(f"✅ J'ai supprimé {number} messages", delete_after=3)

    
async def setup(bot):
    await bot.add_cog(UtilitairesMod(bot))