import discord
import json
from discord.ext import commands


class UtilitairesMod(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self,ctx,number: int = 0):
        """
        Clear x messages dans le salon où c'est demandé si l'utilisateur ET le bot ont le droit de gérer des messages.
        Limit +1 pour aussi supprimer la commande elle-même

        Arguments : 
            number : nombre de messages à supprimer
        """
        # Si l'utilisateur n'a pas donné de nombre de messages, le bot crash, donc on vérifie cela.
        if number == 0:
            ctx.send("Il me faut un nombre de messages !", delete_after=2)
            return
        await ctx.channel.purge(limit=number+1)
        await ctx.send(f"✅ J'ai supprimé {number} messages", delete_after=3)

    @commands.command()
    @commands.bot_has_permissions(add_reactions=True)
    async def setup_roles(self,ctx):
        """
        """
        try:
            channel = await self.bot.fetch_channel(972935312156291202)

            try:
                msg = await channel.fetch_message(1473461649498439711)

            except discord.NotFound as e:
                print(f"Le message n'existe pas ou a été supprimé. On le renvoi.")


            embed_role = discord.Embed(
                title="Bienvenu ! Pour accéder au contenu du serveur veuillez vous attribuer le rôle",
                description="Cliquez sur l'emoji pour devenir un Titan déviant et accéder au serveur",
                color=discord.Color.from_rgb(237,100,26)
            )
            role_msg = await channel.send(embed=embed_role)
        except discord.HTTPException as e :
            print(f"L'envoi du message a échoué : {e}")

        except discord.Forbidden as e:
            print(f"Permissions nécessaires insuffisantes : {e}")

        try:
            await role_msg.add_reaction('rin:966507969091084308')
        except discord.HTTPException as e:
            print(f"L'ajout de la réaction a échoué : {e}")
        except discord.Forbidden as e:
            print(f"Permissions insuffisantes pour ajouter la réaction : {e}")
        except discord.NotFound as e:
            print(f"Emoji introuvable : {e}")
        except TypeError as e:
            print(f"Emoji invalide : {e}")




    
async def setup(bot):
    await bot.add_cog(UtilitairesMod(bot))