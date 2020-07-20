from django.db import models
from system_info.models import Brand, Subordinate, Company
# Create your models here.


class CompanyDeviceStatistic(models.Model):
    company = models.ForeignKey(Company, related_name="company_device_statistics", on_delete=models.CASCADE,
                                verbose_name="厂商", help_text="厂商")
    num = models.IntegerField(default=None, verbose_name="设备数", help_text="设备数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "厂商上传设备数统计"
        verbose_name_plural = verbose_name
        db_table = 'companyDeviceStatistic'


class BrandDeviceStatistic(models.Model):
    brand = models.ForeignKey(Brand, related_name="brand_device_statistics", on_delete=models.CASCADE,
                              verbose_name="品牌", help_text="品牌")
    num = models.IntegerField(default=None, verbose_name="型号数", help_text="型号数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "品牌上传设备数统计"
        verbose_name_plural = verbose_name
        db_table = 'brandDeviceStatistic'


class SubordinateDeviceStatistic(models.Model):
    subordinate = models.ForeignKey(Subordinate, related_name="subordinate_device_statistic", on_delete=models.CASCADE,
                              verbose_name="从", help_text="从")
    num = models.IntegerField(default=None, verbose_name="设备数", help_text="设备数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "subordinate设备数统计"
        verbose_name_plural = verbose_name
        db_table = 'subordinateDeviceStatistic'


class CompanyImgStatistic(models.Model):
    company = models.ForeignKey(Company, related_name="company_img_statistics",on_delete=models.CASCADE,
                                verbose_name="厂商", help_text="厂商")
    num = models.IntegerField(default=None, verbose_name="图片数", help_text="图片数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "厂商上传图片统计"
        verbose_name_plural = verbose_name
        db_table = 'companyImgStatistic'


class BrandImgStatistic(models.Model):
    brand = models.ForeignKey(Brand, related_name="brand_img_statistic", on_delete=models.CASCADE,
                              verbose_name="品牌", help_text="品牌")
    num = models.IntegerField(default=None, verbose_name="图片数", help_text="型号数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "品牌上传图片统计"
        verbose_name_plural = verbose_name
        db_table = 'brandImgStatistic'
