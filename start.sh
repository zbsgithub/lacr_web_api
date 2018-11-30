#!/usr/bin/env bash
celery -A lacr_api worker -l info &
celery -A lacr_api beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &