#/bin/bash
case "$1" in
  "up")
    docker compose up -d --build
    ;;
  "down")
    docker compose down
    ;;
  "restart")
    docker compose down && docker compose up -d --build
    ;;
  "attack")
    docker exec -it seed-attacker bash
    ;;
  "term")
    docker exec -it x-terminal-10.9.0.5 bash
    ;;
  "serv")
    docker exec -it trusted-server-10.9.0.6 bash
    ;;
  *)
    echo "You have failed to specify what to do correctly."
    exit 1
    ;;
esac