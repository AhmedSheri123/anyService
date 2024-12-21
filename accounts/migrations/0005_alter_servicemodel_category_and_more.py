# Generated by Django 4.2.1 on 2024-11-15 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_servicemodel_location_servicemodel_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicemodel',
            name='category',
            field=models.ForeignKey(help_text='الفئة العامة التي تندرج تحتها الخدمة.', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.servicecategory', verbose_name='الفئة'),
        ),
        migrations.AlterField(
            model_name='servicemodel',
            name='description',
            field=models.TextField(help_text='وصف شامل للخدمة يوضح تفاصيلها وما تقدمه.', verbose_name='وصف الخدمة'),
        ),
        migrations.AlterField(
            model_name='servicemodel',
            name='duration',
            field=models.DurationField(help_text='المدة الزمنية المتوقع لإكمال الخدمة.', null=True, verbose_name='المدة المتوقعة'),
        ),
        migrations.AlterField(
            model_name='servicemodel',
            name='is_active',
            field=models.BooleanField(default=True, help_text='حالة الخدمة، سواء كانت متاحة أم لا.', verbose_name='حالة الخدمة'),
        ),
        migrations.AlterField(
            model_name='servicemodel',
            name='name',
            field=models.CharField(help_text='اسم الخدمة التي يقدمها صاحب المهنة.', max_length=100, verbose_name='اسم الخدمة'),
        ),
        migrations.AlterField(
            model_name='servicemodel',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='سعر الخدمة أو التكلفة المبدئية لها.', max_digits=10, verbose_name='السعر'),
        ),
    ]
