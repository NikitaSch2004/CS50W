# Generated by Django 4.2.5 on 2023-11-05 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_new_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_listing',
            name='category',
            field=models.CharField(choices=[('None', 'None'), ('New', 'New'), ('Used', 'Used'), ('Junk', 'Junk')], max_length=20),
        ),
    ]
