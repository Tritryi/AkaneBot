## Tout ce qu'il faut savoir sur moi !
Je suis un bot tout simple créé par Tristan pour s'amuser. Un petit résumé des commandes que je peux accomplir : 

- **a!clear** [nombre_de_messages]
Permet de clear le nombre de messages spécifiés.
- **a!help**
Envoie par mp la fiche d'aide du bot à celui qui la demande.
- **a!pres**
Envoie dans le channel la présentation du bot.
- **a!kick** [@utilisateur_à_kick] [raison]
Permet de kick l'utilisateur spécifié pour la raison donnée.
- **a!mute** [@utilisateur_à_mute] [temps_de_mute] [raison]
Permet de timeout l'utilisateur spécifié durant le temps donné et pour la raison spécifiée.   
- **a!unmute** [@utilisateur_à_unmute]
Permet de unmute l'utilisateur spécifié.
- **a!setup_roles**
Créé un message servant d'ajout de rôle. Ecrit un message dans un salon spécifique, où, lorsqu'on réagit on obtient le rôle d'accès au serveur.

### Autres fonctionnalités :
- **on_ready**
Lorsque le bot se connecte il change son statut.

- **on_message**
Le bot réagit quand un utilisateur dit bonjour.
Le bot réagit lorsqu'on mentionne son nom.

- **on_member_join**
Le bot réagit à l'arrivée d'un utilisateur à la fois dans le général et en tant que log.

- **on_member_remove**
Même chose que pour join mais pour le départ d'un utilisateur.

- **on_member_update**
Le bot surveille que les membres ne mettent pas des pseudos interdits. Gare à vous !

- **change_status**
Le bot change de status toutes les 4 heures.

