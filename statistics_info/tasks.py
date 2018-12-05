# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery import shared_task
from statistics_info.daily_statistic.device_statistic import DeviceStatistic
from statistics_info.daily_statistic.img_statistic import ImageStatistic


@shared_task
def image_upload_statistic(snapshots_dir):
    image_statistic = ImageStatistic(snapshots_dir=snapshots_dir)
    image_statistic.start()


@shared_task
def device_statistic(archive_dir):
    statistic = DeviceStatistic(archive_path=archive_dir)
    statistic.start()
