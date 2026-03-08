import discord
import datetime
from datetime import timedelta
from discord.ext import commands
import utils.config_management as cm


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
        config = cm.get_config()
        channel_id = config["channel_log_id"]
        # Vérification que le rôle du bot est au dessus de l'utilisateur à kick
        if user.top_role >= ctx.me.top_role:
            return await ctx.send("Désolée ! cet utilisateur a une meilleure position que moi...")
        
        # Enfin, on prévient l'utilisateur si ses dm sont ouverts
        try:
            await user.send(f"Tu as été expulsé de {ctx.guild.name} car {reason}. Désolée :-(")
        except discord.HTTPException as e:
            cm.logger(f"Impossible de dm cet utilisateur : {e}", __file__)

        # On essaie de kick l'utilisateur
        try:
            await user.kick(reason=reason)
            await ctx.send(f"{user.name} a été expulsé(e) !!!")

            # Si l'utilisateur a pu être kick, on log cela dans le channel de notre choix
            try:
                channel = await self.bot.fetch_channel(channel_id)
                embed = discord.Embed(
                    title="📛 Expulsion d'un membre",
                    description=f"**{user.name}** a été expulsé(e) pour cause de **{reason}**",
                    color=discord.Color.from_rgb(156,14,2)
                )   
                await channel.send(embed=embed)

            except discord.NotFound as e:
                cm.logger(f"Le kick a fonctionné mais impossible de trouver le channel de log : {e}", __file__)
        
        # Exceptions en cas de problème de droits ou autres
        except discord.Forbidden as e:
            cm.logger(f"Permissions insuffisantes : {e}", __file__)
        except discord.HTTPException as e:
            cm.logger(f"L'expulsion a échoué : {e}", __file__)

        

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def mute (self, ctx, user:discord.Member, until:int = 10 , *, reason="Raison indéfinie"):
        """
        Mute un membre. Commande utilisable si : le bot et l'utilisateur peut modérer les membres ET le bot a un rôle 
        plus élevé que la cible. Comme le kick on log l'action par contre pas de message à l'utilisateur car il peut lire 
        pourquoi il est mute.

        Arguments:
            user : utilisateur à mute
            until : durée EN MINUTES durant laquelle l'utilisateur doit être mute. Maximum 28 jours soit 40320 minutes
            reaso : raison du mute
        """
        config = cm.get_config()
        channel_id = config["channel_log_id"]
        if user.top_role >= ctx.me.top_role:
            return await ctx.send("Désolée ! cet utilisateur a une meilleure position que moi...")
        
        # duree : temps en minute du mute
        # time_fin : calcule la date de fin du mute car discord a besoin de ça 
        duree = timedelta(minutes=until)
        time_fin = datetime.datetime.now(datetime.timezone.utc) + duree
            
        try:
            # timeout l'utilisateur et envoie une notification   
            await user.timeout(time_fin, reason=reason)
            await ctx.send(f"{user.name} a été mute...")

            try:
                # permet de log le mute
                channel_log = await self.bot.fetch_channel(channel_id)
                embed = discord.Embed(
                    title="🔇 Membre timeout",
                    description=f"**{user.name}** a été timeout pendant {until} minutes",
                    color= discord.Color.from_rgb(71,2,87)
                )
                await channel_log.send(embed=embed)

            # exception en cas de channel non trouvé
            except discord.NotFound as e:
                await ctx.send("Je n'ai pas réussi à logger l'action...")
                cm.logger(f"Le timeout a fonctionné mais impossible de trouver le channel de log :  {e}", __file__)

        # exceptions en cas de soucis sur le timeout
        except discord.HTTPException as e:
            await ctx.send("Je n'ai pas réussi à effectuer le timeout...")
            cm.logger(f"Une erreur est survenue du côté de discord : {e}", __file__)
        except TypeError as e :
            await ctx.send("Un problème dans la définition de la date, demandez à l'administrateur...")
            cm.logger(f"La date passée n'a pas un fuseau horaire bien défini : {e}", __file__)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def unmute (self, ctx, user:discord.Member):
        """
        Désactiver le timeout d'un utilisateur (par exemple en cas de fausse manip), pas besoin de raison mais on peut en 
        ajouter une (l'argument) et l'afficher si besoin. La valeur par défaut permet de faire en sorte que la commande 
        fonctionne. De plus, pas besoin de vérifier que l'utilisateur a un rôle supérieur. On log l'action comme toujours

        Arguments:
            user: membre à unmute
        """
        config = cm.get_config()
        channel_id = config["channel_log_id"]
        try:
            # pour unmute, on utilise timeout avec une durée valant 0
            await user.timeout(None, reason="none")
            await ctx.send(f"{user.name}, tu as été demute ! Désolé pour le derangement...")
            
            # évidemment on log l'action
            try:
                channel_log = await self.bot.fetch_channel(channel_id)
                embed = discord.Embed(
                    title="🔈 Membre untimeout",
                    description=f"**{user.name}** a été untimeout",
                    color= discord.Color.from_rgb(215,72,247)
                )
                await channel_log.send(embed=embed)

            # problème de channel comme d'habitude
            except discord.NotFound as e:
                await ctx.send("Je n'ai pas réussi à logger l'action...")
                cm.logger(f"Le timeout a fonctionné mais impossible de trouver le channel de log : {e}", __file__)

        # exception générale si le untimeout ne réussit pas
        except discord.HTTPException as e:
            await ctx.send("Le untimeout n'a pas fonctionné")
            cm.logger(f"Une erreur est survenue du côté de discord : {e}", __file__)
        


    
async def setup(bot):
    await bot.add_cog(Moderation(bot))