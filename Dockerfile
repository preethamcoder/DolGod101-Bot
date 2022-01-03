from ubuntu
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
COPY discord_bot/ .
WORKDIR "discord_bot/"
COPY . discord_bot/
#RUN python3 -m poetry install
RUN export FLASK_ENV=keep_alive
#RUN flask run