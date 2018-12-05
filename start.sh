#!/bin/bash
WORK_DIR=/opt/lacr_web_api
PY_ENV=/home/pyenvs/lacr_api
LOG=/tmp/lacr_web_api.log
if [ ! -f ${LOG} ]; then
    touch ${LOG}
fi

export PYTHONIOENCODING=utf-8
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}
mkdir -p ${WORK_DIR}/log/
source ${PY_ENV}/bin/activate

echo "$(date +%Y-%m-%dT%H:%M:%S) INFO process not run and restart" >> ${LOG}
(${PY_ENV}/bin/python manage.py runserver 0.0.0.0:5081 &)
sleep 1
(${PY_ENV}/bin/python ${PY_ENV}/bin/celery -A lacr_api worker -l info &)
sleep 1
(${PY_ENV}/bin/python ${PY_ENV}/bin/celery -A lacr_api beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &)
echo "$(date +%Y-%m-%dT%H:%M:%S) INFO process is start" >> ${LOG}