import discord
import random
from discord.ext import commands, tasks
import utils.config_management as cm


class UtilitairesPublics(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        # pour que la task soit lancée
        self.change_status.start()

    def cog_unload(self):
        # couper la task en même temps que le cog
        self.change_status.cancel()

    @commands.command(name="help")
    async def help(self,ctx):
        """
        Envoie un bloc d'aide en mp à l'utilisateur.
        Pour cela on lit le fichier help.md qui est la documentation du bot, on le met dans embed pour l'UI

        Arguments : 
            aucun
        """
        # On récupère le contenu du help
        helpcontent = self.bot.helpcontent
        # Création du embed
        embed = discord.Embed(
            title="📖 Guide d'utilisation d'Akane <:akane_think:1469869490249531564>",
            description=helpcontent,
            color=discord.Color.from_rgb(63,60,107)
        )
        
        await ctx.send("Je t'ai envoyé l'aide en mp !", delete_after=2) 
        try: 
            await ctx.author.send(embed=embed)
        except discord.HTTPException as e:
            cm.logger(f"Impossible de dm cet utilisateur : {e}", __file__)

    @commands.command()
    async def pres(self,ctx):
        """
        Envoie d'un bloc servant de présentation en utilisaent un embed et un dictionnaire pour les informations.

        Arguments : 
            aucun
        """
        # Ici on définit les informations qu'on veut inclure
        datas = {
            "Prénom" : "Akane",
            "Nom" : "Kurokawa",
            "Inspiration": "Je viens d'un animé qui s'appelle Oshi no Ko",
            "Présentation": """En temps normal, je suis une jeune comédienne de 19 ans qui profite de sa jeunesse et a beaucoup de succès au théâtre tout comme au cinéma. Mais ici, je suis plutôt là pour vous aider à gérer cet endroit. J'aime quand les choses sont en ordre et j'aime beaucoup rigoler pour décompresser. Du coup je peux vous aider à modérer cet endroit !"""
        }
        # On créé une liste contenant nos deux images (thumbnail et bannière), on utilise discord.File car cela est obligé
        # par discord.
        images = ["logo.webp","illustration.webp"]
        files_to_send = []
        for x in images:
            y = discord.File("./img/"+x, filename=x)
            files_to_send.append(y)

        # Création du embed 
        embed = discord.Embed(
            title="🤔 Qui est Akane ?",
            color=discord.Color.from_rgb(63,60,107)
        )
        # Ajout du thumbnail et de l'image
        embed.set_thumbnail(url="attachment://logo.webp")
        embed.set_image(url="attachment://illustration.webp")
        # Boucle permettant d'ajouter toutes nos informations
        for new_data in datas:
            embed.add_field(name=new_data,value=datas[new_data],inline=False)
        try:
            await ctx.send(embed=embed,files=files_to_send)
        except discord.HTTPException as e:
            cm.logger(f"L'envoi du message a échoué : {e}", __file__)

    @tasks.loop(hours=4.0)
    async def change_status(self):
        """
        Task qui a lieu une fois toutes les 4h. Permet simplement de changer le statut du bot parmis 4 status random définis dans le json.
        Nécessite le before_loop pour fonctionner puisqu'il utilise self.bot !!
        """
        config = cm.get_config()
        status_list = config["status"]
        status_text = random.choice(list(status_list.values()))
        activite = discord.Game(name=status_text)

        await self.bot.change_presence(status=discord.Status.online,activity=activite)
       

    @change_status.before_loop
    async def before_change_status(self):
        """
        Dit à discord : attend que le bot soit prêt avant de lancer change_status. Sans ça, on a une erreur car la task se lance avant que l'objet
        bot soit créé.
        """
        #print("attente que le bot soit prêt...")
        await self.bot.wait_until_ready()


    @commands.command()
    async def pfp(self,ctx, user:discord.Member=None):
        """
        Permet d'afficher l'avatar d'un utilisateur. Si un utilisateur est mentionné, on affiche son avatar, sinon le bot affiche son propre avatar

        Arguments : 
            user : l'utilisateur dont on veut l'avateur (peut être NULL)
        """
        # Récupération de la bonne url avec un opérateur ternaire
        avatar = self.bot.user.avatar if not user else user.avatar.url
        
        # création de l'embed
        e = discord.Embed(
            color=discord.Color.from_rgb(109, 110, 151)
        )

        e.set_image(url=avatar)
        
        # envoi de l'avatar
        try:
            await ctx.send(embed=e)
        except discord.HTTPException as e:
            cm.logger(f"L'envoi de l'avatar a échoué : {e}", __file__)

           
        
        
    
    
async def setup(bot):
    await bot.add_cog(UtilitairesPublics(bot))