#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd )
COMMAND=$1

#exit the script if the version is not defined
if [ -z "$COMMAND" ]
  then
    echo "No command supplied! eg: ./recipe-service.sh start"
    exit 1
fi

echo $COMMAND

case "$COMMAND" in
  "start")
      docker-compose build
      docker-compose up -d
      ;;
  "stop")
      docker-compose down
      ;;
  *)
      echo "Invalid command. eg: ./recipe-service.sh start, ./recipe-service.sh stopts"
      ;;
esac

echo "done!"
exit 0