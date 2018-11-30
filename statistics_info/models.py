from django.db import models
from system_info.models import Company
from system_info.models import Brand
# Create your models here.


'''
firm upload img statistic 
'''
class FirmUploadImgStatistic(models.Model):
    firm_name = models.CharField(max_length=65, default=None, verbose_name="厂商名称", help_text="厂商名称")
    img_num = models.IntegerField(default=None, verbose_name="图片数", help_text="图片数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "FirmUploadImgStatistic信息"
        verbose_name_plural = verbose_name
        db_table = 'FirmUploadImgStatistic'

'''
model statistic
'''
class ModelStatistic(models.Model):
    firm_name = models.CharField(max_length=65, default=None, verbose_name="厂商名称", help_text="厂商名称")
    model = models.CharField(max_length=65,default=None, verbose_name="型号", help_text="型号")
    model_num = models.IntegerField(default=None, verbose_name="型号数", help_text="型号数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    firmUploadImgStatistic_id = models.ForeignKey(FirmUploadImgStatistic, related_name="firmUploadImgStatistic_id", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "modelStatistic信息"
        verbose_name_plural = verbose_name
        db_table = 'modelStatistic'
'''
slave statistic
'''
class SlaveStatistic(models.Model):
    ip = models.CharField(max_length=65, default=None, verbose_name="公司名称", help_text="公司名称")
    did_num = models.IntegerField(default=None, verbose_name="设备数", help_text="设备数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "slaveStatistic信息"
        verbose_name_plural = verbose_name
        db_table = 'slaveStatistic'



class CompanyDailyImg(models.Model):
    num = models.IntegerField(default=None, verbose_name="图片数", help_text="图片数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    company = models.ForeignKey(Company, related_name="company_daily_img",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "company_daily_img信息"
        verbose_name_plural = verbose_name
        db_table = 'company_daily_img'
'''
model daily dynamic
'''
class BrandDailyImg(models.Model):
    num = models.IntegerField(default=None, verbose_name="图片数", help_text="型号数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    brand_daily_img = models.ForeignKey(Brand, related_name="brand_daily_img", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "brand_daily_img信息"
        verbose_name_plural = verbose_name
        db_table = 'brand_daily_img'