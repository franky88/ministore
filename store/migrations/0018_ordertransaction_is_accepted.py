# Generated by Django 4.2.3 on 2023-07-27 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_product_on_display_customerorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertransaction',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
    ]