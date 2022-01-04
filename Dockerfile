from ubuntu

WORKDIR "discord_bot/"

COPY discord_bot/ .

RUN apt-get update

RUN apt-get install -y ffmpeg

RUN apt-get upgrade -y

RUN apt-get install -y python3

RUN apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

RUN pip3 install poetry

RUN python3 -m poetry install --no-root
