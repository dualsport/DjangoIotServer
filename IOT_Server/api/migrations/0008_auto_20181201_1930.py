# Generated by Django 2.1.3 on 2018-12-02 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20181201_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iotdata',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tags',
            name='value_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.ValueTypes'),
        ),
    ]
