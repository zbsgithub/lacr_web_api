# Generated by Django 2.1.3 on 2018-11-30 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics_info', '0003_auto_20181130_1218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branddevicestatistic',
            options={'verbose_name': '品牌上传设备数统计', 'verbose_name_plural': '品牌上传设备数统计'},
        ),
        migrations.AlterModelOptions(
            name='companydevicestatistic',
            options={'verbose_name': '厂商上传设备数统计', 'verbose_name_plural': '厂商上传设备数统计'},
        ),
        migrations.AlterModelOptions(
            name='subordinatedevicestatistic',
            options={'verbose_name': 'subordinate设备数统计', 'verbose_name_plural': 'subordinate设备数统计'},
        ),
    ]
