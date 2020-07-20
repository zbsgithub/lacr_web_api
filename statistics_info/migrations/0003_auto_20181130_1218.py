# Generated by Django 2.1.3 on 2018-11-30 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system_info', '0005_subordinate'),
        ('statistics_info', '0002_branddailyimg_companydailyimg'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandDeviceStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=None, help_text='型号数', verbose_name='型号数')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('brand', models.ForeignKey(help_text='品牌', on_delete=django.db.models.deletion.CASCADE, related_name='brand_device_statistics', to='system_info.Brand', verbose_name='品牌')),
            ],
            options={
                'verbose_name_plural': '品牌上传设备数',
                'db_table': 'brandDeviceStatistic',
                'verbose_name': '品牌上传设备数',
            },
        ),
        migrations.CreateModel(
            name='BrandImgStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=None, help_text='型号数', verbose_name='图片数')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('brand', models.ForeignKey(help_text='品牌', on_delete=django.db.models.deletion.CASCADE, related_name='brand_img_statistic', to='system_info.Brand', verbose_name='品牌')),
            ],
            options={
                'verbose_name_plural': '品牌上传图片统计',
                'db_table': 'brandImgStatistic',
                'verbose_name': '品牌上传图片统计',
            },
        ),
        migrations.CreateModel(
            name='CompanyDeviceStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=None, help_text='设备数', verbose_name='设备数')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('company', models.ForeignKey(help_text='厂商', on_delete=django.db.models.deletion.CASCADE, related_name='company_device_statistics', to='system_info.Company', verbose_name='厂商')),
            ],
            options={
                'verbose_name_plural': '厂商上传设备数',
                'db_table': 'companyDeviceStatistic',
                'verbose_name': '厂商上传设备数',
            },
        ),
        migrations.CreateModel(
            name='CompanyImgStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=None, help_text='图片数', verbose_name='图片数')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('company', models.ForeignKey(help_text='厂商', on_delete=django.db.models.deletion.CASCADE, related_name='company_img_statistics', to='system_info.Company', verbose_name='厂商')),
            ],
            options={
                'verbose_name_plural': '厂商上传图片统计',
                'db_table': 'companyImgStatistic',
                'verbose_name': '厂商上传图片统计',
            },
        ),
        migrations.CreateModel(
            name='SubordinateDeviceStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=None, help_text='设备数', verbose_name='设备数')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('subordinate', models.ForeignKey(help_text='从', on_delete=django.db.models.deletion.CASCADE, related_name='subordinate_device_statistic', to='system_info.Subordinate', verbose_name='从')),
            ],
            options={
                'verbose_name_plural': 'subordinateStatistic信息',
                'db_table': 'subordinateDeviceStatistic',
                'verbose_name': 'subordinateStatistic信息',
            },
        ),
        migrations.RemoveField(
            model_name='branddailyimg',
            name='brand_daily_img',
        ),
        migrations.RemoveField(
            model_name='companydailyimg',
            name='company',
        ),
        migrations.RemoveField(
            model_name='modelstatistic',
            name='firmUploadImgStatistic_id',
        ),
        migrations.DeleteModel(
            name='SubordinateStatistic',
        ),
        migrations.DeleteModel(
            name='BrandDailyImg',
        ),
        migrations.DeleteModel(
            name='CompanyDailyImg',
        ),
        migrations.DeleteModel(
            name='FirmUploadImgStatistic',
        ),
        migrations.DeleteModel(
            name='ModelStatistic',
        ),
    ]
