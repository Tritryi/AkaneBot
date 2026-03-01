FROM python:3.15.0a6-trixie
# il me faut : copier le code, installer les bibliothèques, lancer le bot

WORKDIR /app

# copie le contenu du dossier actuel dans le dossier /app sur le conteneur
COPY . .

RUN python -m pip install --upgrade pip && \
    python -m pip install discord.py python-dotenv

RUN ls /app 

CMD ["python3","main.py"]
