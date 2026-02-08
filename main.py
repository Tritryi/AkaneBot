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

@bot.event
async def on_ready():
    status = discord.CustomActivity(name="I'm on your side, no matter what happens")
    await bot.change_presence(status=discord.Status.online,activity=status)
    print("Bot prêt !")


@bot.event
async def on_message(message):
    # On empêche le bot de répondre à lui-même
    if message.author == bot.user:
        return
    # Petit ajout drôle d'exemple
    salutations = ["salut","bonjour","hello"]
    if any(mot in message.content.lower() for mot in salutations):
        await message.channel.send(f"Hello {message.author.name} !")

    if "akane" in message.content.lower():
        img = discord.File("./akane.webp")
        await message.channel.send("On parle de moi ? La best girl", file=img)

    await bot.process_commands(message)

bot.remove_command("help")
@bot.command(name="help")
async def help(ctx):
    with open("help.md") as f:
        contenu = f.read()
    
    embed = discord.Embed(
        title="📖 Guide d'utilisation d'Akane <:akane_think:1469869490249531564>",
        description=contenu,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx,number: int):
    await ctx.channel.purge(limit=number+1)
    await ctx.send(f"✅ J'ai supprimé {number} messages", delete_after=3)

    
#     # COMMANDES PLUS GENERALES
#     if message.content.startswith("a!del"):
#         # coupe "a!del 10" en deux et récupère le 2eme élément
#         number = message.content.split()
#         if len(number) < 2:
#             await message.channel.send("⚠️ Il manque le nombre de messages")
#             return
#         number = int(number[1])
#         # regarde l'historique de message, +1 pour la commande en elle-même
#         deleted = await message.channel.purge(limit=number+1)
#         await message.channel.send(f"✅ J'ai supprimé {number} messages", delete_after=3)
        











bot.run(os.getenv("DISCORD_TOKEN"))
