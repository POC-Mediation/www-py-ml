#!/bin/bash

# Define a timestamp function
timestamp() {
  #date +"%T"
  date '+%Y-%m-%d %H:%M:%S'
}

#USERID=xavier
#USERPW=valer1e!
#export USERID USERPW

GIT_EMAIL=xavier.mary@outlook.com
GIT_USERNAME=xavier
GIT_USERPSW=valer1e!
GIT_SERVER=valeriadiportela.sytes.net:3000
GIT_HOST=https://${GIT_USERNAME}:${GIT_USERPSW}@${GIT_SERVER}
#GIT_HOME=/Workspace/bluemix/
#GIT_PATH=/Workspace/bluemix/bin/
export GIT_PATH GIT_EMAIL GIT_HOST

GIT_ORG=/DEMO/
GIT_SPACE=${GIT_HOST}${GIT_ORG}
GIT_PROJECT=www-py-ml.git
GIT_CMD=git

export GIT_CMD GIT_ORG GIT_SPACE

${GIT_CMD} config --global user.email "${GIT_EMAIL}"
${GIT_CMD} config --global user.name "${GIT_USERNAME}"
${GIT_CMD} config credential.helper store

export GIT_SSL_NO_VERIFY=1

${GIT_CMD} config --global http.sslverify false
#git init
echo git remote add origin ${GIT_SPACE}${GIT_PROJECT}
git remote add origin ${GIT_SPACE}${GIT_PROJECT}

${GIT_CMD} add .
${GIT_CMD} add -u

#git add IP_valeriadiportela.sytes.net.txt
#git add IP_valeriadiportela.sytes.net.txt

#git status
#git commit -a

TS=`timestamp`
echo "TIMESTAMP = $TS"

git commit -m "update myIP - $TS"
git push -u origin master

#git push https://xavier:valer1e!@myhomesweethome.sytes.net:3000/xavier/valeria_IP.git --all
