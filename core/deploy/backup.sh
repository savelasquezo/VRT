#!/bin/bash

export FECHA=`date +%d_%m_%Y_%H_%M_%S`
export NAME=vrt_${FECHA}.dump
export DIR=/home/savelasquezo/apps/vrt/core/vrtbackup
USER_DB=postgres
NAME_DB=dbvaortrading
cd $DIR
> ${NAME}
export PGPASSWORD=4oPn2655Lmn
chmod 777 ${NAME}
echo "BACKUP - Iniciando!"
pg_dump -U $USER_DB -h localhost --port 5432 -f ${NAME} $NAME_DB
echo "BACKUP - Finalizado"
