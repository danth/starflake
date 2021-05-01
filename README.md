# Starflake

A game about chemicals, played through a Discord bot.

## Run

Starflake is run inside a Docker container:

```sh
docker build -t starflake .
docker container create \
  -e DISCORD_TOKEN=… \
  -e STARFLAKE_DIR=/var/lib/starflake \
  --mount source=starflake,target=/var/lib/starflake \
  --name starflake \
  starflake
docker start -a starflake
```
