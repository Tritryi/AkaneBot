import discord
from discord.ext import commands


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
        config = self.bot.get_config()
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
        config = self.bot.get_config()
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






async def setup(bot):
    await bot.add_cog(Listener(bot))