#!/bin/bash

if [ "$#" == "0" ]; then
    echo "ERROR: Please specify a directory name"
    echo
    echo "USAGE: prep DIRNAME"
    exit
fi

DIR=$1
if [ ! -d "${DIR}" ]; then
    mkdir -p ${DIR}/app/{static,templates} 
	touch ${DIR}/app/__init__.py
	touch ${DIR}/app/models.py 
	touch ${DIR}/app/views.py
	touch ${DIR}/app/static/bootstrap.css 
	touch ${DIR}/app/static/index.css
	touch ${DIR}/app/templates/index.html
	touch ${DIR}/config.py
	touch ${DIR}/manage.py
	touch ${DIR}/run.py
    ls -lR ${DIR}
else
    echo "Directory "${DIR}" already exists"
fi
                        
