# Generated by Django 2.1.3 on 2018-11-25 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('value_int', models.IntegerField(blank=True)),
                ('value_dec', models.DecimalField(blank=True, decimal_places=3, max_digits=8)),
                ('value_text', models.CharField(blank=True, max_length=50)),
                ('value_bool', models.BooleanField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('device_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('type', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('tag_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Devices')),
            ],
        ),
        migrations.CreateModel(
            name='Valuetypes',
            fields=[
                ('value_type_id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15)),
                ('type', models.CharField(choices=[('TEXT', 'Alphanumeric text'), ('DEC', 'Decimal Number'), ('INT', 'Integer'), ('BOOL', 'Boolean')], max_length=4)),
            ],
        ),
        migrations.AddField(
            model_name='tags',
            name='value_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Valuetypes'),
        ),
        migrations.AddField(
            model_name='data',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Tags'),
        ),
    ]
