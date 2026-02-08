import discord
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".config")


# Activer les intents pour que le bot suive ce qui se passe sur le serveur
intents = discord.Intents.default()
# Ici pour qu'il lise les messages des utilisateurs (répondre à des pattern, des commandes)
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot prêt !")

@client.event
async def on_message(message):
    # On empêche le bot de répondre à lui-même
    if message.author == client.user:
        return
    # Petit ajout drôle d'exemple
    salutations = ["salut","bonjour","hello"]
    if any(mot in message.content.lower() for mot in salutations):
        await message.channel.send(f"Hello {message.author.name} !")

    # Commande d'affichage de la doc
    if message.content == "a!help":
        with open ("help.md") as f:
            contenu = (f.read())
        await message.channel.send(contenu)
    
    
    # COMMANDES PLUS GENERALES
    if message.content.startswith("a!del"):
        # coupe "a!del 10" en deux et récupère le 2eme élément
        number = message.content.split()
        if len(number) < 2:
            await message.channel.send("⚠️ Il manque le nombre de messages")
            return
        number = int(number[1])
        # regarde l'historique de message, +1 pour la commande en elle-même
        deleted = await message.channel.purge(limit=number+1)
        await message.channel.send(f"✅ J'ai supprimé {number} messages", delete_after=3)
        











client.run(os.getenv("DISCORD_TOKEN"))
