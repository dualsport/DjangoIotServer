# Generated by Django 2.1.3 on 2018-12-16 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20181216_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='value_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.ValueTypes'),
        ),
    ]
