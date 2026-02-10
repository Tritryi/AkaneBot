# <img src="presentation" height="40"> Présentation

# Utilité du bot
Avant toute chose, je vous invite à vous rendre sur le [Discord Developer Portal](https://discord.com/developers/applications) et cliquer sur "New Application" afin de créer votre bot. Ensuite, libre à vous d'utiliser mon code comme bon vous semble.

Le code que je fournis ici est un code de base pour votre bot discord. Il peut convenir à n'importe quel bot tant que vous en avez créé un (après tout, chacun son bot, je ne donnerai pas accès au mien 🙂). 
Il propose des fonctions de modération de base (kick, clear, etc.) mais aussi des fonctionnalités plus simples comme réagir à des mots clés.

Libre à vous de personnaliser le code pour qu'il réagisse à ce que vous voulez, je vous fournis la recette et à vous de faire votre préparation. Notamment, je vous invite à modifier le préfixe de commande, le nom du bot, les images, le statut, enfin tout ce qui fait la personnalité de votre bot ! Ne gardez pas les informations du mien ce n'est pas très utile.

# Préparer le bot
## Environnement nécessaire
Afin de pouvoir lancer le bot (éxecuter le script main.py) vous allez devoir vous munir d'un environnement adapté.
Je conseille d'utiliser un environnement virtuel python, pour ce faire : 

>`python -m venv .venv`
>
>`source .venv/bin/activate`
>
>`pip install -U discord.py`
>
>`pip install python-dotenv`

Avec tout cela, votre environnement python est prêt.

## Variables d'environnement
Le code fournit propose d'aller chercher les variables d'environnement dans un fichier nommé `.config`
Dans ce fichier vous devrez utiliser une seule et unique variable d'environnement : 

> `DISCORD_TOKEN` le token du bot

## ⚠️ Variables propres à votre utilisation
Dans le code fourni, à certains endroits on récupère des identifiants de salon notamment avec la fonction `fetch_channel()`, cet identifiant est propre à votre serveur ! Si vous voulez que cela fonctionne à vous de changer cet identifiant.

# Utiliser le bot 
Pour lancer le bot, rien de plus simple, il vous suffit de taper la commande suivante : 

>`python3 main.py`

⚠️ Le bot n'est actif que lorsque votre script tourne !!



## Structure du code

```
./
    cogs/ 
    .gitignore
    akane.webp
    help.md
    main.py
```
- **cogs/** : ensemble de fichiers python permettant de définir les commandes du bot, on range les commandes par catégories.
- **.gitignore** : proposition de gitignore, à vous de le changer comme vous le voulez.
- **akane.webp** : simple image pour illustrer l'envoi d'images avec le bot, vous pouvez la modifier.
- **help.md** : fichier lu par le bot pour expliquer aux utilisateurs son fonctionnement, il contient un ensemble d'explications qui seront envoyés par message privé à un utilisateur en tapant la commande `a!help`.
- **main.py** : script principal, c'est lui qu'on éxecute pour lancer le bot. Il contient la déclaration du bot, le lancement de celui-ci ainsi que quelques fonctions de base comme répondre aux messages.

# Un bug ?
En cas de bug n'hésitez pas à ouvrir une [issue](https://github.com/Tritryi/DiscordBot/issues).