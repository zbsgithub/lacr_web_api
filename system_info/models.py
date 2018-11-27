from django.db import models

# Create your models here.
'''
create models
'''
class Company(models.Model):
    name = models.CharField(max_length=65, default=None, verbose_name="公司名称", help_text="公司名称")
    alias = models.CharField(max_length=65, default=None, verbose_name="公司别名", help_text="公司别名")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        verbose_name = "company信息"
        verbose_name_plural = verbose_name
        db_table = 'company'


class Brand(models.Model):
    name = models.CharField(max_length=65, default=None, verbose_name="品牌名称", help_text="品牌名称")
    alias = models.CharField(max_length=65, default=None, verbose_name="品牌别名", help_text="品牌别名")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")
    company = models.ForeignKey(Company, related_name="companys", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "brand信息"
        verbose_name_plural = verbose_name
        db_table = 'brand'


class ChannelType(models.Model):
    name = models.CharField(max_length=200, verbose_name="类型名称", help_text="类型名称", unique=True)
    alias = models.CharField(max_length=200, verbose_name="类型别名", help_text="类型别名")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        verbose_name = "频道类型信息"
        verbose_name_plural = verbose_name
        db_table = "channel_type"

    def __str__(self):
        return self.name


class ChannelName(models.Model):
    classify = models.ForeignKey(ChannelType, related_name="channelnames", on_delete=models.SET_NULL, null=True,
                                 verbose_name="频道类别", help_text="频道类别")
    chid = models.CharField(max_length=65, default=None, verbose_name="频道id", help_text="频道id")
    name = models.CharField(max_length=200, verbose_name="频道名称", help_text="频道名称", unique=True)
    alias = models.CharField(max_length=200, verbose_name="频道别名", help_text="频道别名")
    image = models.ImageField(upload_to="system_info/std_channel/", null=True,
                              verbose_name="频道图片", help_text="频道图片")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        verbose_name = "频道名称信息"
        verbose_name_plural = verbose_name
        db_table = "channel_name"

    def __str__(self):
        return self.name

