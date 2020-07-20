# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import logging
import traceback
import datetime
from concurrent.futures import wait
from concurrent.futures import ThreadPoolExecutor as Pool
from system_info.models import Brand, Company, Subordinate
from statistics_info.models import BrandDeviceStatistic, CompanyDeviceStatistic, SubordinateDeviceStatistic
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


logger = logging.getLogger(__name__)


class DeviceStatistic(object):
    def __init__(self, archive_path):
        self.archive_path = archive_path
        self.max_workers = 10
        self.print_line = True

    def statistic(self, last_archive_dir):
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
                if self.print_line:
                    self.print_line = False
                    for i, v in enumerate(line_info, 0):
                        logger.info("line %d: %s", i, v)
                dm = line_info[4]
                on = line_info[8]
                dn = line_info[10]
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
            "subordinate": {},
            "on": {},
            "dm_dn": {},
        }
        subordinate_statistic = archive_stat["subordinate"]
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

                subordinate_statistic[archive] = {
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
        with open("/root/s.txt", "w") as f:
            import json
            s = json.dumps(statistic)
            f.write(s)
            f.flush()
        subordinate_statistics = statistic["subordinate"]
        company_statistics = statistic["on"]
        brand_statistics = statistic["dm_dn"]

        for subordinate in subordinate_statistics:
            try:
                subordinate_obj = Subordinate.objects.get(mac=subordinate)
            except ObjectDoesNotExist:
                logger.info("new subordinate insert %s", subordinate)
                subordinate_obj = Subordinate(
                    mac=subordinate
                )
                subordinate_obj.save()
            except MultipleObjectsReturned:
                logger.error("more than one subordinate %s", subordinate)
                continue

            subordinate_device_statistic = SubordinateDeviceStatistic(
                subordinate=subordinate_obj,
                num=subordinate_statistics[subordinate]["num"],
            )
            subordinate_device_statistic.save()

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
