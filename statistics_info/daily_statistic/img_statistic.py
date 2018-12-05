# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import logging
import traceback
import datetime
from concurrent.futures import wait
from concurrent.futures import ThreadPoolExecutor as Pool
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from system_info.models import Brand, Company
from statistics_info.models import BrandImgStatistic, CompanyImgStatistic

logger = logging.getLogger(__name__)


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

