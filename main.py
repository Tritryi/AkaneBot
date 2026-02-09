import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".config")


# Activer les intents pour que le bot suive ce qui se passe sur le serveur
intents = discord.Intents.default()
# Ici pour qu'il lise les messages des utilisateurs (répondre à des pattern, des commandes)
intents.message_content = True

bot = commands.Bot(command_prefix="a!",intents=intents)

"""
Paramètres de base, ce que fait le bot une fois qu'il est connecté
"""
@bot.event
async def on_ready():
    status = discord.CustomActivity(name="I'm on your side, no matter what happens")
    await bot.change_presence(status=discord.Status.online,activity=status)
    print("Bot prêt !")


"""
Permet de faire réagir le bot à ce qui se passe sur le serveur, ce qui est dit.
"""
@bot.event
async def on_message(message):
    # On empêche le bot de répondre à lui-même
    if message.author == bot.user:
        return
    # Petits ajouts drôles d'exemple
    salutations = ["salut","bonjour","hello"]
    if any(mot in message.content.lower() for mot in salutations):
        await message.channel.send(f"Hello {message.author.name} !")

    if "akane" in message.content.lower():
        img = discord.File("./akane.webp")
        await message.channel.send("On parle de moi ? La best girl", file=img)

    # Pour que le bot écoute les commandes et pas seulement les events
    await bot.process_commands(message)

"""
Envoie un bloc d'aide en mp à l'utilisateur.
Pour cela on lit le fichier help.md qui est la documentation du bot, on le met dans embed pour l'UI

Arguments : 
    user : l'utilsateur qui a demandé

"""
bot.remove_command("help")
@bot.command(name="help")
async def help(ctx, user:discord.Member):
    with open("help.md") as f:
        contenu = f.read()
    
    embed = discord.Embed(
        title="📖 Guide d'utilisation d'Akane <:akane_think:1469869490249531564>",
        description=contenu,
        color=discord.Color.blue()
    )
    await ctx.send("Je t'ai envoyé l'aide en mp !", delete_after=2)
    await user.send(embed=embed)

"""
Clear x messages dans le salon où c'est demandé si l'utilisateur a le droit de gérer des messages.
Limit +1 pour aussi supprimer la commande elle-même

Arguments : 
    number : nombre de messages à supprimer


"""
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,number: int):
    await ctx.channel.purge(limit=number+1)
    await ctx.send(f"✅ J'ai supprimé {number} messages", delete_after=3)


"""
Expulser un utilisateur. Commande utilisable uniquement si : l'utilisateur ET le bot ont ce droit ET si le bot est
au dessus de la cible hiérarchiquement. Log l'expulsion dans un channel spécifique.

Arguments : 
    user: l'utilisateur à expulser
    * : permet de traiter user comme un argument[1] et reason comme une chaine avec espaces
    reason : pourquoi l'utilisateur est expulsé

"""
@bot.command()
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def kick (ctx, user:discord.Member, *, reason="Raison indéfinie"):
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
            channel = await bot.fetch_channel(1051971103217684572)
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



    
        











bot.run(os.getenv("DISCORD_TOKEN"))
