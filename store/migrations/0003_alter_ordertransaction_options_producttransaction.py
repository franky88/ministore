# Generated by Django 4.2.3 on 2023-08-08 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_itemrequest_request_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordertransaction',
            options={'ordering': ['-is_accepted', '-created']},
        ),
        migrations.CreateModel(
            name='ProductTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'ordering': ['-created', '-updated'],
            },
        ),
    ]