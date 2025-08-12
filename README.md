# Installation

docker run \
    --detach \
    --interactive \
    --name icecast \
    --user $(id -u):$(id -g) \

    --volume /etc/localtime:/etc/localtime:ro \
    --env TZ=Europe/Paris \
    --env HOME=/config \
    ghcr.io/jee-r/icecast:latest

