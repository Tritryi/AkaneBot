import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick (self,ctx, user:discord.Member, *, reason="Raison indéfinie"):
        """
        Expulser un utilisateur. Commande utilisable uniquement si : l'utilisateur ET le bot ont ce droit ET si le bot est
        au dessus de la cible hiérarchiquement. Log l'expulsion dans un channel spécifique.

        Arguments : 
            user: l'utilisateur à expulser
            * : permet de traiter user comme un argument[1] et reason comme une chaine avec espaces
            reason : pourquoi l'utilisateur est expulsé
        """
        if user.top_role >= ctx.me.top_role:
            return await ctx.send("Désolée ! cet utilisateur a une meilleure position que moi...")
        
        try:
            await user.send(f"Tu as été expulsé de {ctx.guild.name} car {reason}. Désolée :-(")
        except discord.HTTPException:
            print("Impossible de dm cet utilisateur")

        try:
            await user.kick(reason=reason)
            await ctx.send(f"{user.name} a été expulsée !!!")

            try:
                channel = await self.bot.fetch_channel(1051971103217684572)
                embed = discord.Embed(
                    title="📛 Expulsion de membre",
                    description=f"**{user.name}** a été expulsé(e) pour cause de **{reason}**",
                    color=discord.Color.dark_blue()
                )   
                await channel.send(embed=embed)

            except discord.NotFound:
                print("Le kick a fonctionné mais impossible de trouver le channel de log")
        
        except discord.Forbidden:
            await ctx.send("Malheureusement, je n'ai pas le droit de faire ceci !")
        except discord.HTTPException:
            await ctx.send("Je n'ai pas réussi à l'expulser...")

    
async def setup(bot):
    await bot.add_cog(Moderation(bot))