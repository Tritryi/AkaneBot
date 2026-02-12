import discord
from discord.ext import commands


class UtilitairesPublics(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

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
            color=discord.Color.blue()
        )
        await ctx.send("Je t'ai envoyé l'aide en mp !", delete_after=2)
        await ctx.author.send(embed=embed)

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
            color=discord.Color.from_rgb(69,56,90)
        )
        # Ajout du thumbnail et de l'image
        embed.set_thumbnail(url="attachment://logo.webp")
        embed.set_image(url="attachment://illustration.webp")
        # Boucle permettant d'ajouter toutes nos informations
        for new_data in datas:
            embed.add_field(name=new_data,value=datas[new_data],inline=False)

        await ctx.send(embed=embed,files=files_to_send)

    
    
    
async def setup(bot):
    await bot.add_cog(UtilitairesPublics(bot))