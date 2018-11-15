from django.db import models


class LogoTemplate(models.Model):
    cid = models.IntegerField(default=0, verbose_name="频道ID", help_text="频道ID")
    chuid = models.CharField(max_length=65, default=None, verbose_name="频道UID", help_text="频道UID")
    gzcid = models.CharField(max_length=65, default=None, verbose_name="勾正标准ID", help_text="勾正标准ID")
    gzchname = models.CharField(max_length=128, default=None, verbose_name="勾正标准频道名", help_text="勾正标准频道名")
    gzchtype = models.CharField(max_length=128, default=None, verbose_name="勾正台标类", help_text="勾正台标类")
    company = models.CharField(max_length=128, default=None, verbose_name="电视企业", help_text="电视企业")
    ledmodel = models.CharField(max_length=128, default=None, verbose_name="显示器类型", help_text="显示器类型")
    tvmodel = models.CharField(max_length=128, default=None, verbose_name="电视型号", help_text="电视型号")
    did = models.CharField(max_length=65, default=None, verbose_name="终端did", help_text="终端did")
    gzid = models.CharField(max_length=65, default=None, verbose_name="终端gzid", help_text="终端gzid")
    region = models.CharField(max_length=200, default=None, verbose_name="终端区域", help_text="终端区域")
    machine = models.CharField(max_length=200, default=None, verbose_name="终端唯一标示", help_text="终端唯一标示")

    x = models.FloatField(default=0., verbose_name="台标起始坐标x", help_text="台标起始坐标x")
    y = models.FloatField(default=0., verbose_name="台标起始坐标y", help_text="台标起始坐标y")
    w = models.FloatField(default=0., verbose_name="台标宽度", help_text="台标宽度")
    h = models.FloatField(default=0., verbose_name="台标长度", help_text="台标长度")

    mask = models.ImageField(max_length=200, verbose_name="掩码特征", help_text="掩码特征")
    temp = models.ImageField(max_length=200, verbose_name="匹配特征", help_text="匹配特征")
    best = models.ImageField(max_length=200, verbose_name="样本抽样", help_text="样本抽样")

    match = models.FloatField(default=0., verbose_name="匹配值", help_text="匹配值")

    award = models.IntegerField(default=0, verbose_name="评分", help_text="评分")
    pixes = models.IntegerField(default=0, verbose_name="像素数", help_text="像素数")

    checked = models.BooleanField(default=0, verbose_name="已校验", help_text="已校验")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")

    class Meta:
        verbose_name = "lacr特征"
        verbose_name_plural = verbose_name
        db_table = 'logo_templats'

