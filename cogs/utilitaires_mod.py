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
        Permet d'envoyer le message d'association de rôles. Ici on a simplement un embed avec un rôle qui permet de devenir 
        membre du serveur. Cette fonction utilise des fonctionnalités Python un peu plus complexe comme aller chercher des variables dans un fichier json.
        Pour comprendre tout cela, référez vous au README ou au dépôt github.

        Arguments :
            aucun
        """
        # chargement des variables depuis le fichier json
        config = self.bot.get_config()
        msg_id = config["role_message_id"]
        channel_id = config["role_channel_id"]
        
        # récupération du channel, fin s'il n'est pas trouvé
        channel = await self.bot.fetch_channel(channel_id)
        if not channel:
            print("Salon introuvable")
            return

        # on regarde si ce message existe déjà, si c'est le cas la fonction s'arrête
        try:
            msg = await channel.fetch_message(msg_id)
            await channel.send("Ce setup a déjà été fait !")
            return

        # cas où le setup n'a pas encore été fait, on catch l'erreur pour éviter des messages rouges ;)
        except discord.NotFound:
            print(f"Le message n'existe pas ou a été supprimé. On le renvoi.")
        except discord.Forbidden as e:
            print(f"Permissions insuffisantes pour récupérer le message : {e}.")

        # création du message, envoi et update de la configuration (on change l'identifiant du message)
        try:
            embed_role = discord.Embed(
                title="Bienvenu ! Pour accéder au contenu du serveur veuillez vous attribuer le rôle",
                description="Cliquez sur l'emoji pour devenir un Titan déviant et accéder au serveur",
                color=discord.Color.from_rgb(237,100,26)
            )
            role_msg = await channel.send(embed=embed_role)
            self.update_config("role_message_id",role_msg.id)
        except discord.HTTPException as e :
            print(f"L'envoi du message a échoué : {e}")
        # le bot n'a pas ces permissions
        except discord.Forbidden as e:
            print(f"Permissions nécessaires insuffisantes : {e}")

        # ajout de la réaction et toutes les erreurs que cela peut supposer
        # ici il y a un emoji personnalisé, sinon vous mettez simplement quelque chose comme '🤓'
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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        """
        Event listener pour l'ajout de réactions sur notre message de setup_roles (voir fonction précédente). Si la réaction est ajoutée
        sur notre message alors on s'occupe d'ajouter des rôles à l'utilisateur.

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






    
async def setup(bot):
    await bot.add_cog(UtilitairesMod(bot))