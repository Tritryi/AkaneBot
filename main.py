import discord
from discord.ext import commands
import os, datetime
from dotenv import load_dotenv
load_dotenv(dotenv_path=".config")

# FIXME GENERAL : AJOUTER DES TRY-CATCH UN PEU PARTOUT POUR LA PROPRETÉ DU CODE
class AkaneBot(commands.Bot):
    def __init__(self):
        # Activer les intents pour que le bot suive ce qui se passe sur le serveur
        intents = discord.Intents.default()
        intents.members = True
        # Ici pour qu'il lise les messages des utilisateurs (répondre à des pattern, des commandes)
        intents.message_content = True
        super().__init__(command_prefix="a!", intents=intents)

        self.remove_command("help")

        # Récupérer le contenu de help
        with open("help.md") as f:
            self.helpcontent = f.read()

    async def setup_hook(self):
        for file in os.listdir("./cogs"):
            if file.endswith(".py") and not file.startswith("__"):
                extension_name = f'cogs.{file[:-3]}'
                try:
                    await self.load_extension(extension_name)
                except Exception as e:
                    print(f"{extension_name} n'a pas pu être chargée : {e}")
        
 
    async def on_ready(self):
        """
        Paramètres de base, ce que fait le bot une fois qu'il est connecté
        """
        status = discord.CustomActivity(name="I'm on your side, no matter what happens")
        await self.change_presence(status=discord.Status.online,activity=status)
        print("Bot prêt !")

        # à décommenter si on veut voir quelles commandes sont chargées
        # print([command.name for command in self.commands])

    async def on_message(self,message):
        """
        Permet de faire réagir le bot à ce qui se passe sur le serveur, ce qui est dit.
        """
        # On empêche le bot de répondre à lui-même
        if message.author == self.user:
            return
        # Petits ajouts drôles d'exemple
        salutations = ["salut","bonjour","hello"]
        if any(mot in message.content.lower() for mot in salutations):
            await message.channel.send(f"Hello {message.author.name} !")

        if "akane" in message.content.lower():
            img = discord.File("./img/akane.webp")
            await message.channel.send("On parle de moi ? La best girl", file=img)

        # Pour que le bot écoute les commandes et pas seulement les events
        await bot.process_commands(message)

    
    async def on_member_join(self,member: discord.User):
        """
        Permet de faire réagir le bot à l'arrivée d'un nouveau membre. On envoie un message de bienvenu dans le général et
        un log pour les modérateurs indiquant qui est arrivé quand.
        """
        # Récupération  des channels et de la date
        channel_log = await self.fetch_channel(1051971103217684572)
        channel_welcome = await self.fetch_channel(792013504969310258)
        date = datetime.datetime.now("%d/%m%/%Y %H:%M")
        # Création du embed pour les logs
        embed_log = discord.Embed(
            title=f"Arrivée du membre {member.name}",
            description=f"<@{member.id}> a rejoint le serveur {date}",
            color=discord.Color.from_rgb(61,247,32)
        )
        # Envoie des messages dans les channels respectifs
        await channel_log.send(embed=embed_log)
        # Ici, on mentionne l'utilisateur (id obligatoire !) et on utilise un emoji personnalisé
        # Pour les emojis personnalisés : "Emojis" sur votre discord developer portal, nom_emoji:id_emoji
        await channel_welcome.send(f"<@{member.id}> nous a rejoint ! Bienvenu !! <:akane_smile:1471298088860913674>")

    # FIXME : CETTE FONCTION N'A PAS ENCORE ÉTÉ TESTÉE
    async def on_member_remove(self,member: discord.User):
        """
        Permet de faire réagir le bot au départ d'un membre. On envoie un message de d'au revoir dans le général et
        un log pour les modérateurs indiquant qui est parti quand.
        """
        # Récupération  des channels et de la date
        channel_log = await self.fetch_channel(1051971103217684572)
        channel_welcome = await self.fetch_channel(792013504969310258)
        date = datetime.datetime.now("%d/%m%/%Y %H:%M")
        # Création du embed pour les logs
        embed_log = discord.Embed(
            title=f"Départ du membre {member.name}",
            description=f"<@{member.id}> a rejoint le serveur {date}",
            color=discord.Color.from_rgb(240,45,38)
        )
        # Envoie des messages dans les channels respectifs
        await channel_log.send(embed=embed_log)
        # Ici, on mentionne l'utilisateur (id obligatoire !) et on utilise un emoji personnalisé
        # Pour les emojis personnalisés : "Emojis" sur votre discord developer portal, nom_emoji:id_emoji
        await channel_welcome.send(f"<@{member.id}> nous a malheureusement quittés... <:akane_cry:1471304232605847839>")

    
    

    # @clear.error
    # async def clear_error(self,ctx,error):
    #     if isinstance(error,commands.MissingPermissions):
    #         ctx.send("Désolée mais vous ne pouvez pas faire ça !",delete_after=2)


        
        


bot = AkaneBot()
bot.run(os.getenv("DISCORD_TOKEN"))
