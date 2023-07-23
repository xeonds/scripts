#!/bin/bash
NAME="atelier-of-zimin"
VERSION="1.20.1"
ACTION=$1

case $ACTION in
run)
  docker run -d -it -p 25565:25565 \
    -v $(pwd)/$NAME:/data \
    -e EULA=TRUE \
    -e VERSION=$VERSION \
    -e DIFFICULTY=hard \
    -e ONLINE_MODE=FALSE \
    -e SERVER_NAME=$NAME \
    -e MOTD="A new legend story" \
    --name $NAME \
    itzg/minecraft-server
  ;;
start)
  docker start $NAME
  ;;
restart)
  docker restart $NAME
  ;;
stop)
  docker stop $NAME
  ;;
down)
  docker stop $NAME | xargs docker rm
  ;;
cli)
  docker exec -i $NAME rcon-cli
  ;;
sh)
  docker exec -it $NAME bash
  ;;
log)
  docker logs -f $NAME
  ;;
monitor) # 监控报警服务
  $(./$0 log) | grep -E --line-buffered "error|fail|warn" |
    while read line; do
      json="{\"token\": \"$TOKEN\", \"title\": \"MC服务端异常报警\", \"content\": \"$line\"}"
      curl -H "Content-Type: application/json" -X POST -d "$json" "http://www.pushplus.plus/send"
    done
  ;;
backup) # 备份文件
  zip -qr [backup]mc-server-$NAME-$(date +%Y%m%d%H%M%S).zip world $NAME/ $0
  ;;
*)
  echo "Invalid argument."
  exit 2
  ;;
esac
