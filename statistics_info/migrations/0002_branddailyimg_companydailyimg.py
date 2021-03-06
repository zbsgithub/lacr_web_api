# Generated by Django 2.1.3 on 2018-11-30 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system_info', '0004_channelname_image'),
        ('statistics_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandDailyImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=None, help_text='型号数', verbose_name='图片数')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('brand_daily_img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_daily_img', to='system_info.Brand')),
            ],
            options={
                'verbose_name': 'brand_daily_img信息',
                'verbose_name_plural': 'brand_daily_img信息',
                'db_table': 'brand_daily_img',
            },
        ),
        migrations.CreateModel(
            name='CompanyDailyImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=None, help_text='图片数', verbose_name='图片数')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_daily_img', to='system_info.Company')),
            ],
            options={
                'verbose_name': 'company_daily_img信息',
                'verbose_name_plural': 'company_daily_img信息',
                'db_table': 'company_daily_img',
            },
        ),
    ]
