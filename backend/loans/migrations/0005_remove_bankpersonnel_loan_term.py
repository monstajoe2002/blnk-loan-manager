# Generated by Django 5.1 on 2024-09-04 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_alter_loan_loan_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankpersonnel',
            name='loan_term',
        ),
    ]
