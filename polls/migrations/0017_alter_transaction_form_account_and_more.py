# Generated by Django 5.1 on 2024-09-17 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_rename_account_historicaltransaction_form_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='form_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='form_account_transactions', to='polls.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='to_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_transactions', to='polls.account'),
        ),
    ]
