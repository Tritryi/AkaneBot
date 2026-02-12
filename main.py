import discord
from discord.ext import commands
import os, datetime
from dotenv import load_dotenv
load_dotenv(dotenv_path=".config")


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
        channel_log = await self.fetch_channel(1051971103217684572)
        channel_welcome = await self.fetch_channel(792013504969310258)

        embed_log = discord.Embed(
            title=f"Arrivée du membre {member.name}",
            description=f"<@{member.id}> a rejoint le serveur {datetime.datetime.now()}",
            color=discord.Color.from_rgb(61,247,32)
        )

        await channel_log.send(embed=embed_log)
        await channel_welcome.send(f"<@{member.id}> nous a rejoint ! Bienvenu !! <:akane_smile:1471298088860913674>")

    
    

    # @clear.error
    # async def clear_error(self,ctx,error):
    #     if isinstance(error,commands.MissingPermissions):
    #         ctx.send("Désolée mais vous ne pouvez pas faire ça !",delete_after=2)


        
        


bot = AkaneBot()
bot.run(os.getenv("DISCORD_TOKEN"))
