import discord
from discord.ext import commands
from utils.config_management import get_config


class Listener(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        """
        Event listener pour l'ajout de réactions sur notre message de setup_roles (voir utilitaires_mod). Si la réaction est ajoutée
        sur notre message alors on s'occupe d'ajouter des rôles à l'utilisateur.

        À noter sur les rôles : le bot ne peut pas ajouter des rôles plus "puissants" que le sien

        Arguments : 
            payload : il s'agit d'un ensemble d'informations envoyées par discord à chaque fois qu'une réaction est ajoutée sur un message
        """
        # chargement des variables
        config = get_config()
        msg_id = config["role_message_id"]
        ch_id = config["role_channel_id"]
        emoji_id = config["emoji_role_id"]
        id_r1 = config["id_role1"]
        id_r2 = config["id_role2"]

        # Si la réaction concerne bien le message de setup des roles et que c'est le bon emoji ajouté, alors 
        # on récupère les rôles que l'on veut ajouter
        if payload.channel_id == ch_id and \
           payload.message_id == msg_id and \
           payload.emoji.id == emoji_id:
            guild = payload.member.guild
            role1 = guild.get_role(id_r1)
            role2 = guild.get_role(id_r2)

            # si les rôles ont bien été récupérés on les ajoute à l'utilisateur
            if role1 and role2:
                try:
                    # en théorie on peut mettre une raison mais ça n'a pas vraiment d'intérêt
                    await payload.member.add_roles(role1,role2)
                except discord.Forbidden:
                    print("Permissions insuffisantes pour ajouter ces rôles")
                except discord.HTTPException:
                    print("Échec de l'ajout des rôles")
            else:
                print("Un des rôles n'a pas pu être récupéré")
                return
            
        # dans le cas où une réaction concerne un autre message ou un autre emoji, on ignore   
        else:
            return
        
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        """
        Event listener pour la suppression de réactions sur notre message de setup_roles (voir utilitaires_mod). Si la réaction est retirée
        sur notre message alors on s'occupe d'enlever des rôles à l'utilisateur.

        À noter sur les rôles : le bot ne peut pas enlever des rôles plus "puissants" que le sien

        Arguments : 
            payload : il s'agit d'un ensemble d'informations envoyées par discord à chaque fois qu'une réaction est retirée sur un message
        """
        # chargement des variables
        config = get_config()
        msg_id = config["role_message_id"]
        ch_id = config["role_channel_id"]
        emoji_id = config["emoji_role_id"]
        id_r1 = config["id_role1"]
        id_r2 = config["id_role2"]

        # Si la réaction concerne bien le message de setup des roles et que c'est le bon emoji ajouté, alors 
        # on récupère les rôles que l'on veut ajouter
        if payload.channel_id == ch_id and \
           payload.message_id == msg_id and \
           payload.emoji.id == emoji_id:
            # on récupère l'objet guild (serveur) et le membre depuis le bot 
            # remove ne renvoie pas les mêmes informations que add
            guild = self.bot.get_guild(payload.guild_id)
            if guild == None:
                return
            member = guild.get_member(payload.user_id)
            if member == None:
                return
            
            role1 = guild.get_role(id_r1)
            role2 = guild.get_role(id_r2)

            # si les rôles ont bien été récupérés, on les enlève à l'utilisateur
            if role1 and role2:
                try:
                    await member.remove_roles(role1,role2)
                except discord.Forbidden:
                    print("Permissions insuffisantes pour retirer ces rôles")
                except discord.HTTPException:
                    print("Échec de la suppression des rôles")
            else:
                print("Un des rôles n'a pas pu être récupéré")
                return
        # dans le cas où une réaction concerne un autre message ou un autre emoji, on ignore   
        else:
            return
        
    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        """
        Listener qui détecte quand un membre change son profil. Ici, l'idée est de bloquer les pseudos interdits donc on va travailler sur 
        nickname. Par contre, on peut aussi surveiller : les rôles, les photos de profil, etc.

        Arguments : 
            before : informations avant changement
            after : informations après changement
        """
        # si autre chose que le nom change, on n'agit pas
        if before.nick == after.nick:
            return
        # on définit des mots/caractères interdits, à vous d'en mettre autant que vous voulez
        pseudos_interdits = ["merde","gueule","!"] # on va rester soft ici :)
        for mot in pseudos_interdits:
            if mot in after.nick.lower():
                # si on trouve un mot interdit dans le pseudo, on prépare l'action en récupérant le channel de log
                config = get_config()
                ch_log_id = config["channel_log_id"]
                try:
                    channel_log = await self.bot.fetch_channel(ch_log_id)
                except discord.NotFound:
                    print("Le channel n'a pas été trouvé")
                try:
                    # on rename l'utilisateur pour que son pseudo vulgaire n'apparaisse plus
                    pseudo_invalide = after.nick
                    await after.edit(nick="renomme toi :)", reason="Pseudo vulgaire !")

                    # on log le rename pour que les modérateurs soient au courant du pseudo qui a été utilisé en précisant l'ancien pseudo
                    embed_success = discord.Embed(
                    title="⭕ Membre renommé car pseudo interdit",
                    description=f"J'ai changé le pseudo du membre anciennement {before.nick} car il avait utilisé **{pseudo_invalide}** comme pseudo.",
                    color= discord.Color.from_rgb(2, 87, 97)
                    )
                    try:
                        await channel_log.send(embed=embed_success)
                    except discord.HTTPException:
                        print("échec de l'envoi du log.")

                # si l'utilisateur ne peut pas être rename, on log quand même c'est important !
                except discord.Forbidden:
                    embed_error = discord.Embed(
                        title="❌ Échec punition membre",
                        description=f"Un membre s'est renommé {after.nick} mais son rôle est trop élevé pour que je le renomme...",
                        color=discord.Color.from_rgb(158,92,5)
                    )
                    await channel_log.send(embed=embed_error)
                    print("Cet utilisateur ne peut pas être renommé par le bot")
                except discord.HTTPException:
                    print("Le changement de pseudo a échoué")

                






async def setup(bot):
    await bot.add_cog(Listener(bot))