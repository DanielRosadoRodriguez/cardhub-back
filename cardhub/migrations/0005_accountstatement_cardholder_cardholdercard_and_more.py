# Generated by Django 4.2.7 on 2023-11-11 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cardhub', '0004_remove_userwithwallet_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountStatement',
            fields=[
                ('statement_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('cut_off_date', models.DateField()),
                ('payment_date', models.DateField()),
                ('current_debt', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_for_no_interest', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='CardHolder',
            fields=[
                ('card_holder_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CardHolderCard',
            fields=[
                ('card_holder_cards_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CardWebPage',
            fields=[
                ('pageID', models.AutoField(primary_key=True, serialize=False)),
                ('page_url', models.CharField(max_length=100)),
                ('page_content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('card_holder', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='cardhub.cardholder')),
            ],
        ),
        migrations.DeleteModel(
            name='UserWithWallet',
        ),
        migrations.RenameField(
            model_name='creditcardproduct',
            old_name='associated_bank',
            new_name='bank_name',
        ),
        migrations.RenameField(
            model_name='creditcardproduct',
            old_name='name',
            new_name='card_name',
        ),
        migrations.AddField(
            model_name='creditcardproduct',
            name='annuity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Wallet',
        ),
        migrations.AddField(
            model_name='cardwebpage',
            name='associated_cards',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardhub.creditcardproduct'),
        ),
        migrations.AddField(
            model_name='cardholdercard',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardhub.creditcardproduct'),
        ),
        migrations.AddField(
            model_name='cardholdercard',
            name='card_holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardhub.cardholder'),
        ),
        migrations.AddField(
            model_name='accountstatement',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardhub.cardholdercard'),
        ),
    ]
