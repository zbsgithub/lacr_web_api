# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import traceback
from celery import shared_task
from statistics_info.daily_statistic.device_statistic import DeviceStatistic
from statistics_info.daily_statistic.img_statistic import ImageStatistic


logger = logging.getLogger(__name__)


@shared_task
def image_upload_statistic(snapshots_dir):
    try:
        image_statistic = ImageStatistic(snapshots_dir=snapshots_dir)
        image_statistic.start()
    except:
        logger.error("imange_upload_statistic exception %s", traceback.format_exc())


@shared_task
def device_statistic(archive_dir):
    try:
        statistic = DeviceStatistic(archive_path=archive_dir)
        statistic.start()
    except:
        logger.error("device_statistic exception %s", traceback.format_exc())
