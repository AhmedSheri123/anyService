# Generated by Django 4.2.1 on 2024-11-13 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboard', '0002_subscriptionsmodel_plan_scope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionsmodel',
            name='plan_scope',
            field=models.CharField(choices=[('1', 'شهري'), ('2', 'سنوي')], max_length=255, null=True, verbose_name='مدة الاشتراك'),
        ),
    ]
