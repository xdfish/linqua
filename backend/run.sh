#!/bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
SERVERPATH="${SCRIPTPATH}/server/server"
MODELPATH="${SERVERPATH}/model"
MODELNAME="vosk-model-en-us-0.42-gigaspeech"

clear
cat << EOF
,--.   ,--.,--.  ,--. ,-----.   ,--. ,--.  ,---.
|  |   |  ||  ,'.|  |'  .-.  '  |  | |  | /  O  \\
|  |   |  ||  |' '  ||  | |  |  |  | |  ||  .-.  |
|  '--.|  ||  | \`   |'  '-'  '-.'  '-'  '|  | |  |
\`-----'\`--'\`--'  \`--' \`-----'--' \`-----' \`--' \`--'
EOF
if test "$1" = "setup"
then
    echo "SETTING UP LINQUA PROJECT"
    mkdir -p $MODELPATH
    if [ ! -d "${MODELPATH}/${MODELNAME}" ]
    then
        echo "[] Downloading VOSK-Model: ${MODELNAME}" && curl "https://alphacephei.com/vosk/models/${MODELNAME}.zip" --output "${MODELNAME}.zip"
        echo "[] Unzipping VOSK-Model: ${MODELNAME}" && unzip -q "${MODELNAME}.zip" -d $MODELPATH && rm "${MODELNAME}.zip"
    fi
    echo "[] Setting up python environment"
    python3 -m venv env && source env/bin/activate && cd server && pip3 install -q -r requirements.txt
    echo "[] Setting up database (mongodb) via Docker"
    if [ ! "$(docker ps -a | grep linqua-db)" ]
    then
         docker run -d -e MONGO_INITDB_ROOT_USERNAME='linqua_db_admin' -e MONGO_INITDB_ROOT_PASSWORD='dev_password' -p 27017:27017 --name linqua-db mongo:latest  
    fi
    echo "LINQUA SETUP COMPLETE"
elif test "$1" = "dev"
then
    echo "DEVELOPMENT MODE!!!! DO NOT USE IN PRODUCTION!!!"
    docker start linqua-db
    echo "WARNING: Data of linqua dev database is only saved inside container (not persistent)"
    source "${SCRIPTPATH}/env/bin/activate" && cd $SERVERPATH && python3 -m uvicorn server:app --reload
elif test "$1" = "prod"
then
    echo "LINQUA PRODUCTION MODE"
    source "${SCRIPTPATH}/env/bin/activate" && cd $SERVERPATH && python3 -m uvicorn server:app
else
    echo -e "OTPIONS:\n\t- setup:  \tsetup python project\n\t- dev:  \tstart server in dev mode (reoload in case of file changes)\n\t- prod:  \tstart server in production mode"
fi
