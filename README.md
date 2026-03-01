# <img src="./img/presentation.webp" height="60"> Présentation
**AkaneBot** est un repository qui a pour vocation de fournir une base à tout ceux voulant créer leur propre bot discord pour leur serveur.

Ce repository est né d'une envie personnelle de créer un bot, puis j'ai réalisé que la documentation python et les exemples étaient peu nombreux sur internet. J'ai donc décidé de mettre à disposition une base de code pour construire le bot discord de vos rêves.

**AkaneBot** est un repository sous **license MIT**, vous pouvez utiliser le code librement tant que vous ne modifiez pas la license et que vous me citez !

**AkaneBot** est une application open-source et entièrement écrite en `Python`.


# <img src="./img/utility.webp" height="40"> Utiliser le bot
Avant toute chose, je vous invite à vous rendre sur le [Discord Developer Portal](https://discord.com/developers/applications) et cliquer sur "New Application" afin de créer votre bot. Ensuite, libre à vous d'utiliser mon code comme bon vous semble.

Le code que je fournis ici est une base solide. Vous pouvez l'appliquer à votre bot et il vous suffira de le personnaliser (après tout, chacun son bot, je ne donnerai pas accès au mien 🙂).
Il propose des fonctions de modération de base (kick, clear, etc.) mais aussi des fonctionnalités plus simples comme réagir à des mots clés ou changer son statut.

Libre à vous de personnaliser le code pour qu'il réagisse à ce que vous voulez, je vous fournis la recette et à vous de faire votre préparation. En particulier, je vous invite à modifier le préfixe de commande, le nom du bot, les images, le statut, enfin tout ce qui fait la personnalité de votre bot ! Ne gardez pas les informations du mien ce n'est pas très utile.

# <img src="./img/prepare.webp" height="40"> Préparer le bot
### Environnement nécessaire (Linux)
Afin de pouvoir lancer le bot (éxecuter le script main.py) vous allez devoir vous munir d'un environnement adapté.
Je conseille d'utiliser un environnement virtuel python, pour ce faire : 

>`python3 -m venv .venv`
>
>`source .venv/bin/activate`
>
>`pip install -U discord.py`
>
>`pip install python-dotenv`

Avec tout cela, votre environnement python est prêt.

### Environnement nécessaire (Windows)
*à venir*

### Variables d'environnement
Le code fourni propose d'aller chercher les variables d'environnement dans un fichier nommé `.config` que vous devrez créer vous même.
Dans ce fichier vous devrez utiliser une seule et unique variable d'environnement : 

> `DISCORD_TOKEN` le token du bot

Pour obtenir ce token, rendez-vous sur le Discord Developer Portal et dans le menu "Bot" copiez le token (c'est une suite de caractères aléatoires et très longue) comme ci-dessous :
```
DISCORD_TOKEN=mon_token
```
Deux choses à noter :
- respectez bien les espaces, DISCORD_TOKEN, le égal et le token ne doivent pas avoir d'espace entre eux.
- Par raison de sécurité, discord cache le token une fois celui-ci copié. Si vous le perdez vous devrez faire "Reset Token" et changer sa valeur dans `.config`

### Variables propres à votre utilisation
Les variables propres à votre serveur sont utilisés d'une façon spécifique : un fichier json, plus exactement le fichier `config.json` va vous intéresser.
Je vais passer les détails techniques, ce qui compte c'est que dans ce fichier vous allez devoir modifier les valeurs, pas les noms de variables.

Par exemple, ce fichier contient une variable `channel_welcome_id` c'est l'identifiant du channel où le bot va souhaiter la bienvenue à un utilisateur. Comme la valeur ici est propre à mon serveur, vous devrez vous même faire "copier l'identifiant du salon" sur votre serveur et la remplacer à cet endroit.
Et c'est la même chose pour toutes les autres variables. Ne changez rien d'autre dans ce fichier cependant, ou vous devrez adapter le code.

# 📑 Lancer le bot 
Pour lancer le bot, rien de plus simple, il vous suffit de taper la commande suivante : 

>`python3 main.py`

⚠️ Le bot n'est actif que lorsque votre script tourne !! Si vous coupez le script ou éteignez votre ordinateur, le bot sera instantanément hors ligne. 
Comment faire pour que votre bot tourne 24h/24 ? Cela dépasse un peu l'objectif de mon application, je vous laisse vous renseigner.

# Alternative : docker
Si vous êtes un peu habitué de l'informatique et que vous avez un minimum de connaissances sur docker vous pouvez utiliser cette alternative. Ici, la procédure à suivre sera la suivante.

Récupérez l'image docker du bot avec la commande suivante : 
```
docker docker pull tritryi/discord-bot:latest
```

Ensuite, créez le conteneur, attention ici à bien respecter la partie token ou le conteneur va crasher !
```
docker run -d -e DISCORD_TOKEN="[votre_token]" --name [nom_conteneur]
```

Normalement dès cette commande utilisée votre bot est en ligne ! Maintenant comment personnaliser tout ça ?
Malheureusement en utilisant Docker on ne peut pas vraiment personnaliser le code, par contre vous aurez un bot qui fonctionne.


# Détails techniques
### Commentaire pour les non-développeurs
Quelques points pour les personnes n'étant pas développeurs.

#### Qu'est-ce que les try;expect
À beaucoup d'endroits dans le code, vous verrez des parties avec un bloc **try** et plusieurs blocs **expect**. Ça peut avoir l'air pompeux mais c'est très utile. C'est notamment cela qui permet de ne pas faire crash totalement votre bot si un problème survient. De plus, s'il y a un problème, il sera expliqué dans votre console.
Par contre ce n'est pas exhaustif, beaucoup d'erreurs sont possibles et j'ai pu en oublier quelques unes.

### Structure du code

```
./
    cogs/
    img/
    .gitignore
    config.json
    help.md
    main.py
```
- **cogs/** : ensemble de fichiers python permettant de définir les commandes du bot, on range les commandes par catégories.
- **img/** : dossiers des images, vous pouvez en changer le contenu elles sont là à titre d'exemple comme pour faire envoyer une image au bot et illustrer ce repository.
- **.gitignore** : proposition de gitignore, à vous de le changer comme vous le voulez (pour les développeurs principalement).
- **config.json** : fichier de configuration qui contient les variables récurrentes comme les identifiants de salons, de rôles, les status, etc.
- **help.md** : fichier lu par le bot pour expliquer aux utilisateurs son fonctionnement, il contient un ensemble d'explications qui seront envoyés par message privé à un utilisateur en tapant la commande `a!help`.
- **main.py** : script principal, c'est lui qu'on éxecute pour lancer le bot. Il contient la déclaration du bot, le lancement de celui-ci ainsi que quelques fonctions de base comme répondre aux messages.



# ⁉️ Un bug ?
En cas de bug n'hésitez pas à ouvrir une [issue](https://github.com/Tritryi/DiscordBot/issues) ou me contacter.