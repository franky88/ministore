# Generated by Django 4.2.3 on 2023-07-18 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_ordertransaction_delete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertransaction',
            name='money_tender',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
