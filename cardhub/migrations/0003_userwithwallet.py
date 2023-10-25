# Generated by Django 4.2.6 on 2023-10-24 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cardhub', '0002_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWithWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardhub.wallet')),
            ],
        ),
    ]