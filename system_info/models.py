from django.db import models
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=65, default=None, verbose_name="公司名称", help_text="公司名称")
    alias = models.CharField(max_length=65, default=None, verbose_name="公司别名", help_text="公司别名")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        verbose_name = "company信息"
        verbose_name_plural = verbose_name
        db_table = 'company'

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class StdChName(models.Model):
    ch_id = models.CharField(max_length=65, default=None, verbose_name="频道id", unique=True, help_text="频道id")
    name = models.CharField(max_length=200, verbose_name="频道名称", help_text="频道名称", unique=True)
    image = models.ImageField(upload_to="system_info/std_channel/", blank=True, null=True,
                              verbose_name="频道图片", help_text="频道图片")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        verbose_name = "频道名称信息"
        verbose_name_plural = verbose_name
        db_table = "std_channel"
        ordering = ("name", )

    def __str__(self):
        return self.name

    @property
    def get_alias(self):
        return self.aliaschnames


class AliasChName(models.Model):
    std_ch = models.ForeignKey(StdChName, related_name="aliaschnames", on_delete=models.CASCADE,
                               verbose_name="频道别名表", help_text="频道别名表")
    name = models.CharField(max_length=200, verbose_name="频道名称", help_text="频道名称", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        verbose_name = "频道别名"
        verbose_name_plural = verbose_name
        db_table = "alias_channel"
        ordering = ("name", )

    def __str__(self):
        return self.name


class Slave(models.Model):
    name = models.CharField(max_length=65, blank=True, null=True, verbose_name="slave别名")
    mac = models.CharField(max_length=65, blank=True, default=None, verbose_name="mac地址", unique=True)
    ip = models.CharField(max_length=65, blank=True, null=True, verbose_name="ip地址")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        verbose_name = "Slave信息"
        verbose_name_plural = verbose_name
        db_table = "slave"

    def __str__(self):
        return self.mac

