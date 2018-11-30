# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import os
import traceback
import datetime
from concurrent.futures import ThreadPoolExecutor as Pool
from concurrent.futures import wait
from celery import shared_task
import logging
logger = logging.getLogger(__name__)
from system_info.models import Company, Brand, Slave
from statistics_info.models import CompanyImgStatistic, BrandImgStatistic, \
    CompanyDeviceStatistic, BrandDeviceStatistic, SlaveDeviceStatistic
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class DeviceStatistic(object):
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.max_workers = 10

    @staticmethod
    def statistic(last_archive_dir):
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

    def start(self):
        logger.info("start archive upload statistic %s", self.archive_path)
        archive_stat = {
            "slave": {},
            "on": {},
            "dm_dn": {},
        }
        slave_statistic = archive_stat["slave"]
        dm_dn_statistic = archive_stat["dm_dn"]
        on_statistic = archive_stat["on"]
        logger.info("start statistic archive path %s", self.archive_path)

        if not os.path.exists(self.archive_path) or not os.path.isdir(self.archive_path):
            logger.error("archive path not exist %s", self.archive_path)
            return None

        last_date = datetime.datetime.now() - datetime.timedelta(days=1)
        last_date_format = last_date.strftime("%Y-%m-%d")

        future_tasks = []
        with Pool(max_workers=10) as executor:
            for archive in os.listdir(self.archive_path):
                last_archive_dir = os.path.join(self.archive_path, archive, last_date_format)

                if not os.path.exists(last_archive_dir) or not os.path.isdir(last_archive_dir):
                    logging.error("archive dir no exist %s", last_archive_dir)
                    continue

                slave_statistic[archive] = {
                    "name": archive,
                    "num": len(os.listdir(last_archive_dir)) - 1,
                }

                future = executor.submit(self.statistic, last_archive_dir)
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

        self.save(archive_stat)

    @staticmethod
    def save(statistic):
        slave_statistics = statistic["slave"]
        company_statistics = statistic["on"]
        brand_statistics = statistic["dm_dn"]

        for slave in slave_statistics:
            slave_obj = None
            try:
                slave_obj = Slave.objects.get(mac=slave)
            except ObjectDoesNotExist:
                logger.info("new slave insert %s", slave)
                slave_obj = Slave(
                    mac=slave
                )
                slave_obj.save()
            except MultipleObjectsReturned:
                logger.error("more than one slave %s", slave)

            slave_device_statistic = SlaveDeviceStatistic(
                slave=slave_obj,
                num=slave_statistics[slave]["num"],
            )
            slave_device_statistic.save()

        for company in company_statistics:
            try:
                company_obj = Company.objects.get(name=company)

                company_device_statistic = CompanyDeviceStatistic(
                    company=company_obj,
                    num=company_statistics[company]["num"]
                )
                company_device_statistic.save()
            except:
                logger.error("company device statistic found company error %s: %s", company, traceback.format_exc())
                continue

        for brand in brand_statistics:
            try:
                brand_obj = Brand.objects.get(name=brand)
                brand_device_statistic = BrandDeviceStatistic(
                    brand=brand_obj,
                    num=brand_statistics[brand]['num']
                )
                brand_device_statistic.save()
            except:
                logger.error("brand statistic found error %s: %s", brand, traceback.format_exc())
                continue


class ImageStatistic(object):

    def __init__(self, snapshots_dir):
        self.meta_one = "0-metainfo.txt"
        self.meta_two = "1-metainfo.txt"
        self.max_workers = 10
        self.snapshots_dir = snapshots_dir

    def snapshots_statistic(self, mac_dir):
        try:

            statistic = dict()

            meta_files = [
                os.path.join(mac_dir, self.meta_one),
                os.path.join(mac_dir, self.meta_two)
            ]

            for meta_file in meta_files:
                logger.info("static meta %s", meta_file)
                if not os.path.exists(meta_file) or not os.path.isfile(meta_file):
                    logger.error("meta file no exist: ", meta_file)
                    continue

                with open(meta_file, 'r') as f:
                    for line in f:
                        line_info = line.strip().split(",")
                        try:
                            dm = line_info[3]
                            on = line_info[7]
                            dn = line_info[9]
                        except:
                            logger.error("error index line %s", line)
                            continue

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
            return None

    def start(self):
        logger.info("start image upload statistic %s", self.snapshots_dir)
        last_date = datetime.datetime.now() - datetime.timedelta(days=1)
        last_date_format = last_date.strftime("%Y-%m-%d")

        last_snapshots_dir = os.path.join(self.snapshots_dir, last_date_format)

        upload_statistic = {
            "company": {},
            "on": {},
            "on_dm_dn": {},
        }

        upload_company_statistic = upload_statistic["company"]
        upload_on_statistic = upload_statistic["on"]
        upload_on_dm_dn_statistic = upload_statistic["on_dm_dn"]

        future_tasks = []
        with Pool(max_workers=self.max_workers) as executor:
            for snapshot in os.listdir(last_snapshots_dir):
                snapshot_dir = os.path.join(last_snapshots_dir, snapshot)
                future = executor.submit(self.snapshots_statistic, snapshot_dir)
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
        self.save(upload_statistic)

    @staticmethod
    def save(statistic):
        company_statistics = statistic["company"]
        dm_dn_statistics = statistic["on_dm_dn"]
        on_statistics = statistic["on"]

        for company in company_statistics:
            try:
                company_obj = Company.objects.get(name=company)
            except ObjectDoesNotExist:
                logger.info("new company insert %s", company)
                company_obj = Company(
                    name=company,
                    alias=company
                )
                company_obj.save()
            except MultipleObjectsReturned:
                logger.error("more than one company %s", company)
                continue
            except:
                logger.error("unknown company error found %s", company)
                continue

            brands = company_statistics[company]
            for brand in brands:
                try:
                    brand_obj = Brand.objects.get(name=brand)
                except ObjectDoesNotExist:
                    logger.info("new brand insert %s", brand)
                    brand_obj = Brand(
                        company=company_obj,
                        name=brand,
                        alias=brand,
                    )
                    brand_obj.save()
                except MultipleObjectsReturned:
                    logger.error("more than one brand %s", brand)
                    continue
                except:
                    logger.error("unknown brand error found %s", brand)
                    continue

                try:
                    dm_dn_statistic = dm_dn_statistics["%s__%s" % (company, brand)]
                    brand_img_statistic = BrandImgStatistic(
                        brand=brand_obj,
                        num=dm_dn_statistic["num"]
                    )
                    brand_img_statistic.save()
                except:
                    logger.error("brand img statistic %s", traceback.format_exc())

            try:
                on_num_static = on_statistics[company]
                company_img_statistic = CompanyImgStatistic(
                    company=company_obj,
                    num=on_num_static["num"]
                )
                company_img_statistic.save()
            except:
                logger.error("company img statistic %s", traceback.format_exc())


@shared_task
def image_upload_statistic(snapshots_dir):
    image_statistic = ImageStatistic(snapshots_dir=snapshots_dir)
    image_statistic.start()


@shared_task
def device_statistic(archive_dir):
    statistic = DeviceStatistic(archive_path=archive_dir)
    statistic.start()
