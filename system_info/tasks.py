# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import json
import traceback
import datetime
from concurrent.futures import ThreadPoolExecutor as Pool
from concurrent.futures import wait
from celery import shared_task
import logging
logger = logging.getLogger(__name__)


def archive_statistic(last_archive_dir):
    statistic = {
        "on": {},
        "dm_dn": {},
    }
    on_statistic = statistic["on"]
    dm_dn_statistic = statistic["dm_dn"]

    if not os.path.exists(last_archive_dir) or not os.path.isdir(last_archive_dir):
        logger.error("last archive dir no exist %s", last_archive_dir)
        return statistic

    for device in os.listdir(last_archive_dir):
        device_dir = os.path.join(last_archive_dir, device)
        if not os.path.exists(device_dir) or not os.path.isdir(device_dir):
            logger.error("last archive device dir no exist %s", device_dir)
            continue

        device_list_csv = os.path.join(device_dir, "list.csv")
        if not os.path.exists(device_list_csv) or not os.path.isfile(device_list_csv):
            logger.error("last archive device list csv file no exist %s", device_list_csv)
            continue

        with open(device_list_csv, 'r') as f:
            line = f.readline()
            line_info = line.strip().split("\t")
            dm = line_info[4]
            on = line_info[8]
            dn = line_info[9]
            dm_dn = "%s:%s" % (dm, dn)

            if on in on_statistic:
                on_statistic[on]["num"] += 1
            else:
                on_statistic[on] = {
                    "name": on,
                    "num": 1
                }

            if dm_dn in dm_dn_statistic:
                dm_dn_statistic[dm_dn]["num"] += 1
            else:
                dm_dn_statistic[dm_dn] = {
                    "name": dm_dn,
                    "num": 1
                }
        return statistic

@shared_task
def task_archive_statistic(archive_path):
    archive_stat = {
        "slave": {},
        "on": {},
        "dm_dn": {},
    }
    slave_statistic = archive_stat["slave"]
    dm_dn_statistic = archive_stat["dm_dn"]
    on_statistic = archive_stat["on"]
    logger.info("start statistic archive path %s", archive_path)

    if not os.path.exists(archive_path) or not os.path.isdir(archive_path):
        logger.error("archive path not exist %s", archive_path)
        return None

    last_date = datetime.datetime.now() - datetime.timedelta(days=1)
    last_date_format = last_date.strftime("%Y-%m-%d")

    future_tasks = []
    with Pool(max_workers=10) as executor:
        for archive in os.listdir(archive_path):
            last_archive_dir = os.path.join(archive_path, archive, last_date_format)

            if not os.path.exists(last_archive_dir) or not os.path.isdir(last_archive_dir):
                logging.error("archive dir no exist %s", last_archive_dir)
                continue

            slave_statistic[archive] = {
                "name": archive,
                "num": len(os.listdir(last_archive_dir)) - 1,
            }

            future = executor.submit(archive_statistic, last_archive_dir)
            future_tasks.append(future)

        wait(future_tasks)

        for f in future_tasks:
            res = f.result()
            ons = res["on"]
            dm_dns = res["dm_dn"]

            for on in ons:
                if on in on_statistic:
                    on_statistic[on]["num"] += ons[on]["num"]
                else:
                    on_statistic[on] = ons[on]

            for dm_dn in dm_dns:
                if dm_dn in dm_dn_statistic:
                    dm_dn_statistic[dm_dn]["num"] += dm_dns[dm_dn]["num"]
                else:
                    dm_dn_statistic[dm_dn] = dm_dns[dm_dn]

    with open("/root/snap.txt", "w") as f:
        js = json.dumps(archive_stat)
        f.write(js)


def snapshots_statistic(mac_dir):
    try:
        meta_one = "0-metainfo.txt"
        meta_two = "1-metainfo.txt"

        statistic = dict()

        meta_files = [
            os.path.join(mac_dir, meta_one),
            os.path.join(mac_dir, meta_two)
        ]

        for meta_file in meta_files:
            logger.info("static meta %s", meta_file)
            if not os.path.exists(meta_file) or not os.path.isfile(meta_file):
                logger.error("meta file no exist: ", meta_file)
                continue

            with open(meta_file, 'r') as f:
                for line in f:
                    line_info = line.strip().split(",")
                    dm = line_info[3]
                    on = line_info[7]
                    dn = line_info[9]

                    dm_dn = "%s:%s" % (dm, dn)

                    if on in statistic:
                        statistic[on]["num"] += 1
                        dm_dn_statistic = statistic[on]["dm_dn"]
                        if dm_dn in dm_dn_statistic:
                            dm_dn_statistic[dm_dn] += 1
                        else:
                            dm_dn_statistic[dm_dn] = 1
                    else:
                        statistic[on] = {
                            "dm_dn": {
                                dm_dn: 1
                            },
                            "num": 1
                        }

        return statistic
    except:
        logger.error("error %s", traceback.format_exc())


@shared_task
def image_upload_statistic(snapshots_dir):
    logger.info("start image upload statistic %s", snapshots_dir)
    last_date = datetime.datetime.now() - datetime.timedelta(days=1)
    last_date_format = last_date.strftime("%Y-%m-%d")

    last_snapshots_dir = os.path.join(snapshots_dir, last_date_format)

    upload_statistic = {
        "company": {},
        "on": {},
        "on_dm_dn": {},
    }

    upload_company_statistic = upload_statistic["company"]
    upload_on_statistic = upload_statistic["on"]
    upload_on_dm_dn_statistic = upload_statistic["on_dm_dn"]

    future_tasks = []
    with Pool(max_workers=10) as executor:
        for snapshot in os.listdir(last_snapshots_dir):
            snapshot_dir = os.path.join(last_snapshots_dir, snapshot)
            future = executor.submit(snapshots_statistic, snapshot_dir)
            future_tasks.append(future)

        wait(future_tasks)

        for f in future_tasks:
            res = f.result()
            for on in res:
                dm_dn = res[on]["dm_dn"]
                num = res[on]["num"]

                if on not in upload_company_statistic:
                    upload_company_statistic[on] = []

                if on in upload_on_statistic:
                    upload_on_statistic[on]["num"] += num
                else:
                    upload_on_statistic[on] = {
                        "name": on,
                        "num": num,
                    }

                for dm_dn_key in dm_dn:
                    on_dm_dn = "%s__%s" % (on, dm_dn_key)
                    if on_dm_dn in upload_on_dm_dn_statistic:
                        upload_on_dm_dn_statistic[on_dm_dn]["num"] += dm_dn[dm_dn_key]
                    else:
                        upload_on_dm_dn_statistic[on_dm_dn] = {
                            "on": on,
                            "name": dm_dn_key,
                            "num": dm_dn[dm_dn_key]
                        }

                    if dm_dn_key not in upload_company_statistic[on]:
                        upload_company_statistic[on].append(dm_dn_key)

    with open("/root/sp.txt", "w") as f:
        js = json.dumps(upload_statistic)
        f.write(js)


